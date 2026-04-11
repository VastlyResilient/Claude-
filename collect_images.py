#!/usr/bin/env python3
"""
Soccer Player Image Collector
Downloads high-quality images of soccer players in their jerseys.
Uses DuckDuckGo Image Search + Bing fallback (no API key needed).
Self-healing: automatically works around errors, rotates strategies,
and retries failed players with alternative approaches.
"""

import argparse
import csv
import json
import os
import random
import re
import sys
import time
import unicodedata
from datetime import datetime
from io import BytesIO
from urllib.parse import quote_plus

import requests

# Auto-install playwright if missing
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# Auto-install Pillow if missing
try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow', '-q'])
    from PIL import Image


# ── Constants ──────────────────────────────────────────────────────────────────

USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

HEADERS = {
    'User-Agent': USER_AGENTS[0],
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

MAX_RETRIES = 4
RETRY_DELAY = 2.0
MIN_IMAGE_SIZE = 15000  # bytes - skip tiny/blurry images
MAX_RESULTS_TO_TRY = 10  # try up to 10 image results before giving up

COUNTRY_SEARCH_NAMES = {
    'Ivory Coast': "Côte d'Ivoire",
    'Cape Verde': 'Cape Verde Cabo Verde',
}

# Track which sources are having issues so we can adapt
_source_health = {'ddg': 0, 'bing': 0, 'sofascore': 0}  # 0 = healthy, >3 = skip temporarily
_consecutive_failures = 0


# ── Helpers ────────────────────────────────────────────────────────────────────

def strip_diacritics(text):
    """Remove accents/diacritics from text for search queries."""
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))


def sanitize_filename(name):
    """Make a string safe for use as a filename."""
    # Keep the name readable but remove problematic characters
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()


def fetch_with_retry(url, headers=None, timeout=30, stream=False):
    """Fetch a URL with retry logic, rotating user agents and exponential backoff."""
    hdrs = {**HEADERS, **(headers or {})}
    for attempt in range(MAX_RETRIES):
        # Rotate user agent on retries to avoid blocks
        hdrs['User-Agent'] = random.choice(USER_AGENTS)
        try:
            r = requests.get(url, headers=hdrs, timeout=timeout, stream=stream,
                             allow_redirects=True)
            if r.status_code == 429:
                wait = RETRY_DELAY * (2 ** attempt)
                print(f"      Rate limited, waiting {wait:.0f}s...")
                time.sleep(wait)
                continue
            if r.status_code == 403:
                # Try different user agent
                time.sleep(1)
                continue
            return r
        except (requests.ConnectionError, requests.Timeout, requests.exceptions.ChunkedEncodingError):
            if attempt == MAX_RETRIES - 1:
                return None
            time.sleep(RETRY_DELAY * (2 ** attempt))
        except Exception:
            # Catch any unexpected error and retry
            if attempt == MAX_RETRIES - 1:
                return None
            time.sleep(RETRY_DELAY * (2 ** attempt))
    return None


# ── DuckDuckGo Image Search ───────────────────────────────────────────────────

def get_ddg_vqd(query):
    """Get DuckDuckGo vqd token needed for image search."""
    url = f"https://duckduckgo.com/?q={quote_plus(query)}"
    r = fetch_with_retry(url)
    if r is None:
        return None
    # Try multiple patterns — DDG changes the format periodically
    patterns = [
        r'vqd=["\x27]([^"\x27]+)["\x27]',  # vqd="..." or vqd='...'
        r'vqd=([0-9]+-[0-9a-f]+)',           # vqd=4-173041784389...
        r'vqd["\x27]?\s*[:=]\s*["\x27]?([0-9]+-[0-9a-f]+)',  # vqd: "..." or vqd="..."
        r'vqd=([^&"\x27\s]+)',               # vqd= followed by anything until delimiter
    ]
    for pattern in patterns:
        match = re.search(pattern, r.text)
        if match:
            return match.group(1)
    return None


def search_ddg_images(query, max_results=10):
    """Search DuckDuckGo for images and return list of image URLs with metadata."""
    vqd = get_ddg_vqd(query)
    if not vqd:
        return []

    url = "https://duckduckgo.com/i.js"
    params = {
        'l': 'us-en',
        'o': 'json',
        'q': query,
        'vqd': vqd,
        'f': ',,,,,',
        'p': '1',
    }

    r = fetch_with_retry(f"{url}?{'&'.join(f'{k}={quote_plus(str(v))}' for k, v in params.items())}")
    if r is None or r.status_code != 200:
        return []

    try:
        data = r.json()
    except (json.JSONDecodeError, ValueError):
        return []

    results = []
    for item in data.get('results', [])[:max_results]:
        results.append({
            'url': item.get('image', ''),
            'thumbnail': item.get('thumbnail', ''),
            'width': item.get('width', 0),
            'height': item.get('height', 0),
            'title': item.get('title', ''),
            'source': item.get('source', ''),
        })

    return results


# ── TheSportsDB API (clean images, no watermarks) ─────────────────────────────

def search_thesportsdb(name):
    """Search TheSportsDB for a player and return image URLs."""
    clean = strip_diacritics(re.sub(r"'[^']*'", '', name).strip())
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={quote_plus(clean)}"
    r = fetch_with_retry(url, timeout=10)
    if r is None or r.status_code != 200:
        return None, None

    try:
        data = r.json()
    except (json.JSONDecodeError, ValueError):
        return None, None

    players = data.get('player') or []
    # Find soccer players
    for p in players:
        if p.get('strSport', '').lower() == 'soccer':
            thumb = p.get('strThumb')
            cutout = p.get('strCutout')
            return thumb, cutout

    return None, None


# ── Ecosia Image Search via Chrome (Playwright) ──────────────────────────────

# Persistent browser instance (reused across players to avoid startup cost)
_browser_instance = None
_browser_context = None

WATERMARK_DOMAINS = [
    'alamy.com', 'alamy', 'gettyimages.com', 'getty', 'shutterstock.com',
    'shutterstock', 'istockphoto.com', 'istock', '123rf.com', '123rf',
    'depositphotos.com', 'dreamstime.com', 'stock.adobe.com', 'wireimage',
    'corbis', 'agefotostock',
]

def _get_browser():
    """Get or create a persistent Playwright browser instance."""
    global _browser_instance, _browser_context
    if _browser_instance and _browser_context:
        return _browser_context
    if not HAS_PLAYWRIGHT:
        return None
    try:
        pw = sync_playwright().start()
        proxy_url = os.environ.get('HTTPS_PROXY', '')
        match = re.match(r'http://([^:]+):([^@]+)@([^:]+):(\d+)', proxy_url)
        if match:
            proxy_conf = {
                "server": f"http://{match.group(3)}:{match.group(4)}",
                "username": match.group(1),
                "password": match.group(2),
            }
        else:
            proxy_conf = None
        _browser_instance = pw.chromium.launch(
            headless=True,
            proxy=proxy_conf,
            args=['--ignore-certificate-errors']
        )
        _browser_context = _browser_instance.new_context(
            ignore_https_errors=True,
            user_agent=random.choice(USER_AGENTS),
        )
        return _browser_context
    except Exception:
        return None


def search_ecosia_chrome(query, max_results=10):
    """Search Ecosia Images using headless Chrome via Playwright."""
    ctx = _get_browser()
    if not ctx:
        return []
    try:
        page = ctx.new_page()
        page.goto(f"https://www.ecosia.org/images?q={quote_plus(query)}",
                  timeout=20000, wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        content = page.content()
        page.close()

        all_imgs = re.findall(r'(https?://[^"\s<>\\]+\.(?:jpg|jpeg|png|webp)[^"\s<>\\]*)', content)
        blocked = WATERMARK_DOMAINS + ['ecosia.org', 'favicon', 'logo', 'icon', 'badge']
        filtered = [u for u in all_imgs if not any(b in u.lower() for b in blocked)]
        # Dedupe
        seen = set()
        unique = []
        for u in filtered:
            if u not in seen:
                seen.add(u)
                unique.append(u)

        results = []
        for img_url in unique[:max_results]:
            results.append({
                'url': img_url,
                'thumbnail': '',
                'width': 0,
                'height': 0,
                'title': '',
                'source': 'ecosia_chrome',
            })
        return results
    except Exception:
        return []


# ── Brave Image Search ────────────────────────────────────────────────────────

def search_brave_images(query, max_results=10):
    """Search Brave for images by extracting URLs from the results page."""
    url = f"https://search.brave.com/images?q={quote_plus(query)}&source=web"
    r = fetch_with_retry(url, timeout=20)
    if r is None or r.status_code != 200:
        return []

    # Extract all external image URLs from the page
    all_imgs = re.findall(r'https?://[^"\s<>\']+?\.(?:jpg|jpeg|png|webp)', r.text)
    # Filter out Brave's own assets
    filtered = [u for u in all_imgs if 'brave.com' not in u and 'favicon' not in u
                and 'amazon.com/images' not in u]
    # Dedupe while preserving order
    seen = set()
    unique = []
    for u in filtered:
        if u not in seen:
            seen.add(u)
            unique.append(u)

    results = []
    for img_url in unique[:max_results]:
        results.append({
            'url': img_url,
            'thumbnail': '',
            'width': 0,
            'height': 0,
            'title': '',
            'source': 'brave',
        })

    return results


# ── Bing Image Search (fallback) ──────────────────────────────────────────────

def search_bing_images(query, max_results=8):
    """Search Bing for images by scraping the results page."""
    url = f"https://www.bing.com/images/search?q={quote_plus(query)}&form=HDRSC2&first=1"
    r = fetch_with_retry(url)
    if r is None or r.status_code != 200:
        return []

    results = []
    # Extract image URLs from the page using murl pattern
    matches = re.findall(r'murl&quot;:&quot;(https?://[^&]+?)&quot;', r.text)
    for img_url in matches[:max_results]:
        results.append({
            'url': img_url,
            'thumbnail': '',
            'width': 0,
            'height': 0,
            'title': '',
            'source': 'bing',
        })

    return results


# ── SofaScore API (additional source) ─────────────────────────────────────────

def search_sofascore_player(name, country):
    """Search SofaScore for a player and return their image URL if found."""
    if _source_health.get('sofascore', 0) > 3:
        return None  # Source is unhealthy, skip

    clean = strip_diacritics(re.sub(r"'[^']*'", '', name).strip())
    url = f"https://api.sofascore.com/api/v1/search/players?q={quote_plus(clean)}"
    r = fetch_with_retry(url, timeout=10)
    if r is None or r.status_code != 200:
        _source_health['sofascore'] = _source_health.get('sofascore', 0) + 1
        return None

    try:
        data = r.json()
    except (json.JSONDecodeError, ValueError):
        return None

    results = data.get('results', [])
    if not results:
        # Try last name only
        parts = clean.split()
        if len(parts) > 1:
            url2 = f"https://api.sofascore.com/api/v1/search/players?q={quote_plus(parts[-1])}"
            r2 = fetch_with_retry(url2, timeout=10)
            if r2 and r2.status_code == 200:
                try:
                    results = r2.json().get('results', [])
                except (json.JSONDecodeError, ValueError):
                    pass
        if not results:
            return None

    # Try to match by country
    country_alias = COUNTRY_SEARCH_NAMES.get(country, country)
    for item in results[:5]:
        entity = item.get('entity', {})
        player_id = entity.get('id')
        if not player_id:
            continue

        # Check country via detail endpoint
        detail_url = f"https://api.sofascore.com/api/v1/player/{player_id}"
        dr = fetch_with_retry(detail_url, timeout=10)
        if dr and dr.status_code == 200:
            try:
                pdata = dr.json().get('player', {})
                pcountry = pdata.get('country', {}).get('name', '')
                if pcountry.lower() in [country.lower(), country_alias.lower()]:
                    return f"https://api.sofascore.com/api/v1/player/{player_id}/image"
            except (json.JSONDecodeError, ValueError):
                pass

    # If only one result and name is close, use it anyway
    if len(results) == 1:
        entity = results[0].get('entity', {})
        player_id = entity.get('id')
        if player_id:
            return f"https://api.sofascore.com/api/v1/player/{player_id}/image"

    return None


# ── Image Download & Validation ───────────────────────────────────────────────

def download_and_save_image(url, save_path, min_size=None):
    """Download an image, validate it, convert to JPEG, and save."""
    if min_size is None:
        min_size = MIN_IMAGE_SIZE

    r = fetch_with_retry(url, timeout=15, stream=True)
    if r is None or r.status_code != 200:
        return False, f"download failed (status={r.status_code if r else 'None'})"

    content_type = r.headers.get('Content-Type', '')
    if not content_type.startswith('image/'):
        return False, f"not an image ({content_type})"

    image_data = r.content
    if len(image_data) < min_size:
        return False, f"too small ({len(image_data)} bytes)"

    try:
        img = Image.open(BytesIO(image_data))

        # Check dimensions - we want decent sized images
        w, h = img.size
        if w < 250 or h < 250:
            return False, f"dimensions too small ({w}x{h})"

        # Convert to RGB JPEG
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        img.save(save_path, 'JPEG', quality=92)
        file_size = os.path.getsize(save_path)
        return True, f"{file_size / 1024:.1f}KB, {w}x{h}"

    except Exception as e:
        return False, f"image processing error: {str(e)}"


# ── Main Collection Logic ─────────────────────────────────────────────────────

def build_search_queries(name, country, attempt=0):
    """Build a list of search queries to try, from most specific to least.
    On retry attempts, generates different query variations."""
    country_search = COUNTRY_SEARCH_NAMES.get(country, country)
    clean_name = strip_diacritics(name)

    # Remove quotes/nicknames for cleaner search
    base_name = re.sub(r"'[^']*'", '', name).strip()
    base_name = re.sub(r'\s+', ' ', base_name)
    clean_base = strip_diacritics(base_name)

    # Extract nickname if present (e.g., 'Memo', 'Coco')
    nickname_match = re.search(r"'([^']*)'", name)
    nickname = nickname_match.group(1) if nickname_match else None

    parts = clean_base.split()
    last_name = parts[-1] if parts else clean_base
    first_name = parts[0] if parts else clean_base
    first_last = f"{first_name} {last_name}" if len(parts) > 2 else clean_base

    if attempt == 0:
        queries = [
            f"{clean_base} {country_search} national team football",
            f"{clean_base} footballer {country_search}",
            f"{clean_base} soccer player {country}",
            f"{clean_base} football player",
            f"{first_last} {country} football",
        ]
    else:
        # Alternative queries for retries - try different angles
        queries = [
            f"{last_name} {country} national football team player",
            f"{clean_base} {country} jersey",
            f"{first_last} footballer",
            f"{clean_base} player {country_search}",
            f'"{clean_base}" football',
        ]
        if nickname:
            queries.insert(0, f"{nickname} {last_name} {country} football")

    # For single-name players (like Neymar, Casemiro, Bebé)
    if len(parts) == 1:
        queries.insert(0, f"{clean_base} {country_search} football player")
        queries.insert(1, f"{clean_base} footballer portrait")
        if country == 'Brazil':
            queries.insert(2, f"{clean_base} selecao brasileira")

    return queries


def collect_image_for_player(name, country, output_dir, delay=0.3, attempt=0):
    """Try to find and download an image for a single player.
    Self-healing: adapts strategy based on what's working and what's not."""
    global _consecutive_failures, _source_health

    safe_name = sanitize_filename(name)
    save_path = os.path.join(output_dir, country, f"{safe_name}.jpg")
    errors = []

    queries = build_search_queries(name, country, attempt=attempt)

    # If we've had many consecutive failures, slow down (might be rate limited)
    if _consecutive_failures >= 5:
        print(f"      Cooling down ({_consecutive_failures} consecutive failures)...")
        time.sleep(5)
        _consecutive_failures = 0
        # Reset source health to give them another chance
        for k in _source_health:
            _source_health[k] = max(0, _source_health[k] - 2)

    # Helper to try a search source
    def try_source(source_name, search_fn, query_list, source_label):
        if _source_health.get(source_name, 0) > 3:
            errors.append(f"{source_name}: source temporarily disabled")
            return None

        for qi, query in enumerate(query_list):
            results = search_fn(query, max_results=MAX_RESULTS_TO_TRY)
            if delay > 0:
                time.sleep(delay)

            if not results:
                _source_health[source_name] = _source_health.get(source_name, 0) + 1
                errors.append(f"{source_name}[q{qi}]: no results")
                continue

            _source_health[source_name] = 0

            for ri, result in enumerate(results):
                url = result.get('url', '')
                if not url:
                    continue

                if any(skip in url.lower() for skip in [
                    'logo', 'icon', 'badge', 'flag', 'banner', 'sprite',
                    'favicon', 'placeholder', 'default_avatar',
                    # Watermark sources
                    'alamy.com', 'gettyimages.com', 'shutterstock.com',
                    'depositphotos.com', 'dreamstime.com', 'istockphoto.com',
                    '123rf.com', 'stock.adobe.com',
                ]):
                    continue

                success, info = download_and_save_image(url, save_path)
                if success:
                    return {
                        'status': 'success',
                        'source': source_label,
                        'query': query,
                        'url': url,
                        'info': info,
                        'file': save_path,
                    }

                errors.append(f"{source_name}[q{qi}][r{ri}]: {info}")
        return None

    # Source 1: TheSportsDB (clean images, no watermarks, free API)
    thumb_url, cutout_url = search_thesportsdb(name)
    if thumb_url:
        success, info = download_and_save_image(thumb_url, save_path)
        if success:
            _consecutive_failures = 0
            return {
                'status': 'success',
                'source': 'thesportsdb',
                'url': thumb_url,
                'info': info,
                'file': save_path,
            }
        errors.append(f"thesportsdb_thumb: {info}")
    if cutout_url:
        success, info = download_and_save_image(cutout_url, save_path)
        if success:
            _consecutive_failures = 0
            return {
                'status': 'success',
                'source': 'thesportsdb',
                'url': cutout_url,
                'info': info,
                'file': save_path,
            }
        errors.append(f"thesportsdb_cutout: {info}")
    if not thumb_url and not cutout_url:
        errors.append("thesportsdb: player not found")
    if delay > 0:
        time.sleep(delay * 0.5)

    # Source 2: Ecosia via Chrome (high-quality, no watermarks)
    num_queries = 4 if attempt > 0 else 3
    result = try_source('ecosia_chrome', search_ecosia_chrome, queries[:num_queries], 'ecosia_chrome')
    if result:
        _consecutive_failures = 0
        return result

    # Source 3: Brave Image Search
    result = try_source('brave', search_brave_images, queries[:num_queries], 'brave')
    if result:
        _consecutive_failures = 0
        return result

    # Source 3: DuckDuckGo Image Search
    result = try_source('ddg', search_ddg_images, queries[:num_queries], 'ddg')
    if result:
        _consecutive_failures = 0
        return result

    # Source 4: Bing Image Search
    result = try_source('bing', search_bing_images, queries[:num_queries], 'bing')
    if result:
        _consecutive_failures = 0
        return result

    # Source 5: SofaScore (smaller headshot but better than nothing)
    sofascore_url = search_sofascore_player(name, country)
    if sofascore_url:
        success, info = download_and_save_image(sofascore_url, save_path, min_size=1000)
        if success:
            _consecutive_failures = 0
            return {
                'status': 'warning',
                'source': 'sofascore',
                'url': sofascore_url,
                'info': info,
                'file': save_path,
                'note': 'sofascore headshot (smaller image)',
            }
        errors.append(f"sofascore: {info}")

    # Source 4: Bing thumbnail direct (last resort)
    clean_name = strip_diacritics(re.sub(r"'[^']*'", '', name).strip())
    thumb_url = f"https://tse1.mm.bing.net/th?q={quote_plus(clean_name + ' footballer ' + country)}&w=400&h=400"
    success, info = download_and_save_image(thumb_url, save_path, min_size=2000)
    if success:
        _consecutive_failures = 0
        return {
            'status': 'warning',
            'source': 'bing_thumbnail',
            'url': thumb_url,
            'info': info,
            'file': save_path,
            'note': 'bing thumbnail - review recommended',
        }

    errors.append(f"bing_thumb: {info}")
    _consecutive_failures += 1

    return {
        'status': 'failed',
        'errors': errors,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Soccer Player Image Collector')
    parser.add_argument('--csv', default='players.csv', help='Path to players CSV (default: players.csv)')
    parser.add_argument('--output', default='outputs', help='Output directory (default: outputs)')
    parser.add_argument('--skip-existing', action='store_true', help='Skip players whose image already exists')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between searches in seconds (default: 0.5)')
    parser.add_argument('--start-from', type=int, default=1, help='Start from player number N (default: 1)')
    args = parser.parse_args()

    # Load players
    players = []
    with open(args.csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            players.append((row['name'].strip(), row['country'].strip()))

    total = len(players)
    countries = sorted(set(c for _, c in players))

    # Load existing log if resuming
    log_path = os.path.join(os.path.dirname(args.csv), 'collection_log.json')
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            log = json.load(f)
    else:
        log = {}

    # Print header
    print()
    print("Soccer Player Image Collector")
    print("=" * 50)
    print(f"  CSV:            {args.csv} ({total} players, {len(countries)} countries)")
    print(f"  Output:         {args.output}/")
    print(f"  Skip existing:  {'Yes' if args.skip_existing else 'No'}")
    print(f"  Delay:          {args.delay}s")
    print(f"  Start from:     #{args.start_from}")
    print("=" * 50)
    print()

    # Create country directories
    for country in countries:
        os.makedirs(os.path.join(args.output, country), exist_ok=True)

    # Stats
    stats = {'success': 0, 'warning': 0, 'failed': 0, 'skipped': 0}
    source_counts = {}
    failed_players = []
    warned_players = []

    start_time = time.time()

    for i, (name, country) in enumerate(players):
        num = i + 1

        # Skip if before start-from
        if num < args.start_from:
            continue

        safe_name = sanitize_filename(name)
        save_path = os.path.join(args.output, country, f"{safe_name}.jpg")

        # Skip existing
        if args.skip_existing and os.path.exists(save_path):
            stats['skipped'] += 1
            print(f"[{num:>3}/{total}] {name} ({country}){'.' * max(1, 45 - len(name) - len(country))} SKIP (exists)")
            continue

        # Collect image
        result = collect_image_for_player(name, country, args.output, delay=args.delay)

        # Format output
        pad = '.' * max(1, 45 - len(name) - len(country))

        if result['status'] == 'success':
            stats['success'] += 1
            src = result['source']
            source_counts[src] = source_counts.get(src, 0) + 1
            print(f"[{num:>3}/{total}] {name} ({country}){pad} OK ({src}, {result['info']})")

        elif result['status'] == 'warning':
            stats['warning'] += 1
            src = result['source']
            source_counts[src] = source_counts.get(src, 0) + 1
            warned_players.append((name, country, result.get('note', '')))
            print(f"[{num:>3}/{total}] {name} ({country}){pad} WARN ({src} - review needed)")

        else:
            stats['failed'] += 1
            failed_players.append((name, country, result.get('errors', [])))
            print(f"[{num:>3}/{total}] {name} ({country}){pad} FAIL (all sources exhausted)")

        # Update log
        log[name] = {
            'country': country,
            'status': result['status'],
            'source': result.get('source', 'none'),
            'file': result.get('file', ''),
            'timestamp': datetime.now().isoformat(),
        }
        if result.get('errors'):
            log[name]['errors'] = result['errors'][:5]  # keep first 5 errors

        # Save log periodically (every 10 players)
        if num % 10 == 0:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(log, f, indent=2, ensure_ascii=False)

    # ── Auto-retry failed players with alternative strategies ──────────────
    if failed_players:
        print()
        print(f"  Retrying {len(failed_players)} failed player(s) with alternative strategies...")
        print()

        # Reset source health for retry pass
        for k in _source_health:
            _source_health[k] = 0

        retry_succeeded = []
        for name, country, _ in list(failed_players):
            safe_name = sanitize_filename(name)
            save_path = os.path.join(args.output, country, f"{safe_name}.jpg")
            num_label = f"RETRY"

            result = collect_image_for_player(name, country, args.output,
                                              delay=args.delay * 2, attempt=1)

            pad = '.' * max(1, 45 - len(name) - len(country))

            if result['status'] in ('success', 'warning'):
                src = result['source']
                source_counts[src] = source_counts.get(src, 0) + 1
                stats['failed'] -= 1
                if result['status'] == 'success':
                    stats['success'] += 1
                else:
                    stats['warning'] += 1
                    warned_players.append((name, country, result.get('note', '')))
                retry_succeeded.append((name, country))
                print(f"[{num_label}] {name} ({country}){pad} RECOVERED ({src}, {result.get('info', '')})")

                log[name] = {
                    'country': country,
                    'status': result['status'],
                    'source': result.get('source', 'none'),
                    'file': result.get('file', ''),
                    'timestamp': datetime.now().isoformat(),
                    'recovered_on_retry': True,
                }
            else:
                print(f"[{num_label}] {name} ({country}){pad} STILL FAILED")

        # Remove recovered players from failed list
        for item in retry_succeeded:
            failed_players = [(n, c, e) for n, c, e in failed_players
                              if (n, c) != item]

    # Final log save
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    elapsed = time.time() - start_time

    # Print summary
    print()
    print("=" * 50)
    print(f"  DONE in {elapsed / 60:.1f} minutes")
    print(f"  Success:  {stats['success']}")
    print(f"  Warnings: {stats['warning']} (manual review recommended)")
    print(f"  Failed:   {stats['failed']}")
    print(f"  Skipped:  {stats['skipped']}")
    print()
    if source_counts:
        print("  Sources:")
        for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
            print(f"    {src}: {count}")
    print("=" * 50)

    # Write summary file
    summary_path = os.path.join(os.path.dirname(args.csv), 'collection_summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"Collection Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        f.write(f"Total: {total} | Success: {stats['success']} | Warnings: {stats['warning']} | Failed: {stats['failed']} | Skipped: {stats['skipped']}\n")
        f.write(f"Time: {elapsed / 60:.1f} minutes\n\n")

        if warned_players:
            f.write("WARNINGS (manual review recommended):\n")
            for name, country, note in warned_players:
                f.write(f"  - {name} ({country}) - {note}\n")
            f.write("\n")

        if failed_players:
            f.write("FAILURES:\n")
            for name, country, errs in failed_players:
                f.write(f"  - {name} ({country})\n")
                for err in errs[:3]:
                    f.write(f"      {err}\n")
            f.write("\n")

        if source_counts:
            f.write("Source breakdown:\n")
            for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
                f.write(f"  {src}: {count}\n")

    print(f"\n  Summary saved to: {summary_path}")
    print(f"  Full log saved to: {log_path}")
    print()


if __name__ == '__main__':
    main()

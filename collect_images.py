#!/usr/bin/env python3
"""
Soccer Player Image Collector
Downloads high-quality images of soccer players in their jerseys.
Uses DuckDuckGo Image Search (no API key needed).
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime
from io import BytesIO
from urllib.parse import quote_plus

import requests

# Auto-install Pillow if missing
try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow', '-q'])
    from PIL import Image


# ── Constants ──────────────────────────────────────────────────────────────────

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

MAX_RETRIES = 3
RETRY_DELAY = 2.0
MIN_IMAGE_SIZE = 5000  # bytes - skip tiny images
MAX_RESULTS_TO_TRY = 8  # try up to 8 image results before giving up

COUNTRY_SEARCH_NAMES = {
    'Ivory Coast': "Côte d'Ivoire",
    'Cape Verde': 'Cape Verde Cabo Verde',
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def strip_diacritics(text):
    """Remove accents/diacritics from text for search queries."""
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))


def sanitize_filename(name):
    """Make a string safe for use as a filename."""
    # Keep the name readable but remove problematic characters
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()


def fetch_with_retry(url, headers=None, timeout=20, stream=False):
    """Fetch a URL with retry logic and exponential backoff."""
    hdrs = {**HEADERS, **(headers or {})}
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, headers=hdrs, timeout=timeout, stream=stream)
            if r.status_code == 429:
                wait = RETRY_DELAY * (2 ** attempt)
                time.sleep(wait)
                continue
            return r
        except (requests.ConnectionError, requests.Timeout):
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
    # Extract vqd token from response
    match = re.search(r'vqd=["\']([^"\']+)["\']', r.text)
    if match:
        return match.group(1)
    match = re.search(r'vqd=([^&"\']+)', r.text)
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


# ── Image Download & Validation ───────────────────────────────────────────────

def download_and_save_image(url, save_path):
    """Download an image, validate it, convert to JPEG, and save."""
    r = fetch_with_retry(url, timeout=15, stream=True)
    if r is None or r.status_code != 200:
        return False, "download failed"

    content_type = r.headers.get('Content-Type', '')
    if not content_type.startswith('image/'):
        return False, f"not an image ({content_type})"

    image_data = r.content
    if len(image_data) < MIN_IMAGE_SIZE:
        return False, f"too small ({len(image_data)} bytes)"

    try:
        img = Image.open(BytesIO(image_data))

        # Check dimensions - we want decent sized images
        w, h = img.size
        if w < 150 or h < 150:
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

def build_search_queries(name, country):
    """Build a list of search queries to try, from most specific to least."""
    country_search = COUNTRY_SEARCH_NAMES.get(country, country)
    clean_name = strip_diacritics(name)

    # Remove quotes/nicknames for cleaner search
    base_name = re.sub(r"'[^']*'", '', name).strip()
    base_name = re.sub(r'\s+', ' ', base_name)
    clean_base = strip_diacritics(base_name)

    queries = [
        f"{clean_base} {country_search} national team football",
        f"{clean_base} footballer {country_search}",
        f"{clean_name} soccer player",
        f"{clean_base} football player",
    ]

    # For single-name players (like Neymar, Casemiro)
    if len(base_name.split()) == 1:
        queries.insert(0, f"{clean_base} {country_search} football player")
        queries.insert(1, f"{clean_base} Brazil footballer")  # many single-name players are Brazilian

    return queries


def collect_image_for_player(name, country, output_dir, delay=0.3):
    """Try to find and download an image for a single player."""
    safe_name = sanitize_filename(name)
    save_path = os.path.join(output_dir, country, f"{safe_name}.jpg")
    errors = []

    queries = build_search_queries(name, country)

    # Source 1: DuckDuckGo Image Search
    for qi, query in enumerate(queries[:3]):  # Try up to 3 DDG queries
        results = search_ddg_images(query, max_results=MAX_RESULTS_TO_TRY)
        if delay > 0:
            time.sleep(delay)

        for ri, result in enumerate(results):
            url = result.get('url', '')
            if not url:
                continue

            # Skip obviously bad URLs
            if any(skip in url.lower() for skip in ['logo', 'icon', 'badge', 'flag', 'banner', 'sprite']):
                continue

            success, info = download_and_save_image(url, save_path)
            if success:
                return {
                    'status': 'success',
                    'source': 'ddg',
                    'query': query,
                    'url': url,
                    'info': info,
                    'file': save_path,
                }

            errors.append(f"ddg[q{qi}][r{ri}]: {info}")

    # Source 2: Bing Image Search (fallback)
    for qi, query in enumerate(queries[:2]):  # Try up to 2 Bing queries
        results = search_bing_images(query, max_results=MAX_RESULTS_TO_TRY)
        if delay > 0:
            time.sleep(delay)

        for ri, result in enumerate(results):
            url = result.get('url', '')
            if not url:
                continue

            if any(skip in url.lower() for skip in ['logo', 'icon', 'badge', 'flag', 'banner', 'sprite']):
                continue

            success, info = download_and_save_image(url, save_path)
            if success:
                return {
                    'status': 'warning',
                    'source': 'bing',
                    'query': query,
                    'url': url,
                    'info': info,
                    'file': save_path,
                    'note': 'bing fallback - manual review recommended',
                }

            errors.append(f"bing[q{qi}][r{ri}]: {info}")

    # Source 3: Bing thumbnail direct (last resort)
    clean_name = strip_diacritics(re.sub(r"'[^']*'", '', name).strip())
    thumb_url = f"https://tse1.mm.bing.net/th?q={quote_plus(clean_name + ' footballer')}&w=400&h=400"
    success, info = download_and_save_image(thumb_url, save_path)
    if success:
        return {
            'status': 'warning',
            'source': 'bing_thumbnail',
            'url': thumb_url,
            'info': info,
            'file': save_path,
            'note': 'bing thumbnail last resort - manual review strongly recommended',
        }

    errors.append(f"bing_thumb: {info}")

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

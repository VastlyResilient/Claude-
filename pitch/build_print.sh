#!/bin/bash
# Print-ready build: 0.125" bleed on every side (8.75 x 11.25" sheets, trim 8.5 x 11"),
# upscaled photos from assets/print/, high JPEG quality, no downsampling.
set -e
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
OUT="Absolute-Transportation-Partnership-Deck-PRINT.pdf"
python3 - <<'PY'
import os, re, cv2
s = open('deck.html').read()
# swap in print-resolution photos where they exist
for f in sorted(os.listdir('assets/print')):
    if f.startswith('_'): continue
    stem = os.path.splitext(f)[0]
    s = re.sub(r'assets/%s\.(jpg|png)' % re.escape(stem), 'assets/print/' + f, s)
# Images with text baked in (client cover, occasions page) must not be enlarged into the
# bleed, or the text drifts toward the cut. Extend their edges by reflection instead, so
# every original pixel stays exactly where it sits in the trimmed page.
def extend(src, dst, sides):
    im = cv2.imread(src); h, w = im.shape[:2]
    p = round(w * 12 / 816)                       # 0.125in at this image's scale
    t, b, l, r = [p if k in sides else 0 for k in 'tblr']
    cv2.imwrite(dst, cv2.copyMakeBorder(im, t, b, l, r, cv2.BORDER_REFLECT), [cv2.IMWRITE_JPEG_QUALITY, 95])
def pick(name, orig):
    return 'assets/print/' + name if os.path.exists('assets/print/' + name) else orig
extend(pick('cover.jpg', 'assets/cover.png'), 'assets/print/_cover_bleed.jpg', 'lr')
extend(pick('occasions.jpg', 'assets/occasions.jpg'), 'assets/print/_occasions_bleed.jpg', 'tblr')
s = re.sub(r'<img class="bleed" src="assets/(print/)?cover\.(png|jpg)" alt="" style="object-position:center 40%">',
           '<img class="bleed" data-bleed="extend" src="assets/print/_cover_bleed.jpg" alt="" style="object-position:center 38.33%">', s)
s = re.sub(r'<img class="bleed" src="assets/(print/)?occasions\.jpg"',
           '<img class="bleed" data-bleed="extend" src="assets/print/_occasions_bleed.jpg"', s)
assert s.count('data-bleed="extend"') == 2
bleed = '''
<style>
@page{size:8.75in 11.25in;margin:0}
.sheet{width:8.75in;height:11.25in;padding:.125in;box-sizing:border-box;overflow:hidden;break-after:page;page-break-after:always}
.sheet:last-child{break-after:auto;page-break-after:auto}
.sheet>.page{overflow:visible!important;break-after:auto!important;page-break-after:auto!important;margin:0!important;box-shadow:none}
</style>
<script>
(function(){
  const B = 12; // 0.125in in CSS px
  document.querySelectorAll('section.page').forEach(pg => {
    const sh = document.createElement('div'); sh.className = 'sheet';
    pg.parentNode.insertBefore(sh, pg); sh.appendChild(pg);
    // carry the page background into the bleed
    sh.style.background = getComputedStyle(pg).backgroundColor;
  });
  document.querySelectorAll('section.page').forEach(pg => {
    const P = pg.getBoundingClientRect();
    const touches = el => {
      const r = el.getBoundingClientRect();
      return {l: r.left <= P.left + .5, t: r.top <= P.top + .5, r: r.right >= P.right - .5, b: r.bottom >= P.bottom - .5, rect: r};
    };
    const visual = el => {
      const cs = getComputedStyle(el);
      return el.tagName === 'IMG' || cs.backgroundImage !== 'none' ||
             (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent') ||
             cs.overflow === 'hidden';
    };
    const walk = el => {
      for (const c of el.children) {
        const t = touches(c);
        if (c.dataset.bleed === 'extend') {
          c.style.inset = `${-B}px`; c.style.width = `calc(100% + ${2 * B}px)`; c.style.height = `calc(100% + ${2 * B}px)`;
        } else if ((t.l || t.t || t.r || t.b) && visual(c)) {
          const r = t.rect, nl = t.l ? B : 0, nt = t.t ? B : 0;
          const nw = r.width + nl + (t.r ? B : 0), nh = r.height + nt + (t.b ? B : 0);
          c.style.transformOrigin = '0 0';
          c.style.transform = `translate(${-nl}px,${-nt}px) scale(${nw / r.width},${nh / r.height})` + (c.style.transform && c.style.transform !== 'none' ? ' ' + c.style.transform : '');
        } else {
          walk(c);
        }
      }
    };
    walk(pg);
  });
})();
</script>
'''
s = s.replace('</body>', bleed + '</body>')
open('_print.html', 'w').write(s)
PY
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=_rawp.pdf _print.html >/dev/null 2>&1
python3 - "$OUT" <<'PY'
import sys, fitz, os
out = sys.argv[1]
d = fitz.open("_rawp.pdf")
smasks = set()
for x in range(1, d.xref_length()):
    if d.xref_is_image(x):
        sm = d.xref_get_key(x, "SMask")
        if sm and sm[0] == "xref": smasks.add(int(sm[1].split()[0]))
for x in range(1, d.xref_length()):
    if not d.xref_is_image(x) or x in smasks: continue
    pix = fitz.Pixmap(d, x)
    if pix.alpha: continue
    if pix.n >= 5: pix = fitz.Pixmap(fitz.csRGB, pix)
    d.update_stream(x, pix.tobytes("jpeg", jpg_quality=92), new=True, compress=False)
    for k, v in (("Filter", "/DCTDecode"), ("ColorSpace", "/DeviceRGB"), ("BitsPerComponent", "8"), ("DecodeParms", "null")):
        d.xref_set_key(x, k, v)
d.subset_fonts()
d.save(out, garbage=4, deflate=True, deflate_images=False, clean=False)
r = d[0].rect
print("pages", d.page_count, "sheet", round(r.width / 72, 3), "x", round(r.height / 72, 3), "in", "size", round(os.path.getsize(out) / 1e6, 1), "MB")
PY
rm -f _rawp.pdf _print.html assets/print/_*_bleed.jpg

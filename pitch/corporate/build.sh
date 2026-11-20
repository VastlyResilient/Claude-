#!/bin/bash
# Build the personalized corporate decks: HTML from ../deck.html, then PDF.
set -e
cd "$(dirname "$0")"
CHROME=$(ls /opt/pw-browsers/chromium-*/chrome-linux*/chrome 2>/dev/null | head -1)
python3 build_corporate.py "$@"
for key in ${@:-charter subway}; do
  case $key in charter) name="Charter-Communications";; subway) name="Subway";; *) name=$key;; esac
  OUT="Absolute-Transportation-x-$name.pdf"
  "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf=_raw.pdf $key.html >/dev/null 2>&1
  python3 -W ignore - "$OUT" <<'PY'
import sys, fitz, os
out = sys.argv[1]; d = fitz.open("_raw.pdf"); smasks = set()
for x in range(1, d.xref_length()):
    if d.xref_is_image(x):
        sm = d.xref_get_key(x, "SMask")
        if sm and sm[0] == "xref": smasks.add(int(sm[1].split()[0]))
for x in range(1, d.xref_length()):
    if not d.xref_is_image(x) or x in smasks: continue
    pix = fitz.Pixmap(d, x)
    if pix.alpha: continue
    if pix.n >= 5: pix = fitz.Pixmap(fitz.csRGB, pix)
    if pix.n != 3: pix = fitz.Pixmap(fitz.csRGB, pix)
    if pix.width > 1800:                      # email build: cap photos at ~210 ppi on a letter page
        import cv2, numpy as np
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)
        h = round(pix.height * 1800 / pix.width)
        a = np.ascontiguousarray(cv2.resize(a, (1800, h), interpolation=cv2.INTER_AREA))
        pix = fitz.Pixmap(fitz.csRGB, 1800, h, a.tobytes(), False)
        d.xref_set_key(x, "Width", "1800"); d.xref_set_key(x, "Height", str(h))
    d.update_stream(x, pix.tobytes("jpeg", jpg_quality=80), new=True, compress=False)
    for k, v in (("Filter", "/DCTDecode"), ("ColorSpace", "/DeviceRGB"), ("BitsPerComponent", "8"), ("DecodeParms", "null")):
        d.xref_set_key(x, k, v)
d.subset_fonts(); d.save(out, garbage=4, deflate=True, deflate_images=False, clean=False)
print(out, "pages", d.page_count, "size", round(os.path.getsize(out) / 1e6, 2), "MB")
PY
  rm -f _raw.pdf
done

#!/bin/bash
set -e
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
OUT="Absolute-Transportation-Partnership-Deck.pdf"
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf=_raw.pdf deck.html >/dev/null 2>&1
python3 - "$OUT" <<'PY'
import sys, fitz, os
out=sys.argv[1]
d=fitz.open("_raw.pdf")
# collect xrefs used as soft masks (transparency) so we never JPEG them
smasks=set()
for xref in range(1, d.xref_length()):
    if not d.xref_is_image(xref): continue
    sm=d.xref_get_key(xref,"SMask")
    if sm and sm[0]=="xref":
        smasks.add(int(sm[1].split()[0]))
for xref in range(1, d.xref_length()):
    if not d.xref_is_image(xref): continue
    if xref in smasks: continue                 # this IS a mask — leave it
    pix=fitz.Pixmap(d, xref)
    if pix.alpha:                               # transparent image (logo) — leave as-is
        continue
    if pix.n>=5: pix=fitz.Pixmap(fitz.csRGB, pix)
    jpg=pix.tobytes("jpeg", jpg_quality=78)
    d.update_stream(xref, jpg, new=True, compress=False)
    d.xref_set_key(xref,"Filter","/DCTDecode")
    d.xref_set_key(xref,"ColorSpace","/DeviceRGB")
    d.xref_set_key(xref,"BitsPerComponent","8")
    d.xref_set_key(xref,"DecodeParms","null")
d.subset_fonts()
d.save(out, garbage=4, deflate=True, deflate_images=False, clean=False)
print("pages",d.page_count,"size",round(os.path.getsize(out)/1e6,2),"MB")
PY
rm -f _raw.pdf _t_*.pdf

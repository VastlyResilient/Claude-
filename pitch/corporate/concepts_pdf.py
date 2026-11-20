"""Compress a Chromium PDF for email. usage: concepts_pdf.py raw.pdf out.pdf"""
import sys, fitz, os, cv2, numpy as np
d = fitz.open(sys.argv[1]); out = sys.argv[2]; sm = set()
for x in range(1, d.xref_length()):
    if d.xref_is_image(x):
        s = d.xref_get_key(x, "SMask")
        if s and s[0] == "xref": sm.add(int(s[1].split()[0]))
for x in range(1, d.xref_length()):
    if not d.xref_is_image(x) or x in sm: continue
    pix = fitz.Pixmap(d, x)
    if pix.alpha: continue
    if pix.n != 3: pix = fitz.Pixmap(fitz.csRGB, pix)
    if pix.width > 1800:
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3); h = round(pix.height * 1800 / pix.width)
        pix = fitz.Pixmap(fitz.csRGB, 1800, h, np.ascontiguousarray(cv2.resize(a, (1800, h), interpolation=cv2.INTER_AREA)).tobytes(), False)
        d.xref_set_key(x, "Width", "1800"); d.xref_set_key(x, "Height", str(h))
    d.update_stream(x, pix.tobytes("jpeg", jpg_quality=80), new=True, compress=False)
    for k, v in (("Filter", "/DCTDecode"), ("ColorSpace", "/DeviceRGB"), ("BitsPerComponent", "8"), ("DecodeParms", "null")): d.xref_set_key(x, k, v)
d.subset_fonts(); d.save(out, garbage=4, deflate=True, deflate_images=False, clean=False)
print(out, d.page_count, "pages", round(os.path.getsize(out) / 1e6, 2), "MB")

"""usage: gen.py out.jpg aspect size model use_logo(0/1) prompt"""
import sys, json, base64, urllib.request, os, time, ssl
out, aspect, size, model, use_logo, prompt = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] == '1', sys.argv[6]
content = [{"type": "text", "text": prompt}]
if use_logo:
    b = base64.b64encode(open('/home/user/Claude-/pitch/corporate/assets/_logo_ref.png', 'rb').read()).decode()
    content.append({"type": "image_url", "image_url": {"url": "data:image/png;base64," + b}})
body = {"model": model, "messages": [{"role": "user", "content": content}], "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": aspect, "image_size": size}}
req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                             headers={"Authorization": "Bearer proxy-injected", "Content-Type": "application/json"})
ctx = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE') or '/root/.ccr/ca-bundle.crt')
for attempt in range(3):
    try:
        t = time.time(); r = json.load(urllib.request.urlopen(req, timeout=300, context=ctx))
        msg = r['choices'][0]['message']; imgs = msg.get('images') or []
        if not imgs: raise RuntimeError('no image: ' + json.dumps(r)[:400])
        url = imgs[0]['image_url']['url']; raw = base64.b64decode(url.split(',', 1)[1])
        tmp = out + '.raw'; open(tmp, 'wb').write(raw)
        import cv2
        im = cv2.imread(tmp); cv2.imwrite(out, im, [cv2.IMWRITE_JPEG_QUALITY, 93]); os.remove(tmp)
        print(f"OK {os.path.basename(out)} {im.shape[1]}x{im.shape[0]} {time.time()-t:.0f}s cost={r.get('usage',{}).get('cost')}", flush=True); break
    except Exception as e:
        print(f"retry {attempt} {os.path.basename(out)}: {str(e)[:300]}", flush=True); time.sleep(5)

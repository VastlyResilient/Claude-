import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
G=os.path.dirname(os.path.abspath(__file__)); A='/home/user/Claude-/pitch/corporate/assets'; GEM='google/gemini-3.1-flash-image'
ST=(" Shot on medium-format film, Kodak Portra tones, muted restrained palette of warm ivory, stone, deep green-black and soft black, fine film grain, natural light with deep soft shadows and gentle falloff, quiet old-money elegance with a modern vehicle, composed and unhurried, nothing flashy, no lens flare. "
    "Proportions true to the real production vehicle. No text, no signage, no watermarks, no license plate text.")
ESC="a gloss-black current-generation Cadillac Escalade (real production model)"; AVI="a gloss-black current-generation Lincoln Aviator (real production model)"
J=[('om_cover.jpg','2:3',"Vertical photograph: "+ESC+" standing half in shadow beneath the stone porte-cochere of an old limestone building, late-afternoon light raking across the bonnet and one column, long soft shadows on pale gravel, a large calm area of shadowed stone in the upper third."+ST),
 ('om_handle.jpg','4:5',"Close detail photograph of a chrome door handle and the curve of a gloss-black car door, a single band of soft window light across the paint, the rest falling into shadow."+ST),
 ('om_leather.jpg','4:5',"Close detail photograph of hand-stitched black leather rear seats in a luxury SUV, a shaft of low sunlight crossing the stitching, a folded linen-coloured blanket at the edge of frame."+ST),
 ('om_hand.jpg','4:5',"Close detail photograph of a chauffeur's hand in a black leather glove resting on the edge of an open car door, white shirt cuff and dark suit sleeve, soft side light, shallow depth of field."+ST),
 ('om_bw.jpg','2:3',"Black-and-white vertical photograph, rich tonal range: a chauffeur in a tailored dark suit seen in profile holding open the rear door of a black luxury SUV beneath a stone arch, strong window-like side light, deep shadows, timeless and dignified."+ST.replace('Kodak Portra tones, muted restrained palette of warm ivory, stone, deep green-black and soft black','classic silver-gelatin black and white')),
 ('om_cabin.jpg','3:2',"Rear cabin of a luxury SUV seen from the open door: black leather seats, a folded newspaper, reading glasses and a leather folio on the seat, slats of morning light and shadow falling across the interior."+ST),
 ('om_drive.jpg','3:2',"Wide photograph: a long tree-lined gravel drive in early morning mist leading toward a stone house, "+AVI+" small in the frame driving away, soft diffused light."+ST),
 ('om_still.jpg','4:5',"Still life on a dark walnut table by a window: a car key, a pair of black leather driving gloves, a folded itinerary card (blank) and a small glass of water, soft daylight from the left, deep shadow on the right."+ST),
 ('om_charter.jpg','3:2',"Wide quiet photograph at early morning: a contemporary glass headquarters on a calm harbor with sailboat masts, "+ESC+" small in the frame waiting on pale stone pavers, soft overcast light, long reflections."+ST),
 ('om_subway.jpg','3:2',"Wide quiet photograph at early morning: a modern low-rise corporate office among New England autumn trees, "+AVI+" small in the frame waiting on the forecourt, soft overcast light, fallen leaves."+ST),
 ('om_fleet.jpg','3:2',"Three gloss-black vehicles, a Cadillac Escalade, a Lincoln Aviator and a Mercedes-Benz Sprinter passenger van, parked in a quiet row along a high old brick wall with climbing ivy, soft even shade with a strip of sunlight on the ground."+ST),
 ('om_window.jpg','2:3',"Vertical photograph from inside the rear seat of a luxury SUV: a rain-beaded window with a softly blurred old stone townhouse street beyond, the dark leather door panel in the foreground, cool quiet light."+ST)]
def run(j):
    out=os.path.join(A,j[0])
    if os.path.exists(out): return 'skip '+j[0]
    r=subprocess.run([sys.executable,'-I',os.path.join(G,'gen.py'),out,j[1],'2K',GEM,'0',j[2]],capture_output=True,text=True); return (r.stdout+r.stderr).strip()[-110:]
with ThreadPoolExecutor(1) as ex:
    for r in ex.map(run,J): print(r,flush=True)
print('ALLDONE')

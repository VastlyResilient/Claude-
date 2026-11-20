import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
G=os.path.dirname(os.path.abspath(__file__)); A='/home/user/Claude-/pitch/corporate/assets'; GEM='google/gemini-3-pro-image'
ST=" Photorealistic editorial photograph shot on a full-frame camera, understated luxury, sharp focus, proportions true to the real production vehicles. No text, no logos on buildings, no watermarks, no license plate text."
ESC="a gloss-black current-generation Cadillac Escalade (real production model, tall vertical LED lights)"; AVI="a gloss-black current-generation Lincoln Aviator (real production model)"; SPR="a gloss-black Mercedes-Benz Sprinter passenger van"
DAY=" Bright, fresh, clean natural morning daylight, lush green trees, airy and optimistic mood."
BLUE=" Blue hour, cool deep-blue tones with small warm accents, calm, modern, precise mood."
J=[('s_chauffeur_day.jpg','2:3',"Vertical photograph: a professional chauffeur in a tailored black suit and tie standing beside the open rear door of "+AVI+" in front of a modern low-rise corporate office with a glass entrance, seen in three-quarter view from behind, welcoming posture."+DAY+ST),
 ('s_road_day.jpg','21:9',"Aerial photograph of a winding Connecticut parkway through dense green summer forest, a single black SUV on the road."+DAY+ST),
 ('s_interior_day.jpg','4:3',"Rear cabin of a gloss-black Cadillac Escalade seen through the open rear door: black leather captain's seats, a bottle of water and a folded newspaper on the console, green trees softly visible through the far window."+DAY+ST),
 ('s_close_day.jpg','2:3',"Vertical photograph: "+AVI+" driving away down a sunlit tree-lined New England road, seen from behind, dappled light on the road, generous open space in the upper half."+DAY+ST),
 ('s_lineup_day.jpg','3:2',ESC+", "+AVI+" and "+SPR+" parked in a neat row on the forecourt of a modern low-rise suburban corporate office building, three-quarter front view, no people."+DAY+ST),
 ('s_team_day.jpg','3:2',"A small group of smiling business professionals in smart casual attire walking from a modern office entrance toward "+SPR+" with its sliding door open, a chauffeur in a black suit waiting beside it."+DAY+ST),
 ('c_lines.jpg','21:9',"Long-exposure photograph of white and red light trails on a highway curving toward a modern city skyline across the water."+BLUE+ST),
 ('c_harbor.jpg','3:2',ESC+" parked on a waterfront promenade beside a marina with sailboats and contemporary glass office buildings, three-quarter front view, wet stone pavers reflecting light, no people."+BLUE+ST),
 ('c_interior_blue.jpg','4:3',"Rear cabin of a gloss-black Cadillac Escalade seen through the open rear door: black leather captain's seats, an open laptop and a phone on the console, city lights softly blurred through the far window."+BLUE+ST),
 ('c_lineup_blue.jpg','3:2',ESC+", "+AVI+" and "+SPR+" parked in a neat row in front of a contemporary glass corporate headquarters on a harbor waterfront, three-quarter front view, no people."+BLUE+ST),
 ('c_chauffeur_blue.jpg','2:3',"Vertical photograph: a professional chauffeur in a tailored black suit and tie standing beside the open rear door of "+ESC+" in front of the glass entrance of a contemporary corporate headquarters, seen in three-quarter view from behind, warm lobby light."+BLUE+ST),
 ('c_exec_blue.jpg','3:2',"A business executive in a navy suit stepping out of "+ESC+" at the entrance of a contemporary glass headquarters, a chauffeur in a black suit holding the door."+BLUE+ST)]
def run(j):
    out=os.path.join(A,j[0])
    if os.path.exists(out): return 'skip '+j[0]
    r=subprocess.run([sys.executable,'-I',os.path.join(G,'gen.py'),out,j[1],'2K',GEM,'0',j[2]],capture_output=True,text=True); return (r.stdout+r.stderr).strip()[-110:]
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(run,J): print(r,flush=True)
print('ALLDONE')

#!/usr/bin/env python3
"""Direction D: a mix of B (cinematic black, large type) and C (the client's logo and
brand colour, numbered structure, clear next steps). 4-page sample per company:
cover, needs, why Absolute, how we'd begin. Writes concepts/<key>-mix.html.
"""
import os, sys
from build_corporate import COMPANIES
from build_concepts import CSS, EXTRA, li

HERE = os.path.dirname(os.path.abspath(__file__))
TINT = {'charter': '#4A9BE6', 'subway': '#19B45A'}     # the brand colour, lifted for legibility on black

MIX_CSS = '''
.D{background:#050505;color:#fff}
.D .lab{font-size:7px;letter-spacing:.34em;text-transform:uppercase;font-weight:500}
.D .dim{color:rgba(255,255,255,.58)} .D .ac{color:var(--ac)}
.D .hair{height:1px;background:rgba(255,255,255,.18)}
.D .big{font-family:'Tight';font-weight:600;text-transform:uppercase;letter-spacing:-.025em;line-height:.94}
.D .thin{font-family:'Tight';font-weight:300}
.D .body{font-size:9.8px;line-height:1.75;font-weight:300;color:rgba(255,255,255,.84)}
.D .num{font-family:'Tight';font-weight:300;font-size:30px;color:var(--ac);line-height:1}
.D .bar{display:flex;justify-content:space-between;align-items:center}
.D .m{left:.6in;right:.6in}
.D .rule{height:2px;background:var(--ac)}
'''


def mix(key):
    c, x = COMPANIES[key], EXTRA[key]
    wl = lambda h: f'<img src="../{c["LOGO_WHITE"]}" alt="{c["CO"]}" style="height:{h}">'
    al = '<img src="../../assets/absolute_logo.png" alt="Absolute Transportation" style="height:22px">'
    foot = lambda n: f'<div class="m bar" style="bottom:.45in"><span class="lab dim">Prepared for {c["CO"]}</span><img src="../../assets/absolute_logo.png" style="height:10px;opacity:.7" alt=""><span class="lab dim">{n}</span></div>'
    cols = [c['COL1'], ('Corporate Travel &amp; Executive Assistants', ['One number and one email for every booking', 'Flight tracking with automatic adjustments', 'Written confirmation of every trip', 'A single, itemized corporate account']), c['COL3'], c['COL4']]
    cards = ''.join(f'''<div><div class="rule"></div><div style="display:flex;gap:14px;align-items:baseline;margin-top:13px"><span class="num">0{i+1}</span><span class="thin" style="font-size:15px">{t}</span></div>{li(its, "font-size:9px;line-height:1.5;font-weight:300;color:rgba(255,255,255,.8);margin-top:7px;padding-left:14px;border-left:1px solid rgba(255,255,255,.2)")}</div>''' for i, (t, its) in enumerate(cols))
    why = [('A real person, every time', 'One number, answered day and night, 365 days a year. No queue, no menu, no call centre.'),
           ('The owners are accountable', 'Family-owned since 2007. The people who own the company dispatch the cars and follow up after the ride.'),
           ('Flights tracked, delays absorbed', 'We watch every arrival in real time and adjust automatically, so the chauffeur is there when the plane actually lands.'),
           ('Chauffeurs built, not found', 'Background-checked, commercially licensed, trained in hospitality, and discreet. What happens in the car stays in the car.'),
           ('Licensed, insured, verifiable', f'U.S. DOT 1567094 · MC-580841 · Connecticut Livery Permit 3117. A certificate naming {c["CO"]} is typically ready the same business day.'),
           ('One clean account', 'Every trip confirmed in writing, and one itemized monthly statement your finance team can reconcile in minutes.')]
    reasons = ''.join(f'''<div style="display:grid;grid-template-columns:.5in 1fr;padding:13px 0;border-bottom:1px solid rgba(255,255,255,.18);align-items:baseline"><span class="num" style="font-size:22px">0{i+1}</span><div><div class="thin" style="font-size:15px">{t}</div><p class="body" style="font-size:9.2px;line-height:1.6;margin-top:4px">{d}</p></div></div>''' for i, (t, d) in enumerate(why))
    steps = [('One call', 'We set up your corporate account and learn how your team travels.'), ('One contact', 'Your travel desk and assistants get one number and one email for every booking.'), ('First trips', 'Every reservation confirmed in writing, every flight tracked in real time.'), ('One statement', 'A single itemized monthly statement, built for easy reconciliation.')]
    st = ''.join(f'''<div><div class="num">0{i+1}</div><div class="thin" style="font-size:15px;margin-top:8px">{t}</div><p class="body" style="font-size:9px;line-height:1.6;margin-top:6px">{d}</p></div>''' for i, (t, d) in enumerate(steps))
    routes = ''.join(f'''<div style="display:grid;grid-template-columns:1fr 1.2in;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.18);align-items:baseline"><span class="thin" style="font-size:13px">{f} <span class="ac">→</span> {t}</span><span class="lab dim" style="font-size:6px;text-align:right">{v}</span></div>''' for f, t, v in c['ROUTES'])
    return f'''
<section class="page D" style="--ac:{TINT[key]}">
  <img class="bleed" src="../assets/{x['NIGHT']}" style="height:74%;object-position:center 30%" alt="">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,5,5,.78) 0%,rgba(5,5,5,.1) 15%,rgba(5,5,5,0) 36%,rgba(5,5,5,.65) 50%,#050505 60%)"></div>
  <div class="m bar" style="top:.5in">{al}<span class="lab dim">Corporate Programme · 2027</span></div>
  <div class="m" style="top:6.05in">
    <div class="lab ac">A partnership proposal for</div>
    <div style="margin-top:16px">{wl('46px')}</div>
    <div class="rule" style="width:64px;margin:26px 0 22px"></div>
    <h1 class="big" style="font-size:66px">{x['CITY_UP']}<br>to anywhere.</h1>
    <p class="body" style="font-size:11px;max-width:4.8in;margin-top:16px">Executive ground transportation built around the way {c['CO_S']} moves — one accountable, family-owned partner for every airport run, every visiting guest, and every travel day that matters.</p>
  </div>
  <div class="m" style="bottom:.5in"><div class="hair"></div><div style="display:grid;grid-template-columns:1.25fr 1.25fr 1fr .8fr;margin-top:14px">
    <div><div class="lab dim" style="font-size:6px">Your headquarters</div><div class="thin" style="font-size:12.5px;margin-top:6px">{x['HQ_ADDR']}</div></div>
    <div><div class="lab dim" style="font-size:6px">Nearest airport</div><div class="thin" style="font-size:12.5px;margin-top:6px">{x['NEAREST']}</div></div>
    <div><div class="lab dim" style="font-size:6px">Our base</div><div class="thin" style="font-size:12.5px;margin-top:6px">North Haven, CT</div></div>
    <div style="text-align:right"><div class="lab dim" style="font-size:6px">Dispatch</div><div class="thin" style="font-size:12.5px;margin-top:6px">24 / 7 / 365</div></div></div></div>
</section>
<section class="page D" style="--ac:{TINT[key]}">
  <img src="../assets/occ_city.jpg" style="position:absolute;left:0;top:0;width:100%;height:4.5in;object-fit:cover;object-position:center 55%" alt="">
  <div style="position:absolute;left:0;right:0;top:0;height:4.5in;background:linear-gradient(180deg,rgba(5,5,5,.7) 0%,rgba(5,5,5,0) 28%,rgba(5,5,5,0) 62%,#050505 100%)"></div>
  <div class="m bar" style="top:.5in"><span class="lab"><span class="ac">01</span> &nbsp;/&nbsp; Your needs</span>{wl(c['LOGO_H_SM'])}</div>
  <div class="m" style="top:4.15in"><h2 class="big" style="font-size:50px">Built around<br>{c['CO_S']}.</h2><p class="body" style="max-width:5.4in;margin-top:14px">{c['NEEDS_LEAD']}</p></div>
  <div class="m" style="top:6.75in;display:grid;grid-template-columns:1fr 1fr;gap:30px .45in">{cards}</div>
  {foot('02')}
</section>
<section class="page D" style="--ac:{TINT[key]}">
  <img src="../assets/chauffeur_{key}.jpg" style="position:absolute;right:0;top:0;width:3.1in;height:100%;object-fit:cover;object-position:42% center" alt="">
  <div style="position:absolute;right:0;top:0;width:3.1in;height:100%;background:linear-gradient(90deg,#050505 0%,rgba(5,5,5,.35) 35%,rgba(5,5,5,.15) 100%)"></div>
  <div style="position:absolute;right:3.1in;top:0;bottom:0;width:0"></div>
  <div style="position:absolute;left:.6in;top:.5in;width:4.75in" class="bar"><span class="lab"><span class="ac">02</span> &nbsp;/&nbsp; Why Absolute</span></div>
  <div style="position:absolute;left:.6in;top:1.05in;width:4.75in">
    <h2 class="big" style="font-size:46px">Six reasons<br>the choice<br>is easy.</h2>
    <p class="body" style="margin-top:14px">You shouldn't have to take our word for it. Here is exactly what {c['CO_S']} gets, in writing, from the first trip.</p>
    <div style="margin-top:18px;border-top:2px solid var(--ac)">{reasons}</div>
    <div style="margin-top:20px;border:1px solid rgba(255,255,255,.3);padding:14px 16px"><div class="lab ac">An easy first step</div><p class="body" style="font-size:10px;margin-top:7px;color:#fff">Send us one trip. See how it feels to hand a traveler to a partner who treats your name the way you do.</p></div>
  </div>
  {foot('03')}
</section>
<section class="page D" style="--ac:{TINT[key]}">
  <div class="m bar" style="top:.5in"><span class="lab"><span class="ac">03</span> &nbsp;/&nbsp; How we'd begin</span>{wl(c['LOGO_H_SM'])}</div>
  <div class="m" style="top:1.05in"><h2 class="big" style="font-size:50px">Simple to start.<br>Simple to keep.</h2></div>
  <div class="m" style="top:2.75in"><div class="rule"></div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.3in;margin-top:16px">{st}</div></div>
  <div class="m" style="top:4.85in"><div class="lab dim">Your most likely routes · corporate rates quoted directly</div><div class="hair" style="margin-top:10px"></div>{routes}</div>
  <div class="m" style="bottom:.95in;height:2.0in;overflow:hidden"><img src="../assets/lineup.jpg" style="width:100%;height:100%;object-fit:cover;object-position:center 64%" alt=""><div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,5,5,.92) 0%,rgba(5,5,5,.6) 50%,rgba(5,5,5,.05) 85%)"></div>
    <div style="position:absolute;left:.3in;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center"><div class="lab ac">Corporate partner reservations</div><div class="big" style="font-size:46px;margin-top:10px;letter-spacing:-.01em">(203) 938-0000</div><div class="thin dim" style="font-size:11px;margin-top:8px">Answered by a real person, day or night · info@absolute-transportation.com</div></div></div>
  {foot('04')}
</section>'''


LIGHT_CSS = '''
.D.L{background:#FAF9F6;color:#0C0C0D}
.D.L .dim{color:rgba(12,12,13,.55)} .D.L .hair{background:rgba(12,12,13,.16)}
.D.L .body{color:#3a3936}
'''


def mix_light(key):
    """White mode: same pages on warm white, daylight photography, the client's true brand colour."""
    c, x = COMPANIES[key], EXTRA[key]
    h = mix(key)
    swaps = [
        ('class="page D"', 'class="page D L"'), (f'--ac:{TINT[key]}', f'--ac:{x["ACCENT"]}'),
        (f'<img class="bleed" src="../assets/{x["NIGHT"]}" style="height:74%;object-position:center 30%" alt="">', f'<img class="bleed" src="../assets/{x["DAY"]}" style="height:56%;object-position:center 55%" alt="">'),
        ('linear-gradient(180deg,rgba(5,5,5,.78) 0%,rgba(5,5,5,.1) 15%,rgba(5,5,5,0) 36%,rgba(5,5,5,.65) 50%,#050505 60%)', 'linear-gradient(180deg,rgba(5,5,5,.5) 0%,rgba(5,5,5,0) 12%,rgba(5,5,5,0) 40%,rgba(5,5,5,.7) 50%,#050505 56%)'),
        ('<div class="m bar" style="top:.5in"><img src="../../assets/absolute_logo.png" alt="Absolute Transportation" style="height:22px"><span class="lab dim">Corporate Programme · 2027</span></div>',
         '<div class="m bar" style="top:.5in"><img src="../../assets/absolute_logo.png" alt="Absolute Transportation" style="height:22px"><span class="lab" style="color:#FFFFFF;text-shadow:0 1px 6px rgba(0,0,0,.6)">Corporate Programme · 2027</span></div>'),
        ('src="../assets/occ_city.jpg"', 'src="../assets/occ_airport.jpg"'), ('object-position:center 55%" alt="">\n  <div style="position:absolute;left:0;right:0;top:0;height:4.5in', 'object-position:center 45%" alt="">\n  <div style="position:absolute;left:0;right:0;top:0;height:4.5in'),
        ('linear-gradient(180deg,rgba(5,5,5,.7) 0%,rgba(5,5,5,0) 28%,rgba(5,5,5,0) 62%,#050505 100%)', 'linear-gradient(180deg,#050505 0%,rgba(5,5,5,.94) 13%,rgba(5,5,5,0) 30%,rgba(5,5,5,0) 68%,#050505 100%)'),
        (f'src="../assets/chauffeur_{key}.jpg"', 'src="../assets/testi.jpg"'), ('object-position:42% center', 'object-position:78% center'),
        ('src="../assets/lineup.jpg" style="width:100%;height:100%;object-fit:cover;object-position:center 64%"', 'src="../assets/occ_group.jpg" style="width:100%;height:100%;object-fit:cover;object-position:center 60%"'),
        (c['LOGO_WHITE'], c['LOGO_COLOR']),
        ('rgba(5,5,5,', 'rgba(250,249,246,'), ('#050505', '#FAF9F6'), ('rgba(255,255,255,', 'rgba(12,12,13,'), ('color:#fff', 'color:#0C0C0D'),
    ]
    for o, n in swaps:
        assert o in h, o[:70]; h = h.replace(o, n)
    return h


if __name__ == '__main__':
    for key in (sys.argv[1:] or COMPANIES):
        html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{COMPANIES[key]["CO"]} — B + C mix</title><style>{CSS}{MIX_CSS}</style></head><body>' + mix(key) + '</body></html>'
        open(os.path.join(HERE, 'concepts', f'{key}-mix.html'), 'w', encoding='utf-8').write(html)
        html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{COMPANIES[key]["CO"]} — B + C mix, white</title><style>{CSS}{MIX_CSS}{LIGHT_CSS}</style></head><body>' + mix_light(key) + '</body></html>'
        open(os.path.join(HERE, 'concepts', f'{key}-mix-white.html'), 'w', encoding='utf-8').write(html)
        print('wrote', key)

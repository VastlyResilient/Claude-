#!/usr/bin/env python3
"""Three design directions per corporate deck, as 3-page samples (cover, needs, routes).

Writes concepts/<key>-concepts.html (9 pages: A, B, C x 3). Content comes from
COMPANIES in build_corporate.py so the samples stay in step with the decks.
"""
import os, sys
from build_corporate import COMPANIES

HERE = os.path.dirname(os.path.abspath(__file__))
F = '../../concepts/fonts'
EXTRA = {
    'charter': dict(ACCENT='#1D5F9E', DAY='day_charter.jpg', DETAIL='detail_escalade.jpg', NIGHT='cover_charter.jpg', CITY_UP='STAMFORD',
                    AIR4='HPN · LGA · JFK · EWR', HQ_ADDR='400 Washington Blvd, Stamford', NEAREST='Westchester County (HPN)'),
    'subway': dict(ACCENT='#008938', DAY='day_subway.jpg', DETAIL='detail_aviator.jpg', NIGHT='cover_subway.jpg', CITY_UP='SHELTON',
                   AIR4='HVN · BDL · HPN · LGA · JFK', HQ_ADDR='1 Corporate Drive, Shelton', NEAREST='Tweed New Haven (HVN)'),
}

CSS = f'''
@font-face{{font-family:'Inter';src:url('{F}/inter-latin-300-normal.woff2') format('woff2');font-weight:300;font-display:block}}
@font-face{{font-family:'Inter';src:url('{F}/inter-latin-400-normal.woff2') format('woff2');font-weight:400;font-display:block}}
@font-face{{font-family:'Inter';src:url('{F}/inter-latin-500-normal.woff2') format('woff2');font-weight:500;font-display:block}}
@font-face{{font-family:'Tight';src:url('{F}/inter-tight-latin-600-normal.woff2') format('woff2');font-weight:600;font-display:block}}
@font-face{{font-family:'Tight';src:url('{F}/inter-tight-latin-300-normal.woff2') format('woff2');font-weight:300;font-display:block}}
@font-face{{font-family:'Cormorant';src:url('{F}/cormorant-garamond-latin-300-normal.woff2') format('woff2');font-weight:300;font-display:block}}
@font-face{{font-family:'Cormorant';src:url('{F}/cormorant-garamond-latin-500-normal.woff2') format('woff2');font-weight:500;font-display:block}}
@font-face{{font-family:'Cormorant';src:url('{F}/cormorant-garamond-latin-400-italic.woff2') format('woff2');font-weight:400;font-style:italic;font-display:block}}
@font-face{{font-family:'Playfair';src:url('../../assets/playfair-700.woff2') format('woff2');font-weight:700;font-display:block}}
@font-face{{font-family:'Playfair';src:url('../../assets/playfair-400i.woff2') format('woff2');font-weight:400;font-style:italic;font-display:block}}
@page{{size:8.5in 11in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased;background:#888}}
.page{{position:relative;width:8.5in;height:11in;overflow:hidden;break-after:page;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page:last-child{{break-after:auto}}
@media screen{{.page{{margin:20px auto}}}}
.m{{position:absolute;left:.75in;right:.75in}}
img.ph{{display:block;width:100%;object-fit:cover}}
.bleed{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
/* A · The Briefing */
.A{{background:#F7F5F1;color:#111}}
.A .label{{font-size:7.5px;letter-spacing:.32em;text-transform:uppercase;font-weight:500}}
.A .mute{{color:#6E6B66}} .A .hair{{height:1px;background:rgba(17,17,17,.16)}}
.A .serif{{font-family:'Cormorant',serif;font-weight:300;letter-spacing:-.01em}} .A .serif i{{font-style:italic;font-weight:400}}
.A .body{{font-size:9.6px;line-height:1.75;font-weight:300;color:#2a2a2a}}
.A .cap{{font-size:7.5px;letter-spacing:.06em;color:#6E6B66;margin-top:8px;font-weight:300}}
.A .cap b{{font-weight:500;color:#111;letter-spacing:.24em;text-transform:uppercase;font-size:7px;margin-right:8px}}
.A .drop::first-letter{{font-family:'Cormorant';font-weight:300;float:left;font-size:54px;line-height:.82;padding:4px 8px 0 0}}
.A .folio{{position:absolute;left:.75in;right:.75in;bottom:.45in;display:flex;justify-content:space-between;align-items:center;font-size:7px;letter-spacing:.3em;text-transform:uppercase;color:#6E6B66}}
/* B · Nocturne */
.B{{background:#050505;color:#fff}}
.B .lab{{font-size:7px;letter-spacing:.34em;text-transform:uppercase;font-weight:500}} .B .dim{{color:rgba(255,255,255,.55)}}
.B .hair{{height:1px;background:rgba(255,255,255,.18)}}
.B .big{{font-family:'Tight';font-weight:600;text-transform:uppercase;letter-spacing:-.025em;line-height:.94}}
.B .thin{{font-family:'Tight';font-weight:300}}
.B .body{{font-size:9.6px;line-height:1.75;font-weight:300;color:rgba(255,255,255,.82)}}
.B .bar{{display:flex;justify-content:space-between;align-items:center}}
/* C · Signature */
.C{{background:#FBFAF7;color:#0C0C0D}}
.C .k{{font-size:8px;letter-spacing:.34em;text-transform:uppercase;font-weight:500;color:var(--ac)}}
.C h1,.C h2{{font-family:'Playfair';font-weight:700;letter-spacing:-.01em}}
.C .body{{font-size:9.8px;line-height:1.75;font-weight:300;color:#3a3936}}
.C .num{{font-family:'Tight';font-weight:300;font-size:34px;color:var(--ac);line-height:1}}
.C .line{{height:1px;background:rgba(12,12,13,.14)}}
'''


def li(items, style):
    return ''.join(f'<div style="{style}">{i}</div>' for i in items)


def concept_a(c, x):
    cols = [c['COL1'], ('Corporate Travel &amp; Executive Assistants', ['One number and one email for every booking', 'Flight tracking with automatic adjustments', 'Written confirmation of every trip', 'A single, itemized corporate account']), c['COL3'], c['COL4']]
    rom = ['I', 'II', 'III', 'IV']
    needs = ''.join(f'''<div style="border-top:1px solid rgba(17,17,17,.16);padding-top:12px"><div style="display:flex;gap:10px;align-items:baseline"><span class="serif" style="font-size:19px"><i>{rom[i]}</i></span><span class="label" style="font-size:7px">{t}</span></div>{li(its, "font-size:8.8px;line-height:1.5;font-weight:300;color:#2a2a2a;margin-top:6px")}</div>''' for i, (t, its) in enumerate(cols))
    routes = ''.join(f'''<div style="display:grid;grid-template-columns:1fr 1.5in;padding:12px 0;border-bottom:1px solid rgba(17,17,17,.16);align-items:baseline"><span class="serif" style="font-size:19px">{f} <i style="color:#6E6B66">to</i> {t}</span><span class="label mute" style="font-size:6.5px;text-align:right">{v}</span></div>''' for f, t, v in c['ROUTES'])
    return f'''
<section class="page A">
  <div class="m" style="top:.55in;display:flex;justify-content:space-between;align-items:center"><img src="../../assets/absolute_logo.png" style="height:17px" alt="Absolute Transportation"><div class="label">The Corporate Edition</div><div class="label mute">Vol. 01 — 2027</div></div>
  <div class="m hair" style="top:.86in"></div>
  <div class="m" style="top:1.2in">
    <div class="label mute">A private briefing prepared for</div>
    <img src="../{c['LOGO_COLOR']}" alt="{c['CO']}" style="height:{c['LOGO_H']};margin-top:14px;display:block">
    <h1 class="serif" style="font-size:78px;line-height:.92;margin-top:26px">Your people,<br><i>well arrived.</i></h1>
    <p class="body" style="font-size:11px;max-width:3.7in;margin-top:20px">Executive ground transportation for your {c['HQ_CITY']} headquarters — and the standards we keep so every traveler arrives composed, and every guest arrives impressed.</p>
  </div>
  <div class="m" style="top:5.55in"><img class="ph" src="../assets/{x['DAY']}" style="height:4.2in;object-position:center 60%" alt=""><div class="cap"><b>Cover</b>Detailed and waiting, before the first traveler of the day.</div></div>
  <div class="m" style="bottom:.45in;display:flex;justify-content:space-between;font-size:7px;letter-spacing:.3em;text-transform:uppercase"><span><span class="mute">01</span>&nbsp; Your Needs</span><span><span class="mute">02</span>&nbsp; Your Routes</span><span><span class="mute">03</span>&nbsp; The Fleet</span><span><span class="mute">04</span>&nbsp; The Chauffeurs</span><span><span class="mute">05</span>&nbsp; The Partnership</span></div>
</section>
<section class="page A">
  <div class="m" style="top:.55in;display:flex;justify-content:space-between;align-items:center"><div class="label">01 — Built around {c['CO_S']}</div><img src="../{c['LOGO_COLOR']}" alt="{c['CO']}" style="height:20px"></div>
  <div class="m hair" style="top:.86in"></div>
  <div class="m" style="top:1.15in;display:grid;grid-template-columns:1fr 2.75in;gap:.4in">
    <div><h2 class="serif" style="font-size:46px;line-height:.98">Whatever {c['CO_S']} plans, <i>we're the ground under it.</i></h2>
      <p class="body drop" style="margin-top:20px;font-size:10.2px">{c['NEEDS_LEAD']}</p></div>
    <div><img class="ph" src="../assets/occ_airport.jpg" style="height:3.15in;object-position:30% center" alt=""><div class="cap"><b>Plate I</b>Door to gate, flights tracked in real time.</div></div>
  </div>
  <div class="m" style="top:5.0in;display:grid;grid-template-columns:1fr 1fr;gap:34px .4in">{needs}</div>
  <div class="m" style="top:8.45in"><div class="hair"></div><p class="serif" style="font-size:23px;line-height:1.22;margin-top:20px;max-width:6.2in"><i>“{c['CO_S']} isn't buying transportation. It's buying how its people and its guests feel at the start and end of a trip.”</i></p></div>
  <div class="folio"><span>Prepared for {c['CO']}</span><img src="../../assets/absolute_logo.png" style="height:10px;opacity:.75" alt=""><span>03</span></div>
</section>
<section class="page A">
  <div class="m" style="top:.55in;display:flex;justify-content:space-between"><div class="label">02 — Your Routes</div><div class="label mute">{x['HQ_ADDR']}</div></div>
  <div class="m hair" style="top:.8in"></div>
  <div class="m" style="top:1.15in;display:grid;grid-template-columns:1fr 2.3in;gap:.45in">
    <div><h2 class="serif" style="font-size:46px;line-height:.98">From your front door <i>to the gate.</i></h2>
      <p class="body" style="margin-top:16px;font-size:10.2px;max-width:3.9in">The trips your team is most likely to take, quoted to you directly — tailored to the route, the vehicle and your volume.</p>
      <div style="margin-top:22px;border-top:1px solid #111">{routes}</div></div>
    <div style="border-left:1px solid rgba(17,17,17,.16);padding-left:.3in">
      <img class="ph" src="../assets/occ_greet.jpg" style="height:2.6in" alt=""><div class="cap"><b>Plate II</b>A familiar welcome at arrivals.</div>
      <div class="hair" style="margin:26px 0 16px"></div>
      <div class="label mute" style="font-size:6.5px">Your direct line</div><div class="serif" style="font-size:30px;margin-top:6px">(203) 938-0000</div>
      <p class="body" style="font-size:8.8px;margin-top:8px">Answered by a real person, 24 hours a day, 365 days a year.</p>
      <div class="hair" style="margin:20px 0 14px"></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;row-gap:14px"><div><div class="serif" style="font-size:26px">2007</div><div class="label mute" style="font-size:6.5px">Established</div></div><div><div class="serif" style="font-size:26px">24/7</div><div class="label mute" style="font-size:6.5px">Dispatch</div></div><div><div class="serif" style="font-size:26px">9</div><div class="label mute" style="font-size:6.5px">Airports</div></div><div><div class="serif" style="font-size:26px">14</div><div class="label mute" style="font-size:6.5px">Guests per Sprinter</div></div></div>
    </div>
  </div>
  <div class="folio"><span>Prepared for {c['CO']}</span><img src="../../assets/absolute_logo.png" style="height:10px;opacity:.75" alt=""><span>11</span></div>
</section>'''


def concept_b(c, x):
    cols = [c['COL1'], ('Travel Desk &amp; Executive Assistants', ['One number, one email, written confirmations', 'Flight tracking with automatic adjustments', 'A single, itemized corporate account']), c['COL3'], c['COL4']]
    rows = ''.join(f'''<div style="display:grid;grid-template-columns:.4in 2.2in 1fr;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.18);align-items:baseline"><span class="thin dim" style="font-size:11px">0{i+1}</span><span class="thin" style="font-size:13.5px">{t}</span><span class="body" style="font-size:8.8px;line-height:1.6">{' · '.join(its[:3])}</span></div>''' for i, (t, its) in enumerate(cols))
    routes = ''.join(f'''<div style="display:grid;grid-template-columns:.4in 1fr 1.2in;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.18);align-items:baseline"><span class="thin dim" style="font-size:11px">0{i+1}</span><span class="thin" style="font-size:13px">{f} <span class="dim">→</span> {t}</span><span class="lab dim" style="font-size:6px;text-align:right">{v}</span></div>''' for i, (f, t, v) in enumerate(c['ROUTES']))
    wl = f'<img src="../{c["LOGO_WHITE"]}" alt="{c["CO"]}" style="height:{c["LOGO_H_SM"]}">'
    al = '<img src="../../assets/absolute_logo.png" alt="Absolute Transportation" style="height:22px">'
    return f'''
<section class="page B">
  <img class="bleed" src="../assets/{x['NIGHT']}" style="height:78%;object-position:center 30%" alt="">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,5,5,.78) 0%,rgba(5,5,5,.1) 16%,rgba(5,5,5,0) 40%,rgba(5,5,5,.6) 54%,#050505 66%)"></div>
  <div class="m bar" style="top:.5in;left:.6in;right:.6in"><div style="display:flex;align-items:center;gap:16px">{al}<span style="width:1px;height:24px;background:rgba(255,255,255,.4)"></span>{wl}</div><span class="lab dim">Corporate Programme · 2027</span></div>
  <div class="m" style="left:.6in;right:.6in;bottom:1.55in"><div class="lab dim">Prepared exclusively for {c['CO']}</div><h1 class="big" style="font-size:84px;margin-top:18px">{x['CITY_UP']}<br>to anywhere.</h1></div>
  <div class="m" style="left:.6in;right:.6in;bottom:.5in"><div class="hair"></div><div style="display:grid;grid-template-columns:1.25fr 1.25fr 1fr .8fr;margin-top:14px">
    <div><div class="lab dim" style="font-size:6px">Your headquarters</div><div class="thin" style="font-size:12.5px;margin-top:6px">{x['HQ_ADDR']}</div></div>
    <div><div class="lab dim" style="font-size:6px">Nearest airport</div><div class="thin" style="font-size:12.5px;margin-top:6px">{x['NEAREST']}</div></div>
    <div><div class="lab dim" style="font-size:6px">Our base</div><div class="thin" style="font-size:12.5px;margin-top:6px">North Haven, CT</div></div>
    <div style="text-align:right"><div class="lab dim" style="font-size:6px">Dispatch</div><div class="thin" style="font-size:12.5px;margin-top:6px">24 / 7 / 365</div></div></div></div>
</section>
<section class="page B">
  <img src="../assets/occ_city.jpg" style="position:absolute;left:0;top:0;width:100%;height:5.3in;object-fit:cover;object-position:center 55%" alt="">
  <div style="position:absolute;left:0;right:0;top:0;height:5.3in;background:linear-gradient(180deg,rgba(5,5,5,.7) 0%,rgba(5,5,5,0) 26%,rgba(5,5,5,0) 66%,#050505 100%)"></div>
  <div class="m bar" style="left:.6in;right:.6in;top:.5in"><span class="lab">01 / Your needs</span>{wl}</div>
  <div class="m" style="left:.6in;right:.6in;top:5.0in"><h2 class="big" style="font-size:54px">Built around<br>{c['CO_S']}.</h2><p class="body" style="max-width:5in;margin-top:16px">{c['NEEDS_LEAD']}</p></div>
  <div class="m" style="left:.6in;right:.6in;top:7.75in"><div style="display:grid;grid-template-columns:.4in 2.2in 1fr;padding-bottom:8px" class="lab dim"><span>№</span><span>For</span><span>What we handle</span></div><div class="hair"></div>{rows}</div>
  <div class="m bar" style="left:.6in;right:.6in;bottom:.45in"><span class="lab dim">Prepared for {c['CO']}</span><span class="lab dim">03</span></div>
</section>
<section class="page B">
  <img src="../assets/lineup.jpg" style="position:absolute;left:0;top:0;width:100%;height:4.6in;object-fit:cover;object-position:center 62%" alt="">
  <div style="position:absolute;left:0;right:0;top:0;height:4.6in;background:linear-gradient(180deg,rgba(5,5,5,.6) 0%,rgba(5,5,5,0) 30%,rgba(5,5,5,.1) 60%,#050505 100%)"></div>
  <div class="m bar" style="left:.6in;right:.6in;top:.5in"><span class="lab">02 / Your routes</span><span class="lab dim">{x['AIR4']}</span></div>
  <div class="m" style="left:.6in;right:.6in;top:4.2in"><h2 class="big" style="font-size:54px">Every airport.<br>One number.</h2></div>
  <div class="m" style="left:.6in;right:.6in;top:5.95in"><div class="hair"></div>{routes}</div>
  <div class="m" style="left:.6in;right:.6in;bottom:1.0in;display:flex;justify-content:space-between;align-items:flex-end"><div><div class="lab dim" style="font-size:6px">Corporate partner reservations · answered by a real person</div><div class="big" style="font-size:58px;margin-top:10px;letter-spacing:-.01em">(203) 938-0000</div></div><div class="thin dim" style="font-size:11px;text-align:right;line-height:1.7">Corporate rates quoted directly<br>info@absolute-transportation.com</div></div>
  <div class="m bar" style="left:.6in;right:.6in;bottom:.45in"><span class="lab dim">Prepared for {c['CO']}</span><span class="lab dim">11</span></div>
</section>'''


def concept_c(c, x):
    cols = [c['COL1'], ('Corporate Travel &amp; Executive Assistants', ['One number and one email for every booking', 'Flight tracking with automatic adjustments', 'Written confirmation of every trip', 'A single, itemized corporate account']), c['COL3'], c['COL4']]
    cards = ''.join(f'''<div style="border-top:2px solid var(--ac);padding-top:14px"><div style="display:flex;gap:14px;align-items:baseline"><span class="num">0{i+1}</span><h2 style="font-size:15px">{t}</h2></div>{li(its, "font-size:9.2px;line-height:1.5;font-weight:300;color:#3a3936;margin-top:7px;padding-left:14px;border-left:1px solid rgba(12,12,13,.14)")}</div>''' for i, (t, its) in enumerate(cols))
    routes = ''.join(f'''<div style="display:grid;grid-template-columns:1fr 1.1in 1.5in;padding:10px 0;border-bottom:1px solid rgba(12,12,13,.14);font-size:10.5px;align-items:baseline"><span><b style="font-weight:500">{f}</b> <span style="color:var(--ac)">→</span> <span style="color:#55534e;font-weight:300">{t}</span></span><span style="font-size:8.5px;color:#77746e">{v}</span><span style="text-align:right;font-family:'Playfair';font-style:italic;font-size:10.5px">Corporate Rates Available</span></div>''' for f, t, v in c['ROUTES'])
    steps = [('One call', 'We set up your corporate account and learn how your team travels.'), ('One contact', 'Your travel desk and assistants get one number and one email for every booking.'), ('First trips', 'Every reservation confirmed in writing, every flight tracked in real time.'), ('One statement', 'A single itemized monthly statement, built for easy reconciliation.')]
    st = ''.join(f'''<div><div class="num" style="font-size:28px">0{i+1}</div><h2 style="font-size:13px;margin-top:8px">{t}</h2><p class="body" style="font-size:9px;line-height:1.6;margin-top:6px">{d}</p></div>''' for i, (t, d) in enumerate(steps))
    return f'''
<section class="page C" style="--ac:{x['ACCENT']}">
  <div style="position:absolute;left:0;top:0;bottom:0;width:3.3in;overflow:hidden;background:#0C0C0D"><img src="../assets/{x['DETAIL']}" style="width:100%;height:100%;object-fit:cover" alt=""></div>
  <div style="position:absolute;left:3.3in;top:0;bottom:0;width:4px;background:var(--ac)"></div>
  <div style="position:absolute;left:3.85in;right:.7in;top:.7in;bottom:.6in;display:flex;flex-direction:column">
    <img src="../../assets/absolute_logo.png" alt="Absolute Transportation" style="height:22px;align-self:flex-start">
    <div style="margin-top:auto">
      <div class="k">A Partnership Proposal For</div>
      <img src="../{c['LOGO_COLOR']}" alt="{c['CO']}" style="height:52px;max-width:100%;margin-top:20px;display:block">
      <div style="width:56px;height:2px;background:var(--ac);margin:30px 0 26px"></div>
      <h1 style="font-size:35px;line-height:1.08">Executive ground transportation, built around the way {c['CO_S']} moves.</h1>
      <p class="body" style="font-size:11px;margin-top:18px">For your {c['HQ_CITY']} headquarters: one accountable, family-owned partner for airport transfers, visiting guests, and the travel days that matter most.</p>
    </div>
    <div style="margin-top:auto"><div class="line"></div><div style="display:flex;justify-content:space-between;margin-top:12px;font-size:7px;letter-spacing:.28em;text-transform:uppercase;color:#77746e"><span>Family-owned · Est. 2007</span><span>Vol. 01 · 2027</span></div></div>
  </div>
</section>
<section class="page C" style="--ac:{x['ACCENT']}">
  <div class="m" style="top:.7in;display:flex;justify-content:space-between;align-items:center"><div class="k">01 &nbsp;·&nbsp; Built Around {c['CO']}</div><img src="../{c['LOGO_COLOR']}" alt="{c['CO']}" style="height:20px"></div>
  <div class="m" style="top:1.15in"><h1 style="font-size:36px;line-height:1.05">Whatever {c['CO_S']} plans,<br>we're the ground under it.</h1><p class="body" style="font-size:10.6px;max-width:5.7in;margin-top:14px">{c['NEEDS_LEAD']}</p></div>
  <div class="m" style="top:3.35in;display:grid;grid-template-columns:1fr 1fr;gap:52px .45in">{cards}</div>
  <div class="m" style="bottom:.95in;background:#0C0C0D;color:#F6F3EC;display:grid;grid-template-columns:repeat(4,1fr);padding:20px 8px;text-align:center">
    <div><div style="font-family:'Playfair';font-weight:700;font-size:24px">2007</div><div style="font-size:6.5px;letter-spacing:.26em;text-transform:uppercase;margin-top:6px;opacity:.75">Family owned since</div></div>
    <div style="border-left:1px solid rgba(255,255,255,.2)"><div style="font-family:'Playfair';font-weight:700;font-size:24px">24/7</div><div style="font-size:6.5px;letter-spacing:.26em;text-transform:uppercase;margin-top:6px;opacity:.75">A real person answers</div></div>
    <div style="border-left:1px solid rgba(255,255,255,.2)"><div style="font-family:'Playfair';font-weight:700;font-size:24px">9</div><div style="font-size:6.5px;letter-spacing:.26em;text-transform:uppercase;margin-top:6px;opacity:.75">Regional airports</div></div>
    <div style="border-left:1px solid rgba(255,255,255,.2)"><div style="font-family:'Playfair';font-weight:700;font-size:24px">14</div><div style="font-size:6.5px;letter-spacing:.26em;text-transform:uppercase;margin-top:6px;opacity:.75">Guests per Sprinter</div></div>
  </div>
  <div class="m" style="bottom:.45in;display:flex;justify-content:space-between;align-items:center;font-size:7px;letter-spacing:.28em;text-transform:uppercase;color:#77746e"><span>Prepared for {c['CO']}</span><img src="../../assets/absolute_logo.png" style="height:10px;opacity:.75" alt=""><span>03</span></div>
</section>
<section class="page C" style="--ac:{x['ACCENT']}">
  <div class="m" style="top:.7in;display:flex;justify-content:space-between;align-items:center"><div class="k">02 &nbsp;·&nbsp; How We'd Begin</div><img src="../{c['LOGO_COLOR']}" alt="{c['CO']}" style="height:20px"></div>
  <div class="m" style="top:1.15in"><h1 style="font-size:36px;line-height:1.05">Simple to start.<br>Simple to keep.</h1></div>
  <div class="m" style="top:2.6in;display:grid;grid-template-columns:repeat(4,1fr);gap:.3in;border-top:2px solid var(--ac);padding-top:18px">{st}</div>
  <div class="m" style="top:5.0in"><div class="k" style="color:#0C0C0D">Your most likely routes</div><div style="margin-top:12px;border-top:1px solid #0C0C0D">{routes}</div></div>
  <div class="m" style="bottom:.95in;height:1.75in;overflow:hidden"><img src="../assets/occ_group.jpg" style="width:100%;height:100%;object-fit:cover;object-position:center 60%" alt=""><div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(12,12,13,.86) 0%,rgba(12,12,13,.55) 45%,rgba(12,12,13,0) 75%)"></div>
    <div style="position:absolute;left:.35in;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;color:#fff"><div style="font-size:7px;letter-spacing:.3em;text-transform:uppercase;opacity:.8">Corporate partner reservations</div><div style="font-family:'Playfair';font-weight:700;font-size:30px;margin-top:8px">(203) 938-0000</div><div style="font-size:9px;font-weight:300;margin-top:6px;opacity:.85">Answered by a real person, day or night.</div></div></div>
  <div class="m" style="bottom:.45in;display:flex;justify-content:space-between;align-items:center;font-size:7px;letter-spacing:.28em;text-transform:uppercase;color:#77746e"><span>Prepared for {c['CO']}</span><img src="../../assets/absolute_logo.png" style="height:10px;opacity:.75" alt=""><span>11</span></div>
</section>'''


if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'concepts'), exist_ok=True)
    for key in (sys.argv[1:] or COMPANIES):
        c, x = COMPANIES[key], EXTRA[key]
        html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{c["CO"]} — design directions</title><style>{CSS}</style></head><body>' + concept_a(c, x) + concept_b(c, x) + concept_c(c, x) + '</body></html>'
        open(os.path.join(HERE, 'concepts', f'{key}-concepts.html'), 'w', encoding='utf-8').write(html)
        print('wrote', key)

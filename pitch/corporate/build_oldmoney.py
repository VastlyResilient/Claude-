#!/usr/bin/env python3
"""'Quiet' edition: a restrained, classic, old-money treatment of the corporate deck.

Six sample pages per company: cover, contents, letter, plate, needs + routes table,
assurances + how to begin + colophon. Writes concepts/<key>-quiet.html.
"""
import os, sys
from build_corporate import COMPANIES

HERE = os.path.dirname(os.path.abspath(__file__))
ACC = {'charter': '#1B2A3F', 'subway': '#1F3A2B'}
PLACE = {'charter': ('om_charter.jpg', 'The harbour at Stamford, a little after seven.'), 'subway': ('om_subway.jpg', 'Shelton, in the last week of October.')}
ROM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
ABS = '../../assets/absolute_logo.png'


def ff(fam, path, w, st='normal'):
    return f"@font-face{{font-family:'{fam}';src:url('{path}.woff2') format('woff2');font-weight:{w};font-style:{st};font-display:block}}"


def css(ac):
    C, K, A = '../../concepts/fonts/cormorant-garamond-latin-', 'fonts/libre-caslon-text-latin-', '../../assets/jost-'
    return '\n'.join([ff('Cor', C + '300-normal', 300), ff('Cor', C + '500-normal', 500), ff('Cor', C + '400-italic', 400, 'italic'),
                      ff('Cas', K + '400-normal', 400), ff('Cas', K + '400-italic', 400, 'italic'), ff('Cas', K + '700-normal', 700),
                      ff('Jost', A + '400', 400), ff('Jost', A + '500', 500)]) + f'''
:root{{--paper:#F4F0E7;--ink:#1C1A17;--mut:#756F64;--line:rgba(28,26,23,.22);--ac:{ac}}}
@page{{size:8.5in 11in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#888;-webkit-font-smoothing:antialiased}}
.page{{position:relative;width:8.5in;height:11in;overflow:hidden;break-after:page;background:var(--paper);color:var(--ink);font-family:'Cas',serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page:last-child{{break-after:auto}}
@media screen{{.page{{margin:20px auto}}}}
.a{{position:absolute}} .m{{position:absolute;left:1.1in;right:1.1in}}
.dis{{font-family:'Cor',serif;font-weight:300;letter-spacing:-.005em;line-height:1.08}} .dis i{{font-style:italic;font-weight:400}}
.sc{{font-family:'Jost';font-weight:500;font-size:6.8px;letter-spacing:.34em;text-transform:uppercase}}
.mu{{color:var(--mut)}}
.tx{{font-size:10.4px;line-height:1.78;hyphens:auto;text-align:left}}
.tx + .tx{{text-indent:1.4em}}
.cap{{font-family:'Cas';font-style:italic;font-size:8.4px;color:var(--mut);line-height:1.5}}
.ln{{height:1px;background:var(--line)}}
.plate{{filter:saturate(.82) contrast(.97) brightness(.99);width:100%;height:100%;object-fit:cover;display:block}}
.folio{{position:absolute;left:0;right:0;bottom:.6in;text-align:center;font-family:'Cas';font-size:8.5px;color:var(--mut);font-variant-numeric:oldstyle-nums}}
.run{{position:absolute;left:1.1in;right:1.1in;top:.62in;display:flex;justify-content:space-between}}
table{{width:100%;border-collapse:collapse;font-variant-numeric:lining-nums tabular-nums}}
th{{font-family:'Jost';font-weight:500;font-size:6.4px;letter-spacing:.3em;text-transform:uppercase;color:var(--mut);text-align:left;padding:0 0 7px;border-bottom:1px solid var(--ink)}}
td{{font-size:10px;padding:7.5px 0;border-bottom:1px solid var(--line);vertical-align:baseline}}
td.r,th.r{{text-align:right}} td i{{color:var(--mut)}}
'''


def build(key):
    c = COMPANIES[key]; co, cs = c['CO'], c['CO_S']; logo = '../' + c['LOGO_COLOR']; place, place_cap = PLACE[key]
    lh = '26px' if key == 'charter' else '17px'
    run = lambda l: f'<div class="run sc mu"><span>Absolute Transportation</span><span>{l}</span></div>'
    cols = [c['COL1'], ('Corporate Travel &amp; Executive Assistants', ['One number and one email for every booking', 'Flight tracking with automatic adjustments', 'Written confirmation of every trip', 'A single, itemized corporate account']), c['COL3'], c['COL4']]
    contents = [('A Letter', 'iii'), (f'In the Service of {cs}', 'v'), ('The Fleet', 'vii'), ('The Chauffeurs', 'ix'), ('Coverage &amp; Routes', 'xi'), ('Six Assurances', 'xiii'), ('How We Would Begin', 'xiv')]
    toc = ''.join(f'<div style="display:flex;align-items:baseline;gap:10px;padding:9px 0;border-bottom:1px solid var(--line)"><span class="dis" style="font-size:13px;width:.4in"><i>{ROM[i]}</i></span><span class="dis" style="font-size:17px">{t}</span><span style="flex:1"></span><span class="cap" style="font-style:normal">{p}</span></div>' for i, (t, p) in enumerate(contents))
    needs = ''.join(f'<div style="display:grid;grid-template-columns:.42in 1fr;padding:11px 0;border-bottom:1px solid var(--line)"><span class="dis" style="font-size:15px"><i>{ROM[i]}</i></span><div><div class="dis" style="font-size:17px;font-weight:500">{t}</div><div class="tx" style="font-size:9.4px;line-height:1.65;color:#3b3832;margin-top:3px">{"; ".join(x[0].lower() + x[1:] if not x[:3].isupper() else x for x in its)}.</div></div></div>' for i, (t, its) in enumerate(cols))
    routes = ''.join(f'<tr><td>{f.replace(" HQ", "")}</td><td><i>to</i>&ensp;{t}</td><td class="r">{v}</td></tr>' for f, t, v in c['ROUTES'])
    why = [('A person answers', 'One number, day and night, every day of the year.'), ('The owners are accountable', 'Family-owned since 2007; the people who own the company dispatch the cars.'),
           ('Flights are followed', 'Arrivals are tracked in real time and the chauffeur adjusts with them.'), ('Chauffeurs are made, not found', 'Background-checked, commercially licensed, trained in hospitality, discreet.'),
           ('Licensed and insured', f'U.S. DOT 1567094 · MC-580841 · Connecticut Livery Permit 3117. A certificate naming {co} on request.'), ('One clean account', 'Every trip confirmed in writing; one itemized statement each month.')]
    wl = ''.join(f'<div style="display:grid;grid-template-columns:.42in 1.9in 1fr;padding:9px 0;border-bottom:1px solid var(--line);align-items:baseline"><span class="dis" style="font-size:15px"><i>{ROM[i]}</i></span><span class="dis" style="font-size:16.5px;font-weight:500">{a}</span><span class="tx" style="font-size:9.4px;line-height:1.6;color:#3b3832">{b}</span></div>' for i, (a, b) in enumerate(why))
    steps = [('One call', 'to open your account and learn how your people travel.'), ('One contact', 'a single number and address for every booking.'), ('First journeys', 'each confirmed in writing, each flight followed.'), ('One statement', 'itemized, monthly, simple to reconcile.')]
    sl = ''.join(f'<div><div class="dis" style="font-size:22px"><i>{ROM[i]}</i></div><div class="dis" style="font-size:16px;font-weight:500;margin-top:6px">{a}</div><div class="tx" style="font-size:9.2px;line-height:1.6;color:#3b3832;margin-top:3px">{b}</div></div>' for i, (a, b) in enumerate(steps))
    P = f'''
<section class="page">
  <div class="a" style="left:0;right:0;top:.9in;text-align:center"><img src="{ABS}" style="height:17px" alt="Absolute Transportation"></div>
  <div class="a" style="left:1.75in;right:1.75in;top:1.75in;height:5.35in"><img class="plate" src="../assets/om_cover.jpg" style="object-position:center 70%" alt=""></div>
  <div class="a" style="left:1in;right:1in;top:7.55in;text-align:center">
    <div class="sc mu">A Private Proposal &nbsp;·&nbsp; Prepared for</div><img src="{logo}" alt="{co}" style="height:{lh};margin-top:14px">
    <h1 class="dis" style="font-size:40px;margin-top:22px">On arriving <i>well</i></h1>
    <div style="width:1px;height:26px;background:var(--ink);margin:16px auto 0"></div></div>
  <div class="a sc mu" style="left:1.1in;right:1.1in;bottom:.62in;display:flex;justify-content:space-between"><span>Family-owned since 2007</span><span>North Haven, Connecticut</span><span>Volume I · MMXXVII</span></div>
</section>
<section class="page">{run('Contents')}
  <div class="m" style="top:1.7in;display:grid;grid-template-columns:2.35in 1fr;gap:.55in">
    <div><div style="height:2.95in"><img class="plate" src="../assets/om_still.jpg" alt=""></div><p class="cap" style="margin-top:8px">The day's itinerary, set out the evening before.</p></div>
    <div><div class="sc mu">In this volume</div><h2 class="dis" style="font-size:34px;margin-top:10px">Contents</h2><div style="margin-top:20px;border-top:1px solid var(--ink)">{toc}</div></div>
  </div>
  <div class="m" style="top:7.35in;text-align:center"><div class="ln"></div><p class="dis" style="font-size:22px;line-height:1.35;margin-top:34px;padding:0 .5in"><i>“People don't remember what you sold them. They remember how well you served them.”</i></p><div class="sc mu" style="margin-top:14px">Manmohan Komal</div></div>
  <div class="folio">ii</div>
</section>
<section class="page">{run('I · A Letter')}
  <div class="m" style="top:1.7in"><div class="sc mu">Chapter I</div><h2 class="dis" style="font-size:38px;margin-top:10px">A letter to {cs}</h2></div>
  <div class="m" style="top:3.1in;display:grid;grid-template-columns:1fr 2.1in;gap:.6in">
    <div><p class="tx"><span class="dis" style="float:left;font-size:60px;line-height:.78;padding:5px 9px 0 0">Y</span>our people are asked to be in a great many places, and to arrive in each of them ready. Our family has spent the better part of two decades seeing that travel days of that kind begin and end calmly.</p>
      <p class="tx">We keep one fleet, always in black and always immaculate. We answer the telephone ourselves, at any hour. We follow each flight, so that a chauffeur is waiting when the aircraft actually lands. And we treat every traveler you send us as though your own name were in the back seat, because in every way that matters it is.</p>
      <p class="tx">We would be honoured to serve {co}, and to begin, if you will allow it, with a single journey.</p>
      <p class="dis" style="font-size:19px;margin-top:22px"><i>Manmohan Komal</i></p><div class="sc mu" style="margin-top:5px">Chief Executive Officer</div></div>
    <div><div style="height:2.65in"><img class="plate" src="../assets/om_hand.jpg" alt=""></div><p class="cap" style="margin-top:8px">The door is opened; nothing more need be said.</p></div>
  </div>
  <div class="folio">iii</div>
</section>
<section class="page">
  <div class="a" style="left:1.5in;right:1.5in;top:1.15in;height:7.55in"><img class="plate" src="../assets/om_bw.jpg" style="filter:contrast(.97)" alt=""></div>
  <div class="a" style="left:1.5in;right:1.5in;top:8.85in;display:flex;justify-content:space-between"><span class="cap">Plate I. An arrival.</span><span class="cap">The standard has not changed since 2007.</span></div>
  <div class="folio">iv</div>
</section>
<section class="page">{run(f'II · In the Service of {cs}')}
  <div class="m" style="top:1.5in;display:flex;justify-content:space-between;align-items:flex-end"><div><div class="sc mu">Chapter II</div><h2 class="dis" style="font-size:36px;margin-top:10px">In the service of <i>{cs}</i></h2></div><img src="{logo}" alt="{co}" style="height:{lh}"></div>
  <div class="m" style="top:2.75in;display:grid;grid-template-columns:1fr 2.6in;gap:.5in">
    <div style="border-top:1px solid var(--ink)">{needs}</div>
    <div><div style="height:1.85in"><img class="plate" src="../assets/{place}" alt=""></div><p class="cap" style="margin-top:8px">{place_cap}</p>
      <p class="tx" style="font-size:9.6px;margin-top:16px;color:#3b3832">{c['NEEDS_LEAD'].split(' Here is')[0]}</p></div>
  </div>
  <div class="m" style="top:7.3in"><div class="sc mu">Table I &nbsp;·&nbsp; Your most likely journeys</div>
    <table style="margin-top:10px"><thead><tr><th>From</th><th>To</th><th class="r">Vehicle</th></tr></thead><tbody>{routes}</tbody></table>
    <p class="cap" style="margin-top:8px">Rates are quoted to you directly, according to the route, the vehicle and your volume.</p></div>
  <div class="folio">v</div>
</section>
<section class="page">{run('VI · Six Assurances')}
  <div class="m" style="top:1.5in"><div class="sc mu">Chapter VI</div><h2 class="dis" style="font-size:36px;margin-top:10px">Six assurances, <i>in writing</i></h2></div>
  <div class="m" style="top:2.7in;border-top:1px solid var(--ink)">{wl}</div>
  <div class="m" style="top:6.05in"><div class="sc mu">Chapter VII &nbsp;·&nbsp; How we would begin</div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.3in;margin-top:14px;border-top:1px solid var(--ink);padding-top:14px">{sl}</div></div>
  <div class="m" style="top:8.0in;text-align:center"><div class="ln"></div><div class="sc mu" style="margin-top:22px">Reservations, at any hour</div><div class="dis" style="font-size:34px;margin-top:8px;font-variant-numeric:lining-nums">(203) 938-0000</div><div class="cap" style="margin-top:4px">info@absolute-transportation.com</div></div>
  <div class="a cap" style="left:1.1in;right:1.1in;bottom:.95in;text-align:center;font-size:7.6px">Colophon. Set in Cormorant Garamond and Libre Caslon, with captions in Jost. Prepared in North Haven, Connecticut, for {co}. Volume I, MMXXVII.</div>
  <div class="folio">xiii</div>
</section>'''
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{co} — Quiet edition</title><style>{css(ACC[key])}</style></head><body>{P}</body></html>'
    open(os.path.join(HERE, 'concepts', f'{key}-quiet.html'), 'w', encoding='utf-8').write(html)
    print('wrote', key)


if __name__ == '__main__':
    for k in (sys.argv[1:] or COMPANIES):
        build(k)

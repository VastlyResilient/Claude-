#!/usr/bin/env python3
"""'Quiet' edition: a restrained, classic, old-money treatment of the corporate deck,
built to research/art-direction-brief.md (drawn from research/magazines-100.md).

Nine sample pages per company: cover, contents, letter, plate, needs, routes table,
breather plate, six assurances, how we would begin. Writes concepts/<key>-quiet.html.
Folios follow the planned 16-page order, so the contents page is accurate.
"""
import os, sys
from build_corporate import COMPANIES

HERE = os.path.dirname(os.path.abspath(__file__))
ACC = {'charter': '#1B2A3F', 'subway': '#1F3A2B'}
PLACE = {'charter': ('om_charter.jpg', 'Stamford harbour, a little after seven in the morning.'), 'subway': ('om_subway.jpg', 'Shelton, in the last week of October.')}
CODES = {'Tweed New Haven': 'HVN', 'Bradley International': 'BDL', 'Westchester County': 'HPN', 'LaGuardia': 'LGA', 'JFK International': 'JFK', 'Newark Liberty': 'EWR', 'Midtown Manhattan': 'NYC'}
ROM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
ABS = '../../assets/absolute_logo.png'


def ff(fam, path, w, st='normal'):
    return f"@font-face{{font-family:'{fam}';src:url('{path}.woff2') format('woff2');font-weight:{w};font-style:{st};font-display:block}}"


def css(ac):
    C, K, A = '../../concepts/fonts/cormorant-garamond-latin-', 'fonts/libre-caslon-text-latin-', '../../assets/jost-'
    return '\n'.join([ff('Cor', C + '300-normal', 300), ff('Cor', C + '500-normal', 500), ff('Cor', C + '400-italic', 400, 'italic'),
                      ff('Cas', K + '400-normal', 400), ff('Cas', K + '400-italic', 400, 'italic'), ff('Jost', A + '500', 500)]) + f'''
:root{{--paper:#F4F0E7;--ink:#1C1A17;--mut:#5E584E;--hair:rgba(28,26,23,.35);--ac:{ac}}}
@page{{size:8.5in 11in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#888;-webkit-font-smoothing:antialiased}}
.page{{position:relative;width:8.5in;height:11in;overflow:hidden;break-after:page;background:var(--paper);color:var(--ink);font-family:'Cas',serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page:last-child{{break-after:auto}}
@media screen{{.page{{margin:20px auto}}}}
.a{{position:absolute}} .m{{position:absolute;left:1in;right:1in}}
.dis{{font-family:'Cor',serif;font-weight:300;letter-spacing:-.005em}} .dis i,.it{{font-family:'Cor';font-style:italic;font-weight:400}}
.h1{{font-family:'Cor';font-weight:300;font-size:44px;line-height:48px;letter-spacing:-.005em;text-wrap:balance}} .h1 i{{font-style:italic;font-weight:400}}
.stand{{font-family:'Cor';font-style:italic;font-weight:400;font-size:19px;line-height:27px;max-width:4.6in;margin-top:14px;text-wrap:balance}}
.lb{{font-family:'Jost';font-weight:500;font-size:8.5px;letter-spacing:.18em;text-transform:uppercase}}
.mu{{color:var(--mut)}} .ac{{color:var(--ac)}}
.tx{{font-size:13px;line-height:20px;hyphens:manual;text-align:left;text-wrap:pretty}}
.tx + .tx{{text-indent:1.4em}}
.li{{font-family:'Cor';font-weight:500;font-size:20px;line-height:24px}}
.rn{{font-family:'Cor';font-style:italic;font-weight:400;font-size:20px;line-height:24px;color:var(--ac)}}
.cap{{font-family:'Cas';font-style:italic;font-size:10.5px;line-height:15px;color:var(--mut);margin-top:9px}}
.cap b{{font-family:'Jost';font-style:normal;font-weight:500;font-size:8px;letter-spacing:.18em;text-transform:uppercase;margin-right:8px}}
.hr{{height:1px;background:var(--ink)}} .hl{{height:.67px;background:var(--hair)}}
.plate{{filter:saturate(.82) contrast(.97);width:100%;height:100%;object-fit:cover;display:block}}
.run{{position:absolute;left:1in;right:1in;top:.6in;display:flex;justify-content:space-between;font-family:'Jost';font-weight:500;font-size:8px;letter-spacing:.2em;text-transform:uppercase;color:var(--mut);padding-bottom:6px;border-bottom:.67px solid var(--hair)}}
.folio{{position:absolute;left:0;right:0;top:10.4in;text-align:center;font-size:10.5px;font-variant-numeric:oldstyle-nums}}
.row{{display:grid;grid-template-columns:.45in 2.1in 1fr;padding:12px 0;border-bottom:.67px solid var(--hair);align-items:baseline;break-inside:avoid}}
.row .d{{font-size:12px;line-height:18px}}
table{{width:100%;border-collapse:collapse;font-variant-numeric:lining-nums tabular-nums;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}}
th{{font-family:'Jost';font-weight:500;font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--mut);text-align:left;vertical-align:bottom;padding:10px 0 8px;border-bottom:.67px solid var(--hair)}}
td{{font-size:12.5px;line-height:18px;padding:9px 0;border-bottom:.67px solid var(--hair);vertical-align:baseline}}
tr:last-child td{{border-bottom:0}} td.q{{font-style:italic;color:var(--mut)}} .r{{text-align:right}}
'''


def build(key):
    c = COMPANIES[key]; co, cs, city = c['CO'], c['CO_S'], c['HQ_CITY']; logo = '../' + c['LOGO_COLOR']; place, place_cap = PLACE[key]
    lh = '26px' if key == 'charter' else '17px'
    run = lambda l: f'<div class="run"><span>Absolute Transportation</span><span>{l}</span></div>'
    head = lambda n, t, s='': f'<div class="m" style="top:1.42in"><div class="lb"><span class="ac">Chapter {n}</span></div><h2 class="h1" style="margin-top:12px">{t}</h2>' + (f'<p class="stand">{s}</p>' if s else '') + '</div>'
    fo = lambda n: f'<div class="folio">{n}</div>'
    cols = [c['COL1'], ('Corporate Travel &amp; Executive Assistants', ['One number and one email for every booking', 'Flight tracking with automatic adjustments', 'Written confirmation of every trip', 'A single, itemized corporate account']), c['COL3'], c['COL4']]
    contents = [('A Letter', 5), (f'In the Service of {cs}', 6), (f'From Your {city} Campus', 7), ('The Fleet', 9), ('The Chauffeurs', 11), ('Six Assurances', 12), ('How We Would Begin', 13)]
    toc = ''.join(f'<div style="display:flex;align-items:baseline;gap:12px;padding:15px 0;border-bottom:.67px solid var(--hair)"><span class="rn" style="width:.42in">{ROM[i]}</span><span class="dis" style="font-size:22px;line-height:26px;font-weight:500">{t}</span><span style="flex:1"></span><span style="font-size:12px;font-variant-numeric:oldstyle-nums">{p}</span></div>' for i, (t, p) in enumerate(contents))
    needs = ''.join(f'<div class="row"><span class="rn">{ROM[i]}</span><span class="li" style="padding-right:.2in">{t}</span><div class="d">{"".join(f"<div>{x}</div>" for x in its)}</div></div>' for i, (t, its) in enumerate(cols))
    rrows = ''
    for _, t, v in c['ROUTES']:
        name = t.split(' (')[0]; rrows += f'<tr><td>{name}</td><td class="q">{CODES.get(name, "")}</td><td class="q r">{v}</td></tr>'
    why = [('A person answers', 'One number, answered day and night, every day of the year.'), ('The owners are accountable', 'Family-owned since 2007. The people who own the company dispatch the cars and follow up after the ride.'),
           ('Flights are followed', 'Every arrival is tracked in real time, so the chauffeur is waiting when the aircraft actually lands.'), ('Chauffeurs are made, not found', 'Background-checked, commercially licensed, trained in hospitality, and discreet.'),
           ('Licensed and insured', f'U.S. DOT 1567094. MC-580841. Connecticut Livery Permit 3117. A certificate naming {co} on request.'), ('One clean account', 'Every trip confirmed in writing, and one itemized statement each month.')]
    wl = ''.join(f'<div class="row"><span class="rn">{ROM[i]}</span><span class="li" style="padding-right:.2in">{a}</span><div class="d">{b}</div></div>' for i, (a, b) in enumerate(why))
    steps = [('One call', 'We open your account and learn how your people travel.'), ('One contact', 'A single number and address for every booking.'), ('First journeys', 'Each confirmed in writing, each flight followed.'), ('One statement', 'Itemized, monthly, simple to reconcile.')]
    sl = ''.join(f'<div><div class="rn" style="font-size:26px;line-height:28px">{ROM[i]}</div><div class="li" style="margin-top:8px">{a}</div><div style="font-size:12px;line-height:18px;margin-top:5px">{b}</div></div>' for i, (a, b) in enumerate(steps))
    bill = [('Per trip or on account', 'Bill each reservation on its own, or keep a monthly corporate account.'), ('The quote is the number', 'Chauffeur, tolls, greeting and flight tracking are included. Gratuity and parking are the only extras.'), ('Volume in your favour', 'The more you send our way, the sharper the corporate rate.')]
    bl = ''.join(f'<div><div class="li" style="font-size:18px">{a}</div><div style="font-size:12px;line-height:18px;margin-top:5px">{b}</div></div>' for a, b in bill)
    P = f'''
<section class="page">
  <div class="a" style="left:0;right:0;top:.72in;text-align:center"><img src="{ABS}" style="height:20px" alt="Absolute Transportation"></div>
  <div class="a" style="left:1.5in;right:1.5in;top:1.35in;height:6.2in"><img class="plate" src="../assets/om_cover.jpg" style="object-position:center 72%" alt=""></div>
  <div class="a" style="left:1in;right:1in;top:7.9in;text-align:center">
    <div class="lb mu">A private proposal &nbsp;·&nbsp; Prepared for</div><img src="{logo}" alt="{co}" style="height:{lh};margin-top:14px">
    <h1 class="dis" style="font-size:54px;line-height:58px;letter-spacing:-.01em;margin-top:16px">On arriving <i>well</i></h1></div>
  <div class="a lb mu" style="left:1in;right:1in;top:10.25in;display:flex;justify-content:space-between"><span>Family-owned since 2007</span><span>North Haven, Connecticut</span><span>Volume I · MMXXVII</span></div>
</section>
<section class="page">{run('Contents')}
  <div class="m" style="top:1.42in"><div class="lb mu">In this volume</div><h2 class="h1" style="margin-top:12px">Contents</h2></div>
  <div class="m" style="top:2.9in;display:grid;grid-template-columns:2.6in 1fr;gap:.5in">
    <div><div style="height:5.2in"><img class="plate" src="../assets/om_still.jpg" alt=""></div><p class="cap"><b>Plate I</b>The day's itinerary, set out the evening before.</p></div>
    <div style="border-top:1px solid var(--ink)">{toc}</div>
  </div>
  <div class="m lb mu" style="top:9.5in;text-align:right">Prepared for {co} &nbsp;·&nbsp; Volume I &nbsp;·&nbsp; MMXXVII</div>
  {fo(3)}
</section>
<section class="page">{run('I · A Letter')}{head('I', f'A letter to {cs}')}
  <div class="m" style="top:3.3in;display:grid;grid-template-columns:4.2in 1.8in;gap:.5in">
    <div><p class="tx" style="font-size:14px;line-height:22px"><span class="dis ac" style="float:left;font-size:68px;line-height:54px;padding:6px 9px 0 0">Y</span>our people are asked to be in a great many places, and to arrive in each of them ready. Our family has spent the better part of two decades seeing that travel days of that kind begin and end calmly.</p>
      <p class="tx" style="font-size:14px;line-height:22px">We keep one fleet, always in black and always immaculate. We answer the telephone ourselves, at any hour. We follow each flight, so that a chauffeur is waiting when the aircraft actually lands, and not when it was scheduled to.</p>
      <p class="tx" style="font-size:14px;line-height:22px">None of this is remarkable on its own. What we hope you will notice is that it happens every time: the early arrival, the door held open, the quiet drive, the call returned at once. We treat every traveler you send us as though your own name were in the back seat, because in every way that matters it is.</p>
      <p class="tx" style="font-size:14px;line-height:22px">We would be honoured to serve {co}, and to begin, if you will allow it, with a single journey.</p>
      <div style="height:46px"></div><p class="it" style="font-size:26px;line-height:30px">Manmohan Komal</p><div class="lb mu" style="margin-top:6px">Chief Executive Officer</div></div>
    <div><div style="height:2.25in"><img class="plate" src="../assets/om_handle.jpg" alt=""></div><p class="cap"><b>Plate II</b>Detailed before every reservation.</p></div>
  </div>
  {fo(5)}
</section>
<section class="page">
  <div class="a" style="left:1in;right:1in;top:1in;height:8.3in"><img class="plate" src="../assets/om_bw.jpg" style="filter:contrast(.97);object-position:center 62%" alt=""></div>
  <div class="m" style="top:9.3in;display:flex;justify-content:space-between"><p class="cap"><b>Plate III</b>An arrival.</p><p class="cap">The standard has not changed since 2007.</p></div>
</section>
<section class="page">{run(f'II · In the Service of {cs}')}
  <div class="a" style="right:1in;top:1.45in"><img src="{logo}" alt="{co}" style="height:{lh}"></div>
  {head('II', f'In the service of <i>{cs}</i>', f'Four parts of your company travel differently. Here is what we would take care of for each.')}
  <div class="m" style="top:4.0in;border-top:1px solid var(--ink)">{needs}</div>
  <div class="m" style="top:9.0in"><p class="tx" style="max-width:4.3in;color:var(--mut);font-style:italic">{cs} is not buying transportation. It is buying how its people and its guests feel at the start and end of a journey.</p></div>
  {fo(6)}
</section>
<section class="page">{run(f'III · From Your {city} Campus')}
  {head('III', f'From your {city} campus', 'The journeys your people are most likely to take, and the vehicle we would send.')}
  <div class="m" style="top:3.85in;display:grid;grid-template-columns:3.55in 1fr;gap:.45in">
    <div><div class="lb mu" style="margin-bottom:10px">Table I &nbsp;·&nbsp; Destinations</div>
      <table><thead><tr><th>Destination</th><th>Code</th><th class="r">Vehicle</th></tr></thead><tbody>{rrows}</tbody></table>
      <p class="cap" style="max-width:3.4in">Rates are quoted to you directly, according to the route, the vehicle and your volume.</p></div>
    <div><div style="height:3.35in"><img class="plate" src="../assets/{place}" style="object-position:60% center" alt=""></div><p class="cap"><b>Plate IV</b>{place_cap}</p></div>
  </div>
  <div class="m" style="top:8.35in"><div class="hl"></div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.35in;margin-top:16px">
    <div><div class="lb mu">Also served</div><p style="font-size:12px;line-height:18px;margin-top:6px">Boston Logan, Stewart, Sikorsky and every rail hub on the corridor.</p></div>
    <div><div class="lb mu">States</div><p style="font-size:12px;line-height:18px;margin-top:6px">Connecticut, New York, New Jersey, Massachusetts, Rhode Island and beyond.</p></div>
    <div><div class="lb mu">Hours</div><p style="font-size:12px;line-height:18px;margin-top:6px">Every hour of every day. Early departures are planned the evening before.</p></div></div></div>
  {fo(7)}
</section>
<section class="page">
  <div class="a" style="left:1in;right:1in;top:2.6in;height:4.35in"><img class="plate" src="../assets/om_drive.jpg" alt=""></div>
  <div class="m" style="top:7.0in"><p class="cap"><b>Plate V</b>The drive, a little before eight.</p></div>
</section>
<section class="page">{run('VI · Six Assurances')}
  {head('VI', 'Six assurances, <i>in writing</i>', f'You should not have to take our word for it. This is what {cs} receives from the first journey.')}
  <div class="m" style="top:4.0in;border-top:1px solid var(--ink)">{wl}</div>
  <div class="m" style="top:8.75in"><div class="lb ac">An easy first step</div><p class="tx" style="margin-top:8px;max-width:4.3in">Send us one journey. See how it feels to hand a traveler to a partner who treats your name the way you do.</p></div>
  {fo(12)}
</section>
<section class="page">{run('VII · How We Would Begin')}
  {head('VII', 'How we would begin', 'Four steps, and none of them asks much of you.')}
  <div class="m" style="top:3.85in;border-top:1px solid var(--ink);padding-top:18px;display:grid;grid-template-columns:repeat(4,1fr);gap:.3in">{sl}</div>
  <div class="m" style="top:5.75in"><div class="hl"></div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.35in;margin-top:18px">{bl}</div></div>
  <div class="m" style="top:7.55in;border:1px solid var(--ink);padding:.3in;text-align:center"><div class="lb mu">Reservations, at any hour</div>
    <div class="ac" style="font-family:'Cor';font-weight:500;font-size:46px;line-height:50px;letter-spacing:.01em;font-variant-numeric:lining-nums;margin-top:8px">(203) 938-0000</div>
    <div style="font-size:13px;margin-top:6px">info@absolute-transportation.com</div></div>
  <div class="m cap" style="top:9.75in;text-align:center;margin:0">Set in Cormorant Garamond and Libre Caslon. Prepared in North Haven, Connecticut, for {co}.</div>
  {fo(13)}
</section>'''
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{co} — Quiet edition</title><style>{css(ACC[key])}</style></head><body>{P}</body></html>'
    open(os.path.join(HERE, 'concepts', f'{key}-quiet.html'), 'w', encoding='utf-8').write(html)
    print('wrote', key)


if __name__ == '__main__':
    for k in (sys.argv[1:] or COMPANIES):
        build(k)

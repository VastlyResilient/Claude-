#!/usr/bin/env python3
"""Full 12-page corporate decks in company-specific design themes.

Each theme sets the typefaces, palette, cover layout and photo set, and is applied
to every page. Writes themed/<theme>.html.

  Charter Communications:  signal (modern grotesk, navy + Charter blue, blue-hour photos)
                           harbor (Caslon serif, cream + navy, framed, waterfront photos)
  Subway:                  fresh (geometric sans, warm white + Subway green, daylight photos)
                           evergreen (Bodoni, ivory + forest green, inset frames)
"""
import os, sys
from build_corporate import COMPANIES

HERE = os.path.dirname(os.path.abspath(__file__))
CF, AF, OF = '../concepts/fonts', '../../assets', '../../concepts/fonts'
ABS = '../../assets/absolute_logo.png'

FONTS = {
    'Hanken': [(CF, 'hanken-grotesk-latin-300-normal', 300, 'normal'), (CF, 'hanken-grotesk-latin-400-normal', 400, 'normal'), (CF, 'hanken-grotesk-latin-600-normal', 600, 'normal'), (CF, 'hanken-grotesk-latin-800-normal', 800, 'normal')],
    'Caslon': [(CF, 'libre-caslon-text-latin-400-normal', 400, 'normal'), (CF, 'libre-caslon-text-latin-400-italic', 400, 'italic'), (CF, 'libre-caslon-text-latin-700-normal', 700, 'normal')],
    'CaslonD': [(CF, 'libre-caslon-display-latin-400-normal', 400, 'normal'), (CF, 'libre-caslon-text-latin-400-italic', 400, 'italic')],
    'Source': [(CF, 'source-sans-3-latin-300-normal', 300, 'normal'), (CF, 'source-sans-3-latin-400-normal', 400, 'normal'), (CF, 'source-sans-3-latin-600-normal', 600, 'normal')],
    'Bodoni': [(CF, 'bodoni-moda-latin-400-normal', 400, 'normal'), (CF, 'bodoni-moda-latin-400-italic', 400, 'italic'), (CF, 'bodoni-moda-latin-500-normal', 500, 'normal')],
    'Jost': [(AF, 'jost-300', 300, 'normal'), (AF, 'jost-400', 400, 'normal'), (AF, 'jost-500', 500, 'normal'), (AF, 'jost-600', 600, 'normal')],
}

THEMES = {
    'signal': dict(co='charter', title='Signal', FH='Hanken', FHW=800, FHLS='-.035em', FHLH='1.0', EM='color:var(--ac);font-style:normal', FB='Hanken', FBW=300, FL='Hanken', FLW=600, LLS='.16em', NUMF='Hanken', NUMW=300,
                   BG='#FFFFFF', INK='#0A1626', MUT='#5E6B7A', AC='#1D5F9E', LINE='rgba(10,22,38,.14)', DK='#061A30', ACD='#5BB0F0', PANEL='#F2F5F8', cover='type',
                   img=dict(cover='c_lineup_blue.jpg', open='reframe_charter.jpg', needs='c_exec_blue.jpg', why='c_chauffeur_blue.jpg', chauffeur='chauffeur_charter.jpg', road='c_lines.jpg', interior='c_interior_blue.jpg', testi='c_harbor.jpg', close='close_charter.jpg')),
    'harbor': dict(co='charter', title='Harbor', FH='CaslonD', FHW=400, FHLS='-.005em', FHLH='1.06', EM='font-family:Caslon;font-style:italic', FB='Source', FBW=300, FL='Source', FLW=600, LLS='.28em', NUMF='Caslon', NUMW=400,
                   BG='#F3EFE6', INK='#0F2238', MUT='#5D6470', AC='#1D5F9E', LINE='rgba(15,34,56,.2)', DK='#0F2238', ACD='#A9CDEE', PANEL='#EAE4D6', cover='framed',
                   img=dict(cover='c_harbor.jpg', open='reframe_charter.jpg', needs='c_exec_blue.jpg', why='c_chauffeur_blue.jpg', chauffeur='chauffeur_charter.jpg', road='c_lines.jpg', interior='c_interior_blue.jpg', testi='c_lineup_blue.jpg', close='close_charter.jpg')),
    'fresh': dict(co='subway', title='Fresh', FH='Jost', FHW=500, FHLS='-.025em', FHLH='1.02', EM='color:var(--ac);font-style:normal', FB='Jost', FBW=300, FL='Jost', FLW=500, LLS='.22em', NUMF='Jost', NUMW=300,
                  BG='#FBFAF4', INK='#10261A', MUT='#5C6A60', AC='#008938', LINE='rgba(16,38,26,.15)', DK='#0C3B22', ACD='#F2B700', PANEL='#EFF3EA', cover='split',
                  img=dict(cover='s_lineup_day.jpg', open='s_close_day.jpg', needs='s_team_day.jpg', why='s_chauffeur_day.jpg', chauffeur='s_chauffeur_day.jpg', road='s_road_day.jpg', interior='s_interior_day.jpg', testi='testi.jpg', close='s_close_day.jpg')),
    'evergreen': dict(co='subway', title='Evergreen', FH='Bodoni', FHW=400, FHLS='-.01em', FHLH='1.05', EM='font-style:italic', FB='Jost', FBW=300, FL='Jost', FLW=500, LLS='.36em', NUMF='Bodoni', NUMW=400,
                      BG='#F3EFE7', INK='#0B1A12', MUT='#5E6259', AC='#0C5B34', LINE='rgba(11,26,18,.2)', DK='#0B2417', ACD='#E3D7B4', PANEL='#E9E3D5', cover='full',
                      img=dict(cover='detail_aviator.jpg', open='reframe_subway.jpg', needs='day_subway.jpg', why='chauffeur_subway.jpg', chauffeur='chauffeur_subway.jpg', road='s_road_day.jpg', interior='s_interior_day.jpg', testi='testi.jpg', close='close_subway.jpg')),
}

WHY = [('A real person, every time', 'One number, answered day and night, 365 days a year. No queue and no menu.'),
       ('The owners are accountable', 'Family-owned since 2007. The people who own the company dispatch the cars and follow up after the ride.'),
       ('Flights tracked, delays absorbed', 'We watch every arrival in real time and adjust automatically, so the chauffeur is there when the plane actually lands.'),
       ('Chauffeurs built, not found', 'Background-checked, commercially licensed, trained in hospitality, and discreet.'),
       ('Licensed, insured, verifiable', 'U.S. DOT 1567094 · MC-580841 · Connecticut Livery Permit 3117, with a certificate naming {CO} on request.'),
       ('One clean account', 'Every trip confirmed in writing, and one itemized monthly statement.')]
OPS = [('Reservations, made simple', 'Book by phone or email with the details you have; we confirm every trip in writing.'),
       ('Flights tracked in real time', "We monitor arrivals and adjust for delays automatically."),
       ('Meet &amp; greet, done right', 'A name-board welcome, luggage handled, and a calm walk to the car.'),
       ('Early departures, planned ahead', 'We build in time for traffic, weather and security lines.'),
       ('Response you can set a watch to', 'Quotes and confirmations come back quickly, around the clock.'),
       ('Support when it matters most', 'There is always a live person and a backup plan. That is what 24/7 means.'),
       ('Billing that fits your workflow', 'Per-trip billing or a standing corporate account, itemized and clean.'),
       ('Clear, fair cancellation terms', 'Straightforward policies, shared up front and in writing.')]
FLEET = [('veh_aviator.jpg', 'Executive Crossover', 'Lincoln Aviator · Lincoln MKT', 'Up to 4', 'The quiet standard for airport runs and executive travel.'),
         ('veh_escalade.jpg', 'Luxury Full-Size SUV', 'Cadillac Escalade · Suburban · Expedition', 'Up to 6', 'Presence and space for executives and their luggage.'),
         ('veh_sprinter.jpg', 'Executive Sprinter', 'Mercedes-Benz Sprinter · Ford Transit', 'Up to 14', 'Move a leadership team or visiting guests together.'),
         ('veh_stretch.jpg', 'Stretch Limousine', 'Lincoln Super-Stretch', 'Up to 8', 'For milestones, the evening begins at the curb.')]
STEPS = [('One call', 'We set up your corporate account and learn how your team travels.'), ('One contact', 'Your travel desk and assistants get one number and one email.'),
         ('First trips', 'Every reservation confirmed in writing, every flight tracked.'), ('One statement', 'A single itemized monthly statement, built for easy reconciliation.')]
REVIEWS = [('The limos were on time, and the drives from Hamden, CT to NYC and back were smooth and easy. The drivers are very courteous, and the cars clean and comfortable. A stress-free experience.', 'Mark', 'Executive Transfer · Hamden → NYC'),
           ('We’ve been using Absolute Transportation for years, and have always found them prompt, courteous, and professional.', 'Rafael', 'Client of Many Years'),
           ('A great experience all around. The team was prompt, attentive, and flexible when I needed a second limousine just a few weeks before the wedding. Wonderful service.', 'Lindsay', 'Wedding Client'),
           ('The trolley was super fun and looked great. Our wedding party and their plus-ones took a ride around town for photos — and everyone absolutely loved it.', 'Gail', 'Wedding Celebration')]


def rgb(h):
    h = h.lstrip('#'); return ','.join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def css(t):
    fams = {t['FH'], t['FB'], t['FL'], t['NUMF']} | ({'Caslon'} if t['FH'] == 'CaslonD' else set())
    faces = ''.join(f"@font-face{{font-family:'{f}';src:url('{b}/{n}.woff2') format('woff2');font-weight:{w};font-style:{s};font-display:block}}" for f in fams for b, n, w, s in FONTS[f])
    return faces + f'''
:root{{--bg:{t['BG']};--ink:{t['INK']};--mut:{t['MUT']};--ac:{t['AC']};--line:{t['LINE']};--panel:{t['PANEL']}}}
@page{{size:8.5in 11in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#888;font-family:'{t['FB']}',sans-serif;font-weight:{t['FBW']};-webkit-font-smoothing:antialiased}}
.page{{position:relative;width:8.5in;height:11in;overflow:hidden;break-after:page;background:var(--bg);color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page:last-child{{break-after:auto}}
@media screen{{.page{{margin:20px auto}}}}
.dk{{--bg:{t['DK']};--ink:#FFFFFF;--mut:rgba(255,255,255,.66);--ac:{t['ACD']};--line:rgba(255,255,255,.2);--panel:rgba(255,255,255,.06)}}
.a{{position:absolute}} .m{{position:absolute;left:.7in;right:.7in}}
.hd{{font-family:'{t['FH']}',serif;font-weight:{t['FHW']};letter-spacing:{t['FHLS']};line-height:{t['FHLH']}}}
.hd em{{{t['EM']}}}
.lb{{font-family:'{t['FL']}';font-weight:{t['FLW']};font-size:7.4px;letter-spacing:{t['LLS']};text-transform:uppercase}}
.mu{{color:var(--mut)}} .ac{{color:var(--ac)}}
.bd{{font-size:10.2px;line-height:1.72;color:var(--ink);opacity:.86}}
.sm{{font-size:9.2px;line-height:1.6;color:var(--mut)}}
.ln{{height:1px;background:var(--line)}} .rule{{height:2px;background:var(--ac)}}
.num{{font-family:'{t['NUMF']}';font-weight:{t['NUMW']};color:var(--ac);line-height:1}}
.sub{{font-family:'{t['FH']}';font-weight:{t['FHW'] if t['FHW'] < 700 else 600};font-size:13.5px;letter-spacing:{'-.01em' if t['FHW'] >= 500 else '0'};line-height:1.25}}
img.cv{{width:100%;height:100%;object-fit:cover;display:block}}
'''


def build(name):
    t = THEMES[name]; key = t['co']; c = COMPANIES[key]; I = t['img']; D = rgb(t['DK'])
    logo_c, logo_w = '../' + c['LOGO_COLOR'], '../' + c['LOGO_WHITE']
    pn = [1]

    def head(label, dark=False):
        pn[0] += 1
        return (f'<div class="m" style="top:.55in;display:flex;justify-content:space-between;align-items:center"><span class="lb"><span class="ac">{pn[0] - 1:02d}</span> &nbsp;—&nbsp; {label}</span><img src="{logo_w if dark else logo_c}" alt="{c["CO"]}" style="height:{c["LOGO_H_SM"] if key == "charter" else "17px"}"></div>'
                f'<div class="m ln" style="top:.92in"></div>')

    def foot():
        return f'<div class="m lb mu" style="bottom:.45in;display:flex;justify-content:space-between;align-items:center;font-size:6.6px"><span>Prepared for {c["CO"]}</span><img src="{ABS}" style="height:10px;opacity:.75" alt=""><span>{pn[0]:02d}</span></div>'

    img = lambda k, pos='center': f'<img class="cv" src="../assets/{I[k]}" style="object-position:{pos}" alt="">'
    hq = {'charter': '400 Washington Boulevard, Stamford', 'subway': '1 Corporate Drive, Shelton'}[key]

    # ---------- 1 cover ----------
    cv = t['cover']
    if cv == 'type':
        cover = f'''<section class="page">
  <div class="m" style="top:.55in;display:flex;justify-content:space-between;align-items:center"><div style="display:flex;align-items:center;gap:16px"><img src="{ABS}" style="height:20px" alt="Absolute Transportation"><span class="mu" style="font-size:15px">×</span><img src="{logo_c}" style="height:{c['LOGO_H_SM']}" alt="{c['CO']}"></div><span class="lb mu">Partnership Proposal · Vol. 01 · 2027</span></div>
  <div class="m ln" style="top:1.0in;background:var(--ink)"></div>
  <div class="m" style="top:1.45in"><h1 class="hd" style="font-size:66px">Every trip,<br>connected.<br><em>{c['HQ_CITY']} to anywhere.</em></h1></div>
  <div class="m" style="top:4.85in;display:grid;grid-template-columns:repeat(4,1fr);gap:.2in"><div><div class="lb mu">Prepared for</div><div style="font-size:11px;margin-top:5px;line-height:1.45">{c['CO']}<br>{hq.split(',')[0]}</div></div><div><div class="lb mu">Nearest airport</div><div style="font-size:11px;margin-top:5px;line-height:1.45">{c['NEAR'][0].split(' ·')[0].replace('&amp; Sikorsky (BDR)','')}</div></div><div><div class="lb mu">Our base</div><div style="font-size:11px;margin-top:5px;line-height:1.45">North Haven, CT<br>Family-owned, 2007</div></div><div><div class="lb mu">Reservations</div><div style="font-size:11px;margin-top:5px;line-height:1.45">(203) 938-0000<br>24 hours, 365 days</div></div></div>
  <div class="a" style="left:0;right:0;top:5.9in;bottom:0">{img('cover', 'center 60%')}<div class="a" style="left:0;top:0;width:100%;height:5px;background:var(--ac)"></div></div>
</section>'''
    elif cv == 'framed':
        cover = f'''<section class="page"><div class="a" style="inset:.42in;border:1px solid var(--ink);outline:1px solid var(--line);outline-offset:4px"></div>
  <div class="a" style="left:1in;right:1in;top:.95in;text-align:center"><img src="{ABS}" style="height:20px" alt="Absolute Transportation"><div class="lb mu" style="margin-top:32px">A Proposal of Partnership · Prepared for</div><img src="{logo_c}" style="height:44px;margin-top:20px" alt="{c['CO']}">
    <div style="width:1px;height:30px;background:var(--ink);margin:24px auto"></div><h1 class="hd" style="font-size:50px">Executive Ground<br><em>Transportation</em></h1><p class="hd" style="font-size:15px;margin-top:14px;color:var(--mut)"><em>for the {c['HQ_CITY']} headquarters, and everyone who visits it</em></p></div>
  <div class="a" style="left:1.1in;right:1.1in;top:5.75in;height:3.6in;border:1px solid var(--ink);padding:6px">{img('cover', 'center 60%')}</div>
  <div class="a lb" style="left:1in;right:1in;bottom:.95in;display:flex;justify-content:space-between;font-size:6.8px"><span>Family-Owned · Est. 2007</span><span>North Haven, Connecticut</span><span>Volume 01 · 2027</span></div>
</section>'''
    elif cv == 'split':
        cover = f'''<section class="page dk">
  <div class="a" style="left:3.7in;right:0;top:0;bottom:0">{img('cover', '38% center')}</div>
  <div class="a" style="left:3.7in;top:0;bottom:0;width:6px;background:{t['ACD']}"></div>
  <div class="a" style="left:.6in;top:.6in;width:2.7in;bottom:.6in;display:flex;flex-direction:column">
    <img src="{ABS}" style="height:20px;align-self:flex-start" alt="Absolute Transportation">
    <div style="margin-top:auto"><div class="lb ac">A partnership proposal for</div><img src="{logo_w}" style="height:34px;margin-top:18px;display:block" alt="{c['CO']}">
      <div class="rule" style="width:48px;margin:26px 0 22px"></div><h1 class="hd" style="font-size:43px">Fresh thinking for every <em>travel day.</em></h1>
      <p class="bd" style="margin-top:16px;font-size:10.6px">Executive ground transportation for your {c['HQ_CITY']} headquarters, your leadership, and every franchisee and partner who visits.</p></div>
    <div style="margin-top:auto"><div class="ln"></div><div class="lb mu" style="margin-top:12px;display:flex;justify-content:space-between;font-size:6.4px"><span>Family-Owned · Est. 2007</span><span>Vol. 01 · 2027</span></div></div>
  </div>
</section>'''
    else:
        cover = f'''<section class="page dk">{img('cover', 'center 40%').replace('class="cv"', 'class="cv a" ')}
  <div class="a" style="inset:0;background:linear-gradient(180deg,rgba({D},.78) 0%,rgba({D},.25) 30%,rgba({D},.4) 55%,rgba({D},.95) 82%)"></div><div class="a" style="inset:.4in;border:1px solid rgba(255,255,255,.5)"></div>
  <div class="a" style="left:1in;right:1in;top:.95in;text-align:center"><img src="{ABS}" style="height:22px" alt="Absolute Transportation"><div class="lb mu" style="margin-top:14px">Family-Owned · Est. 2007</div></div>
  <div class="a" style="left:1in;right:1in;bottom:1.05in;text-align:center"><div class="lb mu">Prepared exclusively for</div><img src="{logo_w}" style="height:30px;margin-top:18px" alt="{c['CO']}"><div style="width:1px;height:36px;background:rgba(255,255,255,.5);margin:22px auto"></div>
    <h1 class="hd" style="font-size:54px">The <em>quiet</em> art<br>of arriving well.</h1><div class="lb" style="margin-top:24px">Executive Ground Transportation · Volume 01 · 2027</div></div>
</section>'''

    # ---------- 2 opening ----------
    opening = f'''<section class="page dk"><div class="a" style="inset:0">{img('open')}</div><div class="a" style="inset:0;background:linear-gradient(90deg,rgba({D},.94) 0%,rgba({D},.78) 48%,rgba({D},.35) 100%)"></div>
  {head('The Difference That Matters', True)}
  <div class="m" style="top:3.1in;right:2.2in"><h1 class="hd" style="font-size:46px">When your people ride with us, they're not just being driven. <em>They're carrying your name.</em></h1>
    <div class="rule" style="width:52px;margin:28px 0 22px"></div>
    <p class="bd" style="font-size:11.5px;max-width:4.6in">An executive's first hour of a travel day, and a visiting guest's first impression of {c['CO']}, both happen in the back of a car — the chauffeur who greets them, the condition of the vehicle, whether it arrives early or arrives at all.</p>
    <p class="bd" style="font-size:11.5px;max-width:4.6in;margin-top:12px">That moment reflects on you long before it reflects on us. So we treat every traveler you send as if your reputation is riding in the back seat — because it is.</p></div>
  {foot()}</section>'''

    # ---------- 3 needs ----------
    cols = [c['COL1'], ('Corporate Travel &amp; Executive Assistants', ['One number and one email for every booking', 'Flight tracking with automatic adjustments', 'Written confirmation of every trip', 'A single, itemized corporate account']), c['COL3'], c['COL4']]
    cards = ''.join(f'''<div><div class="rule"></div><div style="display:flex;gap:12px;align-items:baseline;margin-top:12px"><span class="num" style="font-size:26px">{i + 1:02d}</span><span class="sub">{ti}</span></div>{''.join(f'<div class="sm" style="margin-top:5px;padding-left:12px;border-left:1px solid var(--line)">{x}</div>' for x in its)}</div>''' for i, (ti, its) in enumerate(cols))
    needs = f'''<section class="page">{head('Built Around ' + c['CO'])}
  <div class="m" style="top:1.25in;display:grid;grid-template-columns:1fr 2.9in;gap:.4in;align-items:start"><div><h1 class="hd" style="font-size:40px">Whatever {c['CO_S']} plans, <em>we're the ground under it.</em></h1><p class="bd" style="margin-top:16px">{c['NEEDS_LEAD']}</p></div><div style="height:3.0in">{img('needs')}</div></div>
  <div class="m" style="top:4.95in;display:grid;grid-template-columns:1fr 1fr;gap:30px .45in">{cards}</div>
  <div class="m" style="bottom:.95in;background:var(--panel);padding:16px 20px"><p class="hd" style="font-size:16px;line-height:1.35">{c['CO_S']} isn't buying transportation. <em>It's buying how its people and its guests feel at the start and end of a trip.</em></p></div>
  {foot()}</section>'''

    # ---------- 4 why ----------
    reasons = ''.join(f'''<div style="display:grid;grid-template-columns:.5in 1fr;padding:12px 0;border-bottom:1px solid var(--line);align-items:baseline"><span class="num" style="font-size:22px">{i + 1:02d}</span><div><div class="sub">{a}</div><p class="sm" style="margin-top:3px">{b.format(CO=c['CO'])}</p></div></div>''' for i, (a, b) in enumerate(WHY))
    why = f'''<section class="page"><div class="a" style="right:0;top:0;bottom:0;width:2.9in">{img('why', '55% center')}</div>
  <div class="a" style="left:.7in;top:.55in;width:4.5in"><span class="lb"><span class="ac">{pn[0]:02d}</span> &nbsp;—&nbsp; Why Absolute</span><div class="ln" style="margin-top:14px"></div>
    <h1 class="hd" style="font-size:42px;margin-top:30px">Six reasons <em>the choice is easy.</em></h1><p class="bd" style="margin-top:14px">You shouldn't have to take our word for it. Here is exactly what {c['CO_S']} gets, in writing, from the first trip.</p>
    <div style="margin-top:18px;border-top:2px solid var(--ac)">{reasons}</div>
    <div style="margin-top:20px;border:1px solid var(--ink);padding:14px 16px"><div class="lb ac">An easy first step</div><p class="bd" style="margin-top:6px;opacity:1">Send us one trip. See how it feels to hand a traveler to a partner who treats your name the way you do.</p></div></div>
  <div class="a lb mu" style="left:.7in;width:4.5in;bottom:.45in;display:flex;justify-content:space-between;font-size:6.6px"><span>Prepared for {c['CO']}</span><span>{pn[0] + 1:02d}</span></div></section>'''
    pn[0] += 1

    # ---------- 5 fleet ----------
    fl = ''.join(f'''<div><div style="height:2.05in;position:relative">{'<img class="cv" src="../assets/' + f + '" alt="">'}<span class="lb" style="position:absolute;right:8px;top:8px;background:rgba(10,10,10,.78);color:#fff;padding:4px 8px;font-size:6.6px">{s} guests</span></div><div class="sub" style="margin-top:11px;font-size:14.5px">{n}</div><div class="lb mu" style="margin-top:4px;font-size:6.6px">{mo}</div><p class="sm" style="margin-top:5px">{d}</p></div>''' for f, n, mo, s, d in FLEET)
    fleet = f'''<section class="page">{head('The Fleet')}
  <div class="m" style="top:1.25in;display:flex;justify-content:space-between;align-items:flex-end"><h1 class="hd" style="font-size:40px">Every vehicle, <em>a reflection of you.</em></h1><p class="sm" style="max-width:2.3in;text-align:right">Each one is detailed before it reaches your people, always in black, always immaculate.</p></div>
  <div class="m" style="top:2.55in;display:grid;grid-template-columns:1fr 1fr;gap:22px .3in">{fl}</div>
  <div class="m" style="bottom:.95in;display:grid;grid-template-columns:1fr 1fr;gap:.3in"><div style="background:var(--panel);padding:14px 16px"><div class="lb ac">All-electric option</div><p class="sm" style="margin-top:5px;color:var(--ink)">Ford Mustang Mach-E, for the traveler who asks. The same standard of care, a lighter footprint.</p></div><div style="background:var(--ink);color:var(--bg);padding:14px 16px"><div class="lb">One fleet, one standard</div><p class="sm" style="margin-top:5px;color:inherit;opacity:.85">Tell us the traveler, the moment and the party size, and we'll recommend the right vehicle.</p></div></div>
  {foot()}</section>'''

    # ---------- 6 chauffeurs ----------
    pillars = [('Vetted &amp; Licensed', 'Background-checked and licensed to commercial livery standards.'), ('Trained in Hospitality', 'Meet-and-greet, luggage, and the quiet courtesies.'), ('Local Expertise', 'Airports, rail stations and back roads known by heart.'), ('Discreet &amp; Composed', 'Calm under pressure, and confidential.')]
    chauffeurs = f'''<section class="page dk"><div class="a" style="left:0;right:0;top:2.5in;height:4.55in">{img('chauffeur', 'center 72%')}</div><div class="a" style="left:0;right:0;top:2.5in;height:4.6in;background:linear-gradient(180deg,rgba({D},1) 0%,rgba({D},0) 14%,rgba({D},0) 70%,rgba({D},1) 100%)"></div>
  {head('The Chauffeurs', True)}
  <div class="m" style="top:1.2in"><h1 class="hd" style="font-size:40px;max-width:6in">The car makes the first impression. <em>The chauffeur makes it last.</em></h1></div>
  <div class="m" style="top:7.25in"><p class="bd" style="font-size:11px">Great chauffeurs aren't found. They're built — and we gladly do the unglamorous work it takes to build them. The vetting. The background checks. The commercial licensing. The training on the hundred small things a passenger only notices when they're missing. Because your name is on the line every time you put someone in our car, ours show up early, dressed sharp, and unshakable when travel goes sideways.</p>
    <div class="ln" style="margin:20px 0 18px"></div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.3in">{''.join(f'<div><div class="rule" style="width:26px"></div><div class="sub" style="margin-top:10px">{a}</div><p class="sm" style="margin-top:5px">{b}</p></div>' for a, b in pillars)}</div></div>
  {foot()}</section>'''

    # ---------- 7 coverage + routes ----------
    routes = ''.join(f'''<div style="display:grid;grid-template-columns:1fr 1fr .8fr;padding:8px 0;border-bottom:1px solid var(--line);font-size:10.2px;align-items:baseline"><span style="font-weight:{t['FLW']}">{a}</span><span>{b}</span><span class="lb mu" style="text-align:right;font-size:6.4px">{v}</span></div>''' for a, b, v in c['ROUTES'])
    coverage = f'''<section class="page">{head('Coverage &amp; Routes')}
  <div class="m" style="top:1.25in"><h1 class="hd" style="font-size:40px">From your front door <em>to the gate.</em></h1><p class="bd" style="margin-top:14px;max-width:5.6in">We are rooted in Connecticut and serve the entire Northeast corridor: nine regional airports, the rail hubs, Manhattan, Boston, and every state that borders ours.</p></div>
  <div class="m" style="top:3.2in;display:grid;grid-template-columns:1.45fr 1fr;gap:.45in"><div><div class="lb">Your most likely routes</div><div style="margin-top:8px;border-top:2px solid var(--ac)">{routes}</div><p class="sm" style="margin-top:10px">Corporate rates are quoted to you directly, tailored to the route, the vehicle and your volume.</p></div>
    <div><div class="lb">{c['NEAR_TITLE']}</div><div style="margin-top:8px;border-top:2px solid var(--ac)">{''.join(f'<div class="sm" style="padding:8px 0;border-bottom:1px solid var(--line);color:var(--ink)">{x}</div>' for x in c['NEAR'])}</div>
      <div class="lb" style="margin-top:22px">States we serve</div><p class="sm" style="margin-top:8px;color:var(--ink)">CT · NY · NJ · MA · RI · PA · VT · NH · DE · DC</p></div></div>
  <div class="m" style="bottom:.95in;height:3.3in">{img('road')}<div class="a" style="inset:0;background:linear-gradient(90deg,rgba({D},.85) 0%,rgba({D},.4) 55%,rgba({D},0) 100%)"></div><div class="a" style="left:.35in;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;color:#fff"><div class="hd" style="font-size:26px">One partner.<br>The entire Northeast corridor.</div><div class="lb" style="margin-top:12px;opacity:.85">Nine airports · Any hour</div></div></div>
  {foot()}</section>'''

    # ---------- 8 partnership ----------
    ops = ''.join(f'''<div style="display:grid;grid-template-columns:.5in 1fr;align-items:baseline"><span class="num" style="font-size:24px">{i + 1:02d}</span><div><div class="sub">{a}</div><p class="sm" style="margin-top:4px">{b}</p></div></div>''' for i, (a, b) in enumerate(OPS))
    partner = f'''<section class="page dk">{head('The Partnership, In Practice', True)}
  <div class="m" style="top:1.25in"><h1 class="hd" style="font-size:40px">How working together <em>actually feels.</em></h1><p class="bd" style="margin-top:14px;max-width:5.4in">No mystery, no surprises. This is the operating standard behind every reservation you send us.</p></div>
  <div class="m" style="top:3.2in;display:grid;grid-template-columns:1fr 1fr;gap:30px .45in">{ops}</div>
  <div class="m" style="bottom:.95in"><div class="ln"></div><div style="display:grid;grid-template-columns:1fr 1.7fr;gap:.4in;margin-top:20px"><div class="hd" style="font-size:20px">When something <em>goes sideways.</em></div><p class="bd">Real travel breaks plans: a flight diverts, a meeting runs long, a traveler adds a stop. Dispatch runs around the clock with backup vehicles and drivers on call, so a problem becomes a call we absorb. You hear about it from us, with a fix already in motion.</p></div></div>
  {foot()}</section>'''

    # ---------- 9 insured ----------
    creds = [('U.S. DOT Number', '1567094'), ('MC Number', 'MC-580841'), ('Connecticut Livery Permit', '3117')]
    insured = f'''<section class="page">{head('Insured · Licensed · Accountable')}
  <div class="m" style="top:1.25in"><h1 class="hd" style="font-size:40px">The question procurement <em>asks first.</em></h1><p class="bd" style="margin-top:14px;max-width:5.7in">The answer is a simple yes, with the credentials to prove it. Absolute Transportation is fully licensed by the State of Connecticut, federally authorized as an interstate motor carrier, and fully insured in accordance with Connecticut and federal regulations.</p></div>
  <div class="m dk" style="top:3.55in;background:var(--bg);color:var(--ink);display:grid;grid-template-columns:repeat(3,1fr)">{''.join(f'<div style="padding:26px 22px;{"border-left:1px solid var(--line)" if i else ""}"><div class="lb mu" style="font-size:6.6px">{a}</div><div style="font-family:{t["NUMF"]};font-weight:{t["NUMW"]};font-size:27px;letter-spacing:.06em;margin-top:8px">{b}</div></div>' for i, (a, b) in enumerate(creds))}</div>
  <div class="m" style="top:5.25in"><p class="sm">Our operating authority is public and independently verifiable through the FMCSA SAFER system.</p></div>
  <div class="m" style="top:5.95in;display:grid;grid-template-columns:repeat(3,1fr);gap:.35in">{''.join(f'<div><div class="rule"></div><div class="sub" style="margin-top:12px">{a}</div><p class="sm" style="margin-top:5px">{b}</p></div>' for a, b in [('Your duty of care, supported', 'Put your people with a fully licensed, fully insured carrier, and your duty of care for traveling employees rests on documented ground.'), ('Coverage built for livery', 'Commercial passenger protection written specifically for professional chauffeured transport.'), ('Paperwork at your pace', f'A Certificate of Insurance naming {c["CO"]} as certificate holder is typically ready the same business day.')])}</div>
  <div class="m" style="bottom:.95in;height:2.2in">{img('interior')}</div>
  {foot()}</section>'''

    # ---------- 10 begin ----------
    begin = f'''<section class="page">{head("How We'd Begin")}
  <div class="m" style="top:1.25in"><h1 class="hd" style="font-size:40px">Simple to start. <em>Simple to keep.</em></h1></div>
  <div class="m" style="top:2.45in"><div class="rule"></div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.3in;margin-top:16px">{''.join(f'<div><div class="num" style="font-size:30px">{i + 1:02d}</div><div class="sub" style="margin-top:8px">{a}</div><p class="sm" style="margin-top:5px">{b}</p></div>' for i, (a, b) in enumerate(STEPS))}</div></div>
  <div class="m" style="top:4.75in;display:grid;grid-template-columns:repeat(3,1fr);gap:.3in">{''.join(f'<div style="background:var(--panel);padding:16px 18px"><div class="sub">{a}</div><p class="sm" style="margin-top:6px">{b}</p></div>' for a, b in [('Per-trip or on account', 'Bill each reservation on its own, or run a monthly corporate account with itemized statements.'), ('The quote is the number', 'Every rate includes the chauffeur, tolls, meet and greet, and flight tracking. Gratuity and parking are the only extras, disclosed up front.'), ('Volume in your favor', 'The more you send our way, the sharper the corporate rate.')])}</div>
  <div class="m dk" style="bottom:.95in;height:3.1in;background:var(--bg);color:var(--ink);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center"><div class="lb ac">Corporate partner reservations</div><div class="hd" style="font-size:58px;margin-top:14px">(203) 938-0000</div><div class="rule" style="width:40px;margin:18px auto"></div><div class="lb mu">Answered by a real person · 24 hours · 365 days</div><div class="sm" style="margin-top:10px">info@absolute-transportation.com &nbsp;·&nbsp; management@absolute-transportation.com</div></div>
  {foot()}</section>'''

    # ---------- 11 testimonials ----------
    revs = ''.join(f'''<div style="background:rgba({D},.72);border:1px solid rgba(255,255,255,.2);padding:20px 22px"><div class="hd ac" style="font-size:34px;line-height:.6">“</div><p class="bd" style="margin-top:8px;opacity:.95">{q}</p><div class="sub" style="margin-top:14px">{n}</div><div class="lb mu" style="margin-top:4px;font-size:6.4px">{r}</div></div>''' for q, n, r in REVIEWS)
    testi = f'''<section class="page dk"><div class="a" style="inset:0">{img('testi')}</div><div class="a" style="inset:0;background:rgba({D},.72)"></div>
  {head('In Their Own Words', True)}
  <div class="m" style="top:1.25in"><h1 class="hd" style="font-size:40px">Trust, earned <em>one ride at a time.</em></h1></div>
  <div class="m" style="top:3.0in;display:grid;grid-template-columns:1fr 1fr;gap:.25in;align-items:start">{revs}</div>
  <div class="m lb mu" style="bottom:.95in;text-align:center">More verified reviews at facebook.com/AbsoluteTransportation · Trusted since 2007</div>
  {foot()}</section>'''

    # ---------- 12 close ----------
    close = f'''<section class="page dk"><div class="a" style="inset:0">{img('close')}</div><div class="a" style="inset:0;background:linear-gradient(180deg,rgba({D},.88) 0%,rgba({D},.62) 40%,rgba({D},.95) 78%)"></div>
  <div class="m" style="top:1.3in"><div class="lb ac">Let's begin</div><h1 class="hd" style="font-size:48px;margin-top:18px;max-width:6.3in">Give your people a reason to remember the ride — <em>and to thank you for it.</em></h1>
    <p class="bd" style="font-size:11.5px;max-width:4.9in;margin-top:20px">Send us one trip. When it goes exactly as promised — and it will — we'll be here for the next one, and the thousand after that.</p></div>
  <div class="m" style="top:5.75in;border:1px solid rgba(255,255,255,.4);padding:28px 40px;text-align:center;background:rgba({D},.5)"><p class="hd" style="font-size:22px;line-height:1.35"><em>“People don't remember what you sold them. They remember how well you served them.”</em></p><div class="lb mu" style="margin-top:16px">Manmohan Komal · Chief Executive Officer</div></div>
  <div class="m" style="bottom:.6in"><div class="ln"></div><div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:22px"><div style="display:grid;grid-template-columns:auto auto;gap:14px 40px"><div><div class="lb mu" style="font-size:6.4px">Reservations · 24/7</div><div class="hd" style="font-size:22px;margin-top:4px">(203) 938-0000</div></div><div><div class="lb mu" style="font-size:6.4px">Home base</div><div class="sm" style="margin-top:4px;color:#fff">341 Washington Avenue<br>North Haven, CT 06473</div></div><div><div class="lb mu" style="font-size:6.4px">Email</div><div class="sm" style="margin-top:4px;color:#fff">info@absolute-transportation.com</div></div><div><div class="lb mu" style="font-size:6.4px">Online</div><div class="sm" style="margin-top:4px;color:#fff">absolute-transportation.com</div></div></div>
    <div style="display:flex;align-items:center;gap:18px"><img src="{ABS}" style="height:30px" alt="Absolute Transportation"><span style="width:1px;height:34px;background:rgba(255,255,255,.4)"></span><img src="{logo_w}" style="height:{'30px' if key == 'charter' else '22px'}" alt="{c['CO']}"></div></div></div>
</section>'''

    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Absolute Transportation × {c["CO"]} — {t["title"]}</title><style>{css(t)}</style></head><body>' + '\n'.join([cover, opening, needs, why, fleet, chauffeurs, coverage, partner, insured, begin, testi, close]) + '</body></html>'
    os.makedirs(os.path.join(HERE, 'themed'), exist_ok=True)
    open(os.path.join(HERE, 'themed', f'{name}.html'), 'w', encoding='utf-8').write(html)
    print('wrote', name)


if __name__ == '__main__':
    for n in (sys.argv[1:] or THEMES):
        build(n)

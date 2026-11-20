#!/usr/bin/env python3
"""Build the personalized corporate decks from the main deck.

Reads ../deck.html (the master design), swaps in the custom image set from
./assets, rewrites the copy for a corporate reader, and personalizes it for
each company in COMPANIES. Writes <key>.html next to this script.

usage: python3 build_corporate.py [charter subway]
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

COMPANIES = {
    'charter': dict(
        CO='Charter Communications', CO_S='Charter', HQ_CITY='Stamford',
        LOGO_COLOR='assets/logo_charter.png', LOGO_WHITE='assets/logo_charter_white.png', LOGO_H='38px', LOGO_H_SM='30px',
        WHERE="From 400 Washington Boulevard to Westchester County, LaGuardia, JFK and Newark — plus Manhattan, Bradley, Boston and every state that borders Connecticut.",
        NEEDS_LEAD="Your Stamford campus sits beside the train station and within reach of four major airports — and with the Cox combination, your company now has a significant presence in Atlanta as well. Here is exactly where we fit, so travel never costs your team a second thought.",
        COL1=('Executive Office &amp; Board', ['Airport transfers to HPN, LGA, JFK &amp; Newark', 'Stamford ↔ Atlanta travel days, door to gate', 'Board, investor &amp; analyst meetings in Manhattan', 'Hourly, as-directed service for multi-stop days']),
        COL3=('Visitors, Candidates &amp; Partners', ['Meet &amp; greet at the airport or Stamford Station', 'Arrivals for visiting leaders and guests', 'Candidate and new-hire travel that sells the role', 'Hotel, campus and dinner transfers']),
        COL4=('Events &amp; Team Travel', ['Sprinters for teams of up to 14', 'Off-sites, town halls and leadership meetings', 'Timed, multi-vehicle event shuttles', 'Client entertainment and celebrations']),
        NEAR_TITLE='Closest To Your Stamford Campus',
        NEAR=['Westchester County (HPN) · your nearest airport', 'LaGuardia &amp; JFK · domestic and international', 'Newark Liberty · the United hub', 'Stamford Station · Metro-North &amp; Amtrak, at your door'],
        ROUTES=[('Stamford HQ', 'Westchester County (HPN)', 'Sedan / SUV'), ('Stamford HQ', 'LaGuardia', 'Sedan / SUV'), ('Stamford HQ', 'JFK International', 'Sedan / SUV'),
                ('Stamford HQ', 'Newark Liberty', 'Sedan / SUV'), ('Stamford HQ', 'Midtown Manhattan', 'Sedan / SUV'), ('Stamford HQ', 'Bradley International', 'SUV / Sprinter')],
        TRUST="Charter has spent decades earning the confidence of its customers, its partners and its people. We never take that for granted — arriving early, presenting immaculately, and handling the quiet courtesies that turn a simple transfer into a reason your traveler thanks you for arranging it.",
        COVER_POS='center 30%', CHAUF_POS='68%',
    ),
    'subway': dict(
        CO='Subway', CO_S='Subway', HQ_CITY='Shelton',
        LOGO_COLOR='assets/logo_subway.svg', LOGO_WHITE='assets/logo_subway_white.svg', LOGO_H='30px', LOGO_H_SM='22px',
        WHERE="From 1 Corporate Drive in Shelton to Bradley, Tweed New Haven, Westchester, LaGuardia, JFK and Newark — plus Manhattan, Boston and every state that borders Connecticut.",
        NEEDS_LEAD="Subway runs from two headquarters — Shelton and Miami — and serves franchisees around the world. That means a steady rhythm of flights, visitors and events. Our home base in North Haven is a short drive from your Shelton campus. Here is exactly where we fit.",
        COL1=('Leadership &amp; Executive Travel', ['Airport transfers to BDL, HVN, HPN, LGA &amp; JFK', 'Shelton ↔ Miami travel days, door to gate', 'Meetings in Manhattan, Boston and beyond', 'Hourly, as-directed service for multi-stop days']),
        COL3=('Franchisees, Partners &amp; Guests', ['Meet &amp; greet for visiting franchisees and partners', 'Airport arrivals to the Shelton headquarters', 'Candidate and new-hire travel that sells the role', 'Hotel, campus and dinner transfers']),
        COL4=('Events &amp; Team Travel', ['Sprinters for teams of up to 14', 'Leadership meetings, trainings and off-sites', 'Timed, multi-vehicle event shuttles', 'Celebrations and team outings']),
        NEAR_TITLE='Closest To Your Shelton Campus',
        NEAR=['Tweed New Haven (HVN) &amp; Sikorsky (BDR)', 'Bradley International (BDL) · Hartford', 'Westchester County, LaGuardia &amp; JFK', 'Bridgeport &amp; New Haven · Metro-North &amp; Amtrak'],
        ROUTES=[('Shelton HQ', 'Tweed New Haven (HVN)', 'Sedan / SUV'), ('Shelton HQ', 'Bradley International', 'Sedan / SUV'), ('Shelton HQ', 'Westchester County (HPN)', 'Sedan / SUV'),
                ('Shelton HQ', 'LaGuardia', 'Sedan / SUV'), ('Shelton HQ', 'JFK International', 'Sedan / SUV'), ('Shelton HQ', 'Midtown Manhattan', 'SUV / Sprinter')],
        TRUST="Subway has spent decades earning the confidence of its guests, its franchisees and its people. We never take that for granted — arriving early, presenting immaculately, and handling the quiet courtesies that turn a simple transfer into a reason your traveler thanks you for arranging it.",
        COVER_POS='center 30%', CHAUF_POS='84%',
    ),
}


def build(key):
    c = COMPANIES[key]
    s = open(os.path.join(HERE, '..', 'deck.html'), encoding='utf-8').read()
    n = [0]

    def R(old, new, count=1):
        nonlocal s
        assert s.count(old) >= count, ('MISSING', key, old[:80], s.count(old))
        s = s.replace(old, new); n[0] += 1

    def section(marker):
        a = s.index('<!-- ============================================================ ' + marker)
        b = s.index('</section>', a) + len('</section>')
        return a, b

    # ---------- shared assets stay in ../assets ; the custom image set is in ./assets ----------
    s = s.replace('assets/', '../assets/')
    IMG = {'luxury_car.jpg': 'strip.jpg', 'hero_night.jpg': f'reframe_{key}.jpg', 'fleet_sedan.jpg': 'family.jpg',
           'veh_aviator.jpg': 'veh_aviator.jpg', 'veh_escalade.jpg': 'veh_escalade.jpg', 'veh_sprinter.jpg': 'veh_sprinter.jpg',
           'veh_stretch.jpg': 'veh_stretch.jpg', 'veh_mache.jpg': 'veh_mache.jpg', 'fleet_b.jpg': 'interior_b.jpg',
           'chauffeur.jpg': f'chauffeur_{key}.jpg', 'atm_highway.jpg': 'highway.jpg', 'limos_in_line.jpg': 'lineup.jpg',
           'satisfaction.jpg': 'testi.jpg'}
    for old, new in IMG.items():
        R(f'src="../assets/{old}"', f'src="assets/{new}"')
    # stretch_c is used twice: interiors hero, then the closing page
    i = s.index('src="../assets/stretch_c.jpg"'); s = s[:i] + 'src="assets/interior_a.jpg"' + s[i + len('src="../assets/stretch_c.jpg"'):]
    R('src="../assets/stretch_c.jpg"', f'src="assets/close_{key}.jpg"')
    R('<title>', '<title>'); s = re.sub(r'<title>.*?</title>', f'<title>Absolute Transportation × {c["CO"]}</title>', s, count=1)

    # ---------- 1 · COVER ----------
    a, b = section('1 · COVER')
    cover = f'''<!-- ============================================================ 1 · COVER ============================================================ -->
<section class="page dark" style="overflow:hidden;background:#070707">
  <img class="bleed" src="assets/cover_{key}.jpg" alt="" style="height:74%;object-position:{c['COVER_POS']}">
  <div class="scrim" style="background:linear-gradient(180deg,rgba(7,7,7,.8) 0%,rgba(7,7,7,.3) 7%,rgba(7,7,7,0) 14%,rgba(7,7,7,0) 44%,rgba(7,7,7,.6) 55%,rgba(7,7,7,.95) 62%,#070707 66%)"></div>

  <div class="pin" style="left:0;right:0;top:.42in;text-align:center;font-family:'Inter';font-weight:500;font-size:7.2px;letter-spacing:.42em;text-transform:uppercase;color:rgba(255,255,255,.88)">Family-Owned &nbsp;·&nbsp; North Haven, Connecticut &nbsp;·&nbsp; Est. 2007</div>

  <div class="pin" style="left:.75in;right:.75in;top:6.95in;text-align:center;color:#fff">
    <div style="display:flex;align-items:center;justify-content:center;gap:16px;font-family:'Inter';font-weight:500;font-size:7.4px;letter-spacing:.5em;text-transform:uppercase;color:rgba(255,255,255,.72)"><span style="width:38px;height:1px;background:rgba(255,255,255,.4)"></span>Prepared Exclusively For<span style="width:38px;height:1px;background:rgba(255,255,255,.4)"></span></div>
    <div style="display:flex;align-items:center;justify-content:center;gap:26px;margin-top:22px">
      <img src="../assets/absolute_logo.png" alt="Absolute Transportation" style="height:34px;width:auto">
      <span style="width:1px;height:40px;background:rgba(255,255,255,.35)"></span>
      <img src="{c['LOGO_WHITE']}" alt="{c['CO']}" style="height:{c['LOGO_H']};width:auto">
    </div>
    <h1 style="font-family:'Cormorant';font-weight:300;font-size:28px;line-height:1;letter-spacing:.16em;text-transform:uppercase;margin-top:30px;padding-left:.16em">Executive Ground Transportation</h1>
    <p style="font-family:'Cormorant';font-style:italic;font-weight:400;font-size:19px;line-height:1.45;letter-spacing:.01em;color:rgba(255,255,255,.8);margin-top:13px">A partnership proposal for your {c['HQ_CITY']} headquarters</p>
  </div>

  <div class="pin" style="left:.75in;right:.75in;top:9.2in;border-top:1px solid rgba(255,255,255,.18);display:grid;grid-template-columns:repeat(4,1fr);color:#fff">
    <div style="padding:13px 10px 0 0"><div style="font-family:'Inter';font-weight:500;font-size:6.4px;letter-spacing:.34em;color:rgba(255,255,255,.5)">01</div><div style="font-family:'Cormorant';font-weight:300;font-size:15px;margin-top:5px">Your Needs</div><div style="font-family:'Cormorant';font-style:italic;font-size:10.5px;color:rgba(255,255,255,.6);margin-top:2px">Built around {c['CO_S']}</div></div>
    <div style="padding:13px 10px 0 14px;border-left:1px solid rgba(255,255,255,.18)"><div style="font-family:'Inter';font-weight:500;font-size:6.4px;letter-spacing:.34em;color:rgba(255,255,255,.5)">02</div><div style="font-family:'Cormorant';font-weight:300;font-size:15px;margin-top:5px">The Fleet</div><div style="font-family:'Cormorant';font-style:italic;font-size:10.5px;color:rgba(255,255,255,.6);margin-top:2px">Every vehicle, a reflection of you</div></div>
    <div style="padding:13px 10px 0 14px;border-left:1px solid rgba(255,255,255,.18)"><div style="font-family:'Inter';font-weight:500;font-size:6.4px;letter-spacing:.34em;color:rgba(255,255,255,.5)">03</div><div style="font-family:'Cormorant';font-weight:300;font-size:15px;margin-top:5px">The Chauffeurs</div><div style="font-family:'Cormorant';font-style:italic;font-size:10.5px;color:rgba(255,255,255,.6);margin-top:2px">Built, never simply found</div></div>
    <div style="padding:13px 0 0 14px;border-left:1px solid rgba(255,255,255,.18)"><div style="font-family:'Inter';font-weight:500;font-size:6.4px;letter-spacing:.34em;color:rgba(255,255,255,.5)">04</div><div style="font-family:'Cormorant';font-weight:300;font-size:15px;margin-top:5px">The Partnership</div><div style="font-family:'Cormorant';font-style:italic;font-size:10.5px;color:rgba(255,255,255,.6);margin-top:2px">How working together feels</div></div>
  </div>

  <div class="pin" style="left:.75in;right:.75in;top:10.1in;text-align:center;font-family:'Inter';font-weight:300;font-size:7.6px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.55)">For Executive Leadership &nbsp;·&nbsp; Corporate Travel &nbsp;·&nbsp; Events &nbsp;·&nbsp; Talent Teams</div>

  <div class="pin" style="left:.75in;right:.75in;bottom:.42in;display:flex;justify-content:space-between;font-family:'Inter';font-weight:500;font-size:6.6px;letter-spacing:.36em;text-transform:uppercase;color:rgba(255,255,255,.5)"><span>Absolute Transportation, LLC</span><span>Volume 01 &nbsp;·&nbsp; 2027</span></div>
</section>'''
    s = s[:a] + cover + s[b:]

    # ---------- 2 · SIXTY-SECOND READ ----------
    R('“Every guest you send us is treated as though your name is in the back seat.”', '“Every traveler you send us is treated as though your name is in the back seat.”')
    R('Everything an agency needs<br>to know — before the<br>first phone call.', f"Everything {c['CO_S']} needs<br>to know — before the<br>first ride.")
    R('Six honest answers to the six questions every agency asks before they put their name next to a transportation company.', 'Six honest answers to the six questions a company asks before it trusts someone with its people.')
    R('Connecticut and every bordering state — NY, NJ, MA, RI and beyond — plus nine regional airports and every major cruise port in the region.', c['WHERE'])
    R('One immaculate, uniformly black fleet: executive sedans, full-size SUVs, group Sprinters, super-stretch limousines, and an all-electric option.', 'One immaculate, uniformly black fleet: executive crossovers, full-size SUVs, Sprinters for teams of up to 14, stretch limousines, and an all-electric option.')
    R("We don't hand your client a car. We hand them an arrival that reflects the standard your agency already set for them.", f"We don't hand your people a car. We hand them an arrival that reflects the standard {c['CO_S']} has already set.")
    R('When a flight slips at 4 a.m. or plans change last-minute, you want a partner who already has the answer.', 'When a flight slips at 4 a.m. or a meeting runs long, you want a partner who already has the answer.')

    # ---------- 3 · REFRAME ----------
    R("When you recommend us,<br>you're not arranging a ride.<br><span style=\"font-style:italic;font-weight:400;color:var(--ivory)\">You're lending us your name.</span>",
      "When your people ride with us,<br>they're not just being driven.<br><span style=\"font-style:italic;font-weight:400;color:var(--ivory)\">They're carrying your name.</span>")
    R("Your client's first impression and last impression of an entire trip both happen in the back of a car — the chauffeur who greets them, the condition of the vehicle, whether it arrives early or arrives at all.",
      f"An executive's first hour of a travel day, and a visiting guest's first impression of {c['CO']}, both happen in the back of a car — the chauffeur who greets them, the condition of the vehicle, whether it arrives early or arrives at all.")
    R('So we treat every guest you send as if your reputation is riding in the back seat', 'So we treat every traveler you send as if your reputation is riding in the back seat')

    # ---------- 4 · FAMILY ----------
    R("so every guest you send receives our full and personal attention", "so every traveler you send receives our full and personal attention")
    R('so every client you send is in familiar, trusted hands', 'so everyone you send is in familiar, trusted hands')
    R("“We build lasting relationships — with the guests we drive, and with the partners who trust us to represent them.”", "“We build lasting relationships — with the people we drive, and with the companies who trust us to represent them.”")
    R("a guest we're welcoming and a partner whose reputation we're carrying", "a traveler we're welcoming and a company whose reputation we're carrying")
    R('for your client and for you.', 'for your traveler and for you.')
    R("Your agency spent years earning your clients' confidence. We never take it for granted — arriving early, presenting immaculately, and handling the quiet courtesies that turn a simple transfer into a reason your client thanks you for the referral.", c['TRUST'])

    # ---------- 5 · FLEET ----------
    R("Each one is detailed before it reaches your client — because when you recommend us, you're recommending how our cars look, too.", "Each one is detailed before it reaches your people — because when you put someone in our car, you're trusting how it looks, too.")
    R('and the client who values arriving composed.', 'and the traveler who values arriving composed.')
    R('Presence and space for clients and their luggage — the natural choice for a seamless airport or cruise transfer.', 'Presence and space for executives and their luggage — the natural choice for a seamless airport transfer.')
    R('Move a wedding party, a cruise group, or a corporate team together', 'Move a leadership team, a project group, or visiting guests together')
    R('For your clients, the celebration begins at the curb.', 'For milestones and celebrations, the evening begins at the curb.')
    R('A sustainable choice for the client who asks', 'A sustainable choice for the traveler who asks')
    R('Tell us the guest, the moment, and the party size', 'Tell us the traveler, the moment, and the party size')
    R('Every interior is cleaned and inspected before it reaches your client', 'Every interior is cleaned and inspected before it reaches your traveler')

    # ---------- 6 · INTERIORS ----------
    R('The details your<br>clients remember.', 'The details your<br>people remember.')
    R("Stemware ready for the toast your client didn't expect.", "Stemware ready for the toast your team didn't expect.")

    # ---------- 6B · CHAUFFEURS ----------
    R('a client only notices when', 'a passenger only notices when')
    R('Because you put your name on the line every single time you recommend someone, and that means something to us.', 'Because your name is on the line every single time you put someone in our car, and that means something to us.')
    R('makes you look brilliant for sending them', 'makes you look brilliant for choosing them')
    R('Airports, cruise ports, and back-road shortcuts known by heart', 'Airports, rail stations, and back-road shortcuts known by heart')

    # ---------- 7 · COVERAGE ----------
    R('Where We Take Your Clients', 'Where We Take Your People')
    R('so you can send one client or an entire itinerary to a single, dependable partner.', 'so you can send one executive or an entire team with a single, dependable partner.')
    R('<svg><use href="#i-ship"/></svg></span>Cruise Ports</div>', f'<svg><use href="#i-pin"/></svg></span>{c["NEAR_TITLE"]}</div>')
    for old, new in zip(['Cape Liberty · Bayonne, NJ', 'Manhattan Cruise Terminal', 'Brooklyn Cruise Terminal', 'Port of New York'], c['NEAR']):
        R(f'</span>{old}</li>', f'</span>{new}</li>')
    R("From your client's front door — to the gate, the port, or the altar", 'From your front door — to the gate, the boardroom, or the venue')

    # ---------- 8 · SERVICES → "BUILT AROUND <CO>" ----------
    R('<div class="kick">Built Around Your Business</div>', f'<div style="display:flex;justify-content:space-between;align-items:center"><div class="kick">Built Around {c["CO"]}</div><img src="{c["LOGO_COLOR"]}" alt="{c["CO"]}" style="height:{c["LOGO_H_SM"]};width:auto"></div>')
    R("Whatever you plan,<br>we're the ground under it.", f"Whatever {c['CO_S']} plans,<br>we're the ground under it.")
    R('Different partners sell different experiences. Here is exactly how we fit into each of yours — so you can quote a client without a second thought.', c['NEEDS_LEAD'])

    def col(icon, title, items):
        return (f'<div class="col">\n        <div class="hd">\n          <span class="mi "><svg><use href="#i-{icon}"/></svg></span>\n          <h3>{title}</h3>\n        </div>\n        <ul>'
                + ''.join(f'<li>{i}</li>' for i in items) + '</ul>\n      </div>')
    a = s.index('<div class="svc"'); a = s.index('>', a) + 1
    b = s.index('<div style="margin-top:38px;background:var(--ink)', a)
    cols = '\n      ' + '\n      '.join([
        col('briefcase', *c['COL1']),
        col('plane', 'Corporate Travel &amp; Executive Assistants', ['One number and one email for every booking', 'Flight tracking with automatic adjustments', 'Written confirmation of every trip', 'A single, itemized corporate account']),
        col('bell', *c['COL3']),
        col('people', *c['COL4']),
    ]) + '\n    </div>\n\n    '
    s = s[:a] + cols + s[b:]
    R("And For Their Clients' Best Days Off", 'And For The Moments That Deserve More')
    R('Casino trips to Foxwoods &amp; Mohegan Sun · Connecticut wine &amp; beer trail tours · sporting events · nights out and celebrations. Whatever the occasion, the standard never changes.',
      'Milestone celebrations · retirement send-offs · client entertainment · sporting events · a stretch limousine when the night calls for one. Whatever the occasion, the standard never changes.')
    R("You're Not Really<br>Selling a Ride", "You're Not Really<br>Booking a Ride")
    R("Agencies, cruise planners, hotels and event teams aren't buying transportation — they're buying how a client feels at the start and end of a trip. <span style=\"font-style:normal;font-weight:500\">So are we.</span> Recommend Absolute and you're not simply arranging a car; you're protecting your reputation and giving your client one more reason to book with you again.",
      f"{c['CO']} isn't buying transportation — it's buying how its people and its guests feel at the start and end of a trip. <span style=\"font-style:normal;font-weight:500\">So are we.</span> Choose Absolute and you're not simply arranging a car; you're protecting the time of the people who lead your company, and the impression you make on everyone who visits it.")

    # ---------- 8B · OCCASIONS → "EVERY ITINERARY" ----------
    a, b = section('8B · THE EXPERIENCE')
    def tile(img, title, text):
        return (f'<figure style="margin:0"><div style="height:2.42in;overflow:hidden;border:1px solid var(--line)"><img src="assets/{img}" alt="" style="width:100%;height:100%;object-fit:cover;display:block"></div>'
                f'<figcaption style="margin-top:11px"><div style="font-family:\'Playfair\';font-weight:700;font-size:13px;color:var(--ink)">{title}</div>'
                f'<p style="font-size:9.3px;color:var(--muted);line-height:1.6;margin-top:5px;font-weight:300">{text}</p></figcaption></figure>')
    itin = f'''<!-- ============================================================ 8B · THE EXPERIENCE (every itinerary) ============================================================ -->
<section class="page">
  <div class="pad" style="height:100%;display:flex;flex-direction:column">
    <div class="kick">The Experience</div>
    <h1 class="display" style="font-size:33px;margin-top:15px;line-height:1.04">Every itinerary.<br>Handled beautifully.</h1>
    <p class="lead" style="margin-top:13px;max-width:5.6in;font-size:11px">From the first departure of the morning to the last arrival of the night, we deliver seamless, reliable, and elevated transportation for the travel days that matter most.</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px 22px;margin-top:24px">
      {tile('occ_airport.jpg', 'Airport transfers', 'Door to gate with flights tracked in real time — on time, relaxed, and well taken care of.')}
      {tile('occ_greet.jpg', 'Meet &amp; greet', 'A familiar, professional welcome at arrivals for visiting leaders, candidates and guests.')}
      {tile('occ_group.jpg', 'Team travel', 'Off-sites, trainings and events — the whole group moving together, and arriving on time.')}
      {tile('occ_city.jpg', 'The city', 'Manhattan meetings and multi-stop days, with a chauffeur who waits so your schedule never has to.')}
    </div>

    <div style="margin-top:auto;background:var(--ink);color:var(--ivory);padding:18px 24px;display:flex;justify-content:space-between;align-items:center">
      <div style="font-family:'Playfair';font-size:14px;line-height:1.4"><b style="font-weight:700">The destination matters.</b><br><span style="font-weight:400;color:rgba(246,243,236,.85)">So does every moment leading to it.</span></div>
      <div style="font-size:8px;letter-spacing:.24em;text-transform:uppercase;color:rgba(246,243,236,.8);text-align:right;line-height:1.9">24/7 Reservations<br>(203) 938-0000</div>
    </div>
  </div>
  <div class="foot"><span>Absolute Transportation, LLC</span><img class="footlogo" src="../assets/absolute_logo.png" alt="Absolute Transportation"><span class="gold">00</span></div>
</section>'''
    s = s[:a] + itin + s[b:]

    # ---------- 9 · PARTNERSHIP ----------
    R('the reason agencies stop worrying once they hand us the trip.', 'the reason travel teams stop worrying once they hand us the trip.')
    R("Your client's chauffeur is there when the plane actually lands", "Your traveler's chauffeur is there when the plane actually lands")
    R('<h3>Cruise pickups, timed to the ship</h3><p>We plan around debarkation windows and port traffic, so a returning guest is never left waiting on the curb after a long voyage.</p>',
      '<h3>Early departures, planned ahead</h3><p>We build in time for traffic, weather and security lines, so a 6 a.m. flight starts with a calm ride — not a race to the gate.</p>')
    R('so you always know where you and your client stand.', 'so you always know exactly where you stand.')
    R('a ship debarks late, a client adds a stop on the way', 'a meeting runs long, a traveler adds a stop on the way')
    R('long before your client notices anything at all.', 'long before your traveler notices anything at all.')
    R("“Reduce the agency's risk” isn't a slogan for us.", "“Reduce the company's risk” isn't a slogan for us.")

    # ---------- 10 · INSURED ----------
    R('The Question Agencies Ask First', 'The Question Procurement Asks First')
    R('is where most partnership conversations begin — and end.', 'is where most vendor conversations begin — and end.')
    R('A Certificate of Insurance naming your agency is available on request.', f"A Certificate of Insurance naming {c['CO']} is available on request.")
    R('A Certificate of Insurance naming your agency as certificate holder is available on request', f"A Certificate of Insurance naming {c['CO']} as certificate holder is available on request")
    R('Ask, and a COI naming your agency as certificate holder is on its way', f"Ask, and a COI naming {c['CO']} as certificate holder is on its way")
    R('What This Means For Your Agency', f"What This Means For {c['CO_S']}")
    R("Your reputation is covered, too</div><p style=\"font-size:9.3px;color:var(--muted);line-height:1.65;margin-top:7px;font-weight:300\">Refer a fully licensed, fully insured carrier and the liability that would otherwise shadow your recommendation sits with us — not with you.",
      "Your duty of care, supported</div><p style=\"font-size:9.3px;color:var(--muted);line-height:1.65;margin-top:7px;font-weight:300\">Put your people with a fully licensed, fully insured carrier, and your duty of care for traveling employees rests on solid, documented ground.")
    R('the level of coverage your clients deserve.', 'the level of coverage your people deserve.')
    R('Name the certificate holder and a COI for your corporate client or a venue is typically in your inbox the same business day.', 'Name the certificate holder and a COI for your risk or procurement team is typically in your inbox the same business day.')

    # ---------- 11 · DIRECT LINE ----------
    R('Preferred Partner Reservations', 'Corporate Partner Reservations')

    # ---------- 12 · RATES ----------
    R('The Partner Rate Guide', 'The Corporate Rate Guide')
    R('Every partner rate is tailored to the route', 'Every corporate rate is tailored to the route')
    R('<th>Popular Point-to-Point Routes</th><th>Vehicle Class</th><th class="r">Partner Rate</th>', '<th>Your Most Likely Routes</th><th>Vehicle Class</th><th class="r">Corporate Rate</th>')
    a = s.index('<tbody>') + len('<tbody>'); b = s.index('</tbody>', a)
    rows = ''.join(f'\n        <tr><td><span class="from">{f}</span> <span class="to">→ {t}</span></td><td style="font-size:9.5px;color:var(--muted)">{v}</td><td class="r">Corporate Rates Available</td></tr>' for f, t, v in c['ROUTES'])
    s = s[:a] + rows + '\n      ' + s[b:]
    R('Flat group rates for parties &amp; corporate teams up to 14.', 'Flat group rates for teams and events of up to 14.')
    R('Package pricing for weddings &amp; celebrations.', 'Package pricing for milestones &amp; celebrations.')
    R("Please call or email and we'll quote your client right away.", "Please call or email and we'll quote your trip right away.")
    R('How Partner Billing Works', 'How Corporate Billing Works')
    R('The more you send our way, the sharper the partner rate.', 'The more you send our way, the sharper the corporate rate.')

    # ---------- 13 · CLOSE ----------
    R('Give your clients a reason<br>to remember the ride —', 'Give your people a reason<br>to remember the ride —')
    R('See how it feels to hand a client to a partner who treats your name the way you do.', 'See how it feels to hand a traveler to a partner who treats your name the way you do.')
    R('Client references and a tailored partner welcome packet are available on request.', f"Client references and a welcome packet tailored to {c['CO']} are available on request.")

    # ---------- image fit for the custom photo set ----------
    R(f'<img class="bleed" src="assets/chauffeur_{key}.jpg" style="object-position:center 28%" alt="">', f'<img class="bleed" src="assets/chauffeur_{key}.jpg" style="height:66%;object-position:center ' + c['CHAUF_POS'] + '" alt="">')
    R('<div class="scrim" style="background:rgba(8,8,9,.55)"></div>', '<div class="scrim" style="background:rgba(8,8,9,.05)"></div>')
    R('rgba(8,8,9,.9),rgba(8,8,9,.82) 40%,rgba(8,8,9,.9))', 'rgba(8,8,9,.82),rgba(8,8,9,.6) 40%,rgba(8,8,9,.8))')
    R('<div class="scrim" style="background:rgba(8,8,9,.38)"></div>', '<div class="scrim" style="background:rgba(8,8,9,0)"></div>')
    R('rgba(8,8,9,.9),rgba(8,8,9,.72) 45%,rgba(8,8,9,.96))', 'rgba(8,8,9,.8),rgba(8,8,9,.5) 45%,rgba(8,8,9,.94))')

    # ---------- order: move "Built around <CO>" up, right after the reframe ----------
    a, b = section('8 · SERVICES BY PARTNER'); svc = s[a:b]; s = s[:a] + s[b:]
    i = s.index('<!-- ============================================================ 4 · WHO WE ARE'); s = s[:i] + svc + '\n\n' + s[i:]

    # ---------- footers: "Prepared for <CO>", sequential page numbers ----------
    s = s.replace('<div class="foot"><span>Absolute Transportation, LLC</span>', f'<div class="foot"><span>Prepared for {c["CO"]}</span>')
    k = [1]
    def renum(m):
        k[0] += 1; return f'{m.group(1)}{k[0]:02d}</span></div>'
    s = re.sub(r'(class="footlogo"[^>]*><span[^>]*>)\d\d</span></div>', renum, s)

    leftovers = [w for w in ('agency', 'agencies', 'Agency', 'Agencies', 'cruise', 'Cruise', ) if w in re.sub(r'<!--.*?-->', '', s, flags=re.S)]
    out = os.path.join(HERE, f'{key}.html'); open(out, 'w', encoding='utf-8').write(s)
    print(f'{key}: {n[0]} edits, footers 02-{k[0]:02d}, leftover terms: {leftovers or "none"}')


if __name__ == '__main__':
    for key in (sys.argv[1:] or COMPANIES):
        build(key)

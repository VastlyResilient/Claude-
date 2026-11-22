# Art-direction brief: "On arriving well" (Absolute Transportation, quiet edition)

Based on the 100-magazine survey, `build_oldmoney.py`, and the rendered six pages. All px values assume 96px/in on an 8.5 x 11in page (1px = 0.75pt). Where a justification rests only on the survey's "(inferred)" text, it is marked *(inf.)*.

## A. Verdict

1. The draft's bones are right: ivory stock, one serif voice, framed plates, roman numerals and a single quiet cover line are what the calmest titles in the set do (Cereal, Sabato, Luncheon, Ark Journal).
2. The photography brief (vehicles in real settings, natural light, details) matches The Road Rat and Yolo Journal.
3. Gap 1, legibility: body is 7–7.8pt and labels are 5pt. Kinfolk's 2021 redesign went the other way and enlarged body text.
4. Gap 2, unfinished space: the white is left over, not composed. Sabato's and Christophorus's "space" and "air" are designed.
5. Gap 3, weak apparatus: tables, captions, folios and chapter numbering are inconsistent, and the accent colour is defined in the CSS but never used.

Your four known weaknesses are all confirmed. The render shows "ar-rive", "an-swer", "train-ings" and "cele-brations".

## B. KEEP

- **Ivory paper, soft black ink, no gold.** Luncheon uses off-white matt stock; Christie's runs its editorial on uncoated; Konfekt uses cream *(inf.)*.
- **One cover image, small logo, one cover line.** Cereal, HTSI and Centurion do the same *(all inf.)*; Magneto isolates one car *(inf.)*.
- **Framed plates with white borders, not full-bleed everywhere.** Sotheby's "between an art journal and exhibition catalogue"; Document Journal *(inf.)*.
- **Roman numerals for volume and chapters.** Ark Journal numbers volumes in roman; Cereal numbers its articles.
- **A strict small type palette.** Monocle (Plantin and Helvetica only), brand eins (Sabon, occasional Futura), The New Yorker (Caslon text).
- **Vehicles in real places and material close-ups.** The Road Rat; Bentley Magazine *(inf.)*.
- **The signed letter, the drop cap, the colophon, and the plain phone block.**

## C. PIVOT

| # | Current | Change to | Why |
|---|---|---|---|
| 1 | Body 10.4px/1.78; secondary 9.2–9.6px | Body **13px/20px**; secondary (list descriptions) **12px/18px**. Nothing in Caslon below 10.5px | Kinfolk 2021 (larger body text) |
| 2 | `hyphens:auto` | `hyphens:manual; text-align:left; text-wrap:pretty` on body; `text-wrap:balance` on titles and quotes. Do not justify | Chromium justification without good hyphenation makes rivers; Rakesprogress "gentle typography" |
| 3 | Measure about 3.6in at 10.4px | Body measure **3.9–4.3in** (55–65 characters). Never the full 6.3in | Sabato, "simplicity and space" |
| 4 | Jost labels 6.4–6.8px, tracking .30–.34em | **8.5px, weight 500, tracking .18em**; running head 8px/.20em | 5pt will not hold in print. Monocle-style sans for labels only |
| 5 | Captions 8.4px italic, #756F64 | **10.5px/15px** Caslon italic, **#5E584E**, max width 3.2in, 9px below the plate | Eye's caption discipline *(inf.)*; Sotheby's small caption under artwork |
| 6 | Muted grey #756F64, hairlines at 22% ink | Muted **#5E584E**; hairline **0.5pt (0.67px) #1C1A17 at 35%**; head rule **0.75pt (1px) solid ink** | Tints this light break up on uncoated stock |
| 7 | Margins 1.1in; elements placed at ad-hoc `top` values | Left/right **1.0in** (text block 6.5in); running head at 0.6in; **every chapter title baseline at 2.2in**; **text starts at 3.3in**; text floor 9.5in; folio at 10.4in. 12 columns, 0.2in gutters; 20px baseline | Christophorus 2016 ("generous presentation, more air"); Fantastic Man's strict rules |
| 8 | Cormorant 300 at 13–17px in lists | Cormorant **500** below 24px; 300 only at 28px and above | Light hairlines vanish in print at small sizes |
| 9 | Accent `--ac` (#1F3A2B) unused | Use it in **three places only**: drop cap, chapter roman numerals, the phone number | Departures (one ownable colour); MIT Technology Review (one accent) *(inf.)* |
| 10 | Roman folios (ii, iii, xiii) on body pages; "Chapter VI" and "VII" share a page that Contents lists as xiii and xiv | Arabic oldstyle folios 2–15, none on plates or covers. Roman for chapters only. Contents must match real pages | Ark Journal, Cereal |
| 11 | Cover title 40px under a plate 5.0 x 5.35in | Plate **5.5 x 6.6in** (left/right 1.5in, top 1.35in); title **54px**; delete the 26px vertical tick; logo 20px high | HTSI single quiet line *(inf.)*; Magneto *(inf.)* |
| 12 | Letter: 124 words in the top 40% of the page | Set the letter at **14px/22px**, measure 4.2in, from 3.3in. Run om_hand as a narrow marginal plate (1.8 x 2.25in, top-aligned). Extend the letter to about 200 words (owner to approve copy) so it ends near 7.8in with the signature | The Gentlewoman, large text *(inf.)*; Patek Philippe, essay-first *(inf.)* |
| 13 | Contents: list ends at 5.2in, quote floats at 7.35in | Photo **2.6 x 5.2in** (2.2in to 7.4in). Contents rows 22px titles with 15px row padding, so the list fills the same height. Move the quote to its own page | Luncheon (contents as a designed menu) |
| 14 | Email in 8.4px grey italic | Email **13px roman, ink colour** | See J |

## D. ADD (ten; the first three matter most)

1. **Standfirst** under every chapter title: Cormorant italic 19px/27px, max 4.5in, one sentence. This is what fills the head of each page deliberately. Kinfolk (deck cut).
2. **A breather page**: one plate, one caption, nothing else, after the routes page. Vogue and Travel + Leisure (feature well); Yolo Journal.
3. **A complete plate system**: "Plate I" to "Plate VI" in Jost caps, then an italic caption that states place and moment; list the plates in the colophon. Sotheby's; Eye *(inf.)*.
4. **Frontispiece** on the inside cover: a fixed, named opening picture. Country Life *(inf.)*.
5. **Running head with a rule**: Jost 8px, company on the left, chapter on the right, 0.5pt rule 6px below. Fantastic Man (rules and boxes).
6. **A ruled box** around the phone block only: 0.75pt ink, 0.3in padding. Fantastic Man.
7. **Marginalia**: licence numbers, "est. 2007" and the airport codes as side notes in a 1.6in outer column, Caslon italic 10.5px. Sabato (captions pushed to the edge) *(inf.)*.
8. **A hand-drawn-style line map** of Shelton, North Haven and the six destinations, single ink weight. Lodestars Anthology.
9. **A facts panel kept apart from the essay pages** (fleet, permits, coverage). NetJets *(inf.)*; Christie's (two halves, clearly divided).
10. **A paired cover and inside cover**: the car outside on the cover, the same doorway from inside on page 2. Zeit Magazin (double covers).

## E. Typography spec

| Role | Typeface | Size / leading | Tracking, case |
|---|---|---|---|
| Cover title | Cormorant Garamond 300, italic 400 for one word | 54 / 58px | -0.01em, sentence case |
| Chapter title | Cormorant Garamond 300 | 44 / 48px | -0.005em, sentence case |
| Standfirst | Cormorant Garamond italic 400 | 19 / 27px | 0 |
| Body | Libre Caslon Text 400 | 13 / 20px (letter 14 / 22px) | 0, ragged right; paragraph indent 1.4em, none on the first |
| List item title | Cormorant Garamond 500 | 20 / 24px | 0 |
| Caption | Libre Caslon Text italic | 10.5 / 15px | 0, #5E584E |
| Label, chapter number | Jost 500 | 8.5px | .18em, caps |
| Running head | Jost 500 | 8px | .20em, caps, #5E584E |
| Folio | Libre Caslon Text 400 | 10.5px | oldstyle figures, centred |
| Table head | Jost 500 | 8.5px | .16em, caps |
| Table body | Libre Caslon Text 400 | 12.5 / 18px | tabular lining figures |
| Pull quote | Cormorant Garamond italic 400 | 28 / 37px | max 4.8in, balanced |
| Roman numerals | Cormorant Garamond italic 400 | 20px (steps 26px) | accent colour |
| Phone number | Cormorant Garamond 500 | 46px | lining figures, .01em |
| Drop cap | Cormorant Garamond 300 | 3 lines (about 66px) | accent colour |

Do not add a fourth family. Bodoni Moda and Playfair would push the look towards Vogue and Vanity Fair didone gloss. Do not use `font-variant:small-caps` unless the render proves the font has real small caps; use the Jost label style.

## F. Tables and lists

- **Rules:** horizontal only. 1px ink above the header; 0.67px at 35% under the header and between rows; 1px ink under the last row. No vertical rules, no fills, no zebra striping.
- **Header:** Jost caps, #5E584E, bottom-aligned, 8px padding below.
- **Rows:** 9px padding top and bottom; baseline-aligned; text columns left, figures right; 0.25in gutters. The first column takes the weight (Caslon 400 ink); qualifiers in italic #5E584E.
- **Figures:** tabular lining in tables and the phone number; oldstyle in running text and folios. Set both explicitly and check the render.
- **Routes table:** remove the repeated "Shelton" column. Title it "Table I · From your Shelton campus". Columns: Destination / Code / Vehicle, with drive time as a fourth column only if the owner supplies real figures. Keep the rates note at 10.5px.
- **Numbered lists** (needs, assurances): three columns of 0.45in numeral / 2.1in title / remainder for the description at 12px/18px. 12px row padding. Bullets inside a row become separate lines, not a semicolon run. Never split a row across pages.
- **Steps:** four columns with a 1px rule above, numeral over title over one line. Keep as drafted, at the new sizes.

Justified by Spear's (ruled columns and adviser tables) *(inf.)* and Bloomberg Businessweek (data set as design).

## G. Photography

1. One idea per picture: a vehicle, a hand, or a place.
2. The vehicle occupies no more than 40% of the frame, and architecture carries the rest (The Road Rat; Type 7 *(inf.)*).
3. Every car is a recognisable Escalade, Aviator or Sprinter, in black. On the contact sheet, om_hand appears to show a pale car, om_cabin's trim does not read as the fleet, and om_window shows a terraced street that does not look like Connecticut. Check these three, then re-shoot or drop them.
4. One light logic: low side light, shadows open but deep, no lens flare, no wet-street gloss. Sirene's "essential but never cold" is the tone to aim for.
5. Use only two crop ratios: 4:5 portrait and 3:2 landscape. Drop the near-square.
6. Sequence wide, then detail, then person, then wide. Never run two details in a row (The World of Interiors, unhurried sequences *(inf.)*).
7. One black-and-white plate only. Keep `saturate(.82)` on the rest so the set matches.
8. No faces to camera. Use chauffeurs' hands, backs and profiles. This reads as discretion and hides AI portrait artefacts.

**Additional shots (the first three are the most valuable):**
1. **The chauffeur**, three-quarter back view, adjusting a cuff beside an Escalade, stone wall, morning light. This is for the Chauffeurs page.
2. **Dawn at a small airport kerb**: Aviator waiting, chauffeur standing, empty forecourt. This is the picture for "flights are followed".
3. **The telephone still life**: desk, lamp, open ledger, handset, at night. This is the picture for "a person answers".
4. An empty wooded Connecticut parkway in October with no cars, for the breather page (Curves *(inf.)*).
5. A Sprinter interior, seats in raking light.
6. The doorway of the cover picture seen from inside, for device D10.

## H. Page notes and 16-page order

- **Cover:** larger plate and title; remove the tick; raise the three footer labels to 8.5px.
- **Contents:** tall photo and a larger list (C13); move the quote out; put "Prepared for Subway · Volume I · MMXXVII" as an anchored line at 9.5in.
- **Letter:** C12. Print the signature in Cormorant italic 26px with space for a real ink signature above it.
- **Plate:** keep. Widen it to the 6.5in block; number it; captions at 10.5px. Check the vehicle reads as an Escalade.
- **In the service of Subway:** too dense. Split it into a facing pair: needs on the left with a standfirst, routes table with the map on the right. Subway's logo appears once, at 17px.
- **Six assurances:** keep the structure, at the new sizes. "How we would begin" and the phone move to the facing page.

**Order:** 1 cover · 2 frontispiece plate · 3 contents · 4 plate (hand) · 5 letter · 6 in the service of Subway · 7 routes table and map · 8 breather plate · 9 the fleet and facts table · 10 plate (arrival, black-and-white) · 11 the chauffeurs · 12 six assurances · 13 how we would begin and phone · 14 closing plate · 15 the quote, alone · 16 back cover with colophon and phone repeated. Pages 12–13 face each other, so the pages that make saying yes easy form one spread.

## I. Two alternative directions

**1. The Gazette.** Text-led and strictly black-and-white. Centred titles inside ruled boxes, Caslon throughout, photographs small and monochrome. It reads like a private newsletter from a club. *Draws from:* Fantastic Man, brand eins, The New Yorker, Spear's *(inf.)*. *Cost in clarity:* low, and it is the clearest of the three. The cost is in warmth: the "artsy" and lighting-and-shadow part of the brief largely disappears.

**2. The Portfolio.** A picture book: 11 of 16 pages are plates, text is reduced to captions, and the offer is confined to one spread at the back. *Draws from:* Yolo Journal, Type 7, The Road Rat, Holiday. *Cost in clarity:* high. The buyer must reach page 12 to learn what is offered. It depends entirely on image quality, which is the weakest point with AI photography on a tight budget.

Recommendation: stay with the present direction and apply this brief.

## J. Risks

- **Small type is the magazines' habit, not a virtue here.** HTSI, System and The World of Interiors run small text *(inf.)*, but a procurement reader will not squint. Protect 13px body and 46px phone.
- **Covers with no cover lines** (Centurion, Patek Philippe *(inf.)*) would hide who this is for. Keep "Prepared for" and the client logo.
- **Mostly non-product editorial** (Patek Philippe *(inf.)*) suits a 300,000-copy members' title, not a 16-page proposal. Cap atmosphere at 6 of 16 pages.
- **Wit, illustrated covers and deliberate awkwardness** (Tatler, Noble Rot, 032c) conflict with "nothing flashy". Avoid them.
- **Paper changes, tip-ins, slipcases** (Christie's, Type 7, Cabana) cost money. One good uncoated stock is enough (Fortune started its redesign with paper).
- **Pages 12, 13 and 16 are protected.** No picture behind the text, no italic for facts, the licence numbers in full, and the phone number and email in ink colour at full size.
- **AI imagery of a real fleet.** Any vehicle the company does not own, or a place that is plainly not New England, undermines trust more than a plain page would.

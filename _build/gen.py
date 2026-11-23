#!/usr/bin/env python3
"""LPS Plumbing Group site generator (Latitude SAL template, LPS palette)."""
import os, sys, json, html

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
BASE = sys.argv[2] if len(sys.argv) > 2 else ''          # '' at launch, '/preview/lps-plumbing-group' for preview
NOINDEX = BASE != ''
DOMAIN = 'https://www.lpsplumbinggroup.com.au'
PHONE, TEL, EMAIL = '0452 611 522', '0452611522', 'info@lpsplumbinggroup.com'
LIC, ABN = '476073C', '34 280 954 515'
FORMSPREE = 'https://formspree.io/f/mjglroqj'          # TODO at launch: LPS's own Formspree form
GA4 = ''                                                  # TODO at launch: LPS GA4 ID
IG = 'lpsplumbinggroup'
CSS = open(os.path.join(os.path.dirname(__file__), 'base.css')).read()

def W(i, w=1600, h=1200):
    ids = {
        'vanity': '84f08c_57eb2384d0024e58ab621dfb068bc016~mv2.jpg',
        'ensuite': '84f08c_c9c2809182b140beaeb077a0cccf09d3~mv2.jpg',
        'shower': '84f08c_13a4fc071c0343bbaa0cc895a6ffb2ad~mv2.jpg',
        'hotwater': '84f08c_e65ea6674cb2471dbd05dbee0262826f~mv2.jpg',
        'kitchen': '84f08c_ea4c88c3d56a454490664f932a2cdc4a~mv2.jpg',
        'commercial': '84f08c_9eb455ae0f5146ac8238442c67aa7bd7~mv2.jpg',
        'basin': '84f08c_2135e71c90944570b443375bdf56af56~mv2.jpg',
        'miranda': '84f08c_054dfe7868444f069aebf91cd0aa9533~mv2.jpg',
        'logo': '84f08c_9dd65380a4c24c1b927187305cc5b8ae~mv2.png',
    }
    f = ids[i]
    if f.endswith('.png'):
        return f'https://static.wixstatic.com/media/{f}/v1/fit/w_{w},h_{h},q_95/lps.png'
    return f'https://static.wixstatic.com/media/{f}/v1/fill/w_{w},h_{h},al_c,q_82/lps.jpg'

def L(path):  # internal link
    return BASE + path if path != '/' else (BASE + '/' if BASE else '/')

ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
PHONE_SVG = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'

def btn(href, label, kind='gold', icon=ARROW):
    return f'<a href="{href}" class="btn btn-{kind}"><span class="roll"><i><b>{label}</b><b>{label}</b></i></span><span class="circ">{icon}</span></a>'

FAV = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='18' fill='%230B384D'/%3E%3Ctext x='50' y='66' font-family='Poppins,Arial,sans-serif' font-size='40' font-weight='700' fill='%23CFEADF' text-anchor='middle'%3ELPS%3C/text%3E%3C/svg%3E"

SERVICES = [
    ('new-builds', 'New builds', 'kitchen',
     'Full plumbing for custom homes and high end builds, from first fix to final.',
     'We plumb custom homes and architect designed builds from slab to handover. Drainage, rough in, gas, hot water and fit off, run to your program and finished to the standard your clients are paying for.',
     ['Stormwater, sewer and drainage set out', 'Rough in and pressure testing', 'Gas fitting and hot water systems', 'Fit off of premium tapware and fixtures', 'Compliance certificates on handover']),
    ('renovations', 'Renovations', 'vanity',
     'Kitchens, laundries and whole home renos, planned around the existing house.',
     'Renovations need a plumber who can work around what is already there. We plan the runs early, keep the site tidy and line up with your trades so walls close on time.',
     ['Kitchen and laundry relocations', 'Re-piping older homes', 'Wall hung and concealed fixtures', 'Coordination with builders and trades', 'Clean, protected work areas']),
    ('bathrooms', 'Bathrooms', 'ensuite',
     'Bathrooms and ensuites with the detail high end finishes need.',
     'In a bathroom, everything we do is on show. Set outs to the millimetre, wall mixers dead level and waterproofing friendly penetrations. We work with your tiler and waterproofer so the finish comes up clean.',
     ['Ensuites and main bathrooms', 'In wall mixers and concealed cisterns', 'Freestanding baths and floor wastes', 'Outdoor showers', 'Accurate set out for tilers']),
    ('commercial', 'Commercial', 'commercial',
     'Commercial fit outs and multi unit work, delivered to program.',
     'From fit outs to multi unit developments, we bring the same care to commercial work. Clear communication with site managers, documented testing and a crew that turns up when the program says.',
     ['Multi unit and townhouse developments', 'Commercial fit outs', 'Stack and riser installs', 'Fire and backflow coordination', 'Documented testing and sign off']),
    ('emergency', '24/7 emergency', 'hotwater',
     'Burst pipes, blocked drains and no hot water. Call any hour.',
     'When something fails, you need someone who picks up. We take emergency calls 24/7 across our service area and come prepared to fix it properly the first time, not patch it.',
     ['Burst and leaking pipes', 'Blocked drains and sewer', 'Hot water failures', 'Gas leaks', 'Make safe on builder sites']),
]

AREAS = [
    ('plumber-miranda', 'Miranda', 'Sutherland Shire', 'miranda',
     'Our home base. We plumb new builds, renovations and bathrooms across Miranda and the Sutherland Shire, including the ensuite renovation pictured.',
     ['Miranda', 'Caringbah', 'Gymea', 'Sylvania', 'Cronulla', 'Kirrawee']),
    ('plumber-mascot', 'Mascot', 'Inner South', 'commercial',
     'Mascot and the inner south have no shortage of townhouse, multi unit and commercial work. We plumb it start to finish and keep the site manager in the loop.',
     ['Mascot', 'Rosebery', 'Botany', 'Alexandria', 'Zetland', 'Eastlakes']),
    ('plumber-neutral-bay', 'Neutral Bay', 'Lower North Shore', 'basin',
     'High end homes and renovations across the lower north shore, where the finish matters as much as what is in the wall.',
     ['Neutral Bay', 'Cremorne', 'Mosman', 'Kirribilli', 'North Sydney', 'Cammeray']),
    ('plumber-eastern-suburbs', 'the Eastern Suburbs', 'Eastern Suburbs', 'shower',
     'Architect designed homes, terraces and full rebuilds across the east. We work with builders who expect premium fixtures installed without a second visit.',
     ['Bondi', 'Coogee', 'Randwick', 'Double Bay', 'Paddington', 'Vaucluse']),
]

FAQ = [
    ('Do you work directly with builders?', 'Yes. Most of our work comes through builders on new builds and renovations. Send your plans through the quote form and we will price the full plumbing scope, then work to your program.'),
    ('What areas do you cover?', 'We are based in the Sutherland Shire and work across Miranda and the Shire, Mascot and the inner south, Neutral Bay and the lower north shore, and the Eastern Suburbs.'),
    ('Are you licensed and insured?', f'Yes. LPS Plumbing Group is fully licensed (licence number {LIC}) and insured for residential and commercial work.'),
    ('Do you do emergency call outs?', f'Yes, 24/7. Call Lewis on <a href="tel:{TEL}">{PHONE}</a> for burst pipes, blocked drains, hot water failures or gas leaks.'),
    ('How do I get a quote?', f'Use the quote form and attach a link to your plans or photos, or call <a href="tel:{TEL}">{PHONE}</a>. We will come back to you with a clear, itemised price.'),
]

NAV = [('/services', 'Services'), ('/builders', 'For builders'), ('/projects', 'Projects'), ('/about', 'About')]

def head(title, desc, path, extra=''):
    canon = DOMAIN + (path if path != '/' else '/')
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    ga = '' if not GA4 else f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA4}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA4}');</script>"""
    t, d = html.escape(title), html.escape(desc)
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t}</title>
<meta name="description" content="{d}">
{robots}
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#0B384D">
<meta property="og:type" content="website"><meta property="og:site_name" content="LPS Plumbing Group"><meta property="og:locale" content="en_AU">
<meta property="og:url" content="{canon}"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}">
<meta property="og:image" content="{DOMAIN}/lps-share.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{DOMAIN}/lps-share.jpg">
<link rel="icon" type="image/svg+xml" href="{FAV}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,600;1,700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
{ga}
{extra}
<style>
{CSS}
</style>
</head>
<body>
"""

def nav(hold=False):
    h = ''
    if hold:
        h = '''<div class="hold" id="hold" aria-hidden="true"><div class="hold-stack"><div class="hold-mask"><span class="hold-word">LPS<em>.</em>PLUMBING</span></div><div class="hold-track"><div class="hold-fill"></div></div><div class="hold-status">Plumbing · Drainage · Gas</div></div></div>'''
    links = ''.join(f'<a href="{L(p)}">{n}</a>' for p, n in NAV)
    sheet = ''.join(f'<a href="{L(p)}">{n} <i>0{i+1}</i></a>' for i, (p, n) in enumerate(NAV + [('/quote', 'Get a quote')]))
    return h + f'''
<div class="navwrap" id="navwrap">
  <nav class="navbar px" style="padding-left:5px;padding-right:5px">
    <div class="nav-left">
      <a href="{L('/')}" class="nav-chip" aria-label="LPS Plumbing Group home"><img src="{W('logo',400,100)}" alt="LPS Plumbing Group"></a>
      <div class="nav-links">{links}</div>
    </div>
    <div class="nav-right">
      <span class="nav-note">24/7 · Lewis</span>
      {btn('tel:'+TEL, PHONE, 'dark')}
    </div>
    <button class="menu-btn" id="menuBtn" aria-label="Open menu">Menu <span></span></button>
  </nav>
</div>
<div class="sheet-layer" id="sheetLayer">
  <div class="sheet-bd" id="sheetBd"></div>
  <aside class="sheet" role="dialog" aria-label="Menu">
    <div class="sheet-top"><img src="{W('logo',400,100)}" alt="LPS Plumbing Group" style="height:24px;width:auto"><button class="sheet-close" id="sheetClose" aria-label="Close menu">&times;</button></div>
    <nav class="sheet-nav">{sheet}</nav>
    <div class="sheet-foot">{btn('tel:'+TEL, 'Call Lewis: '+PHONE)}</div>
  </aside>
</div>
'''

def phead(crumb, eyebrow, h1, lead, ctas=True):
    c = f'<div class="phead-cta">{btn(L("/quote"), "Get a quote")}{btn("tel:"+TEL, PHONE, "ghost", PHONE_SVG)}</div>' if ctas else ''
    return f'''
<header class="phead">
  <div class="phead-seam"></div>
  <div class="phead-in wrap px">
    <div class="crumb"><a href="{L('/')}">Home</a><span>/</span><span>{crumb}</span></div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {c}
  </div>
</header>'''

def badge(n, lab):
    return f'<div class="badge-row rv"><span class="badge-num">{n}</span><span class="badge-lab">{lab}</span></div>'

def faq_block(n='05'):
    items = ''.join(f'<div class="fq"><button class="fq-q" aria-expanded="false">{q}</button><div class="fq-a"><p>{a}</p></div></div>' for q, a in FAQ)
    return f'''
<section class="sec">
  <div class="wrap px">
    {badge(n, 'Before you call')}
    <div class="rv"><h2 class="big">Common <em>questions.</em></h2></div>
    <div class="faq rv">{items}</div>
  </div>
</section>'''

def quote_form(n='06', heading='Send us the plans.', sub='Builders, send through plans or a scope and we will price the full plumbing package. Homeowners, tell us about the job and we will come back with a clear, itemised quote.'):
    return f'''
<section class="sec sec-dark" id="quote">
  <div class="wrap px">
    {badge(n, 'Get a quote')}
    <div class="rv" style="max-width:60ch">
      <h2 class="big">{heading.split(' ',1)[0]} <em>{heading.split(' ',1)[1]}</em></h2>
      <p class="lead" style="margin-top:16px">{sub}</p>
    </div>
    <div class="contact-grid">
      <div class="cinfo rv">
        <div class="crow"><div class="crow-k">Call Lewis, 24/7</div><div class="crow-v"><a href="tel:{TEL}">{PHONE}</a></div><div class="crow-s">You deal with the director, start to finish.</div></div>
        <div class="crow"><div class="crow-k">Email</div><div class="crow-v" style="font-size:16px"><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
        <div class="crow"><div class="crow-k">Hours</div><div class="crow-v" style="font-size:16px">7am to 7pm, 7 days</div><div class="crow-s">Emergency call outs 24/7.</div></div>
        <div class="crow"><div class="crow-k">Service area</div><div class="crow-v" style="font-size:16px">Shire, Inner South, North Shore &amp; the East</div><div class="crow-s">Miranda, Mascot, Neutral Bay and the Eastern Suburbs.</div></div>
      </div>
      <div class="form-card rv">
        <div class="form-head"><h3>Request a quote</h3><p>Takes a minute. We reply within one business day.</p></div>
        <form id="quoteForm" action="{FORMSPREE}" method="POST" onsubmit="handleSubmit(event)">
          <input type="hidden" name="_subject" value="New quote request: LPS Plumbing Group website">
          <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
          <div class="fgrid two">
            <div class="field"><label for="f-name">Your name *</label><input id="f-name" type="text" name="name" required autocomplete="name"></div>
            <div class="field"><label for="f-phone">Phone *</label><input id="f-phone" type="tel" name="phone" required autocomplete="tel"></div>
          </div>
          <div class="fgrid two" style="margin-top:14px">
            <div class="field"><label for="f-email">Email *</label><input id="f-email" type="email" name="email" required autocomplete="email"></div>
            <div class="field"><label for="f-co">Company <span style="text-transform:none;letter-spacing:0">(builders)</span></label><input id="f-co" type="text" name="company" autocomplete="organization"></div>
          </div>
          <div class="fgrid two" style="margin-top:14px">
            <div class="field"><label for="f-type">I am a *</label><select id="f-type" name="client_type" required><option value="">Select…</option><option>Builder</option><option>Homeowner</option><option>Developer</option><option>Strata or property manager</option><option>Commercial client</option></select></div>
            <div class="field"><label for="f-job">Job type *</label><select id="f-job" name="job_type" required><option value="">Select…</option><option>New build</option><option>Renovation</option><option>Bathroom</option><option>Commercial</option><option>Emergency</option><option>Other</option></select></div>
          </div>
          <div class="fgrid" style="margin-top:14px">
            <div class="field"><label for="f-sub">Site suburb *</label><input id="f-sub" type="text" name="suburb" required></div>
            <div class="field"><label for="f-plans">Link to plans or photos</label><input id="f-plans" type="url" name="plans_link" placeholder="Dropbox, Google Drive or WeTransfer link"><span class="hint">No link? Mention it below and we will send you an email to reply to with attachments.</span></div>
            <div class="field"><label for="f-msg">About the job</label><textarea id="f-msg" name="message" placeholder="Scope, timing, stage of the build…"></textarea></div>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-gold"><span class="roll"><i><b>Send enquiry</b><b>Send enquiry</b></i></span><span class="circ">{ARROW}</span></button>
            <span class="form-note">Licensed &amp; insured · Lic {LIC}</span>
          </div>
          <div id="formStatus" role="status"></div>
        </form>
      </div>
    </div>
  </div>
</section>'''

def band():
    return f'''
<section class="band">
  <div class="wrap px band-in">
    <div class="rv"><h2>Burst pipe or no hot water? <em>Call now.</em></h2><p>24/7 emergency plumbing across the Shire, the inner south, the north shore and the east.</p></div>
    <div class="rv">{btn('tel:'+TEL, PHONE, 'dark')}</div>
  </div>
</section>'''

def foot():
    svc = ''.join(f'<li><a href="{L("/"+s[0])}">{s[1]}</a></li>' for s in SERVICES)
    areas = ''.join(f'<li><a href="{L("/"+a[0])}">{a[1].replace("the ","").title() if a[1].startswith("the") else a[1]}</a></li>' for a in AREAS)
    return f'''
<footer class="foot">
  <div class="wrap px">
    <div class="foot-top" style="grid-template-columns:1.4fr 1fr 1fr 1fr">
      <div>
        <img class="foot-logo" src="{W('logo',600,150)}" alt="LPS Plumbing Group">
        <p>Plumbing, drainage and gas fitting for high end builds, renovations and commercial projects across Sydney.</p>
        <p style="margin-top:12px">Lic {LIC} · ABN {ABN}</p>
      </div>
      <div><h5>Services</h5><ul>{svc}</ul></div>
      <div><h5>Areas</h5><ul>{areas}</ul></div>
      <div><h5>Contact</h5><ul>
        <li><a href="tel:{TEL}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="https://www.instagram.com/{IG}/" target="_blank" rel="noopener">@{IG}</a></li>
        <li><a href="{L('/builders')}">For builders</a></li>
        <li><a href="{L('/privacy')}">Privacy</a></li>
        <li><a href="{L('/terms')}">Terms</a></li>
      </ul></div>
    </div>
    <div class="foot-btm">
      <span>© <span id="yr">2026</span> LPS Plumbing Group · Licensed &amp; insured</span>
      <span>Site by <a href="https://www.latitudemarketing.au/?utm_source=lps-plumbing&utm_medium=referral&utm_campaign=client_credit" target="_blank" rel="noopener">Latitude Marketing</a></span>
    </div>
  </div>
</footer>
<div class="callbar" id="callbar"><a href="tel:{TEL}" class="cb-call">Call Lewis</a><a href="{L('/quote')}" class="cb-quote">Get a quote</a></div>
'''

JS = open(os.path.join(os.path.dirname(__file__), 'site.js')).read()

def tail():
    return f'<script>{JS}</script>\n<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};</script><script defer src="/_vercel/insights/script.js"></script>\n</body>\n</html>\n'

pages = {}

# ---------------- HOME ----------------
schema = {
    "@context": "https://schema.org", "@type": "Plumber", "name": "LPS Plumbing Group",
    "description": "Plumbing, drainage and gas fitting for high end residential builds, renovations, bathrooms and commercial projects across Sydney.",
    "telephone": "+61452611522", "email": EMAIL, "url": DOMAIN, "image": DOMAIN + "/lps-share.jpg",
    "founder": {"@type": "Person", "name": "Lewis Slatter"},
    "address": {"@type": "PostalAddress", "addressRegion": "NSW", "addressCountry": "AU"},
    "areaServed": [{"@type": "Place", "name": n} for n in ["Miranda", "Sutherland Shire", "Mascot", "Neutral Bay", "Eastern Suburbs, Sydney"]],
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "07:00", "closes": "19:00"},
    "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES],
    "sameAs": [f"https://www.instagram.com/{IG}/"],
}
faqschema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(__import__('re').sub('<[^>]+>', '', a))}} for q, a in FAQ]}
ld = f'<script type="application/ld+json">{json.dumps(schema)}</script><script type="application/ld+json">{json.dumps(faqschema)}</script>'

svc_rows = ''.join(f'''<article class="svc-row rv"><span class="svc-n">0{i+1}</span><h3 class="svc-t">{s[1]}</h3><p class="svc-d">{s[3]} <a href="{L('/'+s[0])}" style="color:var(--gold);font-weight:500;white-space:nowrap">Learn more</a></p><div class="svc-img"><img src="{W(s[2],900,560)}" alt="{s[1]} plumbing by LPS Plumbing Group" loading="lazy"></div></article>''' for i, s in enumerate(SERVICES))

home = head('LPS Plumbing Group | Plumber for High End Builds, Sydney',
            'Plumbing, drainage and gas for high end builds, renos and bathrooms across Sydney. Licensed, insured, 24/7. Call Lewis on 0452 611 522.', '/', ld) + nav(True) + f'''
<header class="hero">
  <img class="hero-video" src="{W('vanity',2000,1400)}" alt="Bathroom vanity with brushed brass tapware plumbed by LPS Plumbing Group" fetchpriority="high">
  <div class="hero-shade"></div><div class="hero-seam"></div>
  <div class="hero-inner wrap px">
    <p class="hero-label">Plumbing · Drainage · Gas fitting · Sydney</p>
    <h1><span class="ln"><span>Plumbing for</span></span><span class="ln"><span>builds where the</span></span><span class="ln"><span><em>finish matters.</em></span></span></h1>
    <div class="hero-cta">
      {btn(L('/quote'), 'Send us your plans')}
      {btn('tel:'+TEL, PHONE, 'ghost', PHONE_SVG)}
      <div class="hero-badge"><b>Licensed &amp; insured</b><i>24/7</i></div>
    </div>
  </div>
</header>
<section class="ledger" aria-label="Key facts">
  <div class="ledger-in wrap">
    <div class="lcell"><span class="lnum">8+</span><span class="llab">Years in the trade</span></div>
    <div class="lcell"><span class="lnum">24/7</span><span class="llab">Emergency call outs</span></div>
    <div class="lcell"><span class="lnum">1</span><span class="llab">Point of contact, the director</span></div>
    <div class="lcell"><span class="lnum">{LIC}</span><span class="llab">Licensed &amp; insured</span></div>
  </div>
</section>
<section class="sec">
  <div class="wrap px">
    {badge('01', 'Built for builders')}
    <div class="about-grid">
      <div class="rv"><h2 class="big">The plumber high end builders <em>keep on speed dial.</em></h2></div>
      <div class="rv">
        <p class="lead">LPS Plumbing Group specialises in high end residential builds, renovations and commercial projects. We are a small, tight crew led by director Lewis Slatter, with over 8 years in the trade and a reputation for detail that holds up after handover.</p>
        <div class="pillars">
          <div class="pillar"><span class="pillar-k">A</span><div><h4>Work to your program</h4><p>Rough in and fit off when the schedule says, so the next trade is never waiting on us.</p></div></div>
          <div class="pillar"><span class="pillar-k">B</span><div><h4>Finished like it is our own home</h4><p>Level mixers, tidy set outs and premium fixtures installed right the first time.</p></div></div>
          <div class="pillar"><span class="pillar-k">C</span><div><h4>Straight communication</h4><p>You deal with Lewis directly. Clear quotes, clear updates, no chasing.</p></div></div>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="sec sec-dark">
  <div class="wrap px">
    {badge('02', 'What we do')}
    <div class="rv" style="display:flex;flex-wrap:wrap;gap:24px;justify-content:space-between;align-items:flex-end">
      <h2 class="big">Plumbing, drainage and gas, <em>done properly.</em></h2>
      <p class="lead" style="max-width:38ch">From the first stormwater pit to the last tap. Same crew, same standard, start to finish.</p>
    </div>
    <div class="svc">{svc_rows}</div>
  </div>
</section>
<section class="sec sec-cream2">
  <div class="wrap px">
    {badge('03', 'Recent work')}
    <div class="rv" style="display:flex;flex-wrap:wrap;gap:24px;justify-content:space-between;align-items:flex-end">
      <h2 class="big">The work <em>speaks for itself.</em></h2>
      {btn(L('/projects'), 'See projects', 'dark')}
    </div>
    <div class="gal">
      <figure class="rv"><img src="{W('miranda',600,800)}" alt="Ensuite renovation in Miranda" loading="lazy"></figure>
      <figure class="rv"><img src="{W('shower',600,800)}" alt="Copper outdoor shower installation" loading="lazy"></figure>
      <figure class="rv"><img src="{W('basin',600,800)}" alt="Vessel basin with brushed brass wall mixer" loading="lazy"></figure>
      <figure class="rv"><img src="{W('commercial',600,800)}" alt="Commercial stack and riser installation" loading="lazy"></figure>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap px">
    {badge('04', 'Where we work')}
    <div class="rv"><h2 class="big">Sydney's best suburbs, <em>covered.</em></h2></div>
    <p class="lead rv" style="margin-top:16px">Based in the Sutherland Shire, working across Sydney wherever quality builds are happening.</p>
    <div class="chips rv">{''.join(f'<a href="{L("/"+a[0])}">{a[1][0].upper()+a[1][1:]}</a>' for a in AREAS)}</div>
  </div>
</section>
{faq_block('05')}
{quote_form('06')}
{band()}''' + foot() + tail()
pages['index.html'] = home

# ---------------- SERVICES HUB ----------------
blocks = ''.join(f'''<div class="sblock rv{' flip' if i%2 else ''}"><span class="sb-n">0{i+1}</span><div class="sb-body"><h3>{s[1]}</h3><p>{s[4]}</p><ul class="sb-list">{''.join(f'<li>{x}</li>' for x in s[5])}</ul><div style="margin-top:22px">{btn(L('/'+s[0]), 'More on '+s[1].lower(), 'dark')}</div></div><div class="sb-media"><img src="{W(s[2],1000,750)}" alt="{s[1]} by LPS Plumbing Group" loading="lazy"></div></div>''' for i, s in enumerate(SERVICES))
pages['services.html'] = head('Plumbing Services | LPS Plumbing Group, Sydney',
    'New builds, renovations, bathrooms, commercial and 24/7 emergency plumbing across Sydney. Licensed and insured. Call 0452 611 522.', '/services') + nav() + phead('Services', 'Services', 'Everything in the wall, <em>done right.</em>', 'Plumbing, drainage and gas fitting for builders, developers and homeowners who want it done once, properly.') + f'''
<section class="sec"><div class="wrap px">{badge('01','What we do')}<div class="sblocks">{blocks}</div></div></section>
{quote_form('02')}''' + foot() + tail()

# ---------------- SERVICE PAGES ----------------
for i, s in enumerate(SERVICES):
    slug, name, img, short, long, bullets = s
    others = ''.join(f'<a href="{L("/"+o[0])}">{o[1]}</a>' for o in SERVICES if o[0] != slug)
    h1 = f'{name} plumbing, <em>done properly.</em>' if slug != 'emergency' else 'Emergency plumber, <em>24/7.</em>'
    title = f'{name} Plumbing Sydney | LPS Plumbing Group' if slug != 'emergency' else 'Emergency Plumber Sydney, 24/7 | LPS Plumbing Group'
    desc = f'{short} Licensed and insured plumber across Sydney. Call Lewis on 0452 611 522.'
    if len(desc) > 158: desc = f'{short} Call Lewis on 0452 611 522.'
    pages[f'{slug}.html'] = head(title, desc, '/' + slug) + nav() + phead(name, 'Services', h1, short) + f'''
<section class="sec"><div class="wrap px">
  {badge('01', name)}
  <div class="sblocks"><div class="sblock rv"><span class="sb-n">01</span><div class="sb-body"><h3>What you get</h3><p>{long}</p><ul class="sb-list">{''.join(f'<li>{x}</li>' for x in bullets)}</ul></div><div class="sb-media"><img src="{W(img,1000,750)}" alt="{name} plumbing by LPS Plumbing Group" loading="lazy"></div></div></div>
  <div class="rv" style="margin-top:40px"><span class="badge-lab">Other services</span><div class="chips">{others}</div></div>
</div></section>
{faq_block('02')}
{quote_form('03')}''' + (band() if slug == 'emergency' else '') + foot() + tail()

# ---------------- AREA PAGES ----------------
for a in AREAS:
    slug, place, region, img, blurb, subs = a
    P = place[0].upper() + place[1:]
    title = f'Plumber {P.replace("The ","")} | LPS Plumbing Group'
    desc = f'Licensed plumber for new builds, renovations and bathrooms in {place}. Working with builders and homeowners. Call Lewis on 0452 611 522.'
    svc = ''.join(f'<a href="{L("/"+s[0])}">{s[1]}</a>' for s in SERVICES)
    pages[f'{slug}.html'] = head(title, desc, '/' + slug) + nav() + phead(f'{region}', region, f'Plumber in {place}, <em>for builds done right.</em>', blurb) + f'''
<section class="sec"><div class="wrap px">
  {badge('01', f'Plumbing in {place}')}
  <div class="sblocks"><div class="sblock rv"><span class="sb-n">01</span><div class="sb-body"><h3>Builders and homeowners in {place}</h3><p>Whether it is a new build, a renovation or a bathroom, you get the same crew and the same standard. We price from your plans, work to your program and hand over with all the paperwork sorted.</p><ul class="sb-list"><li>New builds and knockdown rebuilds</li><li>Renovations and bathrooms</li><li>Gas fitting, drainage and hot water</li><li>24/7 emergency call outs</li></ul></div><div class="sb-media"><img src="{W(img,1000,750)}" alt="Plumbing work by LPS Plumbing Group in {place}" loading="lazy"></div></div></div>
  <div class="rv" style="margin-top:40px"><span class="badge-lab">Suburbs we cover nearby</span><div class="chips">{''.join(f'<span>{x}</span>' for x in subs)}</div></div>
  <div class="rv" style="margin-top:30px"><span class="badge-lab">Services</span><div class="chips">{svc}</div></div>
</div></section>
{quote_form('02')}''' + foot() + tail()

# ---------------- BUILDERS ----------------
pages['builders.html'] = head('Plumber for Builders, Sydney | LPS Plumbing Group',
    'A plumbing partner for high end builders in Sydney. Priced from your plans, delivered to program. Send plans or call Lewis on 0452 611 522.', '/builders') + nav() + phead('For builders', 'For builders', 'A plumber that <em>keeps your program moving.</em>', 'We partner with builders on high end homes, renovations and multi unit projects. Send through plans and we will price the full plumbing scope.') + f'''
<section class="sec"><div class="wrap px">
  {badge('01', 'How we work with builders')}
  <div class="track">
    <div class="tstep rv"><span class="tstep-n">01</span><h4>Send plans</h4><p>Drop a link to your plans in the form below.</p></div>
    <div class="tstep rv"><span class="tstep-n">02</span><h4>Itemised price</h4><p>A clear quote for the full plumbing scope.</p></div>
    <div class="tstep rv"><span class="tstep-n">03</span><h4>Rough in</h4><p>Drainage, rough in and testing to program.</p></div>
    <div class="tstep rv"><span class="tstep-n">04</span><h4>Fit off</h4><p>Premium fixtures installed and checked.</p></div>
    <div class="tstep rv"><span class="tstep-n">05</span><h4>Handover</h4><p>Compliance and certificates sorted.</p></div>
  </div>
</div></section>
<section class="sec sec-dark"><div class="wrap px">
  {badge('02', 'Why builders use LPS')}
  <div class="vrows">
    <div class="vrow rv"><span class="vrow-n">01</span><h4>Director on every job</h4><p>Lewis runs every project. You are never passed to a call centre or a different crew halfway through.</p></div>
    <div class="vrow rv"><span class="vrow-n">02</span><h4>Detail that survives handover</h4><p>Set outs your tiler will thank you for and fixtures that go in level the first time.</p></div>
    <div class="vrow rv"><span class="vrow-n">03</span><h4>Capacity for volume</h4><p>We are growing the crew to take on more builds, and we only take on what we can deliver properly.</p></div>
  </div>
</div></section>
{quote_form('03', 'Send the plans.', 'Attach a link to your plans or scope and we will come back with a full plumbing price.')}''' + foot() + tail()

# ---------------- QUOTE ----------------
pages['quote.html'] = head('Get a Plumbing Quote | LPS Plumbing Group',
    'Request a quote from LPS Plumbing Group. Send plans or photos and get a clear, itemised price. Or call Lewis on 0452 611 522.', '/quote') + nav() + phead('Get a quote', 'Get a quote', 'Tell us about <em>the job.</em>', 'Builders, homeowners and developers. Send the details and we reply within one business day.', False) + quote_form('01') + foot() + tail()

# ---------------- PROJECTS ----------------
projs = [('miranda', 'Bathroom', 'Ensuite renovation, Miranda', 'Wall hung vanity, concealed cistern and recessed shelving, set out for a clean tiled finish.'),
         ('shower', 'Outdoor', 'Copper outdoor shower', 'Exposed copper run with brass fittings, mounted against a feature cladding wall.'),
         ('kitchen', 'New build', 'Open plan kitchen, new build', 'Island sink, dishwasher and fridge services run through the slab for a clean, open layout.'),
         ('commercial', 'Commercial', 'Stack and riser install', 'Multi level stack, vent and water services installed and tested ahead of fit out.'),
         ('basin', 'Renovation', 'Brushed brass wall mixer', 'In wall mixer set dead level over a timber top vessel basin.'),
         ('hotwater', 'Hot water', 'Hot water replacement', 'Electric storage system replaced with tidy copper connections and a new tempering valve.')]
cards = ''.join(f'<article class="pcard rv"><div class="pcard-img"><img src="{W(i,1000,625)}" alt="{t}" loading="lazy"></div><div class="pcard-b"><span class="pcard-k">{k}</span><h3>{t}</h3><p>{d}</p></div></article>' for i, k, t, d in projs)
pages['projects.html'] = head('Plumbing Projects | LPS Plumbing Group, Sydney',
    'Recent new builds, renovations, bathrooms and commercial plumbing projects by LPS Plumbing Group across Sydney.', '/projects') + nav() + phead('Projects', 'Projects', 'Recent <em>work.</em>', 'A look at recent builds, renovations and bathrooms we have plumbed.') + f'''
<section class="sec"><div class="wrap px">{badge('01','Projects')}<div class="pgrid">{cards}</div></div></section>
{quote_form('02')}''' + foot() + tail()

# ---------------- ABOUT ----------------
pages['about.html'] = head('About LPS Plumbing Group | Lewis Slatter, Director',
    'LPS Plumbing Group is led by director Lewis Slatter, with 8+ years plumbing high end homes across Sydney. Licensed and insured.', '/about') + nav() + phead('About', 'About', 'Small crew. <em>High standards.</em>', 'LPS Plumbing Group is a licensed plumbing, drainage and gas fitting business led by director Lewis Slatter.') + f'''
<section class="sec"><div class="wrap px">
  {badge('01','Our story')}
  <div class="about-grid">
    <div class="rv"><h2 class="big">Built on <em>doing it once, properly.</em></h2></div>
    <div class="rv"><p class="lead">With over 8 years in the trade, Lewis started LPS to deliver the kind of plumbing he would want in his own home. The focus is high end residential builds and renovations, where the detail is on show and the standard can't slip.</p>
    <p class="lead" style="margin-top:16px">The market is full of cheap plumbing. We are not trying to be the cheapest. We are trying to be the plumber you never have to call back.</p>
    <div class="creds"><div class="cred"><span class="cred-k">Licence</span><span class="cred-v">{LIC}</span></div><div class="cred"><span class="cred-k">Experience</span><span class="cred-v">8+ years</span></div><div class="cred"><span class="cred-k">Emergency</span><span class="cred-v">24/7</span></div></div></div>
  </div>
</div></section>
{quote_form('02')}''' + foot() + tail()

# ---------------- LEGAL ----------------
def legal(slug, title, h1, body):
    return head(f'{title} | LPS Plumbing Group', f'{title} for the LPS Plumbing Group website.', '/' + slug) + nav() + phead(title, 'Legal', h1, 'Last updated November 2026.', False) + f'<section class="sec"><div class="wrap px"><div class="prose">{body}</div></div></section>' + foot() + tail()

pages['privacy.html'] = legal('privacy', 'Privacy Policy', 'Privacy <em>policy.</em>', f'''
<h2>Who we are</h2><p>LPS Plumbing Group (ABN {ABN}) provides plumbing, drainage and gas fitting services in New South Wales. This policy explains how we handle personal information under the Privacy Act 1988 (Cth) and the Australian Privacy Principles.</p>
<h2>What we collect</h2><p>When you contact us or request a quote we collect your name, phone number, email address, company, site suburb, details about your job and any links to plans or photos you provide.</p>
<h2>How we use it</h2><ul><li>To respond to your enquiry and prepare a quote</li><li>To carry out and manage work you engage us for</li><li>To meet our legal, licensing and insurance obligations</li></ul>
<h2>Analytics</h2><p>Our website uses analytics tools such as Google Analytics and Vercel Analytics to understand how visitors use the site. These tools may use cookies and collect information such as pages visited and device type. They do not identify you personally.</p>
<h2>Disclosure</h2><p>We do not sell your information. We may share it with service providers who help us run the business, such as our form and email providers, and where required by law.</p>
<h2>Access and correction</h2><p>You can ask to access or correct the information we hold about you by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>Questions or complaints about privacy can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a> or by calling <a href="tel:{TEL}">{PHONE}</a>.</p>''')

pages['terms.html'] = legal('terms', 'Terms and Conditions', 'Terms and <em>conditions.</em>', f'''
<h2>About these terms</h2><p>These terms apply to your use of this website, operated by LPS Plumbing Group (ABN {ABN}). By using the site you agree to them.</p>
<h2>Website content</h2><p>Information on this site is general in nature. It does not form a quote or contract. Any work we carry out is subject to a written quote and the terms set out in that quote.</p>
<h2>Quotes</h2><p>Quotes are based on the information and plans provided. Prices may change if the scope changes or if site conditions differ from what was supplied.</p>
<h2>Intellectual property</h2><p>All content on this site, including text, photos and logos, belongs to LPS Plumbing Group and may not be reused without permission.</p>
<h2>Liability</h2><p>To the extent permitted by law, we are not liable for any loss arising from use of this website. Nothing in these terms limits your rights under the Australian Consumer Law.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of New South Wales.</p>
<h2>Contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:{TEL}">{PHONE}</a> · Licence {LIC}</p>''')

pages['thank-you.html'] = head('Thanks | LPS Plumbing Group', 'Thanks for your enquiry.', '/thank-you', '<meta name="robots" content="noindex">') + nav() + phead('Thanks', 'Enquiry sent', 'Thanks, <em>got it.</em>', 'Lewis will be in touch within one business day. For anything urgent call 0452 611 522.', False) + foot() + tail()

pages['404.html'] = head('Page not found | LPS Plumbing Group', 'Page not found.', '/404', '<meta name="robots" content="noindex">') + nav() + phead('404', 'Page not found', 'This page <em>does not exist.</em>', 'Head back home or call Lewis on 0452 611 522.', True) + foot() + tail()

os.makedirs(OUT, exist_ok=True)
for f, c in pages.items():
    open(os.path.join(OUT, f), 'w').write(c)

indexable = [p for p in pages if p not in ('thank-you.html', '404.html')]
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{"" if p=="index.html" else p[:-5]}</loc></url>\n' for p in indexable) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
if not BASE:
    open(os.path.join(OUT, 'vercel.json'), 'w').write(json.dumps({"cleanUrls": True, "trailingSlash": False}, indent=2))
print(len(pages), 'pages')

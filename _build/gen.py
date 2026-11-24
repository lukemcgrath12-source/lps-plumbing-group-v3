#!/usr/bin/env python3
"""LPS Plumbing Group site generator (Latitude SAL template, LPS palette)."""
import os, sys, json, html

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
BASE = sys.argv[2] if len(sys.argv) > 2 else ''          # '' at launch, '/preview/lps-plumbing-group' for preview
NOINDEX = BASE != ''
DOMAIN = 'https://www.lpsplumbinggroup.com.au'
# Share image host. Points at the preview until the site moves to DOMAIN, then set back to DOMAIN.
SHARE_HOST = 'https://lps.latitudemarketing.au'
PHONE, TEL, EMAIL = '0452 611 522', '0452611522', 'info@lpsplumbinggroup.com'
LIC, ABN = '476073C', '34 280 954 515'
FORMSPREE = 'https://formspree.io/f/mjglroqj'          # TODO at launch: LPS's own Formspree form
WEB3FORMS_KEY = 'd44920a8-4453-4b3d-bce7-b9d6ed9b8726'                                        # LPS access key from web3forms.com (sent to info@lpsplumbinggroup.com). When set, the quote form posts to Web3Forms.
GA4 = ''                                                  # TODO at launch: LPS GA4 ID
IG = 'lpsplumbinggroup'
META_PIXEL = ''                                           # TODO at launch: Meta Pixel ID
GADS = ''                                                 # TODO at launch: Google Ads ID (AW-XXXXXXXXX)
WA = '61452611522'
LIC_CHECK = 'https://www.service.nsw.gov.au/transaction/check-builder-or-tradespersons-licence'
INSURANCE_PDF = ''                                        # TODO: certificate of currency file from Lewis
# Filled from Lewis. Sections stay hidden while these are empty.
BUILDERS = []   # [('Builder name', 'logo-file.png' or '', 'One line quote or empty', 'Person, Role')]
REVIEWS = [     # real Google reviews only, copied from LPS's Google Business Profile (Nov 2026)
    ('John M.', 'LPS Plumbing did a great job at our home. Connected hot &amp; cold pipes to rear property. Connected new shower mixer, bath vanity, kitchen sink, outdoor bath and gave great advice repositioning washer dryer with lots of savings. Thankyou Lewis'),
    ('Sophie D.', 'Very happy with the service. Had a bayonet fitting installed and the work was completed professionally and efficiently. Great communication, arrived on time, and left everything tidy. Would definitely recommend and use again.'),
    ('Anton L.', 'Big shoutout to Lewis, he\u2019s come through a couple times now when our shop has had issues, handled with professionalism and been great to deal with throughout. Will definitely be in contact again in future when needed!'),
]
CASES = []      # [{'img':'key','title':'','suburb':'','builder':'','scope':'','result':''}]
CSS = open(os.path.join(os.path.dirname(__file__), 'base.css')).read() + open(os.path.join(os.path.dirname(__file__), 'extras.css')).read()

LOCAL = {
    'kitchen': 'lps-new-build-kitchen.jpg', 'vanity': 'lps-brass-kitchen-mixer.jpg', 'ensuite': 'lps-ensuite-brass-fit-off.jpg',
    'shower': 'lps-walk-in-shower.jpg', 'hotwater': 'lps-hot-water-heat-pump.jpg', 'commercial': 'lps-commercial-pipework.jpg',
    'basin': 'lps-brass-wall-spout-basin.jpg', 'miranda': 'lps-terracotta-powder-room.jpg', 'sink': 'lps-brass-sink-mixer.jpg',
    'stone': 'lps-brass-mixer-stone.jpg', 'stonevanity': 'lps-stone-vanity-wall-mixer.jpg', 'gooseneck': 'lps-kitchen-gooseneck.jpg',
    'laundry': 'lps-laundry-fit-off.jpg', 'bathreno': 'lps-bathroom-renovation.jpg', 'kitchensink': 'lps-kitchen-sink-fit-off.jpg',
}

def W(i, w=1600, h=1200):
    if i in LOCAL:   # LPS's own job photos, hosted in /img
        return f'{BASE}/img/{LOCAL[i]}'
    ids = {
        'logo': '84f08c_9dd65380a4c24c1b927187305cc5b8ae~mv2.png',
    }
    f = ids[i]
    return f'https://static.wixstatic.com/media/{f}/v1/fit/w_{w},h_{h},q_95/lps.png'

def L(path):  # internal link
    return BASE + path if path != '/' else (BASE + '/' if BASE else '/')

ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
PHONE_SVG = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'

def btn(href, label, kind='gold', icon=ARROW):
    kind = 'gold' if kind == 'teal' else kind
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
    ('plumber-st-george', 'St George', 'St George', 'vanity',
     'Just over the river from our Shire base. Renovations, bathrooms and new builds across Kogarah, Hurstville and the bayside suburbs.',
     ['Kogarah', 'Hurstville', 'Sans Souci', 'Ramsgate', 'Rockdale', 'Kingsgrove']),
    ('plumber-inner-west', 'the Inner West', 'Inner West', 'kitchen',
     'Terraces, semis and full renovations across the Inner West, where older pipework and tight sites need a plumber who plans ahead.',
     ['Newtown', 'Marrickville', 'Leichhardt', 'Balmain', 'Annandale', 'Summer Hill']),
    ('plumber-northern-beaches', 'the Northern Beaches', 'Northern Beaches', 'ensuite',
     'High end homes and coastal renovations from Manly to Avalon, with fixtures and finishes that need to hold up near the water.',
     ['Manly', 'Dee Why', 'Freshwater', 'Narrabeen', 'Mona Vale', 'Avalon']),
    ('plumber-wollongong', 'Wollongong', 'Illawarra', 'hotwater',
     'New builds, renovations and bathrooms across Wollongong and the northern Illawarra, an easy run down from the Shire.',
     ['Wollongong', 'Thirroul', 'Bulli', 'Corrimal', 'Fairy Meadow', 'Figtree']),
    ('plumber-shellharbour-kiama', 'Shellharbour and Kiama', 'South Coast', 'miranda',
     'Plumbing for the growing South Coast, from new estates at Shell Cove to coastal homes in Kiama and Gerringong.',
     ['Shellharbour', 'Shell Cove', 'Albion Park', 'Kiama', 'Gerringong', 'Lake Illawarra']),
]

FAQ = [
    ('Do you work directly with builders?', 'Yes. Most of our work comes through builders on new builds and renovations. Send your plans through the quote form and we will price the full plumbing scope, then work to your program.'),
    ('What areas do you cover?', 'We are based in the Sutherland Shire and work right across Sydney, from the Shire and St George to the Inner West, the Eastern Suburbs, the North Shore and the Northern Beaches. We also cover the South Coast, including Wollongong, Shellharbour and Kiama.'),
    ('Are you licensed and insured?', f'Yes. LPS Plumbing Group is fully licensed (licence number {LIC}) and insured for residential and commercial work.'),
    ('Do you do emergency call outs?', f'Yes, 24/7. Call Lewis on <a href="tel:{TEL}">{PHONE}</a> for burst pipes, blocked drains, hot water failures or gas leaks.'),
    ('How do I get a quote?', f'Use the quote form and attach a link to your plans or photos, or call <a href="tel:{TEL}">{PHONE}</a>. We will come back to you with a clear, itemised price.'),
]


SFAQ = {
  'new-builds': [
    ('Can you price from architectural plans?', 'Yes. Send the architectural or hydraulic plans and your fixture selections and we will price the full plumbing scope, from drainage to fit off.'),
    ('When do you need to be on site?', 'Usually for stormwater and sewer before the slab, rough in once the frame is up, and fit off after tiling and joinery. We line up with your program at each stage.'),
    ('Do you handle the compliance paperwork?', 'Yes. We lodge the required notices and hand over compliance certificates at completion, so your certifier has what they need.'),
  ],
  'renovations': [
    ('Can you move a kitchen or laundry?', 'Usually, yes. We check the existing drainage and falls first, then plan the new runs so the layout works without surprises later.'),
    ('Do you work with my builder?', 'Yes. Most of our renovation work is through builders. We coordinate with the other trades so walls close on time.'),
    ('Can you re-pipe an older home?', 'Yes. Old galvanised and copper lines can be replaced during a renovation while the walls are open.'),
  ],
  'bathrooms': [
    ('Can you install in wall mixers and concealed cisterns?', 'Yes. These are a big part of our bathroom work. We set them out to your tiler so everything lines up on the finished wall.'),
    ('Do you work with the tiler and waterproofer?', 'Yes. Getting the order right between plumbing, waterproofing and tiling is what makes the finish come up clean.'),
    ('Do you install freestanding baths?', 'Yes, including floor wastes and floor mounted or wall mounted bath fillers.'),
  ],
  'commercial': [
    ('What commercial work do you take on?', 'Multi unit and townhouse developments, commercial fit outs and stack and riser installs. Send the scope and we will let you know quickly if it is a fit.'),
    ('Can you work to a site program?', 'Yes. We work with site managers to hit each stage on time, with documented testing along the way.'),
    ('Do you provide test results and sign off?', 'Yes. Testing is documented and compliance paperwork is handed over at completion.'),
  ],
  'emergency': [
    ('Do you really answer after hours?', f'Yes. Call {PHONE} any time, 24/7. If we miss you, we call straight back.'),
    ('What should I do while I wait?', 'Turn off the water at the main, usually near the front boundary or water meter. For a gas smell, leave the area, do not use switches and call us from outside.'),
    ('What areas do you cover for emergencies?', 'All of Sydney and down the South Coast to Wollongong, Shellharbour and Kiama. Call and we will tell you straight how quickly we can get there.'),
  ],
}

NAV = [('/services', 'Services'), ('/builders', 'For builders'), ('/projects', 'Projects'), ('/about', 'About'), ('/careers', 'Careers')]

def head(title, desc, path, extra=''):
    canon = DOMAIN + (path if path != '/' else '/')
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    tag = GA4 or GADS
    ga = '' if not tag else f"""<script async src="https://www.googletagmanager.com/gtag/js?id={tag}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());{f"gtag('config','{GA4}');" if GA4 else ''}{f"gtag('config','{GADS}');" if GADS else ''}</script>"""
    if META_PIXEL:
        ga += f"""<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','{META_PIXEL}');fbq('track','PageView');</script>"""
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
<meta property="og:image" content="{SHARE_HOST}/lps-share.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{SHARE_HOST}/lps-share.jpg">
<link rel="icon" type="image/png" sizes="32x32" href="{BASE}/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="{BASE}/favicon-16x16.png"><link rel="icon" href="{BASE}/favicon.ico" sizes="any"><link rel="apple-touch-icon" sizes="180x180" href="{BASE}/apple-touch-icon.png"><link rel="manifest" href="{BASE}/site.webmanifest">
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
        h = '<div class="hold" id="hold" aria-hidden="true"><div class="hold-stack"><div class="hold-mask"><span class="hold-word">LPS<em>.</em>PLUMBING</span></div><div class="hold-track"><div class="hold-fill"></div></div><div class="hold-status">Sydney · Plumbing · Drainage · Gas</div></div></div>'
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
    <h1 class="rv">{h1}</h1>
    <p class="lead rv">{lead}</p>
    {c}
  </div>
</header>'''

def hidden(subject):
    if WEB3FORMS_KEY:
        return f'<input type="hidden" name="access_key" value="{WEB3FORMS_KEY}"><input type="hidden" name="subject" value="{subject}"><input type="hidden" name="from_name" value="LPS Plumbing Group website"><input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">'
    return f'<input type="hidden" name="_subject" value="{subject}"><input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">'

def form_action():
    return 'https://api.web3forms.com/submit' if WEB3FORMS_KEY else FORMSPREE

def field(label, inner):
    return f'<div class="field"><label>{label}</label>{inner}</div>'

def badge(n, lab):
    return f'<div class="badge-row rv"><span class="badge-num">{n}</span><span class="badge-lab">{lab}</span></div>'

def faq_ld(faqs):
    import re as _re
    return '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":_re.sub('<[^>]+>','',a)}} for q,a in faqs]}) + '</script>'

def faq_block(n='05', faqs=None):
    items = ''.join(f'<div class="fq"><button class="fq-q" aria-expanded="false">{q}</button><div class="fq-a"><p>{a}</p></div></div>' for q, a in (faqs or FAQ))
    return f'''
<section class="sec">
  <div class="wrap px">
    {badge(n, 'Before you call')}
    <div class="rv"><h2 class="big">Common <em>questions.</em></h2></div>
    <div class="faq rv">{items}</div>
  </div>
</section>'''

def quote_form(n='06', heading='Send us the plans.', sub='Builders, send through plans or a scope and we will price the full plumbing package. Homeowners, tell us about the job and we will come back with a clear, itemised quote.'):
    w = heading.split(' '); h1, h2 = ' '.join(w[:-2]), ' '.join(w[-2:])
    sel = lambda nm, opts: f'<select name="{nm}" required><option value="">Select</option>' + ''.join(f'<option>{o}</option>' for o in opts) + '</select>'
    return f'''
<section class="sec sec-dark" id="quote">
  <div class="wrap px">
    {badge(n, 'Get a quote')}
    <div class="rv" style="max-width:60ch">
      <h2 class="big">{h1} <em>{h2}</em></h2>
      <p class="lead" style="margin-top:16px">{sub}</p>
    </div>
    <div class="contact-grid">
      <div class="cinfo rv">
        <div class="crow"><div class="crow-k">Call Lewis, 24/7</div><div class="crow-v"><a href="tel:{TEL}">{PHONE}</a></div><div class="crow-s">Text or <a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a> works too.</div></div>
        <div class="crow"><div class="crow-k">Email</div><div class="crow-v" style="font-size:16px"><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
        <div class="crow"><div class="crow-k">Service area</div><div class="crow-v" style="font-size:16px">Sydney &amp; the South Coast</div><div class="crow-s">Based in the Sutherland Shire. Hours 7am to 7pm, 7 days, plus 24/7 emergencies.</div></div>
      </div>
      <div class="form-card rv">
        <div class="form-head"><h3>Request a quote</h3><p>We reply within one business day with a clear, itemised price.</p></div>
        <form id="quoteForm" action="{form_action()}" method="POST" onsubmit="handleSubmit(event)">
          {hidden('New quote request: LPS Plumbing Group website')}
          <div class="fgrid two">{field('Name or company *', '<input type="text" name="name" required autocomplete="name">')}{field('Phone *', '<input type="tel" name="phone" required autocomplete="tel">')}</div>
          <div class="fgrid two" style="margin-top:14px">{field('Email *', '<input type="email" name="email" required autocomplete="email">')}{field('Site suburb *', '<input type="text" name="suburb" required>')}</div>
          <div class="fgrid two" style="margin-top:14px">{field('I am a *', sel('client_type', ['Builder','Homeowner','Developer','Strata or property manager','Commercial client']))}{field('Job type *', sel('job_type', ['New build','Renovation','Bathroom','Commercial','Emergency','Other']))}</div>
          <div class="fgrid" style="margin-top:14px">{field('Link to plans or photos (optional)', '<input type="url" name="plans_link" placeholder="Dropbox, Google Drive or WeTransfer">')}{field('About the job', '<textarea name="message" placeholder="Scope, timing, stage of the build"></textarea>')}</div>
          <div class="form-actions">{btn_submit('Send enquiry')}<span class="form-note">Licensed &amp; insured · Lic {LIC}</span></div>
          <div id="formStatus" role="status"></div>
        </form>
      </div>
    </div>
  </div>
</section>'''

def btn_submit(label):
    return f'<button type="submit" class="btn btn-gold"><span class="roll"><i><b>{label}</b><b>{label}</b></i></span><span class="circ">{ARROW}</span></button>'


def creds_block(n='05', dark=False):
    ins = f'<a href="{L("/"+INSURANCE_PDF)}" target="_blank" rel="noopener">Download certificate</a>' if INSURANCE_PDF else 'Certificate of currency on request.'
    items = [('NSW contractor licence', f'Lic {LIC}. <a href="{LIC_CHECK}" target="_blank" rel="noopener">Verify on Service NSW</a>.'),
             ('Fully insured', ins), ('Certificates on every job', 'Compliance paperwork lodged and handed over at completion.'),
             ('Director on every job', 'Lewis Slatter, 8+ years in the trade.')]
    pil = ''.join(f'<div class="pillar"><span class="pillar-k">{"ABCD"[i]}</span><div><h4>{t}</h4><p>{d}</p></div></div>' for i, (t, d) in enumerate(items))
    return f'''
<section class="sec sec-cream2">
  <div class="wrap px">
    {badge(n, 'Licensed and accountable')}
    <div class="about-grid">
      <div class="rv"><h2 class="big">Check us out <em>before you book.</em></h2></div>
      <div class="rv"><div class="pillars">{pil}</div></div>
    </div>
  </div>
</section>'''

def builders_block(n='04'):
    if not BUILDERS:
        return ''
    logos = ''.join((f'<img src="{L("/"+lg)}" alt="{nm}" loading="lazy">' if lg else f'<span>{nm}</span>') for nm, lg, q, who in BUILDERS)
    quotes = ''.join(f'<figure class="bq rv"><blockquote>{q}</blockquote><figcaption><b>{who}</b><span>{nm}</span></figcaption></figure>' for nm, lg, q, who in BUILDERS if q)
    return f'''
<section class="bstrip">
  <div class="wrap px">
    {badge(n, 'Trusted by builders')}
    <div class="bl rv">{logos}</div>
    {f'<div class="bqs">{quotes}</div>' if quotes else ''}
  </div>
</section>'''

def reviews_block(n='04'):
    if not REVIEWS:
        return ''
    q = ''.join(f'<blockquote class="quote rv"><span class="quote-mk">0{i+1}</span><p>{t}</p><cite>{nm}<span>Google review</span></cite></blockquote>' for i, (nm, t) in enumerate(REVIEWS))
    return f'''
<section class="sec sec-cream2">
  <div class="wrap px">
    {badge(n, 'Rated 5.0 on Google')}
    <div class="rv"><h2 class="big">Real jobs. <em>Real reviews.</em></h2></div>
    <div class="rev">{q}</div>
  </div>
</section>'''

def ig_block(n='07'):
    pics = ''.join(f'<a class="igp rv" href="https://www.instagram.com/{IG}/" target="_blank" rel="noopener" aria-label="LPS Plumbing Group on Instagram"><img src="{W(k,600,600)}" alt="{a}" loading="lazy"></a>' for k, a in [('basin','Brushed brass wall mixer'),('shower','Copper outdoor shower'),('ensuite','Ensuite fit off'),('commercial','Commercial stack install')])
    return f'''
<section class="igs">
  <div class="wrap px">
    <div class="igs-h">
      <div>{badge(n, 'On the tools')}<h2 class="big rv">Follow the work <em>@{IG}</em></h2></div>
      {btn('https://www.instagram.com/'+IG+'/', 'Follow on Instagram', 'teal')}
    </div>
    <div class="igg">{pics}</div>
  </div>
</section>'''

def checklist_cta():
    return f'''
<section class="sec">
  <div class="wrap px rv" style="display:flex;flex-wrap:wrap;gap:26px;justify-content:space-between;align-items:flex-end">
    <div><span class="badge-lab">Free for builders</span><h2 class="big" style="margin-top:12px">The builder's <em>plumbing checklist.</em></h2><p class="lead" style="margin-top:14px;max-width:52ch">Everything to lock in before pricing, slab, rough in and handover, so plumbing never holds up your program.</p></div>
    {btn(L('/builders-checklist'), 'Get the checklist')}
  </div>
</section>'''

def band():
    return f'''
<section class="band">
  <div class="wrap px band-in">
    <div class="rv"><h2>Burst pipe or no hot water? <em>Call now.</em></h2><p>24/7 emergency plumbing across Sydney and the South Coast.</p></div>
    <div class="rv">{btn('tel:'+TEL, PHONE, 'dark')}</div>
  </div>
</section>'''

def foot():
    pages_l = [('/services','Services'),('/builders','For builders'),('/projects','Projects'),('/about','About'),('/careers','Careers'),('/builders-checklist','Builder checklist'),('/privacy','Privacy'),('/terms','Terms')]
    li = lambda items: ''.join(f'<li><a href="{L(p)}">{n}</a></li>' for p, n in items)
    svc = li([('/'+x[0], x[1]) for x in SERVICES])
    areas = li([('/'+a[0], a[1][4:].title() if a[1].startswith('the ') else a[1]) for a in AREAS])
    return band() + f'''
<footer class="foot">
  <div class="wrap px">
    <div class="foot-top foot-top5">
      <div>
        <img src="{W('logo',600,150)}" alt="LPS Plumbing Group" style="height:34px;width:auto;margin-bottom:18px">
        <p>Plumbing, drainage and gas fitting for high end builds, renovations and bathrooms across Sydney and the South Coast. Lic {LIC}.</p>
      </div>
      <div><h5>Pages</h5><ul>{li(pages_l)}</ul></div>
      <div><h5>Services</h5><ul>{svc}</ul></div>
      <div><h5>Areas</h5><ul>{areas}</ul></div>
      <div><h5>Contact</h5><ul><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="https://www.instagram.com/{IG}/" target="_blank" rel="noopener">@{IG}</a></li><li><a href="{L('/quote')}">Get a quote</a></li></ul></div>
    </div>
    <div class="foot-btm">
      <span>© <span id="yr">2026</span> LPS Plumbing Group · Lic {LIC} · ABN {ABN}</span>
      <span>Site by <a href="https://www.latitudemarketing.au/?utm_source=lps-plumbing&utm_medium=referral&utm_campaign=client_credit" target="_blank" rel="noopener">Latitude Marketing</a></span>
    </div>
  </div>
</footer>
<div class="callbar" id="callbar"><a href="tel:{TEL}" class="cb-call">Call Lewis</a><a href="{L('/quote')}" class="cb-quote">Get a quote</a></div>
'''

JS = open(os.path.join(os.path.dirname(__file__), 'site.js')).read()
MOTION = open(os.path.join(os.path.dirname(__file__), 'motion.js')).read()
LIBS = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script><script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script><script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>'
def lines(*ls):
    return ''.join(f'<span class="ln-wrap"><span class="ln-in">{l}</span></span>' for l in ls)

def tail():
    return f'<script>{JS}</script>\n<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};</script><script defer src="/_vercel/insights/script.js"></script>\n</body>\n</html>\n'

pages = {}

# ---------------- HOME ----------------
schema = {
    "@context": "https://schema.org", "@type": "Plumber", "name": "LPS Plumbing Group",
    "description": "Plumbing, drainage and gas fitting for high end residential builds, renovations, bathrooms and commercial projects across Sydney.",
    "telephone": "+61452611522", "email": EMAIL, "url": DOMAIN, "image": SHARE_HOST + "/lps-share.jpg",
    "founder": {"@type": "Person", "name": "Lewis Slatter"},
    "address": {"@type": "PostalAddress", "addressRegion": "NSW", "addressCountry": "AU"},
    "areaServed": [{"@type": "Place", "name": n} for n in ["Sutherland Shire", "St George", "Inner West, Sydney", "Mascot", "Eastern Suburbs, Sydney", "Neutral Bay", "Northern Beaches", "Wollongong", "Shellharbour", "Kiama"]],
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "07:00", "closes": "19:00"},
    "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES],
    "sameAs": [f"https://www.instagram.com/{IG}/"],
}
faqschema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(__import__('re').sub('<[^>]+>', '', a))}} for q, a in FAQ]}
ld = f'<script type="application/ld+json">{json.dumps(schema)}</script><script type="application/ld+json">{json.dumps(faqschema)}</script>'

svc_rows = ''.join(f'''<article class="svc-row rv"><span class="svc-n">0{i+1}</span><h3 class="svc-t">{s[1]}</h3><p class="svc-d">{s[3]} <a href="{L('/'+s[0])}" style="color:var(--gold);font-weight:500;white-space:nowrap">Learn more</a></p><div class="svc-img"><img src="{W(s[2],900,560)}" alt="{s[1]} plumbing by LPS Plumbing Group" loading="lazy"></div></article>''' for i, s in enumerate(SERVICES))

scards = ''.join(f'''<article class="scard"><div class="scard-b"><div><span class="scard-n">0{i+1} / 05</span><h3 style="margin-top:18px">{s[1]}</h3><p>{s[4]}</p></div><div><ul>{''.join(f'<li>{x}</li>' for x in s[5][:4])}</ul><a class="more" href="{L('/'+s[0])}" style="margin-top:22px">Explore {s[1].lower()} &rarr;</a></div></div><div class="scard-m"><img src="{W(s[2],1100,1100)}" alt="{s[1]} plumbing by LPS Plumbing Group" loading="lazy"></div></article>''' for i, s in enumerate(SERVICES))
gal = [('miranda','Bathroom','Terracotta powder room'),('basin','Bathroom','Brushed brass wall spout'),('vanity','Kitchen','Brass kitchen mixer fit off'),('ensuite','Bathroom','Ensuite with brass fit off'),('kitchen','New build','Open plan kitchen, new build'),('stonevanity','Renovation','Stone vanity with wall mixer'),('commercial','Commercial','Commercial pipework'),('hotwater','Hot water','Heat pump hot water install')]
hz = ''.join(f'<figure class="hz-item"><div class="hz-img"><img src="{W(i,800,1000)}" alt="{t}" loading="lazy"></div><figcaption class="hz-cap"><b>{t}</b><span>{k}</span></figcaption></figure>' for i,k,t in gal)
mq = ''.join(f'<span>{x}</span>' for x in ['New builds','Renovations','Bathrooms','Commercial','Gas fitting','Drainage','Hot water','24/7 emergency']*2)
arows = ''.join(f'<a class="arow" href="{L("/"+a[0])}"><span>{a[1][0].upper()+a[1][1:]}</span><small>{a[2]} &rarr;</small></a>' for a in AREAS)

work = ''.join(f'<article class="mate rv"><div class="mate-img"><img src="{W(i,700,900)}" alt="{t}" loading="lazy"></div><div class="mate-b"><div class="mate-r">{k}</div><div class="mate-n">{t}</div></div></article>' for i,k,t in gal[:4])
area_chips = ''.join(f'<a href="{L("/"+a[0])}">{a[1][4:].title() if a[1].startswith("the ") else a[1]}</a>' for a in AREAS)
home = head('LPS Plumbing Group | Plumber for High End Builds, Sydney',
            'Plumbing, drainage and gas for high end builds, renos and bathrooms across Sydney. Licensed, insured, 24/7. Call Lewis on 0452 611 522.', '/', ld) + nav(True) + f'''
<header class="hero">
  <video class="hero-video" autoplay muted loop playsinline preload="auto" poster="{BASE}/lps-hero-poster.jpg" aria-hidden="true"><source src="{BASE}/lps-hero.mp4" type="video/mp4"></video>
  <div class="hero-shade"></div>
  <div class="hero-seam"></div>
  <div class="hero-inner wrap px">
    <p class="hero-label">Plumbing · Drainage · Gas · Sydney &amp; South Coast</p>
    <h1>
      <span class="ln"><span>Plumbing for builds</span></span>
      <span class="ln"><span>where the</span></span>
      <span class="ln"><span><em>finish matters.</em></span></span>
    </h1>
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
    <div class="lcell"><span class="lnum">24/7</span><span class="llab">Emergencies, Lewis picks up</span></div>
    <div class="lcell"><span class="lnum">1</span><span class="llab">Point of contact, start to finish</span></div>
    <div class="lcell"><span class="lnum">5.0</span><span class="llab">Rated on Google</span></div>
  </div>
</section>

<section class="sec">
  <div class="wrap px">
    {badge('01', 'Who we are')}
    <div class="about-grid">
      <div class="rv"><h2 class="big">Small crew. High standards. <em>No shortcuts.</em></h2></div>
      <div class="rv">
        <p class="lead">We plumb high end homes, renovations and commercial builds for builders and homeowners who care how the job finishes. Director Lewis Slatter runs every job, from first pit to final tap.</p>
        <div class="pillars">
          <div class="pillar"><span class="pillar-k">A</span><div><h4>Licensed &amp; insured</h4><p>Lic {LIC}. Compliance certificates on every job.</p></div></div>
          <div class="pillar"><span class="pillar-k">B</span><div><h4>Priced from your plans</h4><p>Clear, itemised quotes. No surprises at fit off.</p></div></div>
          <div class="pillar"><span class="pillar-k">C</span><div><h4>Built to program</h4><p>We line up with your trades so walls close on time.</p></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec-dark">
  <div class="wrap px">
    {badge('02', 'What we do')}
    <div class="rv" style="display:flex;flex-wrap:wrap;gap:24px;justify-content:space-between;align-items:flex-end">
      <h2 class="big">Everything in the wall, <em>done properly.</em></h2>
      <p class="lead" style="max-width:38ch">New builds to burst pipes. Same crew, same standard, start to finish.</p>
    </div>
    <div class="svc">{svc_rows}</div>
    <div class="rv" style="margin-top:34px">{btn(L('/services'), 'See all services')}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap px">
    {badge('03', 'Recent work')}
    <div class="rv" style="display:flex;flex-wrap:wrap;gap:24px;justify-content:space-between;align-items:flex-end">
      <h2 class="big">The work <em>speaks for itself.</em></h2>
      {btn(L('/projects'), 'See projects', 'dark')}
    </div>
    <div class="crew">{work}</div>
  </div>
</section>
{reviews_block('04')}

<section class="sec">
  <div class="wrap px">
    {badge('05', 'Where we work')}
    <div class="rv"><h2 class="big">All of Sydney. <em>Down the South Coast.</em></h2></div>
    <div class="chips rv" style="margin-top:30px">{area_chips}</div>
  </div>
</section>
{faq_block('06')}
{quote_form('07')}''' + foot() + tail()
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
    faqs = SFAQ[slug] + FAQ[:2]
    if slug == 'emergency':
        pages[f'{slug}.html'] = head(title, desc, '/' + slug, faq_ld(faqs)) + nav() + phead('Emergency', 'Answering now · 24/7', h1, f'Burst pipe, blocked drain, no hot water or a gas leak. Call Lewis now. Licensed, insured, Lic {LIC}.') + f'''
<section class="ledger" aria-label="Emergency response">
  <div class="ledger-in wrap">{''.join(f'<div class="lcell"><span class="lnum">0{k+1}</span><span class="llab">{x}</span></div>' for k, x in enumerate(bullets[:4]))}</div>
</section>
<section class="sec sec-dark" id="quote">
  <div class="wrap px">
    {badge('01', 'Call back')}
    <div class="contact-grid">
      <div class="cinfo rv">
        <div class="crow"><div class="crow-k">Call now, 24/7</div><div class="crow-v"><a href="tel:{TEL}">{PHONE}</a></div><div class="crow-s">Text or <a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a> if you can't talk.</div></div>
        <div class="crow"><div class="crow-k">While you wait</div><div class="crow-v" style="font-size:16px">Water off at the main</div><div class="crow-s">Smell gas? Leave the house and call from outside.</div></div>
      </div>
      <div class="form-card rv">
        <div class="form-head"><h3>Can't call right now?</h3><p>Leave your number and we'll call you straight back.</p></div>
        <form id="quoteForm" action="{form_action()}" method="POST" onsubmit="handleSubmit(event)">
          {hidden('EMERGENCY call back request: LPS website')}<input type="hidden" name="job_type" value="Emergency">
          <div class="fgrid two">{field('Name *', '<input type="text" name="name" required autocomplete="name">')}{field('Phone *', '<input type="tel" name="phone" required autocomplete="tel">')}</div>
          <div class="fgrid" style="margin-top:14px">{field('Suburb *', '<input type="text" name="suburb" required>')}{field("What's happening?", '<textarea name="message"></textarea>')}</div>
          <div class="form-actions">{btn_submit('Call me back')}</div>
          <div id="formStatus" role="status"></div>
        </form>
      </div>
    </div>
  </div>
</section>
{faq_block('02', faqs)}''' + foot() + tail()
        continue
    pages[f'{slug}.html'] = head(title, desc, '/' + slug, faq_ld(faqs)) + nav() + phead(name, 'Services', h1, short) + f'''
<section class="sec"><div class="wrap px">
  {badge('01', name)}
  <div class="sblocks"><div class="sblock rv"><span class="sb-n">01</span><div class="sb-body"><h3>What you get</h3><p>{long}</p><ul class="sb-list">{''.join(f'<li>{x}</li>' for x in bullets)}</ul></div><div class="sb-media"><img src="{W(img,1000,750)}" alt="{name} plumbing by LPS Plumbing Group" loading="lazy"></div></div></div>
  <div class="rv" style="margin-top:40px"><span class="badge-lab">Other services</span><div class="chips">{others}</div></div>
</div></section>
{faq_block('02', faqs)}
{quote_form('03')}''' + foot() + tail()

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
{builders_block('03')}
{creds_block('03' if not BUILDERS else '04')}
{checklist_cta()}
{quote_form('05', 'Send the plans.', 'Attach a link to your plans or scope and we will come back with a full plumbing price.')}''' + foot() + tail()

# ---------------- QUOTE ----------------
pages['quote.html'] = head('Get a Plumbing Quote | LPS Plumbing Group',
    'Request a quote from LPS Plumbing Group. Send plans or photos and get a clear, itemised price. Or call Lewis on 0452 611 522.', '/quote') + nav() + phead('Get a quote', 'Get a quote', 'Tell us about <em>the job.</em>', 'Builders, homeowners and developers. Send the details and we reply within one business day.', False) + quote_form('01') + foot() + tail()

# ---------------- PROJECTS ----------------
projs = [('miranda', 'Bathroom', 'Terracotta powder room', 'Wall hung basin and wall mixer set out dead level against handmade terracotta tiles, finished in brushed brass.'),
         ('kitchen', 'New build', 'Open plan kitchen, new build', 'Island sink and appliance services run through the slab for a clean, open layout.'),
         ('ensuite', 'Bathroom', 'Ensuite with brass fit off', 'Bath, vanity, wall mixers and heated rail fitted off in matching brass.'),
         ('stonevanity', 'Renovation', 'Stone vanity with wall mixer', 'Wall mixer and spout set into a natural stone splashback over a solid stone basin.'),
         ('vanity', 'Kitchen', 'Brass kitchen mixer', 'Gooseneck mixer fitted to an undermount sink on a marble benchtop.'),
         ('shower', 'Bathroom', 'Walk in shower', 'Rail shower, concealed services and floor waste in a full height marble bathroom.'),
         ('commercial', 'Commercial', 'Commercial pipework', 'Large bore pipework and valves installed and tested on an industrial site.'),
         ('hotwater', 'Hot water', 'Heat pump hot water', 'Heat pump hot water system installed with tidy copper connections.'),
         ('laundry', 'Renovation', 'Laundry fit off', 'Stacked washer and dryer services and floor waste in a fully tiled laundry.')]
cards = ''.join(f'<article class="pcard rv"><div class="pcard-img"><img src="{W(i,1000,625)}" alt="{t}" loading="lazy"></div><div class="pcard-b"><span class="pcard-k">{k}</span><h3>{t}</h3><p>{d}</p></div></article>' for i, k, t, d in projs)
pages['projects.html'] = head('Plumbing Projects | LPS Plumbing Group, Sydney',
    'Recent new builds, renovations, bathrooms and commercial plumbing projects by LPS Plumbing Group across Sydney.', '/projects') + nav() + phead('Projects', 'Projects', 'Recent <em>work.</em>', 'A look at recent builds, renovations and bathrooms we have plumbed.') + f'''
{"".join(f'<section class="case"><div class="wrap px case-in"><div class="case-m rv"><img src="{W(c["img"],1200,900)}" alt="{c["title"]}" loading="lazy"></div><div class="case-b rv"><span class="badge-lab">{c["suburb"]} · Builder: {c["builder"]}</span><h2>{c["title"]}</h2><p><b>Scope.</b> {c["scope"]}</p><p><b>Result.</b> {c["result"]}</p></div></div></section>' for c in CASES)}
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
    <p class="lead" style="margin-top:16px">We are growing. If you are a plumber who takes pride in the finish, <a href="{L('/careers')}" style="color:var(--sea);font-weight:600">come work with us</a>.</p></div>
  </div>
</div></section>
{creds_block('02')}
{quote_form('03')}''' + foot() + tail()


# ---------------- CAREERS ----------------
pages['careers.html'] = head('Plumbing Jobs Sydney | Work with LPS Plumbing Group',
    'LPS Plumbing Group is hiring plumbers and apprentices for high end builds across Sydney. Apply in two minutes or call Lewis on 0452 611 522.', '/careers') + nav() + phead('Careers', 'We are hiring', 'Work on builds <em>worth your name.</em>', 'We are growing the crew to keep up with high end builders across Sydney. If you take pride in the finish, we want to hear from you.', False) + f'''
<section class="sec"><div class="wrap px">
  {badge('01', 'Open roles')}
  <div class="sblocks">
    <article class="sblock noimg rv"><span class="sb-n">01</span><div class="sb-body"><h3>Plumber</h3><p>Full time. Licensed, or close to it. You can run a rough in and fit off on a high end build without being chased, and you care what the finished wall looks like.</p></div></article>
    <article class="sblock noimg rv"><span class="sb-n">02</span><div class="sb-body"><h3>Apprentice plumber</h3><p>Apprenticeship. Already in your apprenticeship, or keen to start. You turn up, listen and want to learn the trade properly on quality work.</p></div></article>
  </div>
</div></section>
<section class="sec sec-dark"><div class="wrap px">
  {badge('02', 'Why LPS')}
  <div class="vrows">
    <div class="vrow rv"><span class="vrow-n">01</span><h4>Quality work, every day</h4><p>Architect designed homes, renovations and bathrooms with premium fixtures. No cheap jobs done fast.</p></div>
    <div class="vrow rv"><span class="vrow-n">02</span><h4>Learn from the director</h4><p>You work alongside Lewis, not three layers of management. Straight feedback, real progression.</p></div>
    <div class="vrow rv"><span class="vrow-n">03</span><h4>Steady builder work</h4><p>Repeat work from builders, so the diary stays full and you are not sitting around waiting for jobs.</p></div>
  </div>
</div></section>
<section class="sec sec-dark" id="apply">
  <div class="wrap px">
    {badge('03', 'Apply')}
    <div class="rv" style="max-width:60ch"><h2 class="big">Two minutes. <em>No resume needed.</em></h2><p class="lead" style="margin-top:16px">Fill this in and Lewis will give you a call. Got a resume? Add a link or email it to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
    <div class="contact-grid">
      <div class="cinfo rv"><div class="crow"><div class="crow-k">Rather chat?</div><div class="crow-v"><a href="tel:{TEL}">{PHONE}</a></div></div></div>
      <div class="form-card rv">
        <div class="form-head"><h3>Apply now</h3><p>Lewis calls every applicant back.</p></div>
        <form id="quoteForm" action="{form_action()}" method="POST" onsubmit="handleSubmit(event)">
          {hidden('Job application: LPS Plumbing Group website')}
          <div class="fgrid two">{field('Name *', '<input type="text" name="name" required autocomplete="name">')}{field('Phone *', '<input type="tel" name="phone" required autocomplete="tel">')}</div>
          <div class="fgrid two" style="margin-top:14px">{field('Email *', '<input type="email" name="email" required autocomplete="email">')}{field('Role *', '<select name="role" required><option value="">Select</option><option>Plumber</option><option>Apprentice plumber</option><option>Other</option></select>')}</div>
          <div class="fgrid two" style="margin-top:14px">{field('Years in the trade', '<input type="text" name="experience" inputmode="numeric">')}{field('Licence number (if any)', '<input type="text" name="licence">')}</div>
          <div class="fgrid two" style="margin-top:14px">{field('Where are you based? *', '<input type="text" name="suburb" required>')}{field("Driver's licence and White Card?", "<select name=\"tickets\"><option>Both</option><option>Driver's licence only</option><option>White Card only</option><option>Neither yet</option></select>")}</div>
          <div class="fgrid" style="margin-top:14px">{field('Tell us about yourself', '<textarea name="message" placeholder="Recent jobs, what you are after, resume link"></textarea>')}</div>
          <div class="form-actions">{btn_submit('Send application')}</div>
          <div id="formStatus" role="status"></div>
        </form>
      </div>
    </div>
  </div>
</section>''' + foot() + tail()

# ---------------- BUILDER CHECKLIST (lead magnet) ----------------
pages['builders-checklist.html'] = head("Builder's Plumbing Checklist | LPS Plumbing Group",
    'Free plumbing checklist for builders: what to lock in before pricing, slab, rough in and handover so plumbing never holds up your program.', '/builders-checklist') + nav() + phead('Builder checklist', 'Free for builders', "The builder's <em>plumbing checklist.</em>", 'What to lock in before pricing, slab, rough in, fit off and handover, so plumbing never holds up your program. One page, free.', False) + f'''
<section class="sec sec-dark">
  <div class="wrap px">
    {badge('01', "What's inside")}
    <div class="contact-grid">
      <div class="cinfo rv">
        <div class="crow"><div class="crow-k">Before pricing</div><div class="crow-s">Plans, selections and site info a plumber needs to give you a real price</div></div>
        <div class="crow"><div class="crow-k">Before the slab</div><div class="crow-s">Set out, sewer and stormwater checks that save a jackhammer later</div></div>
        <div class="crow"><div class="crow-k">Rough in</div><div class="crow-s">Heights, mixer bodies and niches to confirm before walls close</div></div>
        <div class="crow"><div class="crow-k">Fit off</div><div class="crow-s">What needs to be on site so fit off happens in one visit</div></div>
        <div class="crow"><div class="crow-k">Handover</div><div class="crow-s">The compliance paperwork your certifier will ask for</div></div>
      </div>
      <div class="form-card rv">
        <div class="form-head"><h3>Get the checklist</h3><p>Download straight away, no spam.</p></div>
        <form id="ckForm" action="{form_action()}" method="POST">
          {hidden('Builder checklist download: LPS website')}
          <div class="ck-fields">
          <div class="fgrid two">{field('Name *', '<input type="text" name="name" required autocomplete="name">')}{field('Company *', '<input type="text" name="company" required autocomplete="organization">')}</div>
          <div class="fgrid two" style="margin-top:14px">{field('Email *', '<input type="email" name="email" required autocomplete="email">')}{field('Phone', '<input type="tel" name="phone" autocomplete="tel">')}</div>
          <div class="form-actions">{btn_submit('Get the checklist')}</div>
          </div>
          <div id="ckDone" hidden style="margin-top:16px;padding:16px;border-radius:12px;background:var(--gold-soft)"><b>Here you go.</b> <a href="{L('/lps-builders-plumbing-checklist.pdf')}" target="_blank" rel="noopener" style="font-weight:600">Download the checklist (PDF) &rarr;</a></div>
        </form>
      </div>
    </div>
  </div>
</section>
<script>document.addEventListener('DOMContentLoaded',function(){{var f=document.getElementById('ckForm');if(!f)return;f.addEventListener('submit',function(e){{e.preventDefault();var b=f.querySelector('button');b.disabled=true;fetch(f.action,{{method:'POST',body:new FormData(f),headers:{{Accept:'application/json'}}}}).finally(function(){{f.querySelector('.ck-fields').hidden=true;document.getElementById('ckDone').hidden=false;if(typeof gtag==='function')gtag('event','generate_lead',{{form:'builder_checklist'}});if(typeof fbq==='function')fbq('track','Lead');}});}});}});</script>
''' + foot() + tail()

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

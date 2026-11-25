#!/usr/bin/env python3
"""LPS Plumbing Group site generator (Latitude SAL template, LPS palette)."""
import os, sys, json, html, datetime
sys.path.insert(0, os.path.dirname(__file__))
from areas_copy import AREA_COPY, EXTRA_SERVICES, EXTRA_SFAQ, TITLE_KW
from guides import GUIDES

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
GOOGLE_RATING, GOOGLE_COUNT = '5.0', 25
GOOGLE_URL = 'https://www.google.com/maps/search/?api=1&query=LPS%20Plumbing%20Group'
REVIEWS = [     # real Google reviews only, copied from LPS's Google Business Profile (Nov 2026)
    ('John M.', 'LPS Plumbing did a great job at our home. Connected hot &amp; cold pipes to rear property. Connected new shower mixer, bath vanity, kitchen sink, outdoor bath and gave great advice repositioning washer dryer with lots of savings. Thankyou Lewis'),
    ('Sophie D.', 'Very happy with the service. Had a bayonet fitting installed and the work was completed professionally and efficiently. Great communication, arrived on time, and left everything tidy. Would definitely recommend and use again.'),
    ('Jessica S.', 'Highly recommend Lewis of LPS plumbing. On time, friendly, reliable and extremely knowledgeable. Extremely happy!'),
    ('Anton L.', 'Big shoutout to Lewis, he\u2019s come through a couple times now when our shop has had issues, handled with professionalism and been great to deal with throughout. Will definitely be in contact again in future when needed!'),
    ('Kerryanne', 'The entire job was completed perfectly and cleanly in less than half an hour. Before leaving, he also kindly checked if we had any other issues to ensure everything was in order. Thank you for the outstanding service and professionalism.'),
]
CASES = []      # [{'img':'key','title':'','suburb':'','builder':'','scope':'','result':''}]
CSS = open(os.path.join(os.path.dirname(__file__), 'forma.css')).read()

LOCAL = {
    'kitchen': 'lps-new-build-kitchen.jpg', 'vanity': 'lps-brass-kitchen-mixer.jpg', 'ensuite': 'lps-ensuite-brass-fit-off.jpg',
    'shower': 'lps-walk-in-shower.jpg', 'hotwater': 'lps-hot-water-heat-pump.jpg', 'commercial': 'lps-commercial-pipework.jpg',
    'basin': 'lps-brass-wall-spout-basin.jpg', 'miranda': 'lps-terracotta-powder-room.jpg', 'sink': 'lps-brass-sink-mixer.jpg',
    'stone': 'lps-brass-mixer-stone.jpg', 'stonevanity': 'lps-stone-vanity-wall-mixer.jpg', 'gooseneck': 'lps-kitchen-gooseneck.jpg',
    'laundry': 'lps-laundry-fit-off.jpg', 'bathreno': 'lps-bathroom-renovation.jpg', 'kitchensink': 'lps-kitchen-sink-fit-off.jpg',
    'lewis': 'lps-lewis-slatter.jpg',
}

def W(i, w=1600, h=1200):
    if i in LOCAL:   # LPS's own job photos, hosted in /img
        return f'{BASE}/img/{LOCAL[i][:-4]}.webp'
    ids = {
        'logo': '84f08c_9dd65380a4c24c1b927187305cc5b8ae~mv2.png',
    }
    f = ids[i]
    return f'https://static.wixstatic.com/media/{f}/v1/fit/w_{w},h_{h},q_95/lps.png'

def L(path):  # internal link
    return BASE + path if path != '/' else (BASE + '/' if BASE else '/')
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

SERVICES = SERVICES[:-1] + EXTRA_SERVICES + SERVICES[-1:]   # emergency stays last

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

SFAQ.update(EXTRA_SFAQ)
SVC_IMGS = {'new-builds':['kitchen','kitchensink','laundry'],'renovations':['vanity','gooseneck','stonevanity'],'bathrooms':['ensuite','shower','bathreno'],'commercial':['commercial','laundry','kitchensink'],'gas-fitting':['kitchensink','hotwater','stone'],'drainage':['laundry','commercial','shower'],'emergency':['hotwater','laundry','sink']}
IMG_ALT = {'lewis':'Lewis Slatter, director of LPS Plumbing Group','kitchen':'Open plan new build kitchen plumbed by LPS','kitchensink':'Kitchen sink fit off','laundry':'Laundry fit off with floor waste','vanity':'Brass kitchen mixer on marble','gooseneck':'Gooseneck kitchen mixer','stonevanity':'Stone vanity with wall mixer','ensuite':'Ensuite with brass fit off','shower':'Walk in shower with rail shower','bathreno':'Bathroom renovation with brass tapware','commercial':'Commercial pipework install','hotwater':'Heat pump hot water install','sink':'Brass sink mixer','stone':'Brass mixer on stone benchtop','basin':'Brushed brass wall spout and basin','miranda':'Terracotta powder room'}

POOL = ['stone','bathreno','kitchensink','ensuite','basin','stonevanity','kitchen','laundry','gooseneck','shower','miranda','vanity','sink','commercial','hotwater']
def pick(first, n, seed=0):
    out = []
    for k in list(first) + POOL[seed % len(POOL):] + POOL[:seed % len(POOL)]:
        if k not in out: out.append(k)
    return out[:n]

def gstrip(keys, place=''):
    return '<div class="gstrip">' + ''.join(f'<figure class="rv"><img src="{W(k)}" alt="{IMG_ALT.get(k, "Plumbing by LPS Plumbing Group")}{(" in " + place) if place else ""}" loading="lazy"></figure>' for k in keys) + '</div>'

# =====================================================================
# v3 templates: rounded panel layout, LPS palette (Forma-inspired, built from scratch)
# =====================================================================
import re
NAV = [('/services', 'Services'), ('/builders', 'For builders'), ('/projects', 'Projects'), ('/guides', 'Guides'), ('/about', 'About')]

ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
NE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>'
PH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
G_SVG = '''<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'''

def btn(href, label, kind='sea', icon=None, ext=False):
    t = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a href="{href}" class="btn btn-{kind}"{t}>{label}{icon if icon is not None else ARR}</a>'

def ulink(href, label, icon=None):
    return f'<a class="ulink" href="{href}"><span>{label}</span>{icon or ARR}</a>'

def hd(s):
    """Heading text without italics, brand dot on the final full stop."""
    s = s.replace('<em>', '').replace('</em>', '')
    return s[:-1] + '<span class="dot">.</span>' if s.endswith('.') else s

def ttl(p):  # 'the Inner West' -> 'Inner West'
    return p[4:] if p.startswith('the ') else p

def alt(k, extra=''):
    return IMG_ALT.get(k, 'Plumbing by LPS Plumbing Group') + extra

VIDS = {'tap': 'Brushed brass wall spout running into a stone basin', 'bath': 'Bathroom with timber vanity and wall mixer',
        'kitchen': 'Open plan new build kitchen', 'shower': 'Copper outdoor shower on a feature wall', 'vanity': 'Timber vanity with vessel basin and wall mixer'}
VBTN = '<button class="vid-btn" aria-label="Pause video"><svg viewBox="0 0 24 24"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg></button>'
def vsrc(name, lazy):
    a = 'data-src' if lazy else 'src'
    return f'<source {a}="{BASE}/video/{name}.mp4" media="(min-width: 800px)" type="video/mp4"><source {a}="{BASE}/video/{name}-sd.mp4" type="video/mp4">'
def vid(k, cls='', lazy=True, auto=True):
    a = ' autoplay' if auto else ''
    pre = 'none' if lazy else 'auto'
    return f'<video class="{cls}" muted loop playsinline{a} preload="{pre}" poster="{BASE}/video/lps-{k}.jpg" aria-label="{VIDS[k]}">{vsrc("lps-" + k, lazy)}</video>'

def head(title, desc, path, extra=''):
    canon = DOMAIN + (path if path != '/' else '/')
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    tag = GA4 or GADS
    ga = '' if not tag else f"""<script async src="https://www.googletagmanager.com/gtag/js?id={tag}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());{f"gtag('config','{GA4}');" if GA4 else ''}{f"gtag('config','{GADS}');" if GADS else ''}</script>"""
    if META_PIXEL:
        ga += f"""<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','{META_PIXEL}');fbq('track','PageView');</script>"""
    t, d = html.escape(title), html.escape(desc)
    F = 'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap'
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
<link rel="preload" as="style" href="{F}" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="{F}"></noscript>
{ga}
{extra}
<style>
{CSS}
</style>
</head>
<body>
"""

def loader(full):
    """Loading screen on every page load. Full version on the home page, a quick curtain elsewhere."""
    if not full:
        return f'''<div class="ld ld-mini" id="ld" aria-hidden="true"><img class="ld-logo" src="{W("logo",600,150)}" alt=""><div class="ld-bar"><i></i></div></div>
<script>(function(){{var d=document.getElementById('ld');document.documentElement.classList.add('ld-on');window.LPS_LD=0.75;setTimeout(function(){{d.classList.add('out');document.documentElement.classList.remove('ld-on')}},650);setTimeout(function(){{d.remove()}},1500)}})();</script>'''
    return f'''<div class="ld" id="ld" aria-hidden="true">
  <div class="ld-win"><video muted playsinline autoplay loop preload="auto" poster="{BASE}/video/lps-tap.jpg"><source src="{BASE}/video/lps-tap.mp4#t=2.4" media="(min-width: 800px)" type="video/mp4"><source src="{BASE}/video/lps-tap-sd.mp4#t=2.4" type="video/mp4"></video></div>
  <div class="ld-top"><img class="ld-logo" src="{W("logo",600,150)}" alt=""><span>Sydney to the South Coast</span></div>
  <div class="ld-bot"><b><span id="ldN">000</span></b><p>Plumbing, drainage and gas fitting<br>for builds where the finish matters.</p></div>
  <div class="ld-bar"><i id="ldB"></i></div>
</div>
<script>(function(){{var d=document.getElementById('ld'),n=document.getElementById('ldN'),b=document.getElementById('ldB'),v=d.querySelector('video'),t0=performance.now(),T=1700;
document.documentElement.classList.add('ld-on');window.LPS_LD=2.55;
try{{var p=v.play();if(p&&p.catch)p.catch(function(){{}})}}catch(e){{}}
function f(t){{var k=Math.min(1,(t-t0)/T),e=1-Math.pow(1-k,3),x=Math.round(e*100);n.textContent=(x<10?'00':x<100?'0':'')+x;b.style.transform='scaleX('+e+')';if(k<1)requestAnimationFrame(f);else{{d.classList.add('grow');setTimeout(function(){{d.classList.add('out');document.documentElement.classList.remove('ld-on')}},800);setTimeout(function(){{d.remove()}},1900)}}}}
requestAnimationFrame(f)}})();</script>'''

def nav(hold=False, cur=''):
    h = loader(hold)
    links = ''.join(f'<a href="{L(p)}"{" class=on" if p == cur else ""}>{n}</a>' for p, n in NAV)
    sheet = ''.join(f'<a href="{L(p)}">{n} <i>0{i+1}</i></a>' for i, (p, n) in enumerate(NAV + [('/careers', 'Careers'), ('/quote', 'Get a quote')]))
    return h + f'''
<div class="navwrap" id="navwrap">
  <nav class="navbar" aria-label="Main">
    <a href="{L('/')}" class="nav-logo" aria-label="LPS Plumbing Group home"><img src="{W('logo',400,100)}" alt="LPS Plumbing Group" width="97" height="24"></a>
    <div class="nav-links">{links}</div>
    <div class="nav-right">
      <a class="nav-pill" href="tel:{TEL}"><i></i>24/7 · {PHONE}</a>
      {btn(L('/quote'), 'Get a quote', 'sea', NE)}
    </div>
    <button class="menu-btn" id="menuBtn" aria-label="Open menu">Menu <span></span></button>
  </nav>
</div>
<div class="sheet-layer" id="sheetLayer">
  <div class="sheet-bd" id="sheetBd"></div>
  <aside class="sheet" role="dialog" aria-label="Menu">
    <div class="sheet-top"><span class="nav-logo"><img src="{W('logo',400,100)}" alt="LPS Plumbing Group" style="height:22px;width:auto"></span><button class="sheet-close" id="sheetClose" aria-label="Close menu">&times;</button></div>
    <nav class="sheet-nav">{sheet}</nav>
    <div class="sheet-foot">{btn('tel:'+TEL, 'Call Lewis: '+PHONE, 'teal', PH)}</div>
  </aside>
</div>
'''

def phead(crumb, eyebrow, h1, lead, ctas=True, img=None, path=None, extra='', video=None):
    c = f'<div class="cta-row rv">{btn(L("/quote"), "Get a quote")}{btn("tel:"+TEL, PHONE, "ghost", PH)}</div>' if ctas else ''
    bc = ''
    if path:
        bc = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":html.unescape(crumb),"item":DOMAIN+path}]}) + '</script>'
    panel = f'''<div class="hero-panel">
      <div class="crumb"><a href="{L('/')}">Home</a><span>/</span><span>{crumb}</span></div>
      <h1 class="h-xl" data-lines>{hd(h1)}</h1>
      <p class="lead rv">{lead}</p>
      {c}{extra}
    </div>'''
    if not img:
        return f'<header class="hero hero-solo"><div class="wrap"><div class="inner">{panel}</div></div></header>{bc}'
    return f'''<header class="hero"><div class="wrap"><div class="inner hero-grid short">
    <div class="hero-media">{vid(video, lazy=False) + VBTN if video else f'<img src="{W(img)}" alt="{alt(img)}" fetchpriority="high">'}</div>
    {panel}
  </div></div></header>{bc}'''

def hidden(subject):
    if WEB3FORMS_KEY:
        return f'<input type="hidden" name="access_key" value="{WEB3FORMS_KEY}"><input type="hidden" name="subject" value="{subject}"><input type="hidden" name="from_name" value="LPS Plumbing Group website"><input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">'
    return f'<input type="hidden" name="_subject" value="{subject}"><input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">'

def form_action():
    return 'https://api.web3forms.com/submit' if WEB3FORMS_KEY else FORMSPREE

def section(inner, cls='sec', id=''):
    i = f' id="{id}"' if id else ''
    return f'<section class="{cls}"{i}><div class="wrap"><div class="inner">{inner}</div></div></section>'

def sec_head(h, lead='', tag='h2'):
    l = f'<p class="lead rv">{lead}</p>' if lead else ''
    return f'<div class="sec-head"><{tag} class="h-lg" data-lines>{hd(h)}</{tag}>{l}</div>'

def faq_ld(faqs):
    return '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":html.unescape(re.sub('<[^>]+>','',a))}} for q,a in faqs]}) + '</script>'

def faq_block(faqs=None):
    items = ''.join(f'<div class="fq"><button class="fq-q" aria-expanded="false">{q}</button><div class="fq-a"><p>{a}</p></div></div>' for q, a in (faqs or FAQ))
    return section(f'''<div class="faqg">
    <div><h2 class="h-lg" data-lines>Good to know before you call<span class="dot">.</span></h2><p class="lead rv">Straight answers to what builders and homeowners ask us most.</p><div class="rv">{ulink('#quote','Go to the quote form', NE)}</div></div>
    <div class="faq rv">{items}</div>
  </div>''')

def cimg(img, h, p, extra=''):
    if img.startswith('v:'):
        return f'<div class="c-img">{vid(img[2:])}<h2 class="h-lg">{hd(h)}</h2><p>{p}</p>{extra}</div>'
    src, a = (BASE + img, 'LPS Plumbing Group on site') if img.startswith('/') else (W(img), alt(img))
    return f'<div class="c-img"><img src="{src}" alt="{a}" loading="lazy"><h2 class="h-lg">{hd(h)}</h2><p>{p}</p>{extra}</div>'

CLIST = f'''<div class="c-list">
      <a href="tel:{TEL}"><span>Call Lewis, 24/7</span><b>{PHONE}</b></a>
      <a href="mailto:{EMAIL}"><span>Email</span><b>{EMAIL}</b></a>
      <a href="sms:+{WA}"><span>Text</span><b>Send a text</b></a>
      <a href="https://wa.me/{WA}" target="_blank" rel="noopener"><span>WhatsApp</span><b>Message us</b></a>
      <div><span>Hours</span><b>7am to 7pm, 7 days</b></div>
    </div>'''

def quote_form(heading='Tell us what you are building.', sub='Builders, send through plans or a scope and we will price the full plumbing package. Homeowners, tell us about the job and we will come back with a clear, itemised quote.', img='kitchen'):
    return f'''<section class="sec" id="quote"><div class="wrap"><div class="inner contact">
  {cimg(img, heading, sub, CLIST)}
  <form class="c-form rv" id="quoteForm" action="{form_action()}" method="POST" onsubmit="handleSubmit(event)">
    {hidden('New quote request: LPS Plumbing Group website')}
    <h2>Request a quote<span class="dot">.</span></h2>
    <p class="sub">We reply within one business day.</p>
    <div class="qf-g">
      <label class="qf-f"><span>Name or company *</span><input type="text" name="name" required autocomplete="name"></label>
      <label class="qf-f"><span>Phone *</span><input type="tel" name="phone" required autocomplete="tel"></label>
      <label class="qf-f qf-w"><span>Email *</span><input type="email" name="email" required autocomplete="email"></label>
      <label class="qf-f"><span>I am a *</span><select name="client_type" required><option value="">Select</option><option>Builder</option><option>Homeowner</option><option>Developer</option><option>Strata or property manager</option><option>Commercial client</option></select></label>
      <label class="qf-f"><span>Job type *</span><select name="job_type" required><option value="">Select</option><option>New build</option><option>Renovation</option><option>Bathroom</option><option>Commercial</option><option>Gas fitting</option><option>Drainage</option><option>Emergency</option><option>Other</option></select></label>
      <label class="qf-f qf-w"><span>Site suburb *</span><input type="text" name="suburb" required></label>
      <label class="qf-f qf-w"><span>Link to plans or photos <em>(optional)</em></span><input type="url" name="plans_link" placeholder="Dropbox, Google Drive or WeTransfer"></label>
      <label class="qf-f qf-w"><span>About the job</span><textarea name="message" rows="3" placeholder="Scope, timing, stage of the build"></textarea></label>
    </div>
    <p class="qf-n">By sending this you agree to our <a href="{L('/privacy')}">privacy policy</a>. Licensed and insured, Lic {LIC}.</p>
    <button type="submit" class="btn btn-sea qf-btn">Send enquiry {ARR}</button>
    <div id="formStatus" role="status"></div>
  </form>
</div></div></section>'''

def creds_block():
    ins = f'<a href="{L("/"+INSURANCE_PDF)}" target="_blank" rel="noopener">Download certificate</a>' if INSURANCE_PDF else '<p>Certificate of currency on request</p>'
    return section(sec_head('Check us out before you book.', 'Licensed, insured and accountable on every job, big or small.') + f'''<div class="creds">
    <div class="cr rv"><span>NSW contractor licence</span><b>{LIC}</b><a href="{LIC_CHECK}" target="_blank" rel="noopener">Verify on Service NSW</a></div>
    <div class="cr rv"><span>Insurance</span><b>Fully insured</b>{ins}</div>
    <div class="cr rv"><span>Compliance</span><b>Certificates on every job</b><p>Paperwork lodged and handed over at completion</p></div>
    <div class="cr rv"><span>Accountability</span><b>Director on every job</b><p>Lewis Slatter, 8+ years in the trade</p></div>
  </div>''')

def builders_block():
    if not BUILDERS:
        return ''
    logos = ''.join((f'<img src="{L("/"+lg)}" alt="{nm}" loading="lazy" style="height:40px;width:auto">' if lg else f'<span>{nm}</span>') for nm, lg, q, who in BUILDERS)
    return section(sec_head('Trusted by Sydney builders.') + f'<div class="chips on-white rv">{logos}</div>', 'sec sec-tight')

def reviews_block(imgs=None):
    if not REVIEWS:
        return ''
    pics = ''.join(f'<img src="{W(k)}" alt="{alt(k)}" loading="lazy"{" class=on" if i == 0 else ""}>' for i, k in enumerate((imgs or [])[:len(REVIEWS)]))
    slides = ''.join(f'<figure class="rev-slide{" on" if i == 0 else ""}"><blockquote>{t}</blockquote><figcaption class="rev-who"><span class="rev-av">{nm[0]}</span><span><b>{nm}</b><span class="stars">★★★★★</span></span></figcaption></figure>' for i, (nm, t) in enumerate(REVIEWS))
    return section(sec_head('Good work gets talked about.', f'Real reviews from our Google Business Profile. {GOOGLE_RATING} stars from {GOOGLE_COUNT} reviews.') + f'''<div class="rev{'' if imgs else ' solo'}">
    {f'<div class="rev-img rv">{pics}</div>' if imgs else ''}
    <div class="rev-q rv">
      <div class="rev-top"><div class="qm">&ldquo;</div><a class="g-score" href="{GOOGLE_URL}" target="_blank" rel="noopener">{G_SVG}<b>{GOOGLE_RATING}</b><span>{GOOGLE_COUNT} Google reviews</span></a></div>
      <div aria-live="polite">{slides}</div>
      <div class="rev-foot"><div class="rev-nav"><button data-rev="-1" aria-label="Previous review">&larr;</button><span id="revCount">1 / {len(REVIEWS)}</span><button data-rev="1" aria-label="Next review">&rarr;</button></div>{ulink(GOOGLE_URL, 'Read them all on Google', NE)}</div>
    </div>
  </div>''')

def ig_block():
    pics = ''.join(f'<a class="igp rv" href="https://www.instagram.com/{IG}/" target="_blank" rel="noopener" aria-label="LPS Plumbing Group on Instagram"><img src="{W(k)}" alt="{alt(k)}" loading="lazy"></a>' for k in ['basin', 'shower', 'gooseneck', 'laundry'])
    return section(f'<div class="sec-head"><h2 class="h-lg" data-lines>On the tools, @{IG}</h2><div class="rv" style="justify-self:end">{btn("https://www.instagram.com/"+IG+"/", "Follow on Instagram", "ghost", NE, True)}</div></div><div class="igg">{pics}</div>', 'sec sec-tight')

def checklist_cta():
    return section(f'''<div class="band rv"><div><span class="lbl" style="color:rgba(11,56,77,.75)">Free for builders</span><h2 class="h-md">The builder's plumbing checklist<span class="dot" style="color:var(--teal)">.</span></h2><p>Everything to lock in before pricing, slab, rough in and handover, so plumbing never holds up your program.</p></div>{btn(L('/builders-checklist'), 'Get the checklist', 'teal')}</div>''', 'sec sec-tight')

def foot():
    links = [('/services','Services'),('/builders','For builders'),('/projects','Projects'),('/guides','Guides'),('/about','About'),('/careers','Careers'),('/builders-checklist','Builder checklist'),('/quote','Get a quote')]
    nav_l = ''.join(f'<a href="{L(p)}">{n}</a>' for p, n in links)
    svc = ''.join(f'<a href="{L("/"+x[0])}">{x[1]}</a>' for x in SERVICES)
    areas = ''.join(f'<a href="{L("/"+a[0])}">{ttl(a[1])}</a>' for a in AREAS)
    return f'''
<footer class="ft">
  <div class="wrap"><div class="inner">
    <div class="ft-top"><h2>From the first pit to the final tap.</h2><a class="ulink" href="{L('/quote')}"><span>Send us your plans</span>{NE}</a></div>
    <div class="ft-mid">
      <div class="ft-brand"><img src="{W('logo',600,150)}" alt="LPS Plumbing Group" width="138" height="34"><p>Plumbing, drainage and gas fitting for high end builds, renovations and bathrooms across Sydney and the South Coast.</p></div>
      <div class="ft-col"><h5>Explore</h5>{nav_l}</div>
      <div class="ft-col"><h5>Services</h5>{svc}</div>
      <div class="ft-col"><h5>Areas</h5>{areas}</div>
      <div class="ft-col"><h5>Contact</h5><a href="tel:{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="https://www.instagram.com/{IG}/" target="_blank" rel="noopener">Instagram</a><a href="{GOOGLE_URL}" target="_blank" rel="noopener">Google reviews</a></div>
    </div>
    <div class="ft-btm">
      <span>&copy; <span id="yr">2026</span> LPS Plumbing Group · Lic {LIC} · ABN {ABN}</span>
      <span><a href="{L('/privacy')}">Privacy</a> · <a href="{L('/terms')}">Terms</a> · Website created by <a href="https://www.latitudemarketing.au/?utm_source=lps-plumbing&utm_medium=referral&utm_campaign=client_credit" target="_blank" rel="noopener">Latitude Marketing</a></span>
    </div>
  </div></div>
</footer>
<div class="callbar" id="callbar"><a href="tel:{TEL}" class="cb-call">Call</a><a href="sms:+{WA}" class="cb-call">Text</a><a href="{L('/quote')}" class="cb-quote">Get a quote</a></div>
'''

JS = open(os.path.join(os.path.dirname(__file__), 'site.js')).read()
MOTION = open(os.path.join(os.path.dirname(__file__), 'motion.js')).read()
LIBS = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script><script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script><script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>'
MAPLIB = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css"><script defer src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js"></script>'

def tail():
    return f'{LIBS}<script>{JS}</script><script>{MOTION}</script>\n<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};</script><script defer src="/_vercel/insights/script.js"></script>\n</body>\n</html>\n'

SC_VID = {'new-builds': 'kitchen', 'bathrooms': 'bath'}
def scard(i, s, feat=False):
    if feat:
        return f'''<a class="sc feat rv" href="{L('/'+s[0])}"><div class="sc-top"><div class="sc-n">0{i+1}</div><h3>{s[1]}</h3><p>{s[3]}</p><span class="sc-l">Explore {s[1].lower()}</span></div><img src="{W(s[2])}" alt="{alt(s[2])}" loading="lazy"><span class="sc-go"><span>{NE}</span></span></a>'''
    v = vid(SC_VID[s[0]], 'sc-vid', auto=False) if s[0] in SC_VID else ''
    return f'''<a class="sc rv" href="{L('/'+s[0])}"><img src="{W(s[2])}" alt="{alt(s[2])}" loading="lazy">{v}<div class="sc-n">0{i+1}</div><div class="sc-body"><h3>{s[1]}</h3><p>{s[3]}</p><span class="sc-l">Explore {s[1].lower()}</span></div><span class="sc-go"><span>{NE}</span></span></a>'''

def scards():
    return '<div class="scards">' + ''.join(scard(i, s, i == 1) for i, s in enumerate(SERVICES)) + '</div>'

STEPS = [('Send the plans', 'Drop a link to your plans or photos and tell us the stage of the build.'),
         ('Itemised price', 'A clear quote for the full plumbing scope, so there are no surprises later.'),
         ('Rough in to program', 'Drainage, rough in and pressure testing, lined up with your other trades.'),
         ('Fit off and handover', 'Premium fixtures installed level, then compliance certificates handed over.')]
def steps_block(h='From the plans to the final tap.', lead='Every job follows the same clear path, whether it is a single bathroom or a full new build.', link=True):
    st = ''.join(f'<div class="step rv"><b>0{i+1}</b><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(STEPS))
    l = f'<div class="after-link rv">{ulink(L("/quote"), "Tell us about your project")}</div>' if link else ''
    return section(sec_head(h, lead) + f'<div class="steps">{st}</div>{l}')

WHY = [('Director on every job', 'Lewis runs every project. You are never passed to a call centre or a new crew halfway through.'),
       ('Detail that survives handover', 'Set outs your tiler will thank you for and fixtures that go in level the first time.'),
       ('Priced from your plans', 'An itemised price for the full scope, so you know what you are approving.'),
       ('Paperwork sorted', 'Testing documented and compliance certificates handed over, ready for your certifier.')]
def collab_block(h='Builders keep calling for a reason.', keys=('stone', 'bathreno', 'basin', 'gooseneck')):
    pts = ''.join(f'<div class="pt rv"><span>0{i+1}</span><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(WHY))
    a, b, c, d = keys
    return section(f'''<div class="collab">
    <div class="mosaic rv"><div><img src="{W(a)}" alt="{alt(a)}" loading="lazy"><img src="{W(b)}" alt="{alt(b)}" loading="lazy"></div><div><img src="{W(c)}" alt="{alt(c)}" loading="lazy"><img src="{W(d)}" alt="{alt(d)}" loading="lazy"></div></div>
    <div><h2 class="h-lg" data-lines>{hd(h)}</h2><div class="points">{pts}</div></div>
  </div>''')

AREA_LL = {'plumber-miranda': (-34.0336, 151.1018), 'plumber-mascot': (-33.9290, 151.1931), 'plumber-neutral-bay': (-33.8324, 151.2186),
           'plumber-eastern-suburbs': (-33.8915, 151.2767), 'plumber-st-george': (-33.9631, 151.1336), 'plumber-inner-west': (-33.9110, 151.1550),
           'plumber-northern-beaches': (-33.7531, 151.2858), 'plumber-wollongong': (-34.4278, 150.8931), 'plumber-shellharbour-kiama': (-34.6200, 150.8500)}
def areas_block(h='Close to your build.', here=None):
    chips = ''.join(f'<a href="{L("/"+a[0])}">{ttl(a[1])}</a>' for a in AREAS if a[0] != here)
    pts = json.dumps([{'n': ttl(a[1]), 'u': L('/'+a[0]), 'll': AREA_LL[a[0]], 'h': a[0] == here} for a in AREAS])
    return section(f'''<div class="panel areas">
    <div><h2 class="h-lg" data-lines>{hd(h)}</h2><p class="lead rv">Based in the Sutherland Shire and working right across Sydney, from the Shire to the Northern Beaches, and down the South Coast to Kiama.</p><div class="chips rv">{chips}</div><div class="rv" style="margin-top:26px">{btn(L('/quote'), 'Check if we cover your site')}</div></div>
    <div class="map rv" id="map" data-pts='{pts}' role="img" aria-label="Map of the areas LPS Plumbing Group covers"></div>
  </div>''')

GALD = {'miranda': ('Bathroom', 'Terracotta powder room', 'Wall hung basin and wall mixer set out dead level against handmade terracotta tiles, finished in brushed brass.'),
        'stonevanity': ('Renovation', 'Stone vanity with wall mixer', 'Wall mixer and spout set into a natural stone splashback over a solid stone basin.'),
        'bathreno': ('Bathroom', 'Bathroom renovation', 'A full bathroom renovation finished with brass tapware.'),
        'shower': ('Bathroom', 'Walk in shower', 'Rail shower, concealed services and floor waste in a full height marble bathroom.')}
GAL = [('miranda', 'Bathroom', 'Terracotta powder room', 'Wall hung basin and wall mixer set out dead level against handmade terracotta tiles, finished in brushed brass.'),
       ('ensuite', 'Bathroom', 'Ensuite with brass fit off', 'Bath, vanity, wall mixers and heated rail fitted off in matching brass.'),
       ('stonevanity', 'Renovation', 'Stone vanity with wall mixer', 'Wall mixer and spout set into a natural stone splashback over a solid stone basin.'),
       ('kitchen', 'New build', 'Open plan kitchen', 'Island sink and appliance services run through the slab for a clean, open layout.')]
FWV = [('shower', 'Outdoor', 'Copper outdoor shower', 'Exposed copper run with brass fittings, mounted against a feature cladding wall.'),
       ('kitchen', 'New build', 'Open plan kitchen', 'Island sink and appliance services run through the slab for a clean, open layout.'),
       ('bath', 'Bathroom', 'Bathroom fit off', 'Wall mixer, vanity and concealed cistern set out for a clean tiled finish.'),
       ('tap', 'Renovation', 'Brushed brass wall spout', 'Wall spout and mixer set dead level over a stone basin.')]
def featured_block():
    GAL = FWV
    imgs = ''.join(vid(k, 'on' if i == 0 else '') for i, (k, c, t, d) in enumerate(GAL))
    tabs = ''.join(f'<button class="fw-tab{" on" if i == 0 else ""}" data-i="{i}" data-t="{html.escape(t)}" data-d="{html.escape(d)}" aria-pressed="{"true" if i == 0 else "false"}"><small>{c}</small><b>{t}</b>{NE}</button>' for i, (k, c, t, d) in enumerate(GAL))
    k, c, t, d = GAL[0]
    return section(f'''<div class="fw" id="fw">
    <div class="fw-img">{imgs}</div>
    <div class="fw-top"><h2 class="h-lg">The work speaks for itself<span class="dot" style="color:var(--mint)">.</span></h2><p>New builds, renovations and bathrooms across Sydney, all plumbed by the same small crew.</p></div>
    <div><div class="fw-cur" aria-live="polite"><h3 id="fwT">{t}</h3><p id="fwD">{d}</p></div><div class="fw-tabs">{tabs}</div></div>
  </div><div class="after-link rv">{ulink(L('/projects'), 'See more of our work')}</div>''', 'sec sec-tight')

def lewis_block(h='Meet Lewis.'):
    inner = f'''<span class="lbl">Director, LPS Plumbing Group</span><h2 class="h-lg" data-lines>{hd(h)}</h2>
<blockquote class="lq">&ldquo;I started LPS Plumbing Group with the goal of building a plumbing business known for quality work, being reliable and building good relationships with our clients and builders.&rdquo;</blockquote>
<p class="lead">Lewis Slatter has 8+ years on the tools. He runs every job and he is the one who picks up when you call.</p>
<div class="cta-row" style="margin-top:28px">{btn('tel:'+TEL, 'Call Lewis: '+PHONE, 'teal', PH)}{ulink(L('/about'), 'More about LPS')}</div>'''
    return section(f'<div class="split lewis"><div class="split-img rv"><img src="{W("lewis")}" alt="{alt("lewis")}" loading="lazy"></div><div class="rv">{inner}</div></div>')

def split(img, inner, flip=False, alt_extra=''):
    return f'<div class="split{" flip" if flip else ""}"><div class="split-img rv"><img src="{W(img)}" alt="{alt(img, alt_extra)}" loading="lazy"></div><div class="rv">{inner}</div></div>'

def ticks(items):
    return '<ul class="ticks">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'

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
ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>{faq_ld(FAQ)}{MAPLIB}<link rel="preload" as="image" href="{BASE}/video/lps-hero-hd.jpg" fetchpriority="high">'
svc_foot = ''.join(f'<a href="{L("/"+s[0])}">{s[1]}</a>' for s in SERVICES)

pages['index.html'] = head('Plumber Sydney for High End Builds & Renos | LPS Plumbing',
            'Plumbing, drainage and gas for high end builds, renos and bathrooms across Sydney. Licensed, insured, 24/7. Call Lewis on 0452 611 522.', '/', ld) + nav(True) + f'''
<header class="hero"><div class="wrap"><div class="inner hero-grid">
  <div class="hero-media">
    <video autoplay muted loop playsinline preload="auto" poster="{BASE}/video/lps-hero-hd.jpg" aria-label="LPS Plumbing Group work: brass tapware, bathrooms and a new build kitchen"><source src="{BASE}/video/lps-hero-hd.mp4" media="(min-width: 800px)" type="video/mp4"><source src="{BASE}/lps-hero.mp4" type="video/mp4"></video>
    <div class="hero-tag"><i></i><b>24/7</b> emergency call outs · Lic {LIC}</div>
    {VBTN}
  </div>
  <div class="hero-panel">
    <h1 class="h-xl" data-lines="now">Plumbing for builds where the finish matters<span class="dot">.</span></h1>
    <p class="lead rv">High end new builds, renovations, bathrooms and commercial work across Sydney. One crew, led by director Lewis Slatter, from first pit to final tap.</p>
    <div class="cta-row rv">{btn(L('/quote'), 'Send us your plans')}{btn('tel:'+TEL, PHONE, 'ghost', PH)}</div>
    <div class="hero-foot rv">{svc_foot}</div>
  </div>
</div></div></header>
<section class="stats"><div class="wrap"><div class="inner stats-row">
  <div class="stat rv"><b><span data-count="8">8</span>+</b><span>Years in the trade</span></div>
  <div class="stat rv"><b>24/7</b><span>Emergency call outs, any day of the year</span></div>
  <div class="stat rv"><b><span data-count="{GOOGLE_COUNT}">{GOOGLE_COUNT}</span></b><span>Five star Google reviews</span></div>
  <div class="stat rv"><b><span data-count="9">9</span></b><span>Service areas, Sydney to Kiama</span></div>
</div></div></section>
{section('<h2 class="h-lg center" data-lines style="margin-bottom:56px">Everything in the wall, done properly<span class="dot">.</span></h2>' + scards())}
{featured_block()}
{lewis_block()}
{collab_block(keys=('basin', 'sink', 'gooseneck', 'kitchensink'))}
{steps_block()}
{reviews_block()}
{builders_block()}
{areas_block()}
{creds_block()}
{faq_block()}
{quote_form(img='v:vanity')}''' + foot() + tail()

# ---------------- SERVICES HUB ----------------
def svc_split(i, s):
    inner = f'<span class="lbl">0{i+1}</span><h2 class="h-lg">{hd(s[1]+".")}</h2><p class="lead">{s[4]}</p>{ticks(s[5])}{btn(L("/"+s[0]), "More on "+s[1].lower(), "teal")}'
    return split(s[2], inner, i % 2 == 1)

pages['services.html'] = head('Plumbing Services Sydney: Builds, Gas & Drainage | LPS',
    'New builds, renovations, bathrooms, commercial, gas fitting, drainage and 24/7 emergency plumbing across Sydney. Call 0452 611 522.', '/services') + nav(cur='/services') + phead('Services', 'Services', 'Everything in the wall, done right.', 'Plumbing, drainage and gas fitting for builders, developers and homeowners who want it done once, properly.', img='gooseneck', path='/services', video='tap') + f'''
{section('<div class="blocks">' + ''.join(svc_split(i, s) for i, s in enumerate(SERVICES)) + '</div>')}
{steps_block()}
{quote_form(img='miranda')}''' + foot() + tail()

# ---------------- SERVICE PAGES ----------------
for i, s in enumerate(SERVICES):
    slug, name, img, short, long, bullets = s
    others = ''.join(f'<a href="{L("/"+o[0])}">{o[1]}</a>' for o in SERVICES if o[0] != slug)
    h1 = (f'{name}, done properly.' if slug in ('gas-fitting', 'drainage') else f'{name} plumbing, done properly.')
    title = f'{TITLE_KW[slug]} | LPS Plumbing Group'
    svc_ld = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"Service","name":name+' plumbing',"serviceType":name,"description":short,"provider":{"@type":"Plumber","name":"LPS Plumbing Group","telephone":"+61452611522","url":DOMAIN},"areaServed":["Sydney","South Coast NSW"]}) + '</script>'
    desc = f'{short} Licensed and insured plumber across Sydney. Call Lewis on 0452 611 522.'
    if len(desc) > 158: desc = f'{short} Call Lewis on 0452 611 522.'
    faqs = SFAQ[slug] + FAQ[:2]
    K = pick([img] + SVC_IMGS.get(slug, []), 6, i * 3)
    if slug == 'emergency':
        emform = f'''<form class="c-form rv" id="quoteForm" action="{form_action()}" method="POST" onsubmit="handleSubmit(event)">
    {hidden('EMERGENCY call back request: LPS website')}
    <input type="hidden" name="job_type" value="Emergency">
    <h2>Can't call right now<span class="dot">?</span></h2><p class="sub">Leave your number and we will call you straight back.</p>
    <div class="qf-g">
      <label class="qf-f"><span>Name *</span><input type="text" name="name" required autocomplete="name"></label>
      <label class="qf-f"><span>Phone *</span><input type="tel" name="phone" required autocomplete="tel"></label>
      <label class="qf-f qf-w"><span>Suburb *</span><input type="text" name="suburb" required></label>
      <label class="qf-f qf-w"><span>What's happening?</span><textarea name="message" rows="3"></textarea></label>
    </div>
    <button type="submit" class="btn btn-sea qf-btn">Call me back {ARR}</button>
    <div id="formStatus" role="status"></div>
  </form>'''
        pages[f'{slug}.html'] = head(title, desc, '/' + slug, faq_ld(faqs) + svc_ld) + nav() + f'''
<header class="hero"><div class="wrap"><div class="inner hero-grid short">
  <div class="hero-panel em-panel">
    <span class="em-live"><i></i>Answering now · 24/7</span>
    <h1 class="h-xl" data-lines="now">Emergency plumber, 24/7<span class="dot" style="color:var(--mint)">.</span></h1>
    <p class="lead rv">Burst pipe, blocked drain, no hot water or a gas leak. Call Lewis now. Licensed and insured, Lic {LIC}.</p>
    <a class="em-call rv" href="tel:{TEL}">{PH}<span>Call {PHONE}</span></a>
    <div class="em-alt rv"><a href="sms:+{WA}">Text instead</a><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a></div>
    <p class="em-tip rv"><b>While you wait:</b> turn the water off at the main. Smell gas? Leave the house and call from outside.</p>
  </div>
  <div class="hero-media"><img src="{W(K[0])}" alt="{alt(K[0])}" fetchpriority="high"></div>
</div></div></header>
{section(f'<div class="split" style="align-items:start"><div class="rv"><h2 class="h-lg" data-lines>What we fix, any hour<span class="dot">.</span></h2><p class="lead">{long}</p>{ticks(bullets)}<div style="margin-top:26px">{ulink(L("/guides/emergency-plumbing-what-to-do"), "What to do before we arrive")}</div></div>{emform}</div>', id='quote')}
{faq_block(faqs)}''' + foot() + tail()
        continue
    areas_c = ''.join(f'<a href="{L("/"+a[0])}">{ttl(a[1])}</a>' for a in AREAS)
    inner = f'<h2 class="h-lg">What you get<span class="dot">.</span></h2><p class="lead">{long}</p>{ticks(bullets)}<span class="lbl" style="margin-top:30px">Other services</span><div class="chips on-white">{others}</div>'
    pages[f'{slug}.html'] = head(title, desc, '/' + slug, faq_ld(faqs) + svc_ld) + nav(cur='/services') + phead(name, 'Services', h1, short, img=K[0], path='/'+slug, video={'new-builds': 'kitchen', 'bathrooms': 'bath', 'renovations': 'vanity'}.get(slug)) + f'''
{section(split(K[1], inner) + gstrip(K[2:5]) + f'<div class="rv" style="margin-top:40px"><span class="lbl">Areas we cover</span><div class="chips on-white">{areas_c}</div></div>')}
{steps_block(link=False)}
{faq_block(faqs)}
{quote_form(img=K[5])}''' + foot() + tail()

# ---------------- AREA PAGES ----------------
for a in AREAS:
    slug, place, region, img, blurb, subs = a
    Pn = ttl(place)
    ac = AREA_COPY[slug]
    K = pick(ac['imgs'], 7, AREAS.index(a) * 2 + 1)
    title = f'Plumber {Pn} | Builds, Renos & 24/7 | LPS'
    desc = f'Licensed plumber in {Pn}: new builds, renovations, bathrooms, gas and drainage, plus 24/7 emergencies. Call Lewis on 0452 611 522.'
    if len(desc) > 158: desc = f'Licensed plumber in {Pn} for new builds, renos, bathrooms and 24/7 emergencies. Call Lewis on 0452 611 522.'
    svc = ''.join(f'<a href="{L("/"+s[0])}">{s[1]}</a>' for s in SERVICES)
    afaqs = ac['faqs'] + FAQ[2:4]
    ald = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"Service","name":f"Plumbing in {Pn}","serviceType":"Plumbing","provider":{"@type":"Plumber","name":"LPS Plumbing Group","telephone":"+61452611522","url":DOMAIN},"areaServed":[{"@type":"Place","name":x} for x in [Pn]+subs]}) + '</script>'
    paras = ''.join(f'<p class="lead">{x}</p>' for x in ac['body'])
    inner1 = f'<h2 class="h-lg">Local work, done properly<span class="dot">.</span></h2>{paras}'
    inner2 = f'<h2 class="h-lg">What we do in {Pn}<span class="dot">.</span></h2><p class="lead">Whether it is a new build, a renovation, a bathroom or an urgent repair, you get the same crew and the same standard. We price from your plans, work to your program and hand over with the paperwork sorted.</p>{ticks(["New builds and knockdown rebuilds", "Renovations and bathrooms", "Gas fitting, drainage and hot water", "24/7 emergency call outs"])}<span class="lbl" style="margin-top:30px">Suburbs we cover nearby</span><div class="chips on-white">{"".join(f"<span>{x}</span>" for x in subs)}</div><span class="lbl" style="margin-top:22px">Services</span><div class="chips on-white">{svc}</div>'
    pages[f'{slug}.html'] = head(title, desc, '/' + slug, faq_ld(afaqs) + ald + MAPLIB) + nav() + phead(Pn, region, f'Plumber in {place}, for builds done right.', blurb, img=K[0], path='/'+slug) + f'''
{section('<div class="blocks">' + split(K[1], inner1, False, f' in {Pn}') + gstrip(K[2:5], Pn) + split(K[5], inner2, True, f' in {Pn}') + '</div>')}
{areas_block('Other areas we cover.', slug)}
{faq_block(afaqs)}
{quote_form(img=K[6])}''' + foot() + tail()

# ---------------- BUILDERS ----------------
pages['builders.html'] = head('Plumber for Builders, Sydney | LPS Plumbing Group',
    'A plumbing partner for high end builders in Sydney. Priced from your plans, delivered to program. Send plans or call Lewis on 0452 611 522.', '/builders') + nav(cur='/builders') + phead('For builders', 'For builders', 'A plumber that keeps your program moving.', 'We partner with builders on high end homes, renovations and multi unit projects. Send through plans and we will price the full plumbing scope.', img='kitchen', path='/builders') + f'''
{steps_block('How we work with builders.', 'Four clear stages, lined up with your program from the first set out to handover.')}
{collab_block('Why builders use LPS.', ('laundry', 'kitchensink', 'commercial', 'stone'))}
{builders_block()}
{creds_block()}
{checklist_cta()}
{quote_form('Send the plans.', 'Attach a link to your plans or scope and we will come back with a full plumbing price.', 'bathreno')}''' + foot() + tail()

# ---------------- QUOTE ----------------
pages['quote.html'] = head('Get a Plumbing Quote | LPS Plumbing Group',
    'Request a quote from LPS Plumbing Group. Send plans or photos and get a clear, itemised price. Or call Lewis on 0452 611 522.', '/quote') + nav() + phead('Get a quote', 'Get a quote', 'Tell us about the job.', 'Builders, homeowners and developers. Send the details and we reply within one business day.', False, img='basin', path='/quote') + quote_form(img='stone') + steps_block(link=False) + foot() + tail()

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
cards = ''.join(f'<article class="pc rv"><img src="{W(i)}" alt="{t}" loading="lazy"><small>{k}</small><h3>{t}</h3><p>{d}</p></article>' for i, k, t, d in projs)
cases = ''.join(split(c['img'], f'<span class="lbl">{c["suburb"]} · Builder: {c["builder"]}</span><h2 class="h-lg">{hd(c["title"]+".")}</h2><p class="lead"><b>Scope.</b> {c["scope"]}</p><p class="lead"><b>Result.</b> {c["result"]}</p>') for c in CASES)
pages['projects.html'] = head('Plumbing Projects | LPS Plumbing Group, Sydney',
    'Recent new builds, renovations, bathrooms and commercial plumbing projects by LPS Plumbing Group across Sydney.', '/projects') + nav(cur='/projects') + phead('Projects', 'Projects', 'Recent work.', 'A look at recent builds, renovations and bathrooms we have plumbed across Sydney.', img='bathreno', path='/projects', video='shower') + f'''
{section('<div class="blocks">' + cases + '</div>') if CASES else ''}
{section(f'<div class="pgrid">{cards}</div>')}
{reviews_block()}
{quote_form(img='stone')}''' + foot() + tail()

# ---------------- ABOUT ----------------
about_inner = f"""<h2 class="h-lg">Built on doing it once, properly<span class="dot">.</span></h2>
<p class="lead">With over 8 years in the trade, Lewis started LPS to deliver the kind of plumbing he would want in his own home. The focus is high end residential builds and renovations, where the detail is on show and the standard can't slip.</p>
<p class="lead">The market is full of cheap plumbing. We are not trying to be the cheapest. We are trying to be the plumber you never have to call back.</p>
<p class="lead">We are growing. If you are a plumber who takes pride in the finish, <a href="{L('/careers')}" style="color:var(--sea-dk);font-weight:600">come work with us</a>.</p>"""
pages['about.html'] = head('About LPS Plumbing Group | Lewis Slatter, Director',
    'LPS Plumbing Group is led by director Lewis Slatter, with 8+ years plumbing high end homes across Sydney. Licensed and insured.', '/about') + nav(cur='/about') + phead('About', 'About', 'Small crew. High standards.', 'LPS Plumbing Group is a licensed plumbing, drainage and gas fitting business led by director Lewis Slatter.', img='lewis', path='/about') + f'''
{section(split('ensuite', about_inner) + gstrip(['kitchen', 'basin', 'shower']))}
{collab_block('What you can expect.', ('miranda', 'sink', 'bathreno', 'laundry'))}
{reviews_block()}
{creds_block()}
{quote_form(img='gooseneck')}''' + foot() + tail()

# ---------------- CAREERS ----------------
roles = """<div class="cards2">
  <article class="card rv"><small>Full time</small><h3>Plumber</h3><p>Licensed, or close to it. You can run a rough in and fit off on a high end build without being chased, and you care what the finished wall looks like.</p></article>
  <article class="card rv"><small>Apprenticeship</small><h3>Apprentice plumber</h3><p>Already in your apprenticeship, or keen to start. You turn up, listen and want to learn the trade properly on quality work.</p></article>
</div>"""
why_w = '<div class="steps" style="--n:3">' + ''.join(f'<div class="step rv"><b>0{i+1}</b><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate([('Quality work, every day', 'Architect designed homes, renovations and bathrooms with premium fixtures. No cheap jobs done fast.'), ('Learn from the director', 'You work alongside Lewis, not three layers of management. Straight feedback, real progression.'), ('Steady builder work', 'Repeat work from builders, so the diary stays full and you are not sitting around waiting for jobs.')])) + '</div>'
pages['careers.html'] = head('Plumbing Jobs Sydney | Work with LPS Plumbing Group',
    'LPS Plumbing Group is hiring plumbers and apprentices for high end builds across Sydney. Apply in two minutes or call Lewis on 0452 611 522.', '/careers') + nav() + phead('Careers', 'We are hiring', 'Work on builds worth your name.', 'We are growing the crew to keep up with high end builders across Sydney. If you take pride in the finish, we want to hear from you.', False, img='commercial', path='/careers', extra=f'<div class="cta-row rv">{btn("#apply", "Apply in two minutes")}</div>') + f'''
{section(sec_head('Open roles.') + roles)}
{section(sec_head('Why work at LPS.') + why_w)}
<section class="sec" id="apply"><div class="wrap"><div class="inner contact">
  {cimg('laundry', 'Two minutes. No resume needed.', f'Fill this in and Lewis will give you a call. Got a resume? Add a link or email it to {EMAIL}.', f'<div class="c-list"><a href="tel:{TEL}"><span>Rather chat?</span><b>Call {PHONE}</b></a></div>')}
  <form class="c-form rv" id="quoteForm" action="{form_action()}" method="POST" onsubmit="handleSubmit(event)">
    {hidden('Job application: LPS Plumbing Group website')}
    <h2>Apply now<span class="dot">.</span></h2><p class="sub">Lewis calls every applicant back.</p>
    <div class="qf-g">
      <label class="qf-f"><span>Name *</span><input type="text" name="name" required autocomplete="name"></label>
      <label class="qf-f"><span>Phone *</span><input type="tel" name="phone" required autocomplete="tel"></label>
      <label class="qf-f qf-w"><span>Email *</span><input type="email" name="email" required autocomplete="email"></label>
      <label class="qf-f"><span>Role *</span><select name="role" required><option value="">Select</option><option>Plumber</option><option>Apprentice plumber</option><option>Other</option></select></label>
      <label class="qf-f"><span>Years in the trade</span><input type="text" name="experience" inputmode="numeric"></label>
      <label class="qf-f"><span>Licence number <em>(if any)</em></span><input type="text" name="licence"></label>
      <label class="qf-f"><span>Where are you based? *</span><input type="text" name="suburb" required></label>
      <label class="qf-f qf-w"><span>Driver's licence and White Card?</span><select name="tickets"><option>Both</option><option>Driver's licence only</option><option>White Card only</option><option>Neither yet</option></select></label>
      <label class="qf-f qf-w"><span>Tell us about yourself</span><textarea name="message" rows="3" placeholder="Recent jobs, what you're after, resume link"></textarea></label>
    </div>
    <button type="submit" class="btn btn-sea qf-btn">Send application {ARR}</button>
    <div id="formStatus" role="status"></div>
  </form>
</div></div></section>''' + foot() + tail()

# ---------------- BUILDER CHECKLIST (lead magnet) ----------------
pages['builders-checklist.html'] = head("Builder's Plumbing Checklist | LPS Plumbing Group",
    'Free plumbing checklist for builders: what to lock in before pricing, slab, rough in and handover so plumbing never holds up your program.', '/builders-checklist') + nav() + phead('Builder checklist', 'Free for builders', "The builder's plumbing checklist.", 'What to lock in before pricing, slab, rough in, fit off and handover, so plumbing never holds up your program. One page, free.', False, img='laundry', path='/builders-checklist') + f'''
<section class="sec"><div class="wrap"><div class="inner split" style="align-items:start">
  <div class="rv">
    <h2 class="h-lg">What's inside<span class="dot">.</span></h2>
    <ul class="cklist">
      <li><b>Before pricing</b>Plans, selections and site info a plumber needs to give you a real price</li>
      <li><b>Before the slab</b>Set out, sewer and stormwater checks that save a jackhammer later</li>
      <li><b>Rough in</b>Heights, mixer bodies and niches to confirm before walls close</li>
      <li><b>Fit off</b>What needs to be on site so fit off happens in one visit</li>
      <li><b>Handover</b>The compliance paperwork your certifier will ask for</li>
    </ul>
  </div>
  <form class="c-form rv" id="ckForm" action="{form_action()}" method="POST">
    {hidden('Builder checklist download: LPS website')}
    <h2>Get the checklist<span class="dot">.</span></h2><p class="sub">Download straight away, no spam.</p>
    <div class="qf-g">
      <label class="qf-f"><span>Name *</span><input type="text" name="name" required autocomplete="name"></label>
      <label class="qf-f"><span>Company *</span><input type="text" name="company" required autocomplete="organization"></label>
      <label class="qf-f qf-w"><span>Email *</span><input type="email" name="email" required autocomplete="email"></label>
      <label class="qf-f qf-w"><span>Phone</span><input type="tel" name="phone" autocomplete="tel"></label>
    </div>
    <button type="submit" class="btn btn-sea qf-btn">Get the checklist {ARR}</button>
    <div id="ckDone" hidden style="margin-top:16px;padding:16px;border-radius:12px;background:#fff"><b style="color:var(--teal)">Here you go.</b> <a href="{L('/lps-builders-plumbing-checklist.pdf')}" target="_blank" rel="noopener" style="color:var(--sea-dk);font-weight:600">Download the checklist (PDF)</a></div>
  </form>
</div></div></section>
<script>document.addEventListener('DOMContentLoaded',function(){{var f=document.getElementById('ckForm');if(!f)return;f.addEventListener('submit',function(e){{e.preventDefault();var b=f.querySelector('button');b.disabled=true;fetch(f.action,{{method:'POST',body:new FormData(f),headers:{{Accept:'application/json'}}}}).finally(function(){{f.querySelector('.qf-g').hidden=true;b.hidden=true;document.getElementById('ckDone').hidden=false;if(typeof gtag==='function')gtag('event','generate_lead',{{form:'builder_checklist'}});if(typeof fbq==='function')fbq('track','Lead');}});}});}});</script>
''' + foot() + tail()

# ---------------- GUIDES ----------------
gcards = ''
for g in GUIDES:
    url = '/' + g['slug']
    body = ''.join(f'<h2>{h}</h2><p>{t}</p>' for h, t in g['sections'])
    art = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"Article","headline":g['title'],"description":g['meta'],"image":SHARE_HOST+'/img/'+LOCAL[g['img']],"author":{"@type":"Person","name":"Lewis Slatter"},"publisher":{"@type":"Organization","name":"LPS Plumbing Group"},"mainEntityOfPage":DOMAIN+url,"dateModified":datetime.date.today().isoformat()}) + '</script>'
    sv = g['service']
    pages[g['slug'] + '.html'] = head(g['title'] + ' | LPS', g['meta'], url, art) + nav(cur='/guides') + phead('Guides', 'Guide', g['h1'], g['lead'], False, img=g['img'], path=url) + f'''
{section(f"""<div class="guide-grid">
    <div class="prose rv">{body}<p style="margin-top:28px">Written by Lewis Slatter, director of LPS Plumbing Group (Lic {LIC}).</p></div>
    <aside class="rv"><div class="split-img"><img src="{W(g['img2'])}" alt="{alt(g['img2'])}" loading="lazy"></div><div class="cta-row" style="margin-top:18px">{btn(L('/quote'), 'Get a quote')}{btn(L('/'+sv[0]), 'More on '+sv[1].lower(), 'ghost')}</div></aside>
  </div>""")}
{quote_form(img=[k for k in POOL if k not in (g['img'], g['img2'])][0])}''' + foot() + tail()
    gcards += f'<a class="gcard rv" href="{L(url)}"><div><img src="{W(g["img"])}" alt="{alt(g["img"])}" loading="lazy"></div><div><small>Guide</small><h3>{g["title"]}</h3><p>{g["meta"]}</p></div></a>'
pages['guides.html'] = head('Plumbing Guides for Builders & Homeowners | LPS', 'Practical plumbing guides from LPS Plumbing Group: build timelines, renovating older homes and what to do in a plumbing emergency.', '/guides') + nav(cur='/guides') + phead('Guides', 'Guides', 'Plumbing guides, straight from the trade.', 'Practical advice for builders and homeowners from director Lewis Slatter.', False, img='stone', path='/guides') + f'''
{section(f'<div class="pgrid">{gcards}</div>')}
{quote_form(img='miranda')}''' + foot() + tail()

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
from PIL import Image as _Img
_IMGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'img')
def _resp(c):
    import re as _re
    def fix(m):
        tag, name = m.group(0), m.group(1)
        p = os.path.join(_IMGDIR, name + '.webp')
        if not os.path.exists(p) or 'srcset=' in tag: return tag
        w, h = _Img.open(p).size
        extra = f' srcset="{BASE}/img/{name}-800.webp 800w, {BASE}/img/{name}.webp {w}w" sizes="(max-width: 700px) 100vw, 50vw" width="{w}" height="{h}" decoding="async"'
        return tag[:-1] + extra + '>'
    return _re.sub(r'<img [^>]*src="[^"]*/img/([a-z0-9-]+?)\.webp"[^>]*>', fix, c)
pages = {k: _resp(v) for k, v in pages.items()}
for f, c in pages.items():
    os.makedirs(os.path.dirname(os.path.join(OUT, f)), exist_ok=True)
    open(os.path.join(OUT, f), 'w').write(c)

indexable = [p for p in pages if p not in ('thank-you.html', '404.html')]
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{"" if p=="index.html" else p[:-5]}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n' for p in indexable) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
if not BASE:
    open(os.path.join(OUT, 'vercel.json'), 'w').write(json.dumps({"cleanUrls": True, "trailingSlash": False,
        "redirects": [{"source": a, "destination": b, "permanent": True} for a, b in [
            ("/service-page/drainage-inspection", "/drainage"), ("/service-page/gas-fitting", "/gas-fitting"), ("/service-page/general-plumbing", "/services"),
            ("/portfolio-collections/my-portfolio/outdoor-plumbing-installations", "/projects"), ("/portfolio-collections/my-portfolio/modern-bathroom-renovations", "/bathrooms"),
            ("/portfolio-collections/my-portfolio", "/projects"), ("/portfolio", "/projects"), ("/book-online", "/quote")]],
        "headers": [
            {"source": "/(.*)", "has": [{"type": "host", "value": "lps.latitudemarketing.au"}], "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]},
            {"source": "/(.*)", "has": [{"type": "host", "value": "(?<sub>.*)\\.vercel\\.app"}], "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]},
            {"source": "/img/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}]}, indent=2))
print(len(pages), 'pages')

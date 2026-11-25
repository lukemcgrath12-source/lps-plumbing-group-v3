/* LPS Plumbing Group site behaviour */

/* HOLD SCREEN */
window.addEventListener('load', function () {
  setTimeout(function () {
    var h = document.getElementById('hold');
    if (h) h.classList.add('exit');
  }, 1150);
});

/* NAV: shadow, hide-on-scroll, mobile call bar */
(function () {
  var nav = document.getElementById('navwrap'),
      bar = document.getElementById('callbar'),
      last = 0;
  if (!nav) return;
  window.addEventListener('scroll', function () {
    var y = window.pageYOffset;
    nav.classList.toggle('scrolled', y > 20);
    if (y > last && y > 420) { nav.classList.add('hide'); } else { nav.classList.remove('hide'); }
    if (bar) bar.classList.toggle('show', y > 560);
    last = y;
  }, { passive: true });
})();

/* MOBILE SHEET */
(function () {
  var layer = document.getElementById('sheetLayer'),
      open  = document.getElementById('menuBtn'),
      close = document.getElementById('sheetClose'),
      bd    = document.getElementById('sheetBd');
  if (!layer || !open) return;
  function set(o) {
    layer.classList.toggle('open', o);
    document.body.style.overflow = o ? 'hidden' : '';
  }
  open.addEventListener('click', function () { set(true); });
  if (close) close.addEventListener('click', function () { set(false); });
  if (bd) bd.addEventListener('click', function () { set(false); });
  layer.querySelectorAll('.sheet-nav a').forEach(function (a) {
    a.addEventListener('click', function () { set(false); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
})();

/* FAQ ACCORDION */
document.querySelectorAll('.fq-q').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var fq = btn.parentElement,
        a = fq.querySelector('.fq-a'),
        isOpen = fq.classList.contains('open');
    document.querySelectorAll('.fq.open').forEach(function (o) {
      o.classList.remove('open');
      o.querySelector('.fq-a').style.maxHeight = null;
      o.querySelector('.fq-q').setAttribute('aria-expanded', 'false');
    });
    if (!isOpen) {
      fq.classList.add('open');
      a.style.maxHeight = a.scrollHeight + 'px';
      btn.setAttribute('aria-expanded', 'true');
    }
  });
});

/* SCROLL REVEAL */
(function () {
  var els = document.querySelectorAll('.rv');
  if (!('IntersectionObserver' in window)) {
    els.forEach(function (e) { e.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en, i) {
      if (en.isIntersecting) {
        var el = en.target;
        setTimeout(function () { el.classList.add('in'); }, (i % 4) * 70);
        io.unobserve(el);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
  els.forEach(function (e) { io.observe(e); });
})();

/* FOOTER YEAR */
(function () {
  var y = document.getElementById('yr');
  if (y) y.textContent = new Date().getFullYear();
})();

/* QUOTE FORM — fires GA4 generate_lead on success */
async function handleSubmit(event) {
  event.preventDefault();
  var form = event.target,
      status = document.getElementById('formStatus'),
      btn = form.querySelector('button[type="submit"]'),
      roll = btn ? btn.querySelector('.roll i') : null;
  if (btn) btn.disabled = true;
  if (roll) roll.style.opacity = '.6';
  try {
    var r = await fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    });
    if (r.ok) {
      if (typeof fbq === 'function') fbq('track', 'Lead');
      if (typeof gtag === 'function') {
        gtag('event', 'generate_lead', {
          'form_name': 'quote_request',
          'form_destination': form.action
        });
      }
      form.reset();
      status.style.display = 'block';
      status.style.background = 'rgba(62,140,119,.16)'; status.style.marginTop='14px'; status.style.borderRadius='12px';
      status.style.color = 'var(--text)';
      status.textContent = "Thanks, your enquiry's in. Lewis will be in touch within one business day.";
    } else {
      throw new Error('fail');
    }
  } catch (err) {
    status.style.display = 'block';
    status.style.background = 'rgba(220,53,69,.1)';
    status.style.color = '#b02a37';
    status.innerHTML = 'Something went wrong. Call us on <a href="tel:0452611522" style="color:#b02a37;font-weight:600;">0452 611 522</a>.';
  } finally {
    if (btn) btn.disabled = false;
    if (roll) roll.style.opacity = '1';
  }
}


/* click to call + email tracking */
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href^="tel:"],a[href^="mailto:"],a[href^="sms:"],a[href*="wa.me"]'):null;if(!a||typeof gtag!=='function')return;var h=a.getAttribute('href');var ev=h.indexOf('tel:')===0?'click_to_call':h.indexOf('sms:')===0?'click_to_text':h.indexOf('wa.me')>-1?'click_to_whatsapp':'email_click';gtag('event',ev,{page_path:location.pathname});if(typeof fbq==='function'&&ev!=='email_click')fbq('track','Contact');},true);

/* SLIDERS: arrows + drag (recent work, reviews) */
document.querySelectorAll('[data-slider]').forEach(function (wrap) {
  var track = wrap.querySelector('.slider-track'), prev = wrap.querySelector('.sl-prev'), next = wrap.querySelector('.sl-next');
  if (!track) return;
  var step = function () { var c = track.children[0]; return c ? c.getBoundingClientRect().width + 20 : 400; };
  if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
  if (next) next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
  var sync = function () {
    if (prev) prev.disabled = track.scrollLeft < 8;
    if (next) next.disabled = track.scrollLeft + track.clientWidth > track.scrollWidth - 8;
  };
  track.addEventListener('scroll', sync, { passive: true }); window.addEventListener('resize', sync); sync();
  var down = false, sx = 0, sl = 0, moved = false;
  track.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = track.scrollLeft; track.classList.add('drag'); });
  window.addEventListener('pointermove', function (e) { if (!down) return; var dx = e.clientX - sx; if (Math.abs(dx) > 4) moved = true; track.scrollLeft = sl - dx; });
  window.addEventListener('pointerup', function () { if (!down) return; down = false; track.classList.remove('drag'); });
  track.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
});
/* FEATURED WORK TABS */
(function () {
  var fw = document.getElementById('fw');
  if (!fw) return;
  var imgs = fw.querySelectorAll('.fw-img video'), tabs = fw.querySelectorAll('.fw-tab'),
      t = document.getElementById('fwT'), d = document.getElementById('fwD'), cur = 0, timer;
  function go(i) {
    cur = i;
    imgs.forEach(function (im, k) { im.classList.toggle('on', k === i); if (k === i) { window.lpsPlay && window.lpsPlay(im); } else { im.pause(); } });
    tabs.forEach(function (b, k) { b.classList.toggle('on', k === i); b.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
    t.textContent = tabs[i].dataset.t; d.textContent = tabs[i].dataset.d;
  }
  function auto() { clearInterval(timer); timer = setInterval(function () { go((cur + 1) % tabs.length); }, 6000); }
  tabs.forEach(function (b, k) { b.addEventListener('click', function () { go(k); auto(); }); });
  auto();
})();


/* AREA MAP */
window.addEventListener('load', function () {
  var el = document.getElementById('map');
  if (!el || !window.L) return;
  var pts = JSON.parse(el.dataset.pts);
  var m = L.map(el, { scrollWheelZoom: false, zoomControl: true, attributionControl: true });
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap contributors', maxZoom: 18 }).addTo(m);
  
  var b = [];
  pts.forEach(function (p) {
    var mk = L.marker(p.ll, { icon: L.divIcon({ className: '', html: '<div class="pin' + (p.h ? ' here' : '') + '"></div>', iconSize: [30, 30], iconAnchor: [15, 30] }), title: p.n }).addTo(m);
    mk.bindTooltip(p.n, { permanent: !!p.h, direction: 'top', offset: [0, -30], className: 'pin-tip' });
    mk.on('click', function () { location.href = p.u; });
    b.push(p.ll);
  });
  m.fitBounds(b, { padding: [50, 50] });
});

/* REVIEWS: one at a time */
(function () {
  var s = document.querySelectorAll('.rev-slide'), i = 0, imgs = document.querySelectorAll('.rev-img img');
  if (s.length < 2) return;
  var c = document.getElementById('revCount');
  function show(n) {
    s[i].classList.remove('on'); if (imgs[i % imgs.length]) imgs[i % imgs.length].classList.remove('on');
    i = (n + s.length) % s.length;
    s[i].classList.add('on'); if (imgs[i % imgs.length]) imgs[i % imgs.length].classList.add('on');
    if (c) c.textContent = (i + 1) + ' / ' + s.length;
  }
  document.querySelectorAll('[data-rev]').forEach(function (b) {
    b.addEventListener('click', function () { show(i + (+b.dataset.rev)); });
  });
})();


/* VIDEO: load when near view, play only while visible, hover play on service cards */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function load(v) {
    if (v.dataset.loaded) return;
    var s = v.querySelector('source[data-src]');
    if (s && !s.getAttribute('src')) { s.src = s.dataset.src; v.load(); }
    v.dataset.loaded = '1';
  }
  window.lpsPlay = function (v) { load(v); v.muted = true; v.setAttribute('muted', ''); var p = v.play(); if (p && p.catch) p.catch(function () {}); };
  var auto = Array.prototype.slice.call(document.querySelectorAll('video[autoplay]'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (v.closest('.fw-img') && !v.classList.contains('on')) return;
        if (v.dataset.paused) return;
        if (e.isIntersecting) window.lpsPlay(v); else v.pause();
      });
    }, { rootMargin: '200px 0px' });
    auto.forEach(function (v) { io.observe(v); });
  }
  /* phones in low power mode block autoplay until the first tap or scroll: start visible videos then */
  function kick() {
    auto.forEach(function (v) { if (v.dataset.paused || (v.closest('.fw-img') && !v.classList.contains('on'))) return; var r = v.getBoundingClientRect(); if (r.bottom > 0 && r.top < innerHeight) window.lpsPlay(v); });
  }
  ['touchstart', 'pointerdown', 'scroll', 'keydown'].forEach(function (ev) { window.addEventListener(ev, kick, { passive: true, once: true }); });
  window.addEventListener('pageshow', kick);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) kick(); });
  setTimeout(kick, 300);
  document.querySelectorAll('.sc').forEach(function (c) {
    var v = c.querySelector('.sc-vid');
    if (!v || !window.matchMedia('(hover: hover)').matches) return;
    c.addEventListener('mouseenter', function () { c.classList.add('playing'); window.lpsPlay(v); });
    c.addEventListener('mouseleave', function () { c.classList.remove('playing'); v.pause(); });
  });
  document.querySelectorAll('.vid-btn').forEach(function (b) {
    var v = b.parentElement.querySelector('video');
    b.addEventListener('click', function () {
      if (v.paused) { delete v.dataset.paused; window.lpsPlay(v); b.setAttribute('aria-label', 'Pause video'); b.innerHTML = '<svg viewBox="0 0 24 24"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'; }
      else { v.pause(); v.dataset.paused = '1'; b.setAttribute('aria-label', 'Play video'); b.innerHTML = '<svg viewBox="0 0 24 24"><path d="M7 5l12 7-12 7z"/></svg>'; }
    });
  });
})();

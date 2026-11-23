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
      if (typeof gtag === 'function') {
        gtag('event', 'generate_lead', {
          'form_name': 'quote_request',
          'form_destination': form.action
        });
      }
      form.reset();
      status.style.display = 'block';
      status.style.background = 'rgba(62,140,119,.16)';
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
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href^="tel:"],a[href^="mailto:"]'):null;if(!a||typeof gtag!=='function')return;var h=a.getAttribute('href');if(h.indexOf('tel:')===0)gtag('event','click_to_call',{page_path:location.pathname});else gtag('event','email_click',{page_path:location.pathname});},true);

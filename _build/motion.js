/* LPS v3 motion: Lenis smooth scroll + calm GSAP reveals */
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!window.gsap || !window.ScrollTrigger) { return; }
  gsap.registerPlugin(ScrollTrigger);
  document.documentElement.classList.add('js-motion');
  var base = (window.LPS_LD || 0) + 0.1;

  var lenis = window.Lenis ? new Lenis({ lerp: 0.09, smoothWheel: true }) : null;
  if (lenis) {
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function(t){ lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    document.querySelectorAll('a[href^="#"]').forEach(function(a){
      a.addEventListener('click', function(e){ var h = a.getAttribute('href'); if (h.length < 2) return; var t = document.querySelector(h); if (t) { e.preventDefault(); lenis.scrollTo(t, { offset: -90 }); } });
    });
  }

  /* headings: words rise into place */
  document.querySelectorAll('[data-lines]').forEach(function(el){
    var nodes = Array.prototype.slice.call(el.childNodes), out = [];
    nodes.forEach(function(n){
      if (n.nodeType === 3) { n.textContent.split(/(\s+)/).forEach(function(w){ if (!w) return; out.push(/^\s+$/.test(w) ? w : '<span class="ln-wrap" style="display:inline-block"><span class="ln-in">'+w+'</span></span>'); }); }
      else out.push('<span class="ln-wrap" style="display:inline-block"><span class="ln-in">'+n.outerHTML+'</span></span>');
    });
    el.innerHTML = out.join('');
    var now = el.dataset.lines === 'now' || !!el.closest('.hero');
    gsap.from(el.querySelectorAll('.ln-in'), { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: 0.035,
      delay: now ? base : 0, scrollTrigger: now ? null : { trigger: el, start: 'top 88%' } });
  });

  /* grouped items rise in with a stagger */
  var GROUP = '.sc, .step, .pt, .cr, .stat, .pc, .fq, .gcard, .card, .igp';
  ScrollTrigger.batch(GROUP, { start: 'top 92%', once: true,
    onEnter: function(b){ gsap.fromTo(b, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', stagger: 0.09, overwrite: true }); } });

  /* generic reveals */
  var heroI = 0;
  gsap.utils.toArray('.rv').forEach(function(el){
    if (el.matches(GROUP) && !el.closest('.hero')) { gsap.set(el, { opacity: 0, y: 40 }); return; }
    var inHero = !!el.closest('.hero');
    gsap.to(el, { opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', delay: inHero ? base + 0.35 + (heroI++) * 0.08 : 0,
      scrollTrigger: inHero ? null : { trigger: el, start: 'top 90%' } });
  });

  /* hero media settles in */
  document.querySelectorAll('.hero-media').forEach(function(m){
    gsap.from(m, { clipPath: 'inset(8% 8% 8% 8% round 28px)', duration: 1.5, ease: 'expo.out', delay: base });
    var v = m.querySelector('img,video');
    if (v) gsap.to(v, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: m, start: 'top top', end: 'bottom top', scrub: true } });
  });

  /* images: open from a soft inset and settle from a zoom */
  var REVEAL = '.split-img, .gstrip figure, .mosaic img, .c-img, .gcard>div:first-child, .rev-img';
  gsap.utils.toArray(REVEAL).forEach(function(el){
    var r = getComputedStyle(el).borderRadius || '24px';
    var st = { trigger: el, start: 'top 90%', once: true };
    gsap.fromTo(el, { clipPath: 'inset(12% 8% 12% 8% round ' + r + ')' }, { clipPath: 'inset(0% 0% 0% 0% round ' + r + ')', duration: 1.5, ease: 'expo.out', scrollTrigger: st });
    var m = el.matches('img') ? null : el.querySelector('img,video');
    if (m) gsap.fromTo(m, { scale: 1.22 }, { scale: 1.04, duration: 2, ease: 'expo.out', scrollTrigger: st });
  });
  /* gentle parallax inside large images */
  gsap.utils.toArray('.split-img img, .c-img>img, .c-img>video, .sc>img').forEach(function(m){
    gsap.fromTo(m, { yPercent: -4 }, { yPercent: 4, ease: 'none', scrollTrigger: { trigger: m.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* count up */
  document.querySelectorAll('[data-count]').forEach(function(el){
    var end = +el.dataset.count, o = { v: 0 };
    gsap.to(o, { v: end, duration: 1.8, ease: 'power2.out', delay: el.closest('.stats') ? base + 0.4 : 0, scrollTrigger: { trigger: el, start: 'top 95%', once: true }, onUpdate: function(){ el.textContent = Math.round(o.v); } });
  });

  /* featured work zooms gently while in view */
  var fw = document.querySelector('.fw-img');
  if (fw) gsap.fromTo(fw, { scale: 1.08 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: fw.parentElement, start: 'top bottom', end: 'center center', scrub: true } });

  window.addEventListener('load', function(){ ScrollTrigger.refresh(); });
})();

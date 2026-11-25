/* LPS v3 motion: Lenis smooth scroll + calm GSAP reveals */
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !window.gsap || !window.ScrollTrigger) { return; }
  gsap.registerPlugin(ScrollTrigger);
  document.documentElement.classList.add('js-motion');
  var hold = document.getElementById('hold');
  var base = hold ? 1.1 : 0.15;

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

  /* generic reveals */
  var heroI = 0;
  gsap.utils.toArray('.rv').forEach(function(el){
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

  /* featured work zooms gently while in view */
  var fw = document.querySelector('.fw-img');
  if (fw) gsap.fromTo(fw, { scale: 1.08 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: fw.parentElement, start: 'top bottom', end: 'center center', scrub: true } });

  window.addEventListener('load', function(){ ScrollTrigger.refresh(); });
})();

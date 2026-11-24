/* LPS v2 motion: Lenis smooth scroll + GSAP ScrollTrigger */
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !window.gsap || !window.ScrollTrigger) { document.querySelectorAll('.rv').forEach(function(e){e.classList.add('in')}); return; }
  gsap.registerPlugin(ScrollTrigger);
  document.documentElement.classList.add('js-motion');

  var lenis = window.Lenis ? new Lenis({ lerp: 0.085, smoothWheel: true }) : null;
  if (lenis) {
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function(t){ lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    document.querySelectorAll('a[href^="#"]').forEach(function(a){
      a.addEventListener('click', function(e){ var t = document.querySelector(a.getAttribute('href')); if (t) { e.preventDefault(); lenis.scrollTo(t, { offset: -80 }); } });
    });
  }

  /* headings: pre-split lines rise in */
  document.querySelectorAll('[data-lines]').forEach(function(el){
    var now = el.dataset.lines === 'now';
    gsap.from(el.querySelectorAll('.ln-in'), { yPercent: 115, duration: 1.2, ease: 'expo.out', stagger: 0.09,
      delay: now ? 2.05 : 0, scrollTrigger: now ? null : { trigger: el, start: 'top 88%' } });
  });

  /* generic reveals: quick, once, nothing left half-faded */
  var heroI = 0;
  gsap.utils.toArray('.rv').forEach(function(el){
    var inHero = !!el.closest('.h2x,.vh');
    if (inHero) { gsap.to(el, { opacity: 1, y: 0, duration: 1, ease: 'expo.out', delay: 2.1 + (heroI++) * 0.08 }); return; }
    ScrollTrigger.create({ trigger: el, start: 'top 96%', once: true,
      onEnter: function(){ gsap.to(el, { opacity: 1, y: 0, duration: 0.75, ease: 'power3.out' }); } });
  });

  /* image wipes + parallax */
  gsap.utils.toArray('.clip').forEach(function(el){
    gsap.to(el, { clipPath: 'inset(0% 0 0 0)', duration: 1.4, ease: 'expo.inOut', delay: el.dataset.delay ? +el.dataset.delay : 0, scrollTrigger: { trigger: el, start: 'top 85%' } });
  });
  gsap.utils.toArray('[data-par]').forEach(function(img){
    gsap.fromTo(img, { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* statement: rises in once, fully visible */
  document.querySelectorAll('.stmt p.big').forEach(function(p){
    gsap.from(p, { opacity: 0, y: 30, duration: 0.9, ease: 'power3.out', scrollTrigger: { trigger: p, start: 'top 92%', once: true } });
  });

  /* count up */
  document.querySelectorAll('[data-count]').forEach(function(el){
    var end = +el.dataset.count, suf = el.dataset.suf || '', o = { v: 0 };
    gsap.to(o, { v: end, duration: 1.8, ease: 'power2.out', scrollTrigger: { trigger: el, start: 'top 90%' }, onUpdate: function(){ el.textContent = Math.round(o.v) + suf; } });
  });

  /* stacked service cards shrink as next one arrives */
  var cards = gsap.utils.toArray('.scard');
  cards.forEach(function(c, i){
    var img = c.querySelector('.scard-m img');
    if (img) gsap.to(img, { scale: 1, ease: 'none', scrollTrigger: { trigger: c, start: 'top bottom', end: 'top 100px', scrub: true } });
    if (i < cards.length - 1) gsap.to(c, { scale: 0.92, filter: 'brightness(0.7)', ease: 'none', scrollTrigger: { trigger: cards[i+1], start: 'top bottom', end: 'top 96px', scrub: true } });
  });

  window.addEventListener('load', function(){ ScrollTrigger.refresh(); });
})();

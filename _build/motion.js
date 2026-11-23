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

  /* generic reveals */
  var heroI = 0;
  gsap.utils.toArray('.rv').forEach(function(el){
    var inHero = !!el.closest('.h2x,.vh');
    var d = inHero ? 2.2 + (heroI++) * 0.1 : 0;
    gsap.to(el, { opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', delay: d, scrollTrigger: inHero ? null : { trigger: el, start: 'top 90%' } });
  });

  /* image wipes + parallax */
  gsap.utils.toArray('.clip').forEach(function(el){
    gsap.to(el, { clipPath: 'inset(0% 0 0 0)', duration: 1.4, ease: 'expo.inOut', delay: el.dataset.delay ? +el.dataset.delay : 0, scrollTrigger: { trigger: el, start: 'top 85%' } });
  });
  gsap.utils.toArray('[data-par]').forEach(function(img){
    gsap.fromTo(img, { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* statement: words light up as you scroll */
  document.querySelectorAll('.stmt p.big').forEach(function(p){
    p.innerHTML = p.textContent.trim().split(/\s+/).map(function(w){ return '<span class="w">'+w+'</span>'; }).join(' ');
    gsap.to(p.querySelectorAll('.w'), { opacity: 1, stagger: 0.06, ease: 'none', scrollTrigger: { trigger: p, start: 'top 80%', end: 'bottom 45%', scrub: true } });
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

  /* horizontal gallery pinned on desktop */
  ScrollTrigger.matchMedia({
    '(min-width: 900px)': function(){
      var sec = document.querySelector('.hz'), track = document.querySelector('.hz-track');
      if (!sec || !track) return;
      var dist = function(){ return Math.max(0, track.scrollWidth - window.innerWidth + 60); };
      gsap.to(track, { x: function(){ return -dist(); }, ease: 'none',
        scrollTrigger: { trigger: sec, start: 'top top', end: function(){ return '+=' + dist(); }, pin: true, scrub: 1, invalidateOnRefresh: true } });
    }
  });

  window.addEventListener('load', function(){ ScrollTrigger.refresh(); });
})();

/* Núcleo do estudo "O que vale mais?": relógio e laço de animação, telas (canvas), formatação em pt-BR, guia de passos,
   progresso, trava de ordem (só na versão publicada) e menu livre do desenvolvimento. Sem dependências. */
(function () {
  'use strict';
  var OVM = window.OVM = window.OVM || {};
  OVM.dev = !!window.OVM_DEV;
  OVM.reduz = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  OVM.dpr = Math.min(2, window.devicePixelRatio || 1);
  OVM.t = 0;
  OVM.parte = +(document.body.getAttribute('data-parte') || 0);
  OVM.total = 10;

  // ---------------------------------------------------------------- utilidades
  OVM.$ = function (s, r) { return (r || document).querySelector(s); };
  OVM.$$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  OVM.clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  OVM.lerp = function (a, b, t) { return a + (b - a) * t; };
  OVM.suave = function (t) { t = OVM.clamp(t, 0, 1); return t * t * (3 - 2 * t); };
  OVM.saida = function (t) { t = OVM.clamp(t, 0, 1); return 1 - Math.pow(1 - t, 3); };
  OVM.mapa = function (v, a, b, c, d) { return c + (d - c) * ((v - a) / (b - a)); };
  OVM.fonte = function (px, peso, serif) { return (peso || 400) + ' ' + px + 'px ' + (serif ? 'Newsreader, Georgia, serif' : 'Inter, system-ui, sans-serif'); };

  // gerador pseudoaleatório com semente (mulberry32): o mesmo céu em toda visita
  OVM.rand = function (seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };

  // ---------------------------------------------------------------- formatação (pt-BR)
  var F = OVM.fmt = {};
  F.n = function (x, c) { return Number(x).toLocaleString('pt-BR', { minimumFractionDigits: c || 0, maximumFractionDigits: c || 0 }); };
  // 9,46 trilhões · 299.792 · 1,5 milhão
  F.grande = function (x, c) {
    var a = Math.abs(x);
    var u = [[1e24, 'septilhão', 'septilhões'], [1e21, 'sextilhão', 'sextilhões'], [1e18, 'quintilhão', 'quintilhões'], [1e15, 'quatrilhão', 'quatrilhões'],
      [1e12, 'trilhão', 'trilhões'], [1e9, 'bilhão', 'bilhões'], [1e6, 'milhão', 'milhões']];
    for (var i = 0; i < u.length; i++) {
      if (a >= u[i][0]) {
        var v = x / u[i][0], d = c == null ? (v < 10 ? 2 : v < 100 ? 1 : 0) : c;
        var s = F.n(v, d).replace(/,0+$/, '').replace(/(,\d*?)0+$/, '$1');
        return s + ' ' + (Math.abs(v) < 2 ? u[i][1] : u[i][2]);
      }
    }
    return F.n(x, a < 10 && x % 1 ? (c == null ? 2 : c) : 0);
  };
  F.tempo = function (s) {
    var A = 31557600; // ano juliano em segundos
    if (s < 1) return F.n(s, 2) + ' s';
    if (s < 60) return F.n(s, s < 10 ? 1 : 0) + ' s';
    if (s < 3600) { var m = Math.floor(s / 60), r = Math.round(s - m * 60); return m + ' min' + (r ? ' ' + r + ' s' : ''); }
    if (s < 86400) { var h = s / 3600; return F.n(h, h < 10 ? 1 : 0) + ' h'; }
    if (s < 86400 * 60) { var d = s / 86400; return F.n(d, d < 10 ? 1 : 0) + (Math.round(d) === 1 && d < 1.5 ? ' dia' : ' dias'); }
    if (s < A * 1.5) { return F.n(s / (A / 12), 1) + ' meses'; }
    var anos = s / A;
    if (anos < 1000) return F.n(anos, anos < 10 ? 1 : 0) + ' anos';
    if (anos < 1e6) return F.n(Math.round(anos / 100) * 100) + ' anos';
    return F.grande(anos) + ' de anos';
  };
  F.km = function (km) { return F.grande(km) + ' km'; };

  // ---------------------------------------------------------------- laço de animação
  var anims = [], raf = 0, ultimo = 0, pausado = false;
  function laco(agora) {
    raf = 0;
    var dt = Math.min(0.1, (agora - ultimo) / 1000 || 0.016);
    ultimo = agora;
    OVM.t += dt;
    var vivo = false;
    for (var i = 0; i < anims.length; i++) {
      var a = anims[i];
      if (a.parado) continue;
      vivo = true;
      if (a.el && !a.visivel) continue;
      try { a.fn(dt, OVM.t); } catch (e) { if (window.console) console.error(e); }
    }
    if (vivo && !document.hidden && !pausado) raf = requestAnimationFrame(laco);
  }
  function acordar() { if (!raf && !pausado && !document.hidden) { ultimo = performance.now(); raf = requestAnimationFrame(laco); } }
  document.addEventListener('visibilitychange', acordar);
  // registra uma animação; se `el` for dado, ela só roda enquanto o elemento está na tela
  OVM.anima = function (fn, el) {
    var a = { fn: fn, el: el || null, visivel: true, parado: false };
    if (el && 'IntersectionObserver' in window) {
      a.visivel = false;
      new IntersectionObserver(function (es) { a.visivel = es[es.length - 1].isIntersecting; if (a.visivel) acordar(); }, { threshold: 0.01 }).observe(el);
    }
    anims.push(a);
    acordar();
    return { parar: function () { a.parado = true; }, seguir: function () { a.parado = false; acordar(); } };
  };
  // para testes: avança o relógio sem depender do requestAnimationFrame
  OVM.passo = function (seg, n) {
    n = n || 1;
    for (var k = 0; k < n; k++) {
      OVM.t += seg;
      anims.forEach(function (a) { if (!a.parado) { try { a.fn(seg, OVM.t); } catch (e) { if (window.console) console.error(e); } } });
    }
  };
  OVM.pausar = function (p) { pausado = p !== false; if (!pausado) acordar(); };

  // ---------------------------------------------------------------- telas (canvas)
  OVM.tela = function (canvas, aoRedimensionar) {
    var o = { c: canvas, ctx: canvas.getContext('2d'), w: 0, h: 0, dpr: OVM.dpr, aoRedimensionar: aoRedimensionar || null };
    function medir() {
      var r = canvas.getBoundingClientRect();
      var w = Math.max(1, Math.round(r.width)), h = Math.max(1, Math.round(r.height));
      if (w === o.w && h === o.h) return;
      o.w = w; o.h = h;
      canvas.width = Math.round(w * o.dpr); canvas.height = Math.round(h * o.dpr);
      o.ctx.setTransform(o.dpr, 0, 0, o.dpr, 0, 0);
      if (o.aoRedimensionar) o.aoRedimensionar(w, h);
    }
    o.medir = medir;
    if ('ResizeObserver' in window) new ResizeObserver(medir).observe(canvas); else window.addEventListener('resize', medir);
    medir();
    return o;
  };
  OVM.fundoCanvas = function (o, cor) { o.ctx.setTransform(o.dpr, 0, 0, o.dpr, 0, 0); if (cor) { o.ctx.fillStyle = cor; o.ctx.fillRect(0, 0, o.w, o.h); } else o.ctx.clearRect(0, 0, o.w, o.h); };

  // campo de estrelas fixo (posições em 0..1)
  OVM.estrelas = function (seed, n) {
    var r = OVM.rand(seed), s = [];
    for (var i = 0; i < n; i++) s.push({ x: r(), y: r(), r: 0.35 + Math.pow(r(), 3) * 1.6, b: 0.35 + r() * 0.65, f: r() * 6.28, v: 0.4 + r() * 1.6, c: r() });
  return s;
  };
  OVM.pintarEstrelas = function (ctx, w, h, st, t, opt) {
    opt = opt || {};
    var dx = opt.dx || 0, dy = opt.dy || 0, al = opt.alpha == null ? 1 : opt.alpha;
    for (var i = 0; i < st.length; i++) {
      var e = st[i];
      var x = ((e.x * w + dx) % w + w) % w, y = ((e.y * h + dy) % h + h) % h;
      var tw = OVM.reduz ? 1 : 0.7 + 0.3 * Math.sin(t * e.v + e.f);
      ctx.globalAlpha = Math.min(1, e.b * tw * al);
      ctx.fillStyle = e.c < 0.12 ? '#BFD6FF' : e.c > 0.9 ? '#FFD9A8' : '#FFFFFF';
      ctx.beginPath(); ctx.arc(x, y, e.r * (opt.escala || 1), 0, 6.2832); ctx.fill();
    }
    ctx.globalAlpha = 1;
  };
  OVM.brilho = function (ctx, x, y, r, cor, a) {
    var g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, cor.replace('A)', (a == null ? 1 : a) + ')'));
    g.addColorStop(1, cor.replace('A)', '0)'));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832); ctx.fill();
  };

  // ---------------------------------------------------------------- progresso e trava de ordem
  var CHAVE = 'ovm-progresso';
  OVM.progresso = {
    ler: function () { try { return JSON.parse(localStorage.getItem(CHAVE) || '{}') || {}; } catch (e) { return {}; } },
    feito: function (n) { return !!this.ler()[n]; },
    marcar: function (n) { var p = this.ler(); if (p[n]) return; p[n] = 1; try { localStorage.setItem(CHAVE, JSON.stringify(p)); } catch (e) {} OVM.pintarPontos(); },
    maior: function () { var p = this.ler(), m = 0; for (var k = 1; k <= OVM.total; k++) { if (p[k]) m = k; else break; } return m; }
  };
  OVM.pintarPontos = function () {
    OVM.$$('.pontos li').forEach(function (li) {
      var n = +li.getAttribute('data-n');
      li.classList.toggle('feito', OVM.progresso.feito(n));
      li.classList.toggle('atual', n === OVM.parte);
    });
  };
  // na versão publicada ninguém pula para uma parte que ainda não chegou (o fim é uma surpresa); no desenvolvimento tudo é livre
  OVM.trava = function () {
    if (OVM.dev || !OVM.parte) return;
    var ok = OVM.parte === 1 || OVM.progresso.feito(OVM.parte - 1);
    if (!ok) location.replace(OVM.parte > OVM.total ? 'parte-10.html' : 'parte-' + ('0' + (OVM.progresso.maior() + 1)).slice(-2) + '.html');
  };

  // ---------------------------------------------------------------- guia de passos (painel da cena)
  // cfg.passos = [{ rotulo, html, ir: function (i, vindoDe) {} }]
  OVM.guia = function (cfg) {
    var passos = cfg.passos, n = passos.length, atual = -1;
    var rotulo = OVM.$('#rotulo'), texto = OVM.$('#texto'), ant = OVM.$('#ant'), prox = OVM.$('#prox'), pos = OVM.$('#pos');
    var g = { n: n };
    function ir(i, silencioso) {
      i = OVM.clamp(i, 0, n - 1);
      var de = atual;
      atual = i;
      var p = passos[i];
      if (rotulo) rotulo.textContent = p.rotulo || ('Passo ' + (i + 1) + ' de ' + n);
      if (texto) texto.innerHTML = typeof p.html === 'function' ? p.html() : p.html;
      if (pos) pos.textContent = (i + 1) + ' / ' + n;
      if (ant) ant.disabled = i === 0;
      if (prox) {
        var ultimoPasso = i === n - 1;
        prox.textContent = ultimoPasso ? 'Continuar ↓' : 'Próximo →';
        prox.classList.toggle('prox-forte', ultimoPasso);
      }
      if (p.ir && !silencioso) p.ir(i, de);
      if (i === n - 1) { OVM.progresso.marcar(OVM.parte); if (cfg.aoFim) cfg.aoFim(); }
      g.atual = i;
    }
    g.ir = ir;
    if (ant) ant.addEventListener('click', function () { ir(atual - 1); });
    if (prox) prox.addEventListener('click', function () {
      if (atual === n - 1) { var l = OVM.$('#leitura'); if (l) l.scrollIntoView({ behavior: OVM.reduz ? 'auto' : 'smooth', block: 'start' }); }
      else ir(atual + 1);
    });
    document.addEventListener('keydown', function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      var t = e.target && e.target.tagName;
      if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT' || t === 'SUMMARY') return;
      if (e.key === 'ArrowRight' || e.key === 'PageDown') { if (atual < n - 1) { e.preventDefault(); ir(atual + 1); } }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { if (atual > 0) { e.preventDefault(); ir(atual - 1); } }
    });
    ir(0);
    OVM.guiaAtual = g;
    return g;
  };

  // pinta a parte preenchida do controle deslizante (--p) e devolve o valor
  OVM.preencher = function (input) {
    var mn = +input.min || 0, mx = +input.max || 100;
    input.style.setProperty('--p', ((+input.value - mn) / (mx - mn) * 100) + '%');
    return +input.value;
  };
  OVM.pronto = function (fn) { if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); };

  // ---------------------------------------------------------------- inicialização comum
  OVM.pronto(function () {
    OVM.trava();
    OVM.pintarPontos();
    var m = OVM.$('.dev-menu > button'), l = OVM.$('.dev-menu ol');
    if (m && l) m.addEventListener('click', function () { l.hidden = !l.hidden; });
  });
})();

/* ---- extras: contador de números ---- */
(function () {
  var OVM = window.OVM;
  var seq = 0;
  // faz um número "contar" de `de` até `ate` e termina sempre no texto exato `texto`
  OVM.contar = function (el, de, ate, texto, dur, formato) {
    var meu = ++seq;
    el.textContent = texto;
    if (OVM.reduz || de === ate || !window.requestAnimationFrame) return;
    var t0 = null;
    dur = dur || 900;
    formato = formato || function (v) { return Math.round(v).toLocaleString('pt-BR'); };
    function passo(t) {
      if (meu !== seq) return;
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = p >= 1 ? texto : formato(de + (ate - de) * e);
      if (p < 1) requestAnimationFrame(passo);
    }
    requestAnimationFrame(passo);
    setTimeout(function () { if (meu === seq) el.textContent = texto; }, dur + 150);
  };
})();

/* ---- extras 2: rótulos sobre imagens, suavização e medidas ---- */
(function () {
  var OVM = window.OVM, F = OVM.fmt;
  OVM.caminhoArr = function (ctx, x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.arcTo(x + w, y, x + w, y + r, r); ctx.lineTo(x + w, y + h - r); ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
    ctx.lineTo(x + r, y + h); ctx.arcTo(x, y + h, x, y + h - r, r); ctx.lineTo(x, y + r); ctx.arcTo(x, y, x + r, y, r); ctx.closePath();
  };
  // rótulo em pílula escura sobre imagens; devolve a largura
  OVM.pilula = function (ctx, txt, x, y, o) {
    o = o || {};
    var px = o.px || 13;
    ctx.save();
    ctx.font = OVM.fonte(px, o.peso || 600, o.serif);
    var tw = ctx.measureText(txt).width, pad = o.pad == null ? 9 : o.pad, w = tw + pad * 2, h = px + 10;
    var x0 = o.ancora === 'esq' ? x : o.ancora === 'dir' ? x - w : x - w / 2;
    ctx.globalAlpha = o.alpha == null ? 1 : o.alpha;
    ctx.fillStyle = o.fundo || 'rgba(6,10,26,.76)';
    OVM.caminhoArr(ctx, x0, y - h / 2, w, h, h / 2); ctx.fill();
    if (o.borda) { ctx.strokeStyle = o.borda; ctx.lineWidth = 1; ctx.stroke(); }
    ctx.fillStyle = o.cor || '#fff'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
    ctx.fillText(txt, x0 + pad, y + 0.5);
    ctx.restore();
    return w;
  };
  OVM.seguir = function (atual, alvo, taxa, dt) { return atual + (alvo - atual) * (1 - Math.exp(-taxa * dt)); };
  // distância em km -> texto ("384.400 km", "149,6 milhões de km", "4,2 anos-luz", "93 bilhões de anos-luz")
  F.distKm = function (km) {
    var AL = window.OVM_DADOS ? OVM_DADOS.anoLuzKm : 9.4607e12;
    if (km < 1e6) return F.n(km, km < 10 && km % 1 ? 1 : 0) + ' km';
    if (km < AL * 0.1) return F.grande(km) + ' de km';
    var ly = km / AL;
    if (ly < 1000) return F.n(ly, ly < 10 ? 1 : 0) + (Math.round(ly * 10) / 10 === 1 ? ' ano-luz' : ' anos-luz');
    if (ly < 1e6) return F.n(Math.round(ly / 10) * 10) + ' anos-luz';
    return F.grande(ly) + ' de anos-luz';
  };
  // distância em km -> parsecs, em letras pequenas ("≈ 28,5 Gpc")
  F.parsecKm = function (km) {
    var pc = km / (window.OVM_DADOS ? OVM_DADOS.parsecKm : 3.0857e13);
    if (pc < 1000) return '≈ ' + F.n(pc, pc < 10 ? 1 : 0) + ' pc';
    if (pc < 1e6) return '≈ ' + F.n(pc / 1e3, pc / 1e3 < 10 ? 1 : 0) + ' kpc';
    if (pc < 1e9) return '≈ ' + F.n(pc / 1e6, pc / 1e6 < 10 ? 1 : 0) + ' Mpc';
    return '≈ ' + F.n(pc / 1e9, 1) + ' Gpc';
  };
  // comprimento em metros -> texto (18 cm · 3 mm · 30 µm · 2 nm · 5 fm)
  F.metros = function (m) {
    var u = [[1e3, 1e3, 'km'], [1, 1, 'm'], [1e-2, 1e-2, 'cm'], [1e-3, 1e-3, 'mm'], [1e-6, 1e-6, 'µm'], [5e-11, 1e-9, 'nm'], [5e-14, 1e-12, 'pm'], [0, 1e-15, 'fm']];
    for (var i = 0; i < u.length; i++) if (m >= u[i][0]) { var v = m / u[i][1]; return F.n(v, v < 10 && Math.abs(v - Math.round(v)) > 0.05 ? (v < 1 ? 2 : 1) : 0) + ' ' + u[i][2]; }
    return F.n(m / 1e-15, 1) + ' fm';
  };
})();

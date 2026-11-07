/* Parte 6: quem fez tudo isto? Um céu de verdade: Via Láctea, estrelas de verdade chamadas pelo nome ("nenhuma faltará"), este mundo visto de longe, o céu em expansão (reflexão). */
OVM.pronto(function () {
  var D = OVM_DADOS, V = OVM_V, F = OVM.fmt, PI2 = 6.2832;
  var canvas = OVM.$('#tela'), olhos = OVM.$('#p6-olhos'), saida = OVM.$('#p6-saida'), btn = OVM.$('#p6-chamar');
  var tilt = 0.4, tiltAlvo = 0.4, via = null, viaW = 0, viaH = 0, i;
  var T = OVM.tela(canvas, function () { via = null; });
  // estrelas de verdade (nome e distância vêm de OVM_DADOS.estrelas); brilho e cor aproximados; posições escolhidas para o céu ficar legível
  var LOOK = {
    'Alfa do Centauro': { r: 3.6, c: '#FFF1C4' }, 'Sírio': { r: 4.4, c: '#DCEBFF' }, 'Prócion': { r: 3.2, c: '#FFF6DC' }, 'Altair': { r: 3.0, c: '#F2F5FF' }, 'Vega': { r: 3.7, c: '#E4EEFF' }, 'Fomalhaut': { r: 2.8, c: '#EEF3FF' },
    'Pólux': { r: 2.9, c: '#FFD9A6' }, 'Arcturo': { r: 3.8, c: '#FFC890' }, 'Capela': { r: 3.6, c: '#FFEBB0' }, 'Aldebarã': { r: 3.1, c: '#FFB680' }, 'Régulo': { r: 2.6, c: '#D6E4FF' }, 'Espiga': { r: 3.0, c: '#BFD6FF' }
  };
  var POS = [[0.15, 0.3], [0.31, 0.15], [0.47, 0.33], [0.63, 0.13], [0.8, 0.3], [0.92, 0.14], [0.08, 0.58], [0.25, 0.47], [0.41, 0.6], [0.57, 0.48], [0.73, 0.57], [0.88, 0.5]];
  var est = D.estrelas.map(function (e, k) { var L = LOOK[e.nome] || { r: 3, c: '#fff' }; return { nome: e.nome, al: e.al, u: POS[k][0], v: POS[k][1], r: L.r, c: L.c, luz: 0, x: 0, y: 0 }; });
  var rnd = OVM.rand(66), pq = []; for (i = 0; i < 430; i++) pq.push({ u: rnd(), v: rnd(), r: 0.3 + Math.pow(rnd(), 3) * 1.1, b: 0.3 + rnd() * 0.7, f: rnd() * 6, s: 0.5 + rnd() * 1.6 });
  var chamada = -1, sel = -1, terraA = 0, terraAlvo = 0, expA = 0, expAlvo = 0, meteoro = null, proxMeteoro = 6;

  function luzTxt(al) { return al < 10 ? F.n(al, 1) : F.n(al, 0); }

  function prepararVia(w, h) {
    var cv = document.createElement('canvas'); cv.width = w; cv.height = h; var x = cv.getContext('2d'), r = OVM.rand(12), k, u, px, py, nx, ny, d;
    var x0 = -0.1 * w, y0 = 0.95 * h, x1 = 1.1 * w, y1 = 0.05 * h, L = Math.hypot(x1 - x0, y1 - y0), ux = (x1 - x0) / L, uy = (y1 - y0) / L, sg = Math.min(w, h) * 0.12;
    for (k = 0; k < 22; k++) { u = k / 21; px = x0 + (x1 - x0) * u; py = y0 + (y1 - y0) * u; OVM.brilho(x, px, py, sg * (1.4 + r() * 0.8), 'rgba(150,170,255,A)', 0.07); OVM.brilho(x, px + (r() - 0.5) * sg, py + (r() - 0.5) * sg, sg * 0.8, 'rgba(255,225,190,A)', 0.045); }
    for (k = 0; k < 5200; k++) {
      u = r(); d = (r() + r() + r() - 1.5) * sg * 1.4; px = x0 + (x1 - x0) * u - uy * d; py = y0 + (y1 - y0) * u + ux * d;
      x.fillStyle = r() < 0.2 ? 'rgba(255,225,190,' + (0.18 + r() * 0.4) + ')' : 'rgba(205,220,255,' + (0.15 + r() * 0.45) + ')'; var z = 0.5 + r() * 1.1; x.fillRect(px, py, z, z);
    }
    x.strokeStyle = 'rgba(4,6,16,.55)'; x.lineWidth = sg * 0.22; x.lineCap = 'round';
    for (k = 0; k < 4; k++) { u = 0.15 + r() * 0.7; px = x0 + (x1 - x0) * u; py = y0 + (y1 - y0) * u; d = (r() - 0.5) * sg * 0.7; x.beginPath(); x.moveTo(px - uy * d - ux * sg, py + ux * d - uy * sg); x.lineTo(px - uy * d + ux * sg, py + ux * d + uy * sg); x.stroke(); }
    return cv;
  }
  function horizonte(ctx, w, h, hy, t) {
    var g = ctx.createLinearGradient(0, hy - h * 0.2, 0, hy); g.addColorStop(0, 'rgba(30,60,130,0)'); g.addColorStop(1, 'rgba(48,86,170,.38)'); ctx.fillStyle = g; ctx.fillRect(0, hy - h * 0.2, w, h * 0.2);
    ctx.fillStyle = '#04060E'; ctx.beginPath(); ctx.moveTo(0, h);
    for (var x = 0; x <= w + 8; x += 8) ctx.lineTo(x, hy - Math.sin(x / w * 4.2 + 0.6) * h * 0.018 - Math.sin(x / w * 11 + 2) * h * 0.007);
    ctx.lineTo(w, h); ctx.closePath(); ctx.fill();
    // pinheiros
    for (var k = 0; k < 9; k++) { var tx = w * (0.38 + k * 0.07 + (k % 2) * 0.02), th = h * (0.05 + (k % 3) * 0.018), ty = hy - Math.sin(tx / w * 4.2 + 0.6) * h * 0.018 + 2; ctx.beginPath(); ctx.moveTo(tx - th * 0.22, ty); ctx.lineTo(tx, ty - th); ctx.lineTo(tx + th * 0.22, ty); ctx.closePath(); ctx.fill(); }
    // uma pessoa de pé, olhando para cima
    var px = w * 0.17, py = hy - Math.sin(px / w * 4.2 + 0.6) * h * 0.018 + 3, s = Math.max(0.7, Math.min(1.6, Math.min(w, h) / 380));
    ctx.save(); ctx.translate(px, py); ctx.scale(s, s); ctx.fillStyle = '#0A0D1A';
    ctx.beginPath(); ctx.arc(0, -34, 5.2, 0, PI2); ctx.fill(); ctx.beginPath(); ctx.moveTo(-5, -28); ctx.lineTo(5, -28); ctx.lineTo(7, -8); ctx.lineTo(3, -8); ctx.lineTo(3, 0); ctx.lineTo(-3, 0); ctx.lineTo(-3, -8); ctx.lineTo(-7, -8); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = '#0A0D1A'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(-5, -26); ctx.lineTo(-10, -36); ctx.stroke();
    ctx.restore();
  }
  function estrelaD(ctx, x, y, r, cor, a, spikes, t, f) {
    var p = OVM.reduz ? 1 : 0.85 + 0.15 * Math.sin(t * 1.3 + f);
    ctx.globalAlpha = a; OVM.brilho(ctx, x, y, r * 5.5 * p, 'rgba(255,245,215,A)', 0.4 + 0.2 * (spikes ? 1 : 0));
    if (spikes) { ctx.strokeStyle = cor; ctx.lineWidth = 1; ctx.globalAlpha = a * 0.55; ctx.beginPath(); ctx.moveTo(x - r * 4.5, y); ctx.lineTo(x + r * 4.5, y); ctx.moveTo(x, y - r * 4.5); ctx.lineTo(x, y + r * 4.5); ctx.stroke(); ctx.globalAlpha = a; }
    ctx.fillStyle = cor; ctx.beginPath(); ctx.arc(x, y, r, 0, PI2); ctx.fill(); ctx.globalAlpha = 1;
  }

  function quadro(dt, t) {
    var w = T.w, h = T.h, ctx = T.ctx, k, e, wide = w >= 640;
    if (!via || viaW !== w || viaH !== h) { via = prepararVia(w, h); viaW = w; viaH = h; }
    tilt = OVM.reduz ? tiltAlvo : OVM.seguir(tilt, tiltAlvo, 4, dt); terraA = OVM.seguir(terraA, terraAlvo, 4, dt); expA = OVM.seguir(expA, expAlvo, 3, dt);
    OVM.fundoCanvas(T);
    var hy = h * (0.5 + 0.4 * tilt);
    var g = ctx.createLinearGradient(0, 0, 0, hy); g.addColorStop(0, '#02030B'); g.addColorStop(0.7, '#0A1230'); g.addColorStop(1, '#16275A'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ctx.globalAlpha = 0.9; ctx.drawImage(via, 0, (tilt - 0.4) * h * 0.3); ctx.globalAlpha = 1;
    for (k = 0; k < pq.length; k++) { var q = pq[k], tw = OVM.reduz ? 1 : 0.6 + 0.4 * Math.sin(t * q.s + q.f); ctx.globalAlpha = q.b * tw * 0.9; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(q.u * w, q.v * hy * 0.97, q.r, 0, PI2); ctx.fill(); }
    ctx.globalAlpha = 1;
    // meteoro de vez em quando
    proxMeteoro -= dt;
    if (!OVM.reduz && proxMeteoro < 0 && !meteoro) { meteoro = { x: w * (0.3 + rnd() * 0.6), y: hy * (0.05 + rnd() * 0.3), vx: -w * 0.5, vy: hy * 0.3, vida: 0 }; proxMeteoro = 9 + rnd() * 8; }
    if (meteoro) { meteoro.vida += dt; meteoro.x += meteoro.vx * dt; meteoro.y += meteoro.vy * dt; var ma = Math.sin(Math.min(1, meteoro.vida / 0.9) * Math.PI); ctx.strokeStyle = 'rgba(255,255,255,' + ma + ')'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(meteoro.x, meteoro.y); ctx.lineTo(meteoro.x - meteoro.vx * 0.12, meteoro.y - meteoro.vy * 0.12); ctx.stroke(); if (meteoro.vida > 0.9) meteoro = null; }
    // chamada pelo nome
    var tc = chamada < 0 ? -1 : OVM.t - chamada;
    // estrelas nomeadas
    for (k = 0; k < est.length; k++) {
      e = est[k]; e.x = e.u * w; e.y = e.v * hy * 0.95;
      if (tc >= 0) e.luz = OVM.suave((tc - k * 0.7) / 0.45);
      var base = 0.78 + 0.22 * e.luz, ativa = k === sel || (tc >= 0 && tc - k * 0.7 > 0 && tc - k * 0.7 < 1.1);
      estrelaD(ctx, e.x, e.y, e.r * (1 + e.luz * 0.5), e.c, base, e.r > 3.3 || e.luz > 0.5, t, k);
      if (ativa || (wide && e.luz > 0.9 && tc >= 0)) {
        var lado = e.u > 0.8 ? 'dir' : 'esq', ex = e.x + (lado === 'esq' ? 12 : -12);
        OVM.pilula(ctx, ativa ? e.nome + ' · a luz saiu de lá há ' + luzTxt(e.al) + ' anos' : e.nome, ex, e.y - 2, { px: 11.5, ancora: lado, alpha: ativa ? 1 : 0.8, cor: ativa ? '#FFE9B8' : '#fff', fundo: ativa ? 'rgba(80,60,10,.9)' : 'rgba(6,10,26,.7)', pad: 8 });
      }
      if (expA > 0.02) { var cx = w / 2, cy = hy * 0.38, an = Math.atan2(e.y - cy, e.x - cx), d0 = e.r + 8, d1 = d0 + 16 + 8 * Math.sin(t * 2 + k); ctx.globalAlpha = expA * 0.7; ctx.strokeStyle = '#FFD878'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(e.x + Math.cos(an) * d0, e.y + Math.sin(an) * d0); ctx.lineTo(e.x + Math.cos(an) * d1, e.y + Math.sin(an) * d1); ctx.lineTo(e.x + Math.cos(an + 2.7) * 5 + Math.cos(an) * d1, e.y + Math.sin(an + 2.7) * 5 + Math.sin(an) * d1); ctx.moveTo(e.x + Math.cos(an) * d1, e.y + Math.sin(an) * d1); ctx.lineTo(e.x + Math.cos(an - 2.7) * 5 + Math.cos(an) * d1, e.y + Math.sin(an - 2.7) * 5 + Math.sin(an) * d1); ctx.stroke(); ctx.globalAlpha = 1; }
    }
    if (tc > est.length * 0.7 + 0.2) OVM.pilula(ctx, '… e nenhuma faltará.', w / 2, hy * 0.9 - 6, { px: 15, fundo: 'rgba(242,217,160,.96)', cor: '#1F2A44', alpha: Math.min(1, (tc - est.length * 0.7) / 0.6), pad: 12 });
    if (expA > 0.05) OVM.pilula(ctx, 'reflexão: tudo se afasta de tudo', w / 2, 24, { px: 12.5, alpha: expA, fundo: 'rgba(80,45,10,.88)', cor: '#FFD9A8', pad: 10 });
    horizonte(ctx, w, h, hy, t);
    // o mundo visto de longe
    if (terraA > 0.02) {
      var rr = Math.min(w, h) * 0.17, ix = w - rr - 14, iy = rr + 14;
      ctx.save(); ctx.globalAlpha = terraA; ctx.fillStyle = '#02030B'; ctx.beginPath(); ctx.arc(ix, iy, rr, 0, PI2); ctx.fill(); ctx.save(); ctx.beginPath(); ctx.arc(ix, iy, rr, 0, PI2); ctx.clip();
      for (k = 0; k < 90; k++) { var q2 = pq[k]; ctx.globalAlpha = terraA * q2.b * 0.9; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(ix - rr + q2.u * rr * 2, iy - rr + q2.v * rr * 2, q2.r * 0.9, 0, PI2); ctx.fill(); }
      ctx.globalAlpha = terraA; OVM.brilho(ctx, ix, iy, 14, 'rgba(110,175,255,A)', 0.9); ctx.fillStyle = '#6FB4FF'; ctx.beginPath(); ctx.arc(ix, iy, 2.6, 0, PI2); ctx.fill(); ctx.restore();
      ctx.strokeStyle = 'rgba(255,255,255,.5)'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(ix, iy, rr, 0, PI2); ctx.stroke(); ctx.restore();
      OVM.pilula(ctx, 'este mundo, visto de longe', ix, iy + rr + 15, { px: 11.5, alpha: terraA }); OVM.pilula(ctx, '“pequenino átomo”', ix, iy + rr + 41, { px: 11.5, alpha: terraA, fundo: 'rgba(80,60,10,.9)', cor: '#FFE9B8' });
    }
  }
  OVM.anima(quadro, canvas);
  quadro(0.016, 0.5);

  canvas.addEventListener('click', function (ev) {
    var r = canvas.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top, best = -1, bd = 1e9;
    est.forEach(function (e, k) { var d = Math.hypot(e.x - x, e.y - y); if (d < 26 && d < bd) { bd = d; best = k; } });
    sel = best;
  });
  canvas.style.cursor = 'pointer';
  olhos.addEventListener('input', function () { tiltAlvo = (+olhos.value) / 100; OVM.preencher(olhos); saida.textContent = tiltAlvo < 0.25 ? 'quase no chão' : tiltAlvo < 0.7 ? 'um pouco' : 'para o alto'; });
  OVM.preencher(olhos);
  function chamar() { chamada = OVM.t; sel = -1; est.forEach(function (e) { e.luz = 0; }); }
  btn.addEventListener('click', chamar);

  // ---------------------------------------------------------------- passos
  function cit(k) { var v = V[k]; return '<blockquote class="vers">“' + v.t + '”<cite>' + v.ref + '</cite></blockquote>'; }
  function modo(ter, exp) { terraAlvo = ter; expAlvo = exp; }
  var passos = [
    { rotulo: 'Olhe para cima', ir: function () { modo(0, 0); },
      html: '<b class="grande">Quem fez tudo isto?</b><p>Levante os olhos e olhe o céu à noite. Muita gente, em muitas épocas, fez essa mesma pergunta.</p>' + cit('sl19') },
    { rotulo: 'Chamadas pelo nome', ir: function () { modo(0, 0); tiltAlvo = 0.8; olhos.value = 80; OVM.preencher(olhos); setTimeout(chamar, 600); },
      html: cit('is4026') + '<p class="pequeno">Toque em <b>Chamar pelo nome</b>: são estrelas de verdade, e a luz de cada uma saiu de lá há anos.</p>' },
    { rotulo: 'E nós, onde estamos?', ir: function () { modo(1, 0); },
      html: cit('sl8') + '<p class="pequeno">Ellen G. White: “' + V.egw_atomo.t + '.”</p>' },
    { rotulo: 'Nele tudo subsiste', ir: function () { modo(0, 0); },
      html: cit('cl1617') + '<p class="pequeno">E Hebreus 1:3 diz que Ele sustenta “todas as coisas pela palavra do seu poder”. Ellen White: “' + V.egw_estrela.t + '”</p>' },
    { rotulo: 'Uma reflexão', ir: function () { modo(0, 1); },
      html: '<p><span class="marca">reflexão, não é afirmação da Bíblia</span></p><p>A Bíblia e Ellen White dizem que Deus <b>sustenta</b> tudo o tempo todo. Podemos <b>imaginar</b> que o universo em expansão fala de um Deus que não para de agir.</p><p class="pequeno">O que não está escrito: que o universo se expande porque Deus continua criando.</p>' },
    { rotulo: 'A pergunta continua', ir: function () { modo(0, 0); },
      html: '<p>Quem fez tudo isto? A Bíblia responde com um nome: <b>Deus</b>, o Criador de tudo o que existe.</p><p>Um Deus assim é maior que o universo que vimos. <b>Onde estaria o seu trono?</b></p>' }
  ];
  OVM.guia({ passos: passos });
});

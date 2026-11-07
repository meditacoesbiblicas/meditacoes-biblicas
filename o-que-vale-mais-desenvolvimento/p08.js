/* Parte 8: a grandeza no pequeno. Zoom para dentro (motor de escala ao contrário): mão → pele → células → núcleo → DNA → átomo → núcleo do átomo.
   O "átomo como sistema solar" aparece só como modelo antigo e superado (analogia marcada). Todas as imagens são desenhos artísticos. */
OVM.pronto(function () {
  var V = OVM_V, F = OVM.fmt, PI2 = 6.2832, TAM = 1024, C = TAM / 2, R = TAM * 0.45, i, k;
  var cena = OVM.$('#cena'), nomeEl = OVM.$('#hud-nome'), tamEl = OVM.$('#hud-tam'), pcEl = OVM.$('#hud-pc'), escada = OVM.$('#p8-escada');
  var sZoom = OVM.$('#p8-zoom'), oZoom = OVM.$('#p8-zoom-saida'), chipsM = OVM.$$('#p8-modelo .chip');
  var usando = false, ultimo = -1, estadio = 0, estadioAlvo = 0, retic = 1, rungs = [];

  // ---------------------------------------------------------------- desenhos (cada um num quadro de 1024×1024; um disco opaco de 90%)
  function disco(ctx, c0, c1, c2) {
    var g = ctx.createRadialGradient(C, C, R * 0.1, C, C, R);
    g.addColorStop(0, c0); g.addColorStop(0.9, c1); g.addColorStop(0.97, c2 || c1); g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(C, C, R, 0, PI2); ctx.fill();
  }
  function pMao(ctx, rnd) {
    var g = ctx.createLinearGradient(C - 300, C - 420, C + 320, C + 420); g.addColorStop(0, '#F2CDAE'); g.addColorStop(1, '#C98F6B');
    ctx.fillStyle = g; ctx.strokeStyle = 'rgba(110,60,30,.35)'; ctx.lineWidth = 3;
    [[-0.19, 0.1, 0.3], [-0.065, 0.105, 0.36], [0.06, 0.105, 0.33], [0.18, 0.095, 0.27]].forEach(function (d) {
      var w = d[1] * TAM, x = C + d[0] * TAM - w / 2, len = d[2] * TAM, y = C - 0.2 * TAM - len + 0.05 * TAM;
      ctx.fillStyle = g; OVM.caminhoArr(ctx, x, y, w, len + 0.1 * TAM, w / 2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = 'rgba(255,236,224,.75)'; OVM.caminhoArr(ctx, x + w * 0.14, y + 7, w * 0.72, w * 0.62, w * 0.3); ctx.fill();
    });
    ctx.fillStyle = g; OVM.caminhoArr(ctx, C - 0.27 * TAM, C - 0.2 * TAM, 0.54 * TAM, 0.5 * TAM, 0.16 * TAM); ctx.fill(); ctx.stroke();
    ctx.save(); ctx.translate(C - 0.29 * TAM, C + 0.02 * TAM); ctx.rotate(-0.75); OVM.caminhoArr(ctx, -0.055 * TAM, -0.27 * TAM, 0.11 * TAM, 0.34 * TAM, 0.055 * TAM); ctx.fill(); ctx.stroke(); ctx.fillStyle = 'rgba(255,236,224,.75)'; OVM.caminhoArr(ctx, -0.04 * TAM, -0.265 * TAM, 0.08 * TAM, 0.07 * TAM, 0.03 * TAM); ctx.fill(); ctx.restore();
    ctx.fillStyle = g; OVM.caminhoArr(ctx, C - 0.17 * TAM, C + 0.22 * TAM, 0.34 * TAM, 0.22 * TAM, 0.04 * TAM); ctx.fill();
    OVM.brilho(ctx, C - 0.12 * TAM, C - 0.1 * TAM, 0.36 * TAM, 'rgba(255,240,225,A)', 0.22);
    ctx.strokeStyle = 'rgba(110,60,30,.22)'; ctx.lineWidth = 3; for (var j = 0; j < 4; j++) { ctx.beginPath(); ctx.moveTo(C + (j - 1.5) * 0.12 * TAM, C - 0.2 * TAM); ctx.lineTo(C + (j - 1.5) * 0.12 * TAM, C - 0.1 * TAM); ctx.stroke(); }
  }
  function pPele(ctx, rnd) {
    disco(ctx, '#F0C7A5', '#D9A47F', '#C28A66');
    ctx.save(); ctx.beginPath(); ctx.arc(C, C, R, 0, PI2); ctx.clip();
    ctx.strokeStyle = 'rgba(125,72,40,.30)'; ctx.lineWidth = 3;
    [0.55, -0.55].forEach(function (a) { for (var j = -16; j <= 16; j++) { var o = j * 62 + (rnd() - 0.5) * 8; ctx.save(); ctx.translate(C, C); ctx.rotate(a); ctx.beginPath(); ctx.moveTo(-700, o); ctx.lineTo(700, o + (rnd() - 0.5) * 6); ctx.stroke(); ctx.restore(); } });
    for (var j = 0; j < 70; j++) { var x = C + (rnd() - 0.5) * 900, y = C + (rnd() - 0.5) * 900; ctx.fillStyle = 'rgba(130,78,48,.5)'; ctx.beginPath(); ctx.arc(x, y, 2 + rnd() * 3, 0, PI2); ctx.fill(); }
    for (j = 0; j < 15; j++) {   // pelos: cada um com o seu lugar
      var hx = C + (rnd() - 0.5) * 760, hy = C + (rnd() - 0.5) * 760, ang = 0.7 + (rnd() - 0.5) * 0.7, len = 120 + rnd() * 90;
      ctx.fillStyle = '#5A3A27'; ctx.beginPath(); ctx.arc(hx, hy, 8, 0, PI2); ctx.fill();
      ctx.strokeStyle = '#3B2417'; ctx.lineWidth = 5; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(hx, hy); ctx.quadraticCurveTo(hx + Math.cos(ang) * len * 0.6, hy + Math.sin(ang) * len * 0.2, hx + Math.cos(ang + 0.5) * len, hy + Math.sin(ang + 0.5) * len); ctx.stroke();
    }
    ctx.restore();
  }
  function pCelulas(ctx, rnd) {
    disco(ctx, '#F8DDD8', '#EBC2BD', '#D9A5A1');
    ctx.save(); ctx.beginPath(); ctx.arc(C, C, R, 0, PI2); ctx.clip();
    var s = 0.19 * TAM, row, col, v;
    for (row = -4; row <= 4; row++) for (col = -4; col <= 4; col++) {
      var cx = C + (col + (row % 2 ? 0.5 : 0)) * s + (rnd() - 0.5) * s * 0.12, cy = C + row * s * 0.87 + (rnd() - 0.5) * s * 0.12;
      ctx.beginPath(); for (v = 0; v < 6; v++) { var a = v * 1.0472 + 0.52, rr = s * 0.57 * (0.92 + rnd() * 0.12); ctx[v ? 'lineTo' : 'moveTo'](cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); } ctx.closePath();
      ctx.fillStyle = 'rgba(' + (246 + Math.floor(rnd() * 8)) + ',' + (205 + Math.floor(rnd() * 24)) + ',' + (205 + Math.floor(rnd() * 24)) + ',.85)'; ctx.fill(); ctx.strokeStyle = 'rgba(176,100,110,.75)'; ctx.lineWidth = 4; ctx.stroke();
      var g = ctx.createRadialGradient(cx - 4, cy - 4, 2, cx, cy, s * 0.17); g.addColorStop(0, '#9A78CC'); g.addColorStop(1, '#5B3E96'); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx + (rnd() - 0.5) * 8, cy + (rnd() - 0.5) * 8, s * (row === 0 && col === 0 ? 0.2 : 0.15), 0, PI2); ctx.fill();
    }
    ctx.restore();
  }
  function pNucleo(ctx, rnd) {
    disco(ctx, '#8C70C8', '#5A3E9E', '#3E2A78');
    ctx.strokeStyle = 'rgba(225,205,255,.8)'; ctx.lineWidth = 10; ctx.beginPath(); ctx.arc(C, C, R - 6, 0, PI2); ctx.stroke();
    for (k = 0; k < 46; k++) { var a = k / 46 * PI2; ctx.fillStyle = 'rgba(255,240,255,.85)'; ctx.beginPath(); ctx.arc(C + Math.cos(a) * (R - 6), C + Math.sin(a) * (R - 6), 7, 0, PI2); ctx.fill(); }
    ctx.save(); ctx.beginPath(); ctx.arc(C, C, R - 14, 0, PI2); ctx.clip();
    ctx.lineCap = 'round';
    for (k = 0; k < 110; k++) { var x = C + (rnd() - 0.5) * 820, y = C + (rnd() - 0.5) * 820, a2 = rnd() * PI2, l = 60 + rnd() * 130; ctx.strokeStyle = 'rgba(' + (200 + Math.floor(rnd() * 40)) + ',' + (180 + Math.floor(rnd() * 40)) + ',255,' + (0.25 + rnd() * 0.35) + ')'; ctx.lineWidth = 3 + rnd() * 5; ctx.beginPath(); ctx.moveTo(x, y); ctx.bezierCurveTo(x + Math.cos(a2) * l, y + Math.sin(a2) * l, x + Math.cos(a2 + 1.6) * l, y + Math.sin(a2 + 1.6) * l, x + Math.cos(a2 + 0.8) * l * 1.2, y + Math.sin(a2 + 0.8) * l * 1.2); ctx.stroke(); }
    OVM.brilho(ctx, C + 0.17 * TAM, C - 0.15 * TAM, 0.11 * TAM, 'rgba(50,25,100,A)', 0.9);
    OVM.brilho(ctx, C, C, 40, 'rgba(255,255,255,A)', 0.6);
    ctx.restore();
  }
  function pDNA(ctx, rnd) {
    disco(ctx, '#123268', '#0A1C42', '#050E26');
    ctx.save(); ctx.beginPath(); ctx.arc(C, C, R, 0, PI2); ctx.clip(); ctx.translate(C, C); ctx.rotate(-0.55);
    var L = 2 * R, per = L / 5.2, A = 0.17 * TAM, x, ph, y1, y2, z, seg = [];
    for (x = -L / 2; x <= L / 2; x += 6) { ph = x / per * PI2; seg.push({ x: x, y1: Math.sin(ph) * A, y2: -Math.sin(ph) * A, z: Math.cos(ph) }); }
    for (k = 0; k < seg.length; k += 4) { var s0 = seg[k], g = ctx.createLinearGradient(s0.x, s0.y1, s0.x, s0.y2); var par = Math.floor(k / 4) % 2; g.addColorStop(0, par ? '#FFB74D' : '#4DD0E1'); g.addColorStop(0.5, par ? '#FFB74D' : '#4DD0E1'); g.addColorStop(0.5, par ? '#81C784' : '#F06292'); g.addColorStop(1, par ? '#81C784' : '#F06292'); ctx.strokeStyle = g; ctx.lineWidth = 12; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(s0.x, s0.y1); ctx.lineTo(s0.x, s0.y2); ctx.stroke(); }
    function fita(sgn, cor0, cor1) { ctx.lineCap = 'round'; for (var m = 1; m < seg.length; m++) { var a = seg[m - 1], b = seg[m], zz = sgn * (a.z + b.z) / 2, f = (zz + 1) / 2; ctx.strokeStyle = zz > 0 ? cor1 : cor0; ctx.lineWidth = 15 + 7 * f; ctx.beginPath(); ctx.moveTo(a.x, sgn * a.y1); ctx.lineTo(b.x, sgn * b.y1); ctx.stroke(); } }
    // as duas fitas se cruzam: a de trás é desenhada antes, a da frente depois, trecho a trecho
    for (var m2 = 1; m2 < seg.length; m2++) {
      var a = seg[m2 - 1], b = seg[m2], z = (a.z + b.z) / 2, passos = [[a.y1, b.y1, '#2E8FD6', '#7CCBFF', z], [a.y2, b.y2, '#D6457E', '#FF8DB4', -z]].sort(function (p, q) { return p[4] - q[4]; });
      passos.forEach(function (p) { ctx.strokeStyle = p[4] > 0 ? p[3] : p[2]; ctx.lineWidth = 15 + 6 * (p[4] + 1) / 2; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(a.x, p[0]); ctx.lineTo(b.x, p[1]); ctx.stroke(); });
    }
    ctx.restore(); OVM.brilho(ctx, C, C, 50, 'rgba(255,255,255,A)', 0.5);
  }
  function pAtomoNuvem(ctx, rnd) {
    disco(ctx, '#0B1A44', '#060F2B', '#030816');
    ctx.save(); ctx.beginPath(); ctx.arc(C, C, R, 0, PI2); ctx.clip(); ctx.globalCompositeOperation = 'lighter';
    for (k = 0; k < 14000; k++) { var r = (-Math.log(1 - rnd()) - Math.log(1 - rnd()) - Math.log(1 - rnd())) * R * 0.15, a = rnd() * PI2, q = Math.min(1, r / R); ctx.fillStyle = 'rgba(' + Math.floor(110 + 100 * q) + ',' + Math.floor(210 - 40 * q) + ',255,' + (0.18 + 0.5 * (1 - q)) + ')'; var z = 1.4 + rnd() * 1.6; ctx.fillRect(C + Math.cos(a) * r, C + Math.sin(a) * r, z, z); }
    OVM.brilho(ctx, C, C, 26, 'rgba(255,190,120,A)', 0.9); ctx.fillStyle = '#FFE2B8'; ctx.beginPath(); ctx.arc(C, C, 2.2, 0, PI2); ctx.fill();
    ctx.restore();
  }
  function pAtomoOrbitas(ctx, rnd) {
    disco(ctx, '#0B1A44', '#060F2B', '#030816');
    ctx.save(); ctx.beginPath(); ctx.arc(C, C, R, 0, PI2); ctx.clip();
    [0, 1.0472, 2.0944].forEach(function (rot, j) { ctx.save(); ctx.translate(C, C); ctx.rotate(rot); ctx.strokeStyle = 'rgba(160,200,255,.55)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(0, 0, R * 0.82, R * 0.3, 0, 0, PI2); ctx.stroke(); var a = j * 2.1 + 0.5; OVM.brilho(ctx, Math.cos(a) * R * 0.82, Math.sin(a) * R * 0.3, 20, 'rgba(120,200,255,A)', 0.9); ctx.fillStyle = '#9FE0FF'; ctx.beginPath(); ctx.arc(Math.cos(a) * R * 0.82, Math.sin(a) * R * 0.3, 9, 0, PI2); ctx.fill(); ctx.restore(); });
    OVM.brilho(ctx, C, C, 50, 'rgba(255,170,100,A)', 0.8); ctx.fillStyle = '#FF8A5C'; ctx.beginPath(); ctx.arc(C, C, 16, 0, PI2); ctx.fill();
    ctx.restore();
  }
  function pNucleoAt(ctx, rnd) {
    disco(ctx, '#201640', '#0C0720', '#050310');
    var pos = [], r = R * 0.1, tent = 0;
    while (pos.length < 12 && tent++ < 800) { var a = rnd() * PI2, d = Math.sqrt(rnd()) * R * 0.3, x = C + Math.cos(a) * d, y = C + Math.sin(a) * d, ok = true; for (k = 0; k < pos.length; k++) if (Math.hypot(pos[k][0] - x, pos[k][1] - y) < r * 1.55) { ok = false; break; } if (ok) pos.push([x, y]); }
    OVM.brilho(ctx, C, C, R * 0.6, 'rgba(255,140,100,A)', 0.35);
    pos.forEach(function (p, j) { var pr = j % 2 === 0; OVM.motor.esfera(ctx, p[0], p[1], r, pr ? '#FFB0A0' : '#E3E8FA', pr ? '#EE5A48' : '#98A4C8', pr ? '#892016' : '#4F5B80'); });
  }
  var NIV = [
    { id: 'mao', nome: 'A sua mão', d: 0.2, pintar: pMao }, { id: 'pele', nome: 'A pele', d: 2e-3, pintar: pPele }, { id: 'celulas', nome: 'As células da pele', d: 1e-4, pintar: pCelulas },
    { id: 'nucleo', nome: 'O núcleo de uma célula', d: 8e-6, pintar: pNucleo }, { id: 'dna', nome: 'O DNA', d: 2e-8, pintar: pDNA },
    { id: 'atomo', nome: 'Um átomo', d: 3e-10, pintar: pAtomoNuvem }, { id: 'nucleoat', nome: 'O núcleo do átomo', d: 6e-15, pintar: pNucleoAt }
  ];
  var CURTOS = ['Mão', 'Pele', 'Células', 'Núcleo', 'DNA', 'Átomo', 'Núcleo do átomo'], n = NIV.length;
  NIV.forEach(function (nv) { nv.off = [0, 0]; nv.marcas = []; });

  // ---------------------------------------------------------------- o motor (câmera que entra)
  function fundo(ctx, w, h, s, t) { var g = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, Math.max(w, h) * 0.7); g.addColorStop(0, '#15122A'); g.addColorStop(1, '#05040C'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }
  var E, sMao, sFim;
  function aoQuadro(Eng, dt, t) {
    var ctx = Eng.T.ctx, w = Eng.T.w, h = Eng.T.h, L = Math.min(w, h) * 0.94, cx = w / 2, cy = h / 2, k2 = Eng.perto();
    if (k2 !== ultimo) { ultimo = k2; nomeEl.textContent = NIV[k2].nome; tamEl.textContent = 'cerca de ' + F.metros(NIV[k2].d) + ' de lado a lado'; pcEl.textContent = ''; marca(k2); }
    // a mira: onde vamos entrar (o centro de cada desenho)
    var prox = Math.min(n - 1, k2 + 1), px = Eng.px(prox), alvoRet = k2 < n - 1 && !Eng.movendo ? 1 : 0.15; retic = OVM.seguir(retic, alvoRet, 5, dt);
    if (k2 < n - 1 && px < 0.4 * L) {
      var al = retic * (1 - px / (0.4 * L)) * 0.9 + 0.1 * retic, r = 22 + (OVM.reduz ? 0 : Math.sin(t * 3) * 2.5);
      ctx.save(); ctx.globalAlpha = al; ctx.strokeStyle = '#FFE9A8'; ctx.lineWidth = 2.4; ctx.lineCap = 'round';
      [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(function (c) { ctx.beginPath(); ctx.moveTo(cx + c[0] * r, cy + c[1] * (r - 9)); ctx.lineTo(cx + c[0] * r, cy + c[1] * r); ctx.lineTo(cx + c[0] * (r - 9), cy + c[1] * r); ctx.stroke(); });
      OVM.pilula(ctx, 'vamos entrar aqui', cx, cy + r + 20, { px: 11.5, alpha: al, pad: 8 }); ctx.restore();
    }
    // a comparação do estádio (passo do núcleo do átomo)
    estadio = OVM.seguir(estadio, estadioAlvo, 4, dt);
    if (estadio > 0.02) {
      var ex = 14, ey = h - 74, ew = Math.min(150, w * 0.34), eh = 46;
      ctx.save(); ctx.globalAlpha = estadio; ctx.fillStyle = 'rgba(6,10,26,.82)'; OVM.caminhoArr(ctx, ex - 8, ey - eh / 2 - 10, ew + 16, eh + 20, 14); ctx.fill();
      ctx.strokeStyle = '#8FD6A0'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(ex + ew / 2, ey, ew / 2, eh / 2, 0, 0, PI2); ctx.stroke(); ctx.strokeStyle = 'rgba(143,214,160,.5)'; ctx.beginPath(); ctx.moveTo(ex + ew / 2, ey - eh / 2); ctx.lineTo(ex + ew / 2, ey + eh / 2); ctx.stroke();
      ctx.fillStyle = '#FF7A60'; ctx.beginPath(); ctx.arc(ex + ew / 2, ey, 2.2, 0, PI2); ctx.fill();
      OVM.pilula(ctx, 'átomo = estádio de 100 m', ex + ew / 2, ey - eh / 2 - 26, { px: 11, pad: 7 }); OVM.pilula(ctx, 'núcleo = grão de ~2 mm', ex + ew / 2, ey + eh / 2 + 22, { px: 11, pad: 7, fundo: 'rgba(80,60,10,.92)', cor: '#FFE9B8' }); ctx.restore();
    }
    if (!usando && sMao !== undefined) { sZoom.value = OVM.clamp((sMao - Eng.s) / (sMao - sFim) * 100, 0, 100); OVM.preencher(sZoom); }
    oZoom.textContent = F.metros(Eng.campo() / 1.15);
  }
  E = OVM.Escala({ canvas: OVM.$('#tela'), niveis: NIV, folga: 1.15, aqui: false, fundo: fundo, estrelasAlfa: function () { return 0.28; }, barra: function (len) { return F.metros(len); }, aoQuadro: aoQuadro, semente: 51 });
  sMao = E.sDe(0); sFim = E.sDe(n - 1);

  // a escada para dentro
  NIV.forEach(function (nv, j) { var li = document.createElement('li'); li.innerHTML = '<button type="button" aria-label="' + nv.nome + '"><span class="nome">' + CURTOS[j] + '</span><span class="bola"></span></button>'; li.firstChild.addEventListener('click', function () { g.ir(j); }); escada.appendChild(li); rungs.push(li); });
  function marca(j) { rungs.forEach(function (li, q) { li.classList.toggle('ativo', q === j); li.classList.toggle('passou', q < j); }); }
  sZoom.addEventListener('input', function () { usando = true; E.definir(OVM.lerp(sMao, sFim, +sZoom.value / 100)); OVM.preencher(sZoom); });
  sZoom.addEventListener('change', function () { usando = false; });
  function modeloAtomo(m) {
    NIV[5].pintar = m === 'orbitas' ? pAtomoOrbitas : pAtomoNuvem; E.niveis[5].folha = null;
    chipsM.forEach(function (c) { c.classList.toggle('ativo', c.getAttribute('data-m') === m); });
  }
  chipsM.forEach(function (c) { c.addEventListener('click', function () { modeloAtomo(c.getAttribute('data-m')); }); });

  // ---------------------------------------------------------------- passos
  function cit(kk) { var v = V[kk]; return '<blockquote class="vers">“' + v.t + '”<cite>' + v.ref + '</cite></blockquote>'; }
  function vai(j, ctl, est) { cena.setAttribute('data-modo', ctl || 'zoom'); estadioAlvo = est ? 1 : 0; usando = false; E.ir(j, j === 0 ? 2.5 : null); if (j === 5 && ctl !== 'modelo') modeloAtomo('nuvem'); }
  var passos = [
    { rotulo: 'A sua mão', ir: function () { vai(0); },
      html: '<b class="grande">A sua mão</b><p>Até aqui olhamos para o <b>grande</b>. Agora o caminho contrário: vamos <b>entrar</b>, a partir do meio do dorso da sua mão.</p>' + cit('sl139_14') },
    { rotulo: 'A pele', ir: function () { vai(1); },
      html: '<b class="grande">A pele</b><p>Dois milímetros de pele: sulcos finos, poros e <b>pelos</b>, cada um com o seu lugar.</p>' + cit('mt1030') },
    { rotulo: 'As células', ir: function () { vai(2); },
      html: '<b class="grande">As células</b><p>O corpo humano tem uns <b>30 trilhões de células</b>. Estas são células da pele; em cada uma, o ponto roxo é o <b>núcleo</b>.</p>' },
    { rotulo: 'O núcleo da célula', ir: function () { vai(3); },
      html: '<b class="grande">O núcleo da célula</b><p>Dentro do núcleo, com uns 8 milésimos de milímetro, fica guardado o que dá as instruções da célula: o <b>DNA</b>, enrolado e dobrado.</p>' },
    { rotulo: 'O DNA', ir: function () { vai(4); },
      html: '<b class="grande">O DNA</b><p>Uma escada torcida (a <b>dupla hélice</b>) de uns 2 nm de largura. Esticado, o DNA de uma única célula teria <b>cerca de 2 metros</b>.</p><p class="pequeno"><span class="marca">reflexão</span> Diante disso lembramos do Salmo 139:16 (“no teu livro todas estas coisas foram escritas”): é aplicação, o Salmo não fala de DNA.</p>' },
    { rotulo: 'Um átomo', ir: function () { vai(5, 'modelo'); },
      html: '<b class="grande">Um átomo</b><p>Tudo é feito de átomos. E um átomo é <b>quase todo espaço vazio</b>: os elétrons formam uma <b>nuvem</b> em volta de um núcleo minúsculo.</p><p class="pequeno">Pessoas comparam o átomo a um <b>sistema solar</b>. É um modelo antigo e superado, mas dá para ver a analogia (use os botões).</p>' },
    { rotulo: 'O núcleo do átomo', ir: function () { vai(6, 'zoom', true); },
      html: '<b class="grande">O núcleo do átomo</b><p>Prótons e nêutrons, num espaço de uns <b>6 femtômetros</b>: de <b>27 mil a 60 mil vezes menor</b> que o átomo.</p><p>Se o átomo fosse um estádio de 100 m, o núcleo seria um <b>grão de areia</b> no meio do campo.</p>' },
    { rotulo: 'O grande e o pequeno', ir: function () { vai(6, 'zoom', false); E.irS(E.sDe(6), 1); },
      html: '<p>Do <b>universo observável</b> ao <b>núcleo do átomo</b> há mais de <b>40 degraus</b> de potência de dez.</p>' + cit('ed114') + '<p class="pequeno">A mesma sabedoria no grande e no pequeno.</p>' }
  ];
  var g = OVM.guia({ passos: passos });
});

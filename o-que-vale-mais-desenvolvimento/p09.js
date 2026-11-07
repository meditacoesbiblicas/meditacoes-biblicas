/* Parte 9: os preços voltam. As etiquetas de tudo o que vimos; o preço que o mundo já pôs em pessoas (José, um servo); uma balança em que nada do que se paga move o outro prato;
   e a pergunta que fica. Nada aqui diz quem é a resposta: isso é a parte 10. */
OVM.pronto(function () {
  var D = OVM_DADOS, V = OVM_V, F = OVM.fmt, PI2 = 6.2832, P = D.precos, VG = D.viagens, i, k;
  var canvas = OVM.$('#tela'), T = OVM.tela(canvas), cena = OVM.$('#cena'), listaEl = OVM.$('#p9-itens'), bTudo = OVM.$('#p9-tudo'), bLimpar = OVM.$('#p9-limpar');
  var ITENS = [
    { id: 'cafe', nome: 'Chocolate quente', emoji: '🍫', valor: P[0].valor }, { id: 'refeicao', nome: 'Refeição', emoji: '🍽️', valor: P[1].valor }, { id: 'viagem', nome: 'Viagem em família', emoji: '✈️', valor: P[3].valor },
    { id: 'carro', nome: 'Carro', emoji: '🚗', valor: P[4].valor }, { id: 'casa', nome: 'Casa', emoji: '🏠', valor: P[5].valor }, { id: 'estacao', nome: 'Estação Espacial', emoji: '🛰️', valor: VG[2].reais }, { id: 'marte', nome: 'Marte (meta)', emoji: '🔴', valor: VG[4].reais }
  ];
  var modo = 'etiquetas', am = { etiquetas: 1, pessoas: 0, balanca: 0, pergunta: 0 }, prato = [], ang = 0.22, ultimoTotal = 0, msg = 0, est = OVM.estrelas(14, 120);

  function curto(v) { return v < 100 ? F.n(v, 2) : v < 1000 ? F.n(Math.round(v)) : v < 1e6 ? F.n(Math.round(v / 1000)) + ' mil' : F.grande(v); }
  function total() { var t = 0; prato.forEach(function (it) { t += it.valor; }); return t; }

  // ---------------------------------------------------------------- desenhos
  function etiqueta(ctx, x, y, w, h, rot, linhas, opt) {
    opt = opt || {};
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
    ctx.shadowColor = 'rgba(31,42,68,.28)'; ctx.shadowBlur = 10; ctx.shadowOffsetY = 4;
    ctx.fillStyle = opt.fundo || '#FFFBF0'; OVM.caminhoArr(ctx, -w / 2, 0, w, h, 8); ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.strokeStyle = opt.borda || '#1F2A44'; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#E9DCC1'; ctx.beginPath(); ctx.arc(0, 10, 4.5, 0, PI2); ctx.fill(); ctx.stroke();
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = opt.cor || '#1F2A44';
    linhas.forEach(function (l, j) { var px = l.px; ctx.font = OVM.fonte(px, l.peso || 600, true); var mw = ctx.measureText(l.t).width; if (mw > w * 0.88) { px = px * w * 0.88 / mw; ctx.font = OVM.fonte(px, l.peso || 600, true); } ctx.fillText(l.t, 0, 24 + l.y); });
    ctx.restore();
  }
  function pessoa(ctx, x, y, s, cor) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = cor || '#12141F';
    ctx.beginPath(); ctx.arc(0, -86, 13, 0, PI2); ctx.fill();
    ctx.beginPath(); ctx.moveTo(-15, -70); ctx.quadraticCurveTo(0, -78, 15, -70); ctx.lineTo(21, -12); ctx.lineTo(8, -12); ctx.lineTo(8, 0); ctx.lineTo(-8, 0); ctx.lineTo(-8, -12); ctx.lineTo(-21, -12); ctx.closePath(); ctx.fill();
    ctx.lineWidth = 7; ctx.lineCap = 'round'; ctx.strokeStyle = cor || '#12141F'; ctx.beginPath(); ctx.moveTo(-14, -66); ctx.lineTo(-22, -34); ctx.moveTo(14, -66); ctx.lineTo(22, -34); ctx.stroke();
    ctx.restore();
  }

  function modoEtiquetas(ctx, w, h, t, a) {
    ctx.globalAlpha = a;
    var g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#F6E6C8'); g.addColorStop(1, '#E9CFA0'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#7A5230'; ctx.fillRect(0, 0, w, 14); ctx.fillStyle = '#5E3E22'; ctx.fillRect(0, 14, w, 4);
    var cols = Math.max(2, Math.min(7, Math.floor(w / 96))), rows = Math.ceil(ITENS.length / cols), cw = w / cols, th = Math.min(74, (h - 40) / rows * 0.62);
    ITENS.forEach(function (it, j) {
      var col = j % cols, row = Math.floor(j / cols), x = cw * (col + 0.5), fr = Math.log10(it.valor + 1) / 9, y0 = 18 + row * ((h - 30) / rows), cordao = 24 + fr * ((h - 30) / rows - th - 40), rot = OVM.reduz ? 0 : Math.sin(t * 1.1 + j * 0.9) * 0.06;
      ctx.strokeStyle = '#8B6B45'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(x, y0); ctx.lineTo(x + Math.sin(rot) * cordao, y0 + cordao); ctx.stroke();
      var tw = Math.min(cw * 0.88, 112) * (0.78 + 0.28 * fr);
      etiqueta(ctx, x + Math.sin(rot) * cordao, y0 + cordao, tw, th, rot, [{ t: it.nome, px: Math.max(10.5, Math.min(14, tw / 8)), y: 0, peso: 500 }, { t: 'R$ ' + curto(it.valor), px: Math.max(13, Math.min(22, tw / 5.2)), y: th * 0.42, peso: 600 }]);
    });
    ctx.globalAlpha = 1;
  }
  function modoPessoas(ctx, w, h, t, a) {
    ctx.globalAlpha = a;
    var g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#2B2144'); g.addColorStop(0.62, '#C8825A'); g.addColorStop(1, '#E3A266'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    OVM.pintarEstrelas(ctx, w, h * 0.5, est, t, { alpha: 0.5 * a }); ctx.globalAlpha = a;
    ctx.fillStyle = '#7A4A30'; ctx.fillRect(0, h * 0.8, w, h * 0.2);
    ctx.fillStyle = '#3A2530'; [0.12, 0.5, 0.86].forEach(function (fx) { ctx.beginPath(); ctx.moveTo(w * (fx - 0.1), h * 0.8); ctx.lineTo(w * fx, h * 0.52); ctx.lineTo(w * (fx + 0.1), h * 0.8); ctx.closePath(); ctx.fill(); });
    var s = Math.min(1.9, h / 300), nomes = [['José', '20 moedas de prata'], ['Um servo', '30 siclos de prata'], ['Uma pessoa hoje', 'o que você tem?']];
    nomes.forEach(function (n, j) {
      var x = w * (0.2 + j * 0.3), y = h * 0.82, rot = OVM.reduz ? 0 : Math.sin(t * 1.2 + j) * 0.05;
      pessoa(ctx, x, y, s, '#14111C');
      etiqueta(ctx, x, y - 70 * s, Math.min(w * 0.27, 150), 52, rot, [{ t: n[0], px: 12, y: 0, peso: 500 }, { t: n[1], px: Math.min(15, w * 0.026), y: 20, peso: 600 }], j === 2 ? { fundo: '#FFF1BF', borda: '#9A4310' } : {});
    });
    OVM.pilula(ctx, 'o que o mundo já cobrou por pessoas', w / 2, 26, { px: 13, alpha: a, pad: 11 });
    ctx.globalAlpha = 1;
  }
  function modoBalanca(ctx, w, h, t, dt, a) {
    ctx.globalAlpha = a;
    var g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#1A1530'); g.addColorStop(1, '#3A2A3E'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    OVM.pintarEstrelas(ctx, w, h * 0.7, est, t, { alpha: 0.4 * a }); ctx.globalAlpha = a;
    var tot = total(), alvo = 0.22 - 0.045 * OVM.clamp(Math.log10(tot + 1) / 9, 0, 1); ang = OVM.reduz ? alvo : OVM.seguir(ang, alvo, 4, dt);
    var cx = w / 2, y0 = h * 0.3, Lb = Math.min(w * 0.86, 560), hb = Lb / 2, bx = Math.cos(ang) * hb, by = Math.sin(ang) * hb, corda = Math.min(h * 0.26, 110);
    // base e coluna
    ctx.fillStyle = '#8C7A5B'; OVM.caminhoArr(ctx, cx - 60, h * 0.88, 120, 14, 6); ctx.fill(); ctx.fillStyle = '#A8926B'; ctx.fillRect(cx - 7, y0, 14, h * 0.88 - y0);
    ctx.strokeStyle = '#D9C08A'; ctx.lineWidth = 8; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(cx - bx, y0 - by); ctx.lineTo(cx + bx, y0 + by); ctx.stroke();
    ctx.fillStyle = '#F2D9A0'; ctx.beginPath(); ctx.arc(cx, y0, 11, 0, PI2); ctx.fill();
    // prato da esquerda (o que se paga)
    var lx = cx - bx, ly = y0 - by + corda, pw = Math.min(w * 0.3, 150);
    ctx.strokeStyle = '#D9C08A'; ctx.lineWidth = 1.8; ctx.beginPath(); ctx.moveTo(lx, y0 - by); ctx.lineTo(lx - pw / 2, ly); ctx.moveTo(lx, y0 - by); ctx.lineTo(lx + pw / 2, ly); ctx.stroke();
    ctx.fillStyle = '#C9A867'; ctx.beginPath(); ctx.ellipse(lx, ly, pw / 2, 12, 0, 0, PI2); ctx.fill();
    ctx.font = '24px "Apple Color Emoji","Segoe UI Emoji",system-ui'; ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
    prato.slice(-14).forEach(function (it, j) { var colu = j % 5, lin = Math.floor(j / 5); ctx.fillText(it.emoji, lx - pw * 0.36 + colu * pw * 0.18, ly - 6 - lin * 26); });
    // prato da direita (Deus): luz
    var rx = cx + bx, ry = y0 + by + corda;
    ctx.strokeStyle = '#D9C08A'; ctx.beginPath(); ctx.moveTo(rx, y0 + by); ctx.lineTo(rx - pw / 2, ry); ctx.moveTo(rx, y0 + by); ctx.lineTo(rx + pw / 2, ry); ctx.stroke();
    ctx.fillStyle = '#E8C879'; ctx.beginPath(); ctx.ellipse(rx, ry, pw / 2, 12, 0, 0, PI2); ctx.fill();
    var pul = OVM.reduz ? 1 : 0.9 + 0.1 * Math.sin(t * 2); OVM.brilho(ctx, rx, ry - 30, 70 * pul, 'rgba(255,232,150,A)', 0.85); OVM.brilho(ctx, rx, ry - 30, 20, 'rgba(255,255,255,A)', 1);
    ctx.fillStyle = '#FFFBEA'; ctx.beginPath(); ctx.arc(rx, ry - 30, 5, 0, PI2); ctx.fill();
    OVM.pilula(ctx, 'Deus', rx, ry + 30, { px: 14, fundo: 'rgba(242,217,160,.97)', cor: '#1F2A44', pad: 14 }); OVM.pilula(ctx, 'acima de qualquer preço', rx, ry + 58, { px: 11.5, pad: 9, alpha: a });
    OVM.pilula(ctx, prato.length ? 'No prato: R$ ' + F.grande(tot) : 'O prato está vazio', lx, ly + 30, { px: 13, pad: 11, fundo: 'rgba(6,10,26,.8)', alpha: a });
    msg = OVM.seguir(msg, prato.length ? 1 : 0, 3, dt);
    if (msg > 0.05) OVM.pilula(ctx, 'Não importa quanto você some: a balança não se mexe.', cx, h * 0.1, { px: 14, alpha: msg * a, fundo: 'rgba(242,217,160,.96)', cor: '#1F2A44', pad: 13 });
    ctx.globalAlpha = 1;
  }
  function modoPergunta(ctx, w, h, t, a) {
    ctx.globalAlpha = a;
    var g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#04061A'); g.addColorStop(1, '#16204A'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    OVM.pintarEstrelas(ctx, w, h, est, t, { alpha: 0.7 * a }); ctx.globalAlpha = a;
    var cx = w / 2, base = h * 0.9, s = Math.min(2.2, h / 250);
    ctx.fillStyle = '#0B0E1C'; ctx.beginPath(); ctx.ellipse(cx, base + 4, 90 * s, 12 * s, 0, 0, PI2); ctx.fill();
    pessoa(ctx, cx, base, s, '#0B0E1C');
    var rot = OVM.reduz ? 0 : Math.sin(t * 1.4) * 0.09;
    etiqueta(ctx, cx, base - 66 * s, Math.min(w * 0.4, 180), Math.min(86, h * 0.26), rot, [{ t: 'quanto?', px: Math.min(26, w * 0.055), y: Math.min(30, h * 0.07), peso: 600 }], { fundo: '#FFF1BF', borda: '#9A4310' });
    OVM.pilula(ctx, '“O que você tem para oferecer?”', cx, 30, { px: 15, pad: 13, alpha: a });
    ctx.globalAlpha = 1;
  }
  function quadro(dt, t) {
    var w = T.w, h = T.h, ctx = T.ctx;
    OVM.fundoCanvas(T);
    ['etiquetas', 'pessoas', 'balanca', 'pergunta'].forEach(function (m) { am[m] = OVM.reduz ? (m === modo ? 1 : 0) : OVM.seguir(am[m], m === modo ? 1 : 0, 6, dt); });
    ctx.fillStyle = '#0B0E1C'; ctx.fillRect(0, 0, w, h);
    if (am.etiquetas > 0.01) modoEtiquetas(ctx, w, h, t, am.etiquetas);
    if (am.pessoas > 0.01) modoPessoas(ctx, w, h, t, am.pessoas);
    if (am.balanca > 0.01) modoBalanca(ctx, w, h, t, dt, am.balanca);
    if (am.pergunta > 0.01) modoPergunta(ctx, w, h, t, am.pergunta);
  }
  OVM.anima(quadro, canvas);
  quadro(0.016, 0.5);

  // ---------------------------------------------------------------- itens da balança
  ITENS.forEach(function (it) {
    var li = document.createElement('li'), b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.textContent = it.emoji + ' ' + it.nome; b.title = 'R$ ' + curto(it.valor);
    b.addEventListener('click', function () { prato.push(it); }); li.appendChild(b); listaEl.appendChild(li);
  });
  bTudo.addEventListener('click', function () { prato = ITENS.slice(); });
  bLimpar.addEventListener('click', function () { prato = []; });

  // ---------------------------------------------------------------- passos
  function cit(kk) { var v = V[kk]; return '<blockquote class="vers">“' + v.t + '”<cite>' + v.ref + '</cite></blockquote>'; }
  function vai(m, ctl) { modo = m; cena.setAttribute('data-modo', ctl || m); }
  var passos = [
    { rotulo: 'De volta às etiquetas', ir: function () { vai('etiquetas'); },
      html: '<b class="grande">Tudo tem preço</b><p>Voltamos às etiquetas. O chocolate quente, a casa, o carro, a viagem ao espaço: tudo o que vimos tem um preço, e <b>quanto mais vale, mais custa</b>.</p><p class="pequeno">Repare: quanto maior o preço, maior a etiqueta.</p>' },
    { rotulo: 'O que o mundo faz com as pessoas', ir: function () { vai('pessoas'); },
      html: '<p>No mundo, o valor de uma pessoa muitas vezes é medido pelo que ela <b>tem</b> ou pelo que pode <b>oferecer em troca</b>. Já houve quem fosse vendido, por preços irrisórios:</p>' + cit('gn3728') + cit('ex2132') + '<p class="pequeno">Isso nunca foi o valor de ninguém: foi o que o mundo, errado, chegou a cobrar.</p>' },
    { rotulo: 'E quanto custaria alcançar Deus?', ir: function () { vai('balanca'); },
      html: '<p>Se tudo tem preço, e Deus está <b>acima de qualquer preço</b>, tente pagar: ponha no prato o que quiser.</p>' + cit('sl49') },
    { rotulo: 'A pergunta que fica', ir: function () { vai('pergunta'); },
      html: '<p>Se nada que existe à venda alcança Deus, <b>quanto custaria alcançá-lo</b>? E, ao contrário: <b>quanto custaria algo que Ele quisesse comprar</b>?</p><p>Guarde essas duas perguntas. Falta uma parte.</p>' }
  ];
  OVM.guia({ passos: passos });
});

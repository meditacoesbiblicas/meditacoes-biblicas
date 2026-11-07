/* Parte 4: perto e longe. Um eixo com o tempo que a luz leva até cada lugar (1 segundo … 4,2 anos); a luz "voa" pelo eixo até o lugar escolhido. */
OVM.pronto(function () {
  var D = OVM_DADOS, F = OVM.fmt, PI2 = 6.2832, CL = D.c;
  var canvas = OVM.$('#tela'), T = OVM.tela(canvas), est = OVM.estrelas(8, 240), chips = OVM.$$('#p4-chips .chip');
  var LMIN = -0.25, LMAX = 8.55, cabeca = LMIN, alvoLog = LMIN, sel = [], pontos = [];
  var folhaTerra = document.createElement('canvas'); folhaTerra.width = folhaTerra.height = 1024; OVM.cosmos()[0].pintar(folhaTerra.getContext('2d'), OVM.rand(31));
  var ORDEM = ['lua', 'sol', 'venus', 'marte', 'jupiter', 'netuno', 'voyager', 'proxima'];
  var LOOK = {
    lua: { cor: '#D7D7D0', r: 6, frase: 'Pouco mais de <b>1 segundo</b> para a luz. Uma nave com gente leva cerca de <b>3 dias</b>.' },
    sol: { cor: '#FFD25A', r: 11, frase: 'A luz do Sol que te aquece saiu dele há <b>mais de 8 minutos</b>.' },
    venus: { cor: '#F0DDB0', r: 7, frase: 'A distância muda porque os planetas giram: a luz leva de <b>2 a 15 minutos</b>.' },
    marte: { cor: '#E0683F', r: 7, frase: 'De <b>3 a 22 minutos</b>. Um sinal de rádio demora o mesmo para ir ou voltar.' },
    jupiter: { cor: '#E2B88A', r: 11, frase: 'Já passa de <b>meia hora</b> de luz.' },
    netuno: { cor: '#6C8DFF', r: 8, frase: 'Mais de <b>4 horas</b> de luz. A sonda Voyager 2 levou 12 anos para chegar lá.' },
    voyager: { cor: '#FFC24D', r: 7, frase: 'Em <b>18 de novembro de 2026</b> a Voyager 1 chega a <b>1 dia-luz</b>. Um comando leva um dia para chegar, e a resposta, outro dia.' },
    proxima: { cor: '#FF9E7A', r: 8, frase: 'Aqui já não dá para usar segundos nem minutos: são <b>4,2 anos</b> de luz. A Voyager 1 levaria uns <b>75 mil anos</b>.' }
  };
  var C = {}; D.corpos.forEach(function (c) { C[c.id] = c; });
  function segs(c) { return c.km / CL; }
  function logs(c) { return Math.log10(segs(c)); }

  function tl(s) {
    if (s < 60) return F.n(s, s < 10 ? 1 : 0) + ' s';
    if (s < 3600) { var m = Math.floor(s / 60), r = Math.round(s - m * 60); if (r === 60) { m++; r = 0; } return m + ' min' + (r ? ' ' + r + ' s' : ''); }
    if (s < 86400) { var h = Math.floor(s / 3600), mm = Math.round((s - h * 3600) / 60); if (mm === 60) { h++; mm = 0; } return h + ' h' + (mm ? ' ' + mm + ' min' : ''); }
    if (s < 86400 * 1.5) return '1 dia';
    if (s < D.anoS) return F.n(s / 86400, 0) + ' dias';
    return F.n(s / D.anoS, 1) + ' anos';
  }
  function faixaTxt(c) {
    var a = c.min / CL, b = c.max / CL;
    if (b < 3600) return 'de ' + F.n(a / 60, 0) + ' a ' + F.n(b / 60, 0) + ' minutos';
    return 'de ' + F.n(a / 3600, 1) + ' a ' + F.n(b / 3600, 1) + ' horas';
  }
  function distTxt(c) { return c.min ? 'de ' + F.grande(c.min) + ' a ' + F.grande(c.max) + ' de km' : F.distKm(c.km); }

  // ---------------------------------------------------------------- eixo
  function eixo(w, h) {
    var vert = w < 430 || w / h < 1.2;
    if (vert) return { vert: true, x: Math.min(96, w * 0.26), y0: h - 36, y1: 34 };
    return { vert: false, y: h * 0.64, x0: 34, x1: w - 30 };
  }
  function pto(E, lg) { var f = (lg - LMIN) / (LMAX - LMIN); return E.vert ? { x: E.x, y: E.y0 + (E.y1 - E.y0) * f } : { x: E.x0 + (E.x1 - E.x0) * f, y: E.y }; }

  var TICKS = [[0, '1 s'], [1.778, '1 min'], [3.556, '1 h'], [4.936, '1 dia'], [6.42, '1 mês'], [7.5, '1 ano']];
  function corpo(ctx, id, x, y, r, a, t) {
    var L = LOOK[id]; ctx.save(); ctx.globalAlpha = a;
    OVM.brilho(ctx, x, y, r * 2.6, 'rgba(255,240,200,A)', id === 'sol' ? 0.7 : 0.25);
    ctx.fillStyle = L.cor;
    if (id === 'voyager') { ctx.translate(x, y); ctx.rotate(-0.5); ctx.fillRect(-r, -r * 0.55, r * 2, r * 1.1); ctx.fillStyle = '#EDEFF3'; ctx.beginPath(); ctx.ellipse(r * 1.1, 0, r * 0.45, r * 0.95, 0, 0, PI2); ctx.fill(); }
    else if (id === 'proxima') { ctx.beginPath(); for (var k = 0; k < 8; k++) { var rr = k % 2 ? r * 0.45 : r * 1.15, an = k * 0.7854; ctx.lineTo(x + Math.cos(an) * rr, y + Math.sin(an) * rr); } ctx.closePath(); ctx.fill(); }
    else { ctx.beginPath(); ctx.arc(x, y, r, 0, PI2); ctx.fill(); if (id === 'jupiter') { ctx.fillStyle = 'rgba(150,90,50,.5)'; ctx.fillRect(x - r, y - r * 0.2, r * 2, r * 0.25); } }
    ctx.restore();
  }

  // retratos grandes do lugar escolhido (esferas pré-desenhadas; Sol, sonda e estrela são desenhados na hora)
  function esf(c0, c1, c2, det) {
    var cv = document.createElement('canvas'); cv.width = cv.height = 256; var x = cv.getContext('2d'), r = OVM.rand(41);
    OVM.motor.esfera(x, 128, 128, 120, c0, c1, c2); x.save(); x.beginPath(); x.arc(128, 128, 120, 0, PI2); x.clip(); if (det) det(x, r); x.restore(); OVM.motor.sombra(x, 128, 128, 120, 0.9); return cv;
  }
  var RETR = {
    lua: esf('#F2F1EC', '#B9B7B0', '#55544F', function (x, r) { x.fillStyle = 'rgba(80,80,80,.30)'; for (var i = 0; i < 18; i++) { x.beginPath(); x.arc(30 + r() * 196, 30 + r() * 196, 6 + r() * 20, 0, PI2); x.fill(); } }),
    venus: esf('#FFF2CF', '#E9CE92', '#8D6A38', function (x, r) { x.fillStyle = 'rgba(255,255,255,.28)'; for (var i = 0; i < 9; i++) x.fillRect(0, 20 + i * 26 + r() * 6, 256, 8 + r() * 8); }),
    marte: esf('#F6C39A', '#C0623A', '#5A2412', function (x, r) { x.fillStyle = 'rgba(110,45,24,.55)'; for (var i = 0; i < 6; i++) OVM.motor.mancha(x, 40 + r() * 176, 50 + r() * 150, 20 + r() * 26, r, 1.4, 0.8, r() * 3); x.fillStyle = 'rgba(255,255,255,.85)'; x.beginPath(); x.ellipse(128, 16, 44, 13, 0, 0, PI2); x.fill(); }),
    jupiter: esf('#F2D8B6', '#C79B6C', '#6E4A2C', function (x, r) { for (var i = 0; i < 12; i++) { x.fillStyle = i % 2 ? 'rgba(130,80,50,.38)' : 'rgba(255,240,215,.30)'; x.fillRect(0, 12 + i * 20 + r() * 4, 256, 10 + r() * 10); } x.fillStyle = 'rgba(190,80,50,.7)'; x.beginPath(); x.ellipse(160, 160, 20, 12, 0, 0, PI2); x.fill(); }),
    netuno: esf('#9DB8FF', '#3F63D6', '#142566', function (x, r) { x.fillStyle = 'rgba(255,255,255,.22)'; for (var i = 0; i < 5; i++) x.fillRect(0, 40 + i * 44 + r() * 8, 256, 4 + r() * 5); })
  };
  function retrato(ctx, id, cx, cy, rad, a, t) {
    ctx.save(); ctx.globalAlpha = a;
    if (RETR[id]) { OVM.brilho(ctx, cx, cy, rad * 1.7, 'rgba(160,190,255,A)', 0.14); ctx.drawImage(RETR[id], cx - rad, cy - rad, rad * 2, rad * 2); }
    else if (id === 'sol') { OVM.brilho(ctx, cx, cy, rad * 2.6, 'rgba(255,200,90,A)', 0.7); OVM.motor.esfera(ctx, cx, cy, rad, '#FFF6C8', '#FFC93C', '#F08A1C'); }
    else if (id === 'proxima') { OVM.brilho(ctx, cx, cy, rad * 2.4, 'rgba(255,130,90,A)', 0.6); OVM.motor.esfera(ctx, cx, cy, rad * 0.8, '#FFC9A8', '#FF7A4A', '#B83A18'); }
    else if (id === 'voyager') {
      ctx.translate(cx, cy); ctx.rotate(-0.35); var k = rad / 60;
      ctx.scale(k, k); ctx.fillStyle = '#F1F2F5'; ctx.beginPath(); ctx.ellipse(-8, 0, 46, 36, 0, -1.5, 1.5); ctx.fill(); ctx.fillStyle = '#C8CCD6'; ctx.beginPath(); ctx.ellipse(-8, 0, 20, 36, 0, 0, PI2); ctx.fill();
      ctx.fillStyle = '#B0B6C4'; ctx.fillRect(-60, -10, 52, 20); ctx.fillStyle = '#FFC24D'; ctx.fillRect(-58, -7, 46, 14);
      ctx.strokeStyle = '#D9DDE6'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-60, 0); ctx.lineTo(-118, 22); ctx.moveTo(-60, -4); ctx.lineTo(-120, -34); ctx.stroke(); ctx.fillStyle = '#4F5668'; ctx.fillRect(-124, -40, 12, 12); ctx.fillRect(-124, 18, 12, 12);
    }
    ctx.restore();
  }
  function textoTempo(c) { return c.min ? (c.max / CL < 3600 ? F.n(c.min / CL / 60, 0) + ' a ' + F.n(c.max / CL / 60, 0) + ' min' : F.n(c.min / CL / 3600, 1) + ' a ' + F.n(c.max / CL / 3600, 1) + ' h') : (c.id === 'voyager' ? '1 dia' : c.id === 'proxima' ? '4,2 anos' : tl(segs(c))); }
  var figA = 0;

  function quadro(dt, t) {
    var w = T.w, h = T.h, ctx = T.ctx, E = eixo(w, h), vert = E.vert, i, k;
    OVM.fundoCanvas(T);
    var g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#04071A'); g.addColorStop(1, '#0C1330'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    OVM.pintarEstrelas(ctx, w, h, est, t, { alpha: 0.7 });
    cabeca = OVM.reduz ? alvoLog : OVM.seguir(cabeca, alvoLog, 2.3, dt);
    var p0 = pto(E, LMIN), p1 = pto(E, LMAX), ph = pto(E, cabeca);
    // eixo, feixe e marcas de tempo
    ctx.lineCap = 'round'; ctx.strokeStyle = 'rgba(255,255,255,.22)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(p0.x, p0.y); ctx.lineTo(p1.x, p1.y); ctx.stroke();
    var ag = vert ? ctx.createLinearGradient(0, p0.y, 0, p1.y) : ctx.createLinearGradient(p0.x, 0, p1.x, 0); ag.addColorStop(0, '#FFC46B'); ag.addColorStop(1, '#A9C6FF');
    ctx.strokeStyle = ag; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(p0.x, p0.y); ctx.lineTo(ph.x, ph.y); ctx.stroke();
    for (i = 0; i < TICKS.length; i++) {
      var q = pto(E, TICKS[i][0]); ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 1.5; ctx.beginPath();
      if (vert) { ctx.moveTo(q.x - 6, q.y); ctx.lineTo(q.x + 6, q.y); } else { ctx.moveTo(q.x, q.y - 6); ctx.lineTo(q.x, q.y + 6); } ctx.stroke();
      OVM.pilula(ctx, TICKS[i][1], vert ? q.x - 12 : q.x, vert ? q.y : q.y + 20, { px: 10.5, ancora: vert ? 'dir' : 'meio', alpha: 0.85, pad: 6 });
    }
    // a Terra, no começo
    var tr = vert ? 13 : 14, sz = tr * 2 / 0.9; ctx.drawImage(folhaTerra, p0.x - sz / 2, p0.y - sz / 2 + (vert ? 0 : 0), sz, sz);
    OVM.pilula(ctx, 'Terra (aqui)', vert ? p0.x + 20 : p0.x + 8, vert ? p0.y : p0.y - 28, { px: 10.5, ancora: 'esq', alpha: 0.9, pad: 6 });
    // lugares
    pontos = [];
    for (i = 0; i < ORDEM.length; i++) {
      var id = ORDEM[i], c = C[id], lg = logs(c), pos = pto(E, lg), L = LOOK[id], passou = cabeca >= lg - 0.03, ativo = sel.indexOf(id) >= 0, a = ativo ? 1 : passou ? 0.9 : 0.5;
      if (c.min) { var pa = pto(E, Math.log10(c.min / CL)), pb = pto(E, Math.log10(c.max / CL)); ctx.globalAlpha = ativo ? 0.9 : 0.4; ctx.strokeStyle = L.cor; ctx.lineWidth = 9; ctx.beginPath(); ctx.moveTo(pa.x, pa.y); ctx.lineTo(pb.x, pb.y); ctx.stroke(); ctx.globalAlpha = 1; }
      corpo(ctx, id, pos.x, pos.y, L.r * (ativo ? 1.25 : 1), a, t);
      if (ativo) { ctx.strokeStyle = '#FFE9A8'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(pos.x, pos.y, L.r * 1.25 + 7 + (OVM.reduz ? 0 : Math.sin(t * 4) * 1.5), 0, PI2); ctx.stroke(); }
      // nome: na horizontal, em alturas alternadas; na vertical, só do escolhido
      if (!vert) { var alt = 30 + (i % 3) * 26; ctx.strokeStyle = 'rgba(255,255,255,' + (ativo ? 0.7 : 0.25) + ')'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(pos.x, pos.y - L.r - 3); ctx.lineTo(pos.x, pos.y - alt + 11); ctx.stroke(); OVM.pilula(ctx, c.nome, pos.x, pos.y - alt, { px: 11.5, alpha: ativo ? 1 : 0.8, cor: ativo ? '#FFE9B8' : '#fff', fundo: ativo ? 'rgba(80,60,10,.88)' : 'rgba(6,10,26,.76)', pad: 7 }); }
      else if (ativo) OVM.pilula(ctx, c.nome, pos.x + 22, pos.y, { px: 12, ancora: 'esq', cor: '#FFE9B8', fundo: 'rgba(80,60,10,.88)', pad: 8 });
      pontos.push({ id: id, x: pos.x, y: pos.y, r: Math.max(16, L.r + 8) });
    }
    // a luz (a cabeça do feixe)
    OVM.brilho(ctx, ph.x, ph.y, 28, 'rgba(255,240,190,A)', 0.95); ctx.fillStyle = '#FFFBE8'; ctx.beginPath(); ctx.arc(ph.x, ph.y, 5.5, 0, PI2); ctx.fill();
    var ts = Math.pow(10, cabeca), txt = cabeca <= LMIN + 0.02 ? 'a luz sai da Terra' : 'a luz levou ' + tl(ts);
    // retrato(s) grande(s) do(s) lugar(es) escolhido(s), com o tempo da luz em letras grandes
    figA = OVM.seguir(figA, sel.length ? 1 : 0, 6, dt);
    if (figA > 0.02 && sel.length) {
      var n = sel.length, u = Math.min(w, h), rad = u * (n === 1 ? 0.13 : 0.092), gap = rad * 0.55;
      for (k = 0; k < n; k++) {
        var cid = sel[k], cc = C[cid], cxr = vert ? (w * 0.66 + (k - (n - 1) / 2) * (rad * 2 + gap)) : (w - 30 - rad - (n - 1 - k) * (rad * 2 + gap)), cyr = vert ? h * 0.24 : h * 0.2 + (n === 1 ? 6 : 0);
        retrato(ctx, cid, cxr, cyr, rad * figA, figA, t);
        OVM.pilula(ctx, cc.nome, cxr, cyr + rad + 14, { px: 11.5, alpha: figA, pad: 8 });
        ctx.save(); ctx.globalAlpha = figA; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.fillStyle = '#FFE9B8'; ctx.font = OVM.fonte(n === 1 ? Math.max(18, Math.min(30, rad * 0.5)) : 15, 600, true); ctx.fillText(textoTempo(cc), cxr, cyr + rad + (vert ? 40 : 46)); ctx.restore();
      }
    }
    OVM.pilula(ctx, txt, vert ? Math.min(w - 12, ph.x + 22 + 0) : Math.min(w - 90, Math.max(90, ph.x)), vert ? Math.max(30, Math.min(h - 18, ph.y)) + (cabeca > LMAX - 1 ? 0 : 0) : h * 0.64 + 50, { px: 14, ancora: vert ? 'esq' : 'meio', fundo: 'rgba(242,217,160,.97)', cor: '#1F2A44', pad: 11 });
  }
  OVM.anima(quadro, canvas);
  quadro(0.016, 0.5);

  canvas.addEventListener('click', function (e) {
    var r = canvas.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top, best = null, bd = 1e9;
    pontos.forEach(function (p) { var d = Math.hypot(p.x - x, p.y - y); if (d < p.r + 6 && d < bd) { bd = d; best = p; } });
    if (best) irCorpo(best.id);
  });
  canvas.style.cursor = 'pointer';

  // ---------------------------------------------------------------- passos
  function bloco(id) {
    var c = C[id], L = LOOK[id], tempo = c.min ? faixaTxt(c) : (id === 'voyager' ? '1 dia' : id === 'proxima' ? '4,2 anos' : tl(segs(c)));
    return '<b class="grande">' + c.nome + '</b><p class="p1-linha"><span class="p1-preco"><small>luz: </small>' + tempo + '</span></p>' +
      '<p>' + L.frase + '</p><p class="p1-qual"><b>Distância:</b> ' + distTxt(c) + '</p>' +
      '<details class="conta"><summary>Conta e fonte</summary><p>' + c.obs + '. Tempo da luz = distância ÷ 299.792 km/s. ' +
      (id === 'voyager' ? 'Fonte: NASA, "What Is a Light-Day?" (Voyager 1).' : id === 'proxima' ? 'Fonte: NASA (cerca de 4,24 anos-luz).' : 'Fonte: NASA, fichas técnicas dos planetas e da Lua.') + '</p></details>';
  }
  function foca(ids, alvo) { sel = ids; alvoLog = alvo; chips.forEach(function (c) { c.classList.toggle('ativo', ids.indexOf(c.getAttribute('data-c')) >= 0); }); }
  var mapaPasso = { lua: 1, sol: 2, venus: 3, marte: 3, jupiter: 4, netuno: 4, voyager: 5, proxima: 6 };
  function irCorpo(id) { OVM.guiaAtual.ir(mapaPasso[id]); }

  var passos = [
    { rotulo: 'Perto não precisa de ano-luz', ir: function () { foca([], LMIN); },
      html: '<b class="grande">Medir o céu com a luz</b><p>Com a régua da luz dá para medir <b>tudo</b>. Para o que está perto, bastam <b>segundos e minutos</b>. Para o que está muito longe, <b>anos</b>.</p><p class="pequeno">Toque em <b>Próximo</b> e acompanhe a luz saindo da Terra.</p>' },
    { rotulo: 'O vizinho mais perto', ir: function () { foca(['lua'], logs(C.lua)); }, html: function () { return bloco('lua'); } },
    { rotulo: 'A nossa estrela', ir: function () { foca(['sol'], logs(C.sol)); }, html: function () { return bloco('sol'); } },
    { rotulo: 'Vênus e Marte', ir: function () { foca(['venus', 'marte'], logs(C.marte)); }, html: function () { return bloco('venus') + '<hr class="fino">' + bloco('marte'); } },
    { rotulo: 'Os gigantes', ir: function () { foca(['jupiter', 'netuno'], logs(C.netuno)); }, html: function () { return bloco('jupiter') + '<hr class="fino">' + bloco('netuno'); } },
    { rotulo: 'A sonda mais distante', ir: function () { foca(['voyager'], logs(C.voyager)); }, html: function () { return bloco('voyager'); } },
    { rotulo: 'A estrela mais próxima', ir: function () { foca(['proxima'], logs(C.proxima)); }, html: function () { return bloco('proxima'); } },
    { rotulo: 'Perto e longe', ir: function () { foca([], LMAX - 0.2); },
      html: '<p>Para o que está <b>perto</b>, segundos e minutos de luz. Para o que está <b>longe</b>, o <b>ano-luz</b>.</p><p>E a estrela mais próxima já está a 4,2 anos-luz. <b>O que existe depois dela?</b></p>' }
  ];
  var g = OVM.guia({ passos: passos });
  chips.forEach(function (c) { c.addEventListener('click', function () { irCorpo(c.getAttribute('data-c')); }); });
});

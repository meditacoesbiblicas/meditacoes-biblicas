/* Parte 2: a viagem mais cara. Um foguete sobe pelas paradas (beira do espaço, estação, Lua, Marte) e o preço sobe com ele. */
OVM.pronto(function () {
  var V = OVM_DADOS.viagens, F = OVM.fmt, M = OVM.motor, PI2 = 6.2832;
  var canvas = OVM.$('#tela'), T = OVM.tela(canvas), est = OVM.estrelas(5, 260), rnd = OVM.rand(9);
  var etq = OVM.$('#p2-etq'), altEl = OVM.$('#p2-alt'), slider = OVM.$('#p2-botao'), saida = OVM.$('#p2-saida'), chips = OVM.$$('#p2-chips .chip');
  var CASA = OVM_DADOS.precos[5].valor;
  var pos = 0, alvo = 0, fumaca = [], acum = 0, ultimoNum = 0;

  function hex(c) { return [parseInt(c.substr(1, 2), 16), parseInt(c.substr(3, 2), 16), parseInt(c.substr(5, 2), 16)]; }
  function cor(a, b, t) { var x = hex(a), y = hex(b); return 'rgb(' + Math.round(OVM.lerp(x[0], y[0], t)) + ',' + Math.round(OVM.lerp(x[1], y[1], t)) + ',' + Math.round(OVM.lerp(x[2], y[2], t)) + ')'; }

  // ---- as cinco paradas: céu, Terra, Lua, Marte, estação e foguete (posições em frações da largura/altura)
  var K = [
    { c0: '#4FB0F2', c1: '#E3F5FF', st: 0, solo: 1, iss: 0, lua: 0, marte: 0, f: [0.5, 0.72, 1, 0], terra: function (w, h, X) { return [w / 2, h + 2 * X, 2 * X]; } },
    { c0: '#01030A', c1: '#0C2A5C', st: 1, solo: 0, iss: 0, lua: 0, marte: 0, f: [0.5, 0.46, 0.8, 0], terra: function (w, h, X) { var r = 1.7 * X; return [w / 2, 0.86 * h + r, r]; } },
    { c0: '#01030A', c1: '#0A1E48', st: 1, solo: 0, iss: 1, lua: 0, marte: 0, f: [0.5, 0.5, 0.65, 0.15], terra: function (w, h, X) { var r = 1.25 * X; return [w * 0.45, 0.92 * h + r, r]; } },
    { c0: '#01030A', c1: '#050A1C', st: 1, solo: 0, iss: 0, lua: 1, marte: 0, f: [0.5, 0.55, 0.5, 0.55], terra: function (w, h, X) { return [w * 0.17, h * 0.78, 0.14 * X]; } },
    { c0: '#02030A', c1: '#0A0710', st: 1, solo: 0, iss: 0, lua: 0, marte: 1, f: [0.42, 0.58, 0.45, 0.6], terra: function (w, h, X) { return [w * 0.1, h * 0.84, 0.006 * X]; } }
  ];
  var ALTS = [0.5, 100, 400, OVM_DADOS.luaKm, 225e6];
  var NOMES_REGUA = ['Plataforma', '100 km', '400 km', 'Lua', 'Marte'];

  // ---- desenhos pré-prontos
  function folhaEsfera(c0, c1, c2, manchas, calota) {
    var cv = document.createElement('canvas'); cv.width = cv.height = 256; var x = cv.getContext('2d'), r = OVM.rand(77);
    M.esfera(x, 128, 128, 120, c0, c1, c2);
    x.save(); x.beginPath(); x.arc(128, 128, 120, 0, PI2); x.clip();
    manchas(x, r);
    if (calota) { x.fillStyle = 'rgba(255,255,255,.85)'; x.beginPath(); x.ellipse(128, 18, 46, 14, 0, 0, PI2); x.fill(); }
    x.restore(); M.sombra(x, 128, 128, 120, 1);
    return cv;
  }
  var marteSp = folhaEsfera('#F6C39A', '#C0623A', '#5A2412', function (x, r) { x.fillStyle = 'rgba(110,45,24,.55)'; for (var i = 0; i < 6; i++) M.mancha(x, 40 + r() * 176, 50 + r() * 150, 20 + r() * 26, r, 1.4, 0.8, r() * 3); }, true);
  var luaSp = folhaEsfera('#F2F1EC', '#B9B7B0', '#55544F', function (x, r) { x.fillStyle = 'rgba(80,80,80,.30)'; for (var i = 0; i < 18; i++) { x.beginPath(); x.arc(30 + r() * 196, 30 + r() * 196, 6 + r() * 20, 0, PI2); x.fill(); } }, false);
  var nuvens = []; for (var q = 0; q < 46; q++) nuvens.push({ u: rnd(), d: rnd(), rx: 30 + rnd() * 90, ry: 5 + rnd() * 10, a: 0.35 + rnd() * 0.4 });
  var colinas = []; for (var c = 0; c < 4; c++) colinas.push({ ph: rnd() * 6, am: 0.02 + rnd() * 0.03, fr: 1 + rnd() * 2 });

  function terraD(ctx, c, alpha, w, h) {
    var cx = c[0], cy = c[1], r = c[2];
    if (alpha < 0.01 || r < 1) return;
    ctx.save(); ctx.globalAlpha = alpha;
    if (r < 12) { OVM.brilho(ctx, cx, cy, 16, 'rgba(120,180,255,A)', 0.8); ctx.fillStyle = '#74BAFF'; ctx.beginPath(); ctx.arc(cx, cy, Math.max(2, r), 0, PI2); ctx.fill(); ctx.restore(); return; }
    var g = ctx.createRadialGradient(cx, cy, r * 0.985, cx, cy, r * 1.04);
    g.addColorStop(0, 'rgba(120,185,255,.6)'); g.addColorStop(1, 'rgba(120,185,255,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, r * 1.04, 0, PI2); ctx.fill();
    var og = ctx.createRadialGradient(cx, cy - r * 0.15, r * 0.55, cx, cy, r);
    og.addColorStop(0, '#0A3272'); og.addColorStop(0.86, '#1B66C4'); og.addColorStop(1, '#7CC0FF');
    ctx.fillStyle = og; ctx.beginPath(); ctx.arc(cx, cy, r, 0, PI2); ctx.fill();
    if (r > 70) {
      ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, r, 0, PI2); ctx.clip();
      var span = Math.min(Math.PI, w / r * 1.3);
      for (var i = 0; i < nuvens.length; i++) {
        var n = nuvens[i], ang = -Math.PI / 2 + (n.u - 0.5) * span, rr = r - n.d * Math.min(r * 0.3, h * 0.22);
        ctx.save(); ctx.translate(cx + Math.cos(ang) * rr, cy + Math.sin(ang) * rr); ctx.rotate(ang + Math.PI / 2);
        ctx.fillStyle = 'rgba(255,255,255,' + n.a + ')'; ctx.beginPath(); ctx.ellipse(0, 0, Math.min(n.rx, r * 0.4), n.ry, 0, 0, PI2); ctx.fill(); ctx.restore();
      }
      ctx.restore();
    }
    ctx.restore();
  }
  function esferaSp(ctx, sp, cx, cy, r, a) { if (a < 0.01 || r < 1) return; ctx.globalAlpha = a; ctx.drawImage(sp, cx - r, cy - r, r * 2, r * 2); ctx.globalAlpha = 1; }

  function chao(ctx, w, h, dy, u, t) {
    ctx.save(); ctx.translate(0, dy);
    // nuvens do dia
    ctx.fillStyle = 'rgba(255,255,255,.75)';
    for (var i = 0; i < 4; i++) { var x = (w * (0.15 + i * 0.27) + t * (4 + i)) % (w + 160) - 80, y = h * (0.2 + (i % 2) * 0.12); ctx.beginPath(); ctx.ellipse(x, y, 54, 14, 0, 0, PI2); ctx.ellipse(x + 30, y - 8, 36, 14, 0, 0, PI2); ctx.fill(); }
    // colinas
    var base = h * 0.8;
    ctx.fillStyle = '#5BAA68'; ctx.beginPath(); ctx.moveTo(0, h * 2); ctx.lineTo(0, base);
    for (var px = 0; px <= w; px += 12) ctx.lineTo(px, base - Math.sin(px / w * 5 + colinas[0].ph) * h * 0.035 - Math.sin(px / w * 9 + colinas[1].ph) * h * 0.015);
    ctx.lineTo(w, h * 2); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#3F8F55'; ctx.beginPath(); ctx.moveTo(0, h * 2); ctx.lineTo(0, base + h * 0.07);
    for (px = 0; px <= w; px += 12) ctx.lineTo(px, base + h * 0.07 - Math.sin(px / w * 4 + colinas[2].ph) * h * 0.025);
    ctx.lineTo(w, h * 2); ctx.closePath(); ctx.fill();
    // plataforma e torre
    var sc = u / 330, px0 = w / 2, topo = h * 0.72 + 56 * sc;
    ctx.fillStyle = '#8C94A6'; ctx.fillRect(px0 - 62 * sc, topo, 124 * sc, h * 0.2);
    ctx.fillStyle = '#6C7487'; ctx.fillRect(px0 - 62 * sc, topo, 124 * sc, 6 * sc);
    var tx = px0 - 62 * sc - 20 * sc;
    ctx.strokeStyle = '#C9CED8'; ctx.lineWidth = Math.max(1.5, 2.4 * sc);
    ctx.strokeRect(tx, topo - 170 * sc, 22 * sc, 170 * sc);
    for (var k = 0; k < 7; k++) { ctx.beginPath(); ctx.moveTo(tx, topo - k * 24 * sc); ctx.lineTo(tx + 22 * sc, topo - (k + 1) * 24 * sc); ctx.moveTo(tx + 22 * sc, topo - k * 24 * sc); ctx.lineTo(tx, topo - (k + 1) * 24 * sc); ctx.stroke(); }
    ctx.beginPath(); ctx.moveTo(tx + 22 * sc, topo - 118 * sc); ctx.lineTo(px0 - 15 * sc, topo - 118 * sc); ctx.stroke();
    ctx.restore();
  }
  function issD(ctx, x, y, s, a, t) {
    if (a < 0.01) return;
    ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(Math.sin(t * 0.3) * 0.05);
    ctx.fillStyle = '#CDD2DC'; ctx.fillRect(-70, -2.5, 140, 5);
    [-52, -30, 30, 52].forEach(function (px) {
      ctx.fillStyle = '#2B63CC'; ctx.fillRect(px - 9, -34, 18, 28); ctx.fillRect(px - 9, 6, 18, 28);
      ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.lineWidth = 1; for (var g = 1; g < 3; g++) { ctx.beginPath(); ctx.moveTo(px - 9 + g * 6, -34); ctx.lineTo(px - 9 + g * 6, -6); ctx.moveTo(px - 9 + g * 6, 6); ctx.lineTo(px - 9 + g * 6, 34); ctx.stroke(); }
    });
    ctx.fillStyle = '#EEF0F4'; ctx.fillRect(-16, -8, 32, 16); ctx.fillRect(-4, -14, 8, 28); ctx.fillStyle = '#AEB6C6'; ctx.fillRect(-16, -8, 32, 3);
    OVM.brilho(ctx, 0, 0, 40, 'rgba(255,240,200,A)', 0.25);
    ctx.restore();
  }
  function foguete(ctx, x, y, sc, ch, rot, t) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc);
    if (ch > 0.05) ctx.translate(Math.sin(t * 70) * ch * 0.9, Math.cos(t * 60) * ch * 0.5);
    if (ch > 0.04) {
      var L = (34 + 24 * Math.abs(Math.sin(t * 42))) * (0.4 + ch * 0.8), g = ctx.createLinearGradient(0, 56, 0, 56 + L);
      g.addColorStop(0, '#FFF6C4'); g.addColorStop(0.35, '#FFB43C'); g.addColorStop(1, 'rgba(255,90,30,0)');
      OVM.brilho(ctx, 0, 62, 46, 'rgba(255,170,60,A)', 0.7 * ch);
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(-10, 54); ctx.quadraticCurveTo(0, 56 + L * 1.3, 10, 54); ctx.closePath(); ctx.fill();
    }
    ctx.fillStyle = '#D9482B';
    ctx.beginPath(); ctx.moveTo(-14, 26); ctx.lineTo(-30, 64); ctx.lineTo(-14, 54); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(14, 26); ctx.lineTo(30, 64); ctx.lineTo(14, 54); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#F4F6FA'; ctx.beginPath(); ctx.moveTo(0, -64); ctx.quadraticCurveTo(16, -36, 14, 20); ctx.lineTo(14, 56); ctx.lineTo(-14, 56); ctx.lineTo(-14, 20); ctx.quadraticCurveTo(-16, -36, 0, -64); ctx.closePath(); ctx.fill();
    var sg = ctx.createLinearGradient(-14, 0, 14, 0); sg.addColorStop(0, 'rgba(255,255,255,.0)'); sg.addColorStop(1, 'rgba(20,30,70,.30)'); ctx.fillStyle = sg; ctx.fill();
    ctx.fillStyle = '#D9482B'; ctx.fillRect(-14, 10, 28, 7);
    ctx.fillStyle = '#2C86D8'; ctx.beginPath(); ctx.arc(0, -16, 7.5, 0, PI2); ctx.fill(); ctx.strokeStyle = '#B9C2D3'; ctx.lineWidth = 2.6; ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.beginPath(); ctx.arc(-2.4, -18.4, 2.2, 0, PI2); ctx.fill();
    ctx.restore();
  }
  function regua(ctx, w, h, p) {
    var x = 16, y0 = h * 0.9, y1 = h * 0.12, i, yy;
    ctx.strokeStyle = 'rgba(255,255,255,.38)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x, y0); ctx.lineTo(x, y1); ctx.stroke();
    for (i = 0; i < 5; i++) {
      yy = y0 + (y1 - y0) * i / 4; var passou = i <= p + 0.02;
      ctx.fillStyle = passou ? '#FFD878' : 'rgba(255,255,255,.55)'; ctx.beginPath(); ctx.arc(x, yy, passou ? 4.5 : 3.5, 0, PI2); ctx.fill();
      OVM.pilula(ctx, NOMES_REGUA[i], x + 12, yy, { px: 10.5, ancora: 'esq', alpha: passou ? 1 : 0.7, pad: 7 });
    }
    var my = y0 + (y1 - y0) * p / 4;
    OVM.brilho(ctx, x, my, 20, 'rgba(255,214,120,A)', 0.9); ctx.fillStyle = '#FFE9A8'; ctx.beginPath(); ctx.arc(x, my, 5.5, 0, PI2); ctx.fill();
  }

  function altitudeTexto(p) {
    var i = Math.min(3, Math.floor(p)), f = p - i;
    if (p < 0.02) return 'No chão';
    if (f < 0.02 && p - i < 0.02) return V[i].rotulo;
    if (f > 0.98) return V[i + 1].rotulo;
    var a = Math.exp(OVM.lerp(Math.log(ALTS[i]), Math.log(ALTS[i + 1]), f));
    return 'Altura: ' + F.distKm(a);
  }

  var ultimoTexto = '';
  function quadro(dt, t) {
    var w = T.w, h = T.h, ctx = T.ctx, u = Math.min(w, h), X = Math.max(w, h);
    if (OVM.reduz) pos = alvo; else { var d = alvo - pos; pos = Math.abs(d) < 0.004 ? alvo : OVM.seguir(pos, alvo, 1.55, dt); }
    var mov = Math.abs(alvo - pos), chama = OVM.clamp(mov * 2.5, 0, 1);
    var i = Math.min(3, Math.floor(pos)), f = pos - i; if (pos >= 4) { i = 3; f = 1; }
    var e = OVM.suave(f), a = K[i], b = K[i + 1];
    OVM.fundoCanvas(T);
    var g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, cor(a.c0, b.c0, e)); g.addColorStop(1, cor(a.c1, b.c1, e)); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    var sa = OVM.lerp(a.st, b.st, e);
    if (sa > 0.01) OVM.pintarEstrelas(ctx, w, h, est, t, { alpha: sa });
    var ta = a.terra(w, h, X), tb = b.terra(w, h, X), tc = [OVM.lerp(ta[0], tb[0], e), OVM.lerp(ta[1], tb[1], e), OVM.lerp(ta[2], tb[2], e)];
    if (i === 0) { /* a Terra "aparece" subindo; no chão só há o horizonte */ }
    terraD(ctx, tc, OVM.lerp(0.0, 1, OVM.clamp(pos * 3, 0, 1)), w, h);
    esferaSp(ctx, luaSp, w * 0.83, h * 0.27, 0.075 * X * 1.0, OVM.lerp(a.lua, b.lua, e));
    esferaSp(ctx, marteSp, w * 0.74, h * 0.5, 0.2 * X, OVM.lerp(a.marte, b.marte, e));
    var ia = OVM.lerp(a.iss, b.iss, e);
    issD(ctx, w * (0.76 + Math.sin(t * 0.25) * 0.02), h * 0.38, u / 330 * 1.1, ia, t);
    var sl = OVM.lerp(a.solo, b.solo, e);
    if (sl > 0.005) chao(ctx, w, h, pos * h * 1.05, u, t);
    // linha de Kármán na parada 1
    var ka = Math.max(0, 1 - Math.abs(pos - 1) * 2.2);
    if (ka > 0.02) { ctx.save(); ctx.globalAlpha = ka * 0.8; ctx.strokeStyle = 'rgba(255,230,160,.8)'; ctx.setLineDash([6, 7]); ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(0, h * 0.7); ctx.lineTo(w, h * 0.7); ctx.stroke(); ctx.setLineDash([]); OVM.pilula(ctx, 'linha de Kármán: onde o espaço começa', w - 12, h * 0.7 - 14, { px: 11, ancora: 'dir', alpha: 1 }); ctx.restore(); }
    // trajetória pontilhada até a Lua / Marte
    if (pos > 2.4) { ctx.save(); ctx.globalAlpha = OVM.clamp((pos - 2.4) / 0.6, 0, 1) * 0.5; ctx.strokeStyle = '#fff'; ctx.setLineDash([3, 8]); ctx.lineWidth = 1.5; ctx.beginPath(); var t0 = pos < 3.5 ? tc : [w * 0.17, h * 0.78]; ctx.moveTo(w * 0.17 + 24, h * 0.76); ctx.quadraticCurveTo(w * 0.5, h * 0.2, pos < 3.5 ? w * 0.8 : w * 0.7, pos < 3.5 ? h * 0.3 : h * 0.5); ctx.stroke(); ctx.restore(); }
    // fumaça do escapamento
    if (!OVM.reduz) {
      var fxp = OVM.lerp(a.f[0], b.f[0], e), fyp = OVM.lerp(a.f[1], b.f[1], e), fsp = OVM.lerp(a.f[2], b.f[2], e), frot = OVM.lerp(a.f[3], b.f[3], e);
      var sc = u / 330 * fsp, bx = fxp * w - Math.sin(frot) * 56 * sc, by = fyp * h + Math.cos(frot) * 56 * sc;
      if (chama > 0.1) { acum += dt; while (acum > 0.035) { acum -= 0.035; fumaca.push({ x: bx + (rnd() - 0.5) * 10 * sc, y: by + 10 * sc, vx: (rnd() - 0.5) * 30 + Math.sin(frot) * -30, vy: 50 + rnd() * 70, r: (5 + rnd() * 6) * sc, a: 0 }); } }
      for (var k = fumaca.length - 1; k >= 0; k--) { var s = fumaca[k]; s.a += dt * 1.3; s.x += s.vx * dt; s.y += s.vy * dt; s.r += dt * 16 * sc; if (s.a >= 1) fumaca.splice(k, 1); }
      for (k = 0; k < fumaca.length; k++) { s = fumaca[k]; OVM.brilho(ctx, s.x, s.y, s.r * 1.8, 'rgba(235,238,245,A)', Math.pow(1 - s.a, 1.5) * (sl > 0.3 ? 0.55 : 0.32)); }
      foguete(ctx, fxp * w, fyp * h + (chama < 0.05 ? Math.sin(t * 1.6) * 2 : 0), sc, chama, frot, t);
    } else {
      foguete(ctx, OVM.lerp(a.f[0], b.f[0], e) * w, OVM.lerp(a.f[1], b.f[1], e) * h, u / 330 * OVM.lerp(a.f[2], b.f[2], e), 0, OVM.lerp(a.f[3], b.f[3], e), t);
    }
    regua(ctx, w, h, pos);
    var txt = altitudeTexto(pos);
    if (txt !== ultimoTexto) { altEl.textContent = txt; ultimoTexto = txt; }
  }
  OVM.anima(quadro, canvas);
  quadro(0.016, 0.5);

  // ---- textos e controles
  function casas(reais) { var c = reais / CASA; return '≈ ' + F.n(c, c < 10 ? 1 : 0) + (Math.round(c * 10) / 10 === 1 ? ' casa' : ' casas') + ' de R$ 542 mil'; }
  function reaisTexto(v) { return F.grande(v.reais); }
  function etiqueta(i) {
    var v = V[i];
    if (i === 0) { etq.style.opacity = 0; ultimoNum = 0; return; }
    etq.style.opacity = 1;
    if (v.usd) {
      var aprox = (i === 2 || i === 4) ? '<span class="aprox">≈</span>' : '';
      etq.innerHTML = '<span class="furo"></span>' + aprox + '<span class="rs">R$</span><b></b>';
      OVM.contar(etq.querySelector('b'), ultimoNum, v.reais, reaisTexto(v), 1100, function (x) { return F.grande(x); });
      ultimoNum = v.reais;
    } else { etq.innerHTML = '<span class="furo"></span><b class="sem">sem bilhete à venda</b>'; }
    etq.classList.remove('balanca'); void etq.offsetWidth; etq.classList.add('balanca');
  }
  function htmlParada(v, i) {
    var preco = v.usd ? '<span class="p1-preco"><small>' + (i === 2 || i === 4 ? '≈ ' : '') + 'R$ </small>' + reaisTexto(v) + '</span>' : '<span class="p1-preco" style="font-size:22px">sem passagem</span>';
    return '<b class="grande">' + v.nome + '</b>' +
      '<p class="p1-linha">' + preco + (v.usd ? '<span class="p1-cafes">' + casas(v.reais) + '</span>' : '') + '</p>' +
      (i === 4 ? '<p><span class="marca">meta declarada, não é preço</span></p>' : '') +
      '<p class="p1-imagine">' + v.imagine + '</p>' +
      '<p class="p1-qual"><b>Para chegar:</b> ' + v.tempo + '</p>' +
      '<details class="conta"><summary>Conta e fonte</summary><p><b>' + v.preco + '</b></p><p>' + v.nota + '</p></details>';
  }
  function ir(i) {
    alvo = i; saida.textContent = V[i].nome; slider.value = i; OVM.preencher(slider);
    chips.forEach(function (c, k) { c.classList.toggle('ativo', k === i); c.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
    etiqueta(i);
  }
  var passos = V.map(function (v, i) {
    return {
      rotulo: i === 0 ? 'A viagem mais cara' : 'Parada ' + i + ' de 4',
      html: i === 0 ? function () {
        return '<b class="grande">Na plataforma</b><p>Do chocolate quente à casa, o preço foi subindo com o que se recebe. Agora, a viagem que nenhum supermercado vende: <b>sair do planeta</b>.</p>' +
          '<p class="pequeno">Toque em <b>Próximo</b> e o foguete sobe até a parada seguinte. O preço sobe com ele.</p>';
      } : function () { return htmlParada(v, i); },
      ir: function () { ir(i); }
    };
  });
  passos.push({
    rotulo: 'O que a viagem ensina',
    html: '<p>Cada parada é <b>muito mais longe</b> e <b>muito mais cara</b> que a anterior: de milhares de reais a centenas de milhões, até chegar numa viagem que nem tem passagem à venda.</p>' +
      '<p>Fica uma pergunta: <b>quanto é "longe"?</b> Para saber, precisamos de uma régua.</p>',
    ir: function () { ir(4); }
  });
  var g = OVM.guia({ passos: passos });
  slider.addEventListener('input', function () { OVM.preencher(slider); g.ir(+slider.value); });
  chips.forEach(function (c) { c.addEventListener('click', function () { g.ir(+c.getAttribute('data-i')); }); });
});

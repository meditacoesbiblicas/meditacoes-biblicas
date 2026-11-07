/* Motor de escala ("potências de dez"): uma câmera que se afasta (ou se aproxima) por camadas de tamanhos muito diferentes.
   Cada nível é um desenho pré-renderizado ("folha") com um diâmetro físico `d`. Na tela, a folha tem d / campo × L pixels
   (campo = largura visível, L = lado útil da tela). Cada folha aparece quando fica pequena o bastante para caber e some quando
   fica grande demais. A câmera fica sempre centrada em "nós" (a Terra, ou o ponto onde estamos entrando). Sem dependências. */
(function () {
  'use strict';
  var OVM = window.OVM, PI2 = 6.2832;
  var TAM = 1024, C = TAM / 2, RAIO = TAM * 0.45; // o objeto ocupa 90% da folha

  // ---------------------------------------------------------------- ferramentas de desenho
  function gauss(rnd) { return (rnd() + rnd() + rnd() + rnd() - 2) * 1.2; }
  function nova() { var c = document.createElement('canvas'); c.width = c.height = TAM; return c; }
  // mancha de contorno suave (continentes, nuvens…)
  function mancha(ctx, cx, cy, r, rnd, sx, sy, rot) {
    var n = 11, p = [], k, a, rr, q;
    for (k = 0; k < n; k++) { a = k / n * PI2; rr = r * (0.62 + rnd() * 0.72); p.push([Math.cos(a) * rr * (sx || 1), Math.sin(a) * rr * (sy || 1)]); }
    ctx.save(); ctx.translate(cx, cy); if (rot) ctx.rotate(rot);
    ctx.beginPath(); ctx.moveTo((p[n - 1][0] + p[0][0]) / 2, (p[n - 1][1] + p[0][1]) / 2);
    for (k = 0; k < n; k++) { q = p[(k + 1) % n]; ctx.quadraticCurveTo(p[k][0], p[k][1], (p[k][0] + q[0]) / 2, (p[k][1] + q[1]) / 2); }
    ctx.closePath(); ctx.fill(); ctx.restore();
  }
  function esfera(ctx, cx, cy, R, c0, c1, c2) {
    var g = ctx.createRadialGradient(cx - R * 0.38, cy - R * 0.42, R * 0.05, cx, cy, R * 1.05);
    g.addColorStop(0, c0); g.addColorStop(0.55, c1); g.addColorStop(1, c2);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, PI2); ctx.fill();
  }
  function sombra(ctx, cx, cy, R, forca) {
    var g = ctx.createRadialGradient(cx - R * 0.5, cy - R * 0.55, R * 0.25, cx, cy, R * 1.12);
    g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(0.6, 'rgba(0,4,16,' + (0.15 * forca) + ')'); g.addColorStop(1, 'rgba(0,4,16,' + (0.8 * forca) + ')');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, PI2); ctx.fill();
  }

  // ---------------------------------------------------------------- as folhas do cosmos
  function pTerra(ctx, rnd) {
    var R = RAIO * 0.93, i, a, d;
    OVM.brilho(ctx, C, C, R * 1.2, 'rgba(110,175,255,A)', 0.5);
    esfera(ctx, C, C, R, '#7CCBFF', '#2C86D8', '#0B3470');
    ctx.save(); ctx.beginPath(); ctx.arc(C, C, R, 0, PI2); ctx.clip();
    ctx.fillStyle = '#3F9150';
    mancha(ctx, C - R * 0.46, C - R * 0.26, R * 0.26, rnd, 1, 1.25, -0.2); mancha(ctx, C - R * 0.3, C + R * 0.36, R * 0.2, rnd, 0.65, 1.55, 0.35); mancha(ctx, C + R * 0.42, C - R * 0.4, R * 0.28, rnd, 1.35, 0.85);
    ctx.fillStyle = '#C9AD6A'; mancha(ctx, C + R * 0.22, C + R * 0.12, R * 0.27, rnd, 0.85, 1.3, 0.15); mancha(ctx, C + R * 0.64, C + R * 0.02, R * 0.1, rnd, 1, 1);
    ctx.fillStyle = '#3F9150'; mancha(ctx, C + R * 0.2, C + R * 0.34, R * 0.12, rnd, 1, 1.1);
    ctx.fillStyle = '#F4F8FF'; mancha(ctx, C - R * 0.1, C - R * 0.93, R * 0.2, rnd, 2, 0.5); mancha(ctx, C, C + R * 0.99, R * 0.36, rnd, 2, 0.5);
    for (i = 0; i < 28; i++) { a = rnd() * PI2; d = Math.sqrt(rnd()) * R * 0.95; OVM.brilho(ctx, C + Math.cos(a) * d, C + Math.sin(a) * d * 0.92, R * (0.05 + rnd() * 0.12), 'rgba(255,255,255,A)', 0.45 + rnd() * 0.3); }
    ctx.restore();
    sombra(ctx, C, C, R, 1);
    ctx.strokeStyle = 'rgba(150,200,255,.5)'; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(C, C, R - 2, 0, PI2); ctx.stroke();
  }
  function luaDesenho(ctx, cx, cy, R, rnd) {
    esfera(ctx, cx, cy, R, '#F0EFEA', '#B9B7B0', '#55544F');
    ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, R, 0, PI2); ctx.clip();
    ctx.fillStyle = 'rgba(80,80,80,.30)';
    for (var i = 0; i < 16; i++) { var a = rnd() * PI2, d = Math.sqrt(rnd()) * R * 0.85; ctx.beginPath(); ctx.arc(cx + Math.cos(a) * d, cy + Math.sin(a) * d, R * (0.05 + rnd() * 0.16), 0, PI2); ctx.fill(); }
    ctx.restore(); sombra(ctx, cx, cy, R, 0.9);
  }
  function pTerraLua(ctx, rnd) {
    // a Terra e a Lua estão desenhadas MAIORES que o real (na escala certa seriam pontinhos)
    ctx.strokeStyle = 'rgba(200,215,255,.45)'; ctx.lineWidth = 2; ctx.setLineDash([6, 8]); ctx.beginPath(); ctx.arc(C, C, RAIO, 0, PI2); ctx.stroke(); ctx.setLineDash([]);
    OVM.brilho(ctx, C, C, 60, 'rgba(110,175,255,A)', 0.5);
    esfera(ctx, C, C, 30, '#7CCBFF', '#2C86D8', '#0B3470');
    ctx.fillStyle = '#3F9150'; mancha(ctx, C - 8, C - 5, 10, rnd, 1, 1); mancha(ctx, C + 10, C + 8, 9, rnd, 1, 1);
    sombra(ctx, C, C, 30, 1);
    var ang = -0.62; luaDesenho(ctx, C + Math.cos(ang) * RAIO, C + Math.sin(ang) * RAIO, 13, rnd);
  }
  var UA_P = [0.387, 0.723, 1, 1.524, 5.203, 9.537, 19.19, 30.07], ANG_P = [0.5, 2.2, 0, 4.1, 5.0, 2.7, 1.1, 3.9];
  function pSistema(ctx, rnd) {
    var UA = UA_P, cor = ['#B7B1A6', '#EBD39F', '#4FA3E8', '#D1603D', '#DDB78F', '#E8D6A5', '#9BDCE8', '#5B82E6'], r = [2.6, 3.6, 4.2, 3.4, 9, 8, 5.6, 5.6], i, a;
    OVM.brilho(ctx, C, C, 70, 'rgba(255,205,90,A)', 0.95);
    for (i = 0; i < 8; i++) { ctx.strokeStyle = 'rgba(255,255,255,.22)'; ctx.lineWidth = 1.3; ctx.beginPath(); ctx.arc(C, C, RAIO * UA[i] / 30.07, 0, PI2); ctx.stroke(); }
    ctx.fillStyle = '#FFE9A8'; ctx.beginPath(); ctx.arc(C, C, 11, 0, PI2); ctx.fill();
    for (i = 0; i < 8; i++) {
      a = ANG_P[i];                                          // a Terra fica à direita do Sol, no centro da câmera
      var x = C + Math.cos(a) * RAIO * UA[i] / 30.07, y = C + Math.sin(a) * RAIO * UA[i] / 30.07;
      if (i === 5) { ctx.strokeStyle = 'rgba(230,214,165,.8)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x, y, r[i] * 2.1, r[i] * 0.7, -0.4, 0, PI2); ctx.stroke(); }
      OVM.brilho(ctx, x, y, r[i] * 2.6, 'rgba(255,255,255,A)', 0.18);
      ctx.fillStyle = cor[i]; ctx.beginPath(); ctx.arc(x, y, r[i], 0, PI2); ctx.fill();
    }
    return { terra: [C + RAIO / 30.07, C] };
  }
  // vizinhança do Sol: estrelas num raio de 10 anos-luz (as distâncias dos nomes são as reais)
  var VIZ = [
    { n: 'Próxima do Centauro', al: 4.25, ang: 3.5, cor: '#FFB08A', r: 4 }, { n: 'Alfa do Centauro A e B', al: 4.37, ang: 3.62, cor: '#FFE7A6', r: 7 },
    { n: 'Estrela de Barnard', al: 5.96, ang: 1.0, cor: '#FF9E7A', r: 4 }, { n: 'Wolf 359', al: 7.86, ang: 2.5, cor: '#FF8F70', r: 3.5 },
    { n: 'Lalande 21185', al: 8.31, ang: 1.75, cor: '#FFA37F', r: 4 }, { n: 'Sírio', al: 8.6, ang: 5.2, cor: '#DCEBFF', r: 9 }, { n: 'Ross 154', al: 9.69, ang: 0.3, cor: '#FF9A78', r: 3.5 }
  ];
  function pVizinhanca(ctx, rnd) {
    var pxAl = (TAM * 0.9) / 20, i, a, d;
    [5, 10].forEach(function (al) { ctx.strokeStyle = 'rgba(200,215,255,.30)'; ctx.lineWidth = 1.4; ctx.setLineDash([5, 7]); ctx.beginPath(); ctx.arc(C, C, al * pxAl, 0, PI2); ctx.stroke(); });
    ctx.setLineDash([]);
    for (i = 0; i < 12; i++) { a = rnd() * PI2; d = (2 + rnd() * 7.6) * pxAl; OVM.brilho(ctx, C + Math.cos(a) * d, C + Math.sin(a) * d, 9, 'rgba(255,150,110,A)', 0.55); ctx.fillStyle = '#FF9A78'; ctx.beginPath(); ctx.arc(C + Math.cos(a) * d, C + Math.sin(a) * d, 2.4, 0, PI2); ctx.fill(); }
    VIZ.forEach(function (e) { var x = C + Math.cos(e.ang) * e.al * pxAl, y = C + Math.sin(e.ang) * e.al * pxAl; OVM.brilho(ctx, x, y, e.r * 4, 'rgba(255,255,255,A)', 0.4); ctx.fillStyle = e.cor; ctx.beginPath(); ctx.arc(x, y, e.r, 0, PI2); ctx.fill(); });
    OVM.brilho(ctx, C, C, 30, 'rgba(255,214,120,A)', 0.9); ctx.fillStyle = '#FFE08A'; ctx.beginPath(); ctx.arc(C, C, 6, 0, PI2); ctx.fill();
  }
  function marcasViz() {
    var pxAl = 0.9 / 20;
    return VIZ.filter(function (e) { return e.n !== 'Alfa do Centauro A e B' && e.n !== 'Wolf 359' && e.n !== 'Ross 154' && e.n !== 'Lalande 21185'; }).map(function (e) {
      return { t: e.n + ' · ' + String(e.al).replace('.', ',') + ' anos-luz', x: Math.cos(e.ang) * e.al * pxAl, y: Math.sin(e.ang) * e.al * pxAl + 0.03 };
    });
  }
  // galáxia espiral (braços logarítmicos); rot e inclinação opcionais
  function galaxia(ctx, rnd, cx, cy, R, o) {
    o = o || {};
    var tilt = o.tilt == null ? 1 : o.tilt, n = o.n || 8000, bracos = o.bracos || 4, b = 0.22, r0 = R * 0.1, tmax = Math.log(R / r0) / b, k, i, th, r, ang, s, x, y, q, z;
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(o.rot || 0); ctx.scale(1, tilt);
    OVM.brilho(ctx, 0, 0, R * 1.08, 'rgba(100,120,215,A)', 0.2);
    if (o.poeira !== false) {
      ctx.strokeStyle = 'rgba(35,18,12,.42)'; ctx.lineWidth = R * 0.035;
      for (k = 0; k < bracos; k++) { ctx.beginPath(); for (th = 0.4; th < tmax; th += 0.15) { r = r0 * Math.exp(b * th); ang = th + k * PI2 / bracos + 0.2; ctx[th === 0.4 ? 'moveTo' : 'lineTo'](Math.cos(ang) * r, Math.sin(ang) * r); } ctx.stroke(); }
    }
    ctx.globalCompositeOperation = 'lighter';
    OVM.brilho(ctx, 0, 0, R * 0.3, 'rgba(255,212,145,A)', 0.8);
    for (k = 0; k < bracos; k++) {
      for (i = 0; i < n; i++) {
        th = Math.pow(rnd(), 0.8) * tmax; r = r0 * Math.exp(b * th); ang = th + k * PI2 / bracos; s = R * 0.012 + r * 0.075;
        x = Math.cos(ang) * r + gauss(rnd) * s; y = Math.sin(ang) * r + gauss(rnd) * s; q = r / R;
        ctx.fillStyle = q < 0.3 ? 'rgba(255,228,180,.55)' : q < 0.65 ? 'rgba(225,230,255,.5)' : (rnd() < 0.06 ? 'rgba(255,130,180,.8)' : 'rgba(150,195,255,.5)');
        z = (o.ponto || 1.5) * (0.5 + rnd()); ctx.fillRect(x - z / 2, y - z / 2, z, z);
      }
    }
    for (i = 0; i < n * 0.55; i++) { x = gauss(rnd) * R * 0.13; y = gauss(rnd) * R * 0.07; ctx.fillStyle = 'rgba(255,224,170,.55)'; z = (o.ponto || 1.5) * (0.5 + rnd()); ctx.fillRect(x - z / 2, y - z / 2, z, z); }
    ctx.restore();
  }
  var ANG_SOL = 0.96, FRAC_SOL = 0.26; // o Sol está a ~26 mil anos-luz do centro da Via Láctea (26% do diâmetro)
  function pGalaxia(ctx, rnd) {
    var R = RAIO;
    galaxia(ctx, rnd, C, C, R, { n: 9000, ponto: 1.6, rot: -0.3 });
    // o Sol e o braço local
    var x = C + Math.cos(ANG_SOL) * FRAC_SOL * TAM * 0.9, y = C + Math.sin(ANG_SOL) * FRAC_SOL * TAM * 0.9;
    ctx.globalCompositeOperation = 'source-over';
    OVM.brilho(ctx, x, y, 20, 'rgba(255,214,120,A)', 0.8); ctx.fillStyle = '#FFE08A'; ctx.beginPath(); ctx.arc(x, y, 3.2, 0, PI2); ctx.fill();
  }
  // teia cósmica: nós ligados por filamentos de pontos
  function teia(ctx, rnd, R, nNos, o) {
    o = o || {};
    var nos = [], tent = 0, seen = {}, a, d, x, y, ok, j, dx, dy;
    while (nos.length < nNos && tent++ < nNos * 60) {
      a = rnd() * PI2; d = Math.sqrt(rnd()) * R; x = C + Math.cos(a) * d; y = C + Math.sin(a) * d; ok = true;
      for (j = 0; j < nos.length; j++) { dx = nos[j][0] - x; dy = nos[j][1] - y; if (dx * dx + dy * dy < o.min * o.min) { ok = false; break; } }
      if (ok) nos.push([x, y, rnd()]);
    }
    ctx.globalCompositeOperation = 'lighter';
    nos.forEach(function (p, ia) {
      var viz = nos.map(function (q, ib) { return [ib, (q[0] - p[0]) * (q[0] - p[0]) + (q[1] - p[1]) * (q[1] - p[1])]; }).sort(function (u, v) { return u[1] - v[1]; }).slice(1, 3 + (rnd() < 0.4 ? 1 : 0));
      viz.forEach(function (v) {
        var ib = v[0], key = ia < ib ? ia + '-' + ib : ib + '-' + ia, q = nos[ib];
        if (seen[key]) return; seen[key] = 1;
        var mx = (p[0] + q[0]) / 2 + gauss(rnd) * 16, my = (p[1] + q[1]) / 2 + gauss(rnd) * 16;
        ctx.strokeStyle = o.fio || 'rgba(120,140,255,.10)'; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.quadraticCurveTo(mx, my, q[0], q[1]); ctx.stroke();
        var np = Math.floor(Math.sqrt(v[1]) / (o.passo || 4)), m, t, ux, uy;
        ctx.fillStyle = o.ponto || 'rgba(190,205,255,.55)';
        for (m = 0; m < np; m++) { t = rnd(); ux = (1 - t) * (1 - t) * p[0] + 2 * (1 - t) * t * mx + t * t * q[0]; uy = (1 - t) * (1 - t) * p[1] + 2 * (1 - t) * t * my + t * t * q[1]; ctx.fillRect(ux + gauss(rnd) * 3, uy + gauss(rnd) * 3, 1.5, 1.5); }
      });
    });
    nos.forEach(function (p) { OVM.brilho(ctx, p[0], p[1], 7 + p[2] * 15, o.no || 'rgba(255,225,170,A)', 0.3 + p[2] * 0.5); });
    ctx.globalCompositeOperation = 'source-over';
    return nos;
  }
  var GA = { x: 0.0, y: 0.0 };                 // o Grande Atrator, perto do centro de Laniakea
  var POS_LANI = [0.30, 0.29];                 // nós, a ~42% do diâmetro do centro
  function pLaniakea(ctx, rnd) {
    teia(ctx, rnd, RAIO * 0.98, 90, { min: 52, fio: 'rgba(130,150,255,.12)', no: 'rgba(255,214,150,A)' });
    ctx.globalCompositeOperation = 'lighter';
    for (var i = 0; i < 46; i++) {   // correntes de galáxias rumo ao centro
      var a = rnd() * PI2, r1 = RAIO * (0.7 + rnd() * 0.28), x1 = C + Math.cos(a) * r1, y1 = C + Math.sin(a) * r1, g = ctx.createLinearGradient(x1, y1, C, C);
      g.addColorStop(0, 'rgba(160,190,255,0)'); g.addColorStop(0.55, 'rgba(160,190,255,.22)'); g.addColorStop(1, 'rgba(255,225,170,.06)');
      ctx.strokeStyle = g; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.quadraticCurveTo(C + Math.cos(a + 0.6) * r1 * 0.5, C + Math.sin(a + 0.6) * r1 * 0.5, C, C); ctx.stroke();
    }
    OVM.brilho(ctx, C, C, 90, 'rgba(255,210,150,A)', 0.55);
    var nx = C + POS_LANI[0] * TAM * 0.9, ny = C + POS_LANI[1] * TAM * 0.9;
    ctx.globalCompositeOperation = 'source-over';
    OVM.brilho(ctx, nx, ny, 16, 'rgba(255,214,120,A)', 0.95); ctx.fillStyle = '#FFE08A'; ctx.beginPath(); ctx.arc(nx, ny, 3, 0, PI2); ctx.fill();
  }
  var LG = { mw: [-0.12, 0.05], m31: [0.13, -0.07], m33: [0.18, -0.17] };
  function pGrupo(ctx, rnd) {
    var s = TAM * 0.9, i, a, d;
    OVM.brilho(ctx, C, C, RAIO, 'rgba(110,130,230,A)', 0.14);
    for (i = 0; i < 34; i++) { a = rnd() * PI2; d = Math.sqrt(rnd()) * 0.42 * s; var x = C + Math.cos(a) * d, y = C + Math.sin(a) * d; OVM.brilho(ctx, x, y, 5 + rnd() * 5, 'rgba(210,220,255,A)', 0.5); }
    galaxia(ctx, rnd, C + LG.mw[0] * s, C + LG.mw[1] * s, 30, { n: 900, ponto: 1.3, rot: -0.3, poeira: false });
    galaxia(ctx, rnd, C + LG.m31[0] * s, C + LG.m31[1] * s, 44, { n: 1300, ponto: 1.3, rot: 0.9, tilt: 0.38, poeira: false });
    galaxia(ctx, rnd, C + LG.m33[0] * s, C + LG.m33[1] * s, 20, { n: 500, ponto: 1.2, rot: 0.2, tilt: 0.8, poeira: false });
  }
  function pUniverso(ctx, rnd) {
    var g = ctx.createRadialGradient(C, C, 0, C, C, RAIO);
    g.addColorStop(0, '#0C1236'); g.addColorStop(0.8, '#070B24'); g.addColorStop(1, '#0B1030');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(C, C, RAIO, 0, PI2); ctx.fill();
    ctx.save(); ctx.beginPath(); ctx.arc(C, C, RAIO, 0, PI2); ctx.clip();
    teia(ctx, rnd, RAIO * 1.02, 300, { min: 30, passo: 3.2, fio: 'rgba(120,140,255,.10)', no: 'rgba(255,225,175,A)' });
    ctx.restore();
    var e = ctx.createRadialGradient(C, C, RAIO * 0.86, C, C, RAIO * 1.04);
    e.addColorStop(0, 'rgba(120,150,255,0)'); e.addColorStop(0.7, 'rgba(120,150,255,.22)'); e.addColorStop(1, 'rgba(180,200,255,.0)');
    ctx.fillStyle = e; ctx.beginPath(); ctx.arc(C, C, RAIO * 1.04, 0, PI2); ctx.fill();
    ctx.strokeStyle = 'rgba(170,195,255,.55)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(C, C, RAIO, 0, PI2); ctx.stroke();
  }

  var COSMOS = {
    terra: { pintar: pTerra, off: [0, 0] },
    lua: { pintar: pTerraLua, off: [0, 0], marcas: [{ t: 'Terra', x: 0, y: 0.05 }, { t: 'Lua · 384.400 km', x: 0.4, y: -0.31 }], nota: 'Terra e Lua desenhadas maiores que o real, para dar para ver.' },
    sistema: { pintar: pSistema, off: [-1 / 60.14, 0], marcas: [{ t: 'Sol', x: 0, y: 0.045 }, { t: 'Júpiter', x: Math.cos(ANG_P[4]) * 5.203 / 60.14, y: Math.sin(ANG_P[4]) * 5.203 / 60.14 - 0.035 }, { t: 'Netuno', x: Math.cos(ANG_P[7]) * 30.07 / 60.14, y: Math.sin(ANG_P[7]) * 30.07 / 60.14 - 0.035 }, { t: 'Terra', x: 1 / 60.14, y: 0.045 }], nota: 'As órbitas estão na escala certa; os planetas foram desenhados maiores que o real.' },
    vizinhanca: { pintar: pVizinhanca, off: [0, 0], marcas: marcasViz() },
    galaxia: { pintar: pGalaxia, off: [-FRAC_SOL * Math.cos(ANG_SOL), -FRAC_SOL * Math.sin(ANG_SOL)], marcas: [{ t: 'Centro da galáxia', x: 0, y: 0.14 }, { t: 'Nós (Sol)', x: FRAC_SOL * Math.cos(ANG_SOL), y: FRAC_SOL * Math.sin(ANG_SOL) + 0.045 }], nota: 'Desenho artístico: nós vivemos dentro da galáxia e nunca a vimos de fora.' },
    grupo: { pintar: pGrupo, off: [-LG.mw[0], -LG.mw[1]], marcas: [{ t: 'Via Láctea', x: LG.mw[0], y: LG.mw[1] - 0.06 }, { t: 'Andrômeda', x: LG.m31[0], y: LG.m31[1] - 0.07 }, { t: 'Triângulo', x: LG.m33[0], y: LG.m33[1] - 0.045 }], nota: 'As galáxias estão desenhadas maiores que o real.' },
    super: { pintar: pLaniakea, off: [-POS_LANI[0], -POS_LANI[1]], marcas: [{ t: 'Grande Atrator', x: 0, y: 0.06 }, { t: 'Nós (Grupo Local)', x: POS_LANI[0], y: POS_LANI[1] + 0.05 }], nota: 'Desenho artístico dos filamentos de galáxias.' },
    universo: { pintar: pUniverso, off: [0, 0], marcas: [{ t: 'Nós, no centro do que dá para ver', x: 0, y: -0.07 }], nota: 'Cada ponto de luz é um conjunto de galáxias. Desenho artístico.' }
  };

  // ---------------------------------------------------------------- o motor
  // cfg: { canvas, niveis:[{id, nome, d, off, pintar(ctx, rnd), marcas:[{t,x,y}]}], folga, inicio, aqui:'Você está aqui', fundo(ctx,w,h,s,t), barra(len)->texto, aoQuadro(E), semente }
  OVM.Escala = function (cfg) {
    var T = OVM.tela(cfg.canvas), N = cfg.niveis, folga = cfg.folga || 1.3, E = { T: T, niveis: N, s: 0, alvo: cfg.inicio || 0, movendo: false };
    var logs = N.map(function (n) { return Math.log10(n.d); }), mov = null, vel = 0, ordem = N.map(function (n, i) { return i; }).sort(function (a, b) { return N[b].d - N[a].d; });
    var estrelas = OVM.estrelas(cfg.semente || 31, 150), menor = ordem[ordem.length - 1];
    function sDe(i) { return logs[i] + Math.log10(folga); }
    E.sDe = sDe;
    E.s = sDe(cfg.inicio || 0);
    E.ir = function (i, dur, fim) {
      i = OVM.clamp(i, 0, N.length - 1); E.alvo = i;
      var s1 = sDe(i), d = Math.abs(s1 - E.s);
      if (OVM.reduz || d < 0.001) { E.s = s1; mov = null; E.movendo = false; if (fim) fim(); return; }
      mov = { s0: E.s, s1: s1, t0: OVM.t, dur: dur || OVM.clamp(0.8 + d * 0.5, 1.1, 4.4), fim: fim }; E.movendo = true;
    };
    E.irS = function (s1, dur, fim) {   // vai para um campo qualquer (em log10)
      var d = Math.abs(s1 - E.s);
      if (OVM.reduz || d < 0.001) { E.s = s1; mov = null; E.movendo = false; if (fim) fim(); return; }
      mov = { s0: E.s, s1: s1, t0: OVM.t, dur: dur || OVM.clamp(0.8 + d * 0.5, 1.1, 4.4), fim: fim }; E.movendo = true;
    };
    E.definir = function (s) { mov = null; E.movendo = false; E.s = s; };
    E.perto = function () { var m = 0, b = 1e9; for (var i = 0; i < N.length; i++) { var d = Math.abs(E.s - sDe(i)); if (d < b) { b = d; m = i; } } return m; };
    E.campo = function () { return Math.pow(10, E.s); };       // largura visível, na unidade de `d`
    E.px = function (i) { return N[i].d / E.campo() * Math.min(T.w, T.h) * 0.94; };

    function janela(px, L) {
      var ent = OVM.suave((px - 5) / 26), sai = 1 - OVM.suave((px - 1.5 * L) / (1.5 * L));
      return ent * sai;
    }
    var ph = 0, fase = 0;
    function quadro(dt, t) {
      var w = T.w, h = T.h, ctx = T.ctx, sAnt = E.s, i, k;
      if (mov) {
        var p = (OVM.t - mov.t0) / mov.dur;
        if (p >= 1) { E.s = mov.s1; var f = mov.fim; mov = null; E.movendo = false; if (f) f(); } else E.s = OVM.lerp(mov.s0, mov.s1, OVM.suave(p));
      }
      vel = dt > 0 ? OVM.seguir(vel, (E.s - sAnt) / dt, 8, dt) : vel;
      OVM.fundoCanvas(T);
      if (cfg.fundo) cfg.fundo(ctx, w, h, E.s, t);
      else { var g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#04071A'); g.addColorStop(1, '#0A1128'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); }
      var L = Math.min(w, h) * 0.94, FOV = Math.pow(10, E.s), cx0 = w / 2, cy0 = h / 2;
      // estrelas de fundo; com a câmera em movimento viram riscos que correm para o centro (afastando) ou para fora (aproximando)
      var ve = OVM.clamp(Math.abs(vel) / 1.4, 0, 1), R0 = Math.sqrt(w * w + h * h) / 2;
      fase += vel * dt * 0.22;
      for (i = 0; i < estrelas.length; i++) {
        var e = estrelas[i], ang = e.x * PI2, r0 = Math.sqrt(e.y), r = (((r0 - fase * (0.4 + e.b * 0.8)) % 1) + 1) % 1, rr = r * R0;
        var x = cx0 + Math.cos(ang) * rr, y = cy0 + Math.sin(ang) * rr, tw = OVM.reduz ? 1 : 0.7 + 0.3 * Math.sin(t * e.v + e.f);
        ctx.globalAlpha = Math.min(1, e.b * tw * (cfg.estrelasAlfa == null ? 1 : cfg.estrelasAlfa(E.s)) * (0.5 + r * 0.6));
        if (ve > 0.06) {
          var dirx = Math.cos(ang), diry = Math.sin(ang), c = vel > 0 ? 1 : -1, len = ve * (10 + r * 90);
          ctx.strokeStyle = '#DDE8FF'; ctx.lineWidth = e.r * 0.9 + 0.2; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + dirx * len * c, y + diry * len * c); ctx.stroke();
        } else { ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, e.r * 0.8, 0, PI2); ctx.fill(); }
      }
      ctx.globalAlpha = 1;
      // as folhas, da maior para a menor
      for (k = 0; k < ordem.length; k++) {
        i = ordem[k];
        var n = N[i], px = n.d / FOV * L, a = janela(px, L) * (n.alfa == null ? 1 : n.alfa);
        if (a < 0.004) continue;
        if (!n.folha) { n.folha = nova(); var rnd = OVM.rand((cfg.semente || 31) + i * 97), info = n.pintar(n.folha.getContext('2d'), rnd) || {}; n.info = info; }
        var cx = cx0 + (n.off ? n.off[0] : 0) * px, cy = cy0 + (n.off ? n.off[1] : 0) * px, sz = px / 0.9;
        ctx.globalAlpha = a; ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
        ctx.drawImage(n.folha, cx - sz / 2, cy - sz / 2, sz, sz);
        if (px > 16 && px < 0.98 * L && !n.semAnel) {   // anel e nome quando o objeto cabe inteiro
          ctx.strokeStyle = 'rgba(235,240,255,.42)'; ctx.lineWidth = 1.2; ctx.setLineDash([4, 6]); ctx.beginPath(); ctx.arc(cx, cy, px / 2 * 1.03, 0, PI2); ctx.stroke(); ctx.setLineDash([]);
          if (px > 34) OVM.pilula(ctx, n.nome, cx, cy - px / 2 * 1.03 - 13, { px: 12, alpha: a });
        }
        if (n.marcas && px >= 0.5 * L) {
          var am = a * OVM.suave((px - 0.5 * L) / (0.2 * L));
          for (var m = 0; m < n.marcas.length; m++) { var mk = n.marcas[m]; OVM.pilula(ctx, mk.t, cx + mk.x * px, cy + mk.y * px, { px: 11.5, alpha: am }); }
        }
        ctx.globalAlpha = 1;
      }
      // "você está aqui"
      if (cfg.aqui) {
        var pm = E.px(menor), va = 1 - OVM.suave((pm - 40) / 90);
        if (va > 0.01) {
          var pul = OVM.reduz ? 0 : 0.5 + 0.5 * Math.sin(t * 3);
          ctx.globalAlpha = va; ctx.strokeStyle = 'rgba(255,214,120,' + (0.7 - pul * 0.4) + ')'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(cx0, cy0, 8 + pul * 6, 0, PI2); ctx.stroke();
          ctx.fillStyle = '#FFD878'; ctx.beginPath(); ctx.arc(cx0, cy0, 3.6, 0, PI2); ctx.fill();
          OVM.pilula(ctx, cfg.aqui, cx0, cy0 + 24, { px: 12, alpha: va, cor: '#FFE9B8' }); ctx.globalAlpha = 1;
        }
      }
      // barra de escala
      if (cfg.barra) {
        var alvoPx = Math.min(0.3 * L, 160), len = FOV * alvoPx / L, ex = Math.pow(10, Math.floor(Math.log10(len))), m1 = len / ex, bs = m1 >= 5 ? 5 : m1 >= 2 ? 2 : 1, len2 = bs * ex, bpx = len2 / FOV * L, bx = 14, by = h - 20;
        ctx.strokeStyle = 'rgba(255,255,255,.85)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(bx, by - 5); ctx.lineTo(bx, by + 5); ctx.moveTo(bx, by); ctx.lineTo(bx + bpx, by); ctx.moveTo(bx + bpx, by - 5); ctx.lineTo(bx + bpx, by + 5); ctx.stroke();
        OVM.pilula(ctx, cfg.barra(len2), bx + bpx / 2, by - 17, { px: 11.5, alpha: 0.9 });
      }
      if (cfg.aoQuadro) cfg.aoQuadro(E, dt, t);
    }
    E.quadro = quadro;
    OVM.anima(quadro, cfg.canvas);
    quadro(0.016, 0.5);
    return E;
  };

  // os níveis do cosmos já prontos (nomes, tamanhos e notas vêm de OVM_DADOS.niveis, a fonte única)
  OVM.cosmos = function () {
    return OVM_DADOS.niveis.map(function (n) {
      var c = COSMOS[n.id];
      return { id: n.id, nome: n.nome, obs: n.obs, d: n.al, off: c.off, pintar: c.pintar, marcas: c.marcas, nota: c.nota };
    });
  };
  OVM.motor = { TAM: TAM, C: C, RAIO: RAIO, gauss: gauss, mancha: mancha, esfera: esfera, sombra: sombra, galaxia: galaxia, teia: teia };
})();

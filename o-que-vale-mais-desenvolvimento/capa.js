/* Capa: um cartaz da jornada. De uma xícara de café (embaixo) a um ponto de luz (no alto), uma régua com as medidas da viagem.
   Sem pistas do fim: só a escala. */
OVM.pronto(function () {
  var canvas = OVM.$('#tela');
  if (!canvas) return;
  var T = OVM.tela(canvas);
  var est = OVM.estrelas(7, 260);
  var marcas = [
    { r: 0.00, t: 'R$ 6,98', c: '#FFC46B' },
    { r: 0.24, t: 'R$ 542 mil', c: '#FFD27A' },
    { r: 0.50, t: '300.000 km por segundo', c: '#F5E7C6' },
    { r: 0.74, t: '9,5 trilhões de km', c: '#CFE0FF' },
    { r: 1.00, t: '93 bilhões de anos-luz', c: '#A9C6FF' }
  ];
  var vapor = [], rnd = OVM.rand(11), acum = 0;

  function xicara(ctx, cx, cy, s) {
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s);
    OVM.brilho(ctx, 0, -20, 190, 'rgba(255,170,90,A)', 0.35);
    ctx.fillStyle = '#EDE3D2'; ctx.beginPath(); ctx.ellipse(0, 22, 92, 15, 0, 0, 6.2832); ctx.fill();
    ctx.fillStyle = '#CBBFA9'; ctx.beginPath(); ctx.ellipse(0, 19, 74, 10, 0, 0, 6.2832); ctx.fill();
    ctx.fillStyle = '#FFFDF8'; ctx.beginPath(); ctx.moveTo(-58, -28); ctx.lineTo(58, -28); ctx.lineTo(58, -2); ctx.quadraticCurveTo(58, 28, 0, 28); ctx.quadraticCurveTo(-58, 28, -58, -2); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = '#FFFDF8'; ctx.lineWidth = 11; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(58, -18); ctx.quadraticCurveTo(92, -18, 92, 4); ctx.quadraticCurveTo(92, 26, 58, 20); ctx.stroke();
    ctx.fillStyle = '#FFFDF8'; ctx.beginPath(); ctx.ellipse(0, -28, 58, 12, 0, 0, 6.2832); ctx.fill();
    ctx.fillStyle = '#4A2A14'; ctx.beginPath(); ctx.ellipse(0, -27, 50, 8.5, 0, 0, 6.2832); ctx.fill();
    ctx.restore();
  }

  function desenhar(dt, t) {
    var ctx = T.ctx, w = T.w, h = T.h;
    OVM.fundoCanvas(T);
    var g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, '#04071A'); g.addColorStop(0.55, '#0E1838'); g.addColorStop(0.85, '#2A2036'); g.addColorStop(1, '#4A2F2A');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    // estrelas: mais no alto
    for (var i = 0; i < est.length; i++) {
      var e = est[i], x = e.x * w, y = e.y * h, fade = Math.pow(1 - y / h, 0.8);
      var tw = OVM.reduz ? 1 : 0.65 + 0.35 * Math.sin(t * e.v + e.f);
      ctx.globalAlpha = Math.min(1, e.b * tw * fade * 1.1);
      ctx.fillStyle = e.c < 0.12 ? '#BFD6FF' : e.c > 0.9 ? '#FFD9A8' : '#FFFFFF';
      ctx.beginPath(); ctx.arc(x, y, e.r, 0, 6.2832); ctx.fill();
    }
    ctx.globalAlpha = 1;

    var portrait = h > w * 1.05;
    // régua na borda esquerda
    var rx = portrait ? 18 : w - 26, y0 = portrait ? h * 0.93 : h * 0.9, y1 = portrait ? h * 0.7 : h * 0.07, dir = portrait ? 1 : -1;
    var p = OVM.reduz ? 0.5 : ((t * 0.12) % 1.5);
    ctx.lineCap = 'round';
    var rg = ctx.createLinearGradient(0, y0, 0, y1); rg.addColorStop(0, 'rgba(255,196,107,.9)'); rg.addColorStop(1, 'rgba(169,198,255,.9)');
    ctx.strokeStyle = rg; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(rx, y0); ctx.lineTo(rx, y1); ctx.stroke();
    for (var k = 0; k <= 40; k++) {
      var yy = y0 + (y1 - y0) * k / 40, big = k % 8 === 0;
      ctx.globalAlpha = big ? 0.95 : 0.4; ctx.strokeStyle = rg;
      ctx.beginPath(); ctx.moveTo(rx, yy); ctx.lineTo(rx + dir * (big ? 14 : 7), yy); ctx.stroke();
    }
    ctx.globalAlpha = 1;
    var fs = portrait ? 11.5 : 13;
    ctx.font = OVM.fonte(fs, 600);
    ctx.textBaseline = 'middle'; ctx.textAlign = portrait ? 'left' : 'right';
    for (var m = 0; m < marcas.length; m++) {
      var mk = marcas[m], my = y0 + (y1 - y0) * mk.r;
      var br = OVM.reduz ? 0.8 : Math.max(0.45, 1 - Math.abs(p - mk.r) * 5);
      OVM.brilho(ctx, rx, my, 18 * br + 6, 'rgba(255,214,140,A)', 0.55 * br);
      ctx.fillStyle = mk.c; ctx.beginPath(); ctx.arc(rx, my, 4.2, 0, 6.2832); ctx.fill();
      ctx.globalAlpha = 0.55 + 0.45 * br; ctx.fillStyle = mk.c; ctx.fillText(mk.t, rx + dir * 22, my); ctx.globalAlpha = 1;
    }
    // pulso de luz subindo pela régua
    var py = y0 + (y1 - y0) * Math.min(p, 1.05);
    if (p < 1.05) {
      var tr = ctx.createLinearGradient(0, py + 90, 0, py); tr.addColorStop(0, 'rgba(255,230,160,0)'); tr.addColorStop(1, 'rgba(255,240,200,.9)');
      ctx.strokeStyle = tr; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(rx, py + 90); ctx.lineTo(rx, py); ctx.stroke();
      OVM.brilho(ctx, rx, py, 22, 'rgba(255,240,200,A)', 0.9);
    }

    // xícara e vapor
    var cs = Math.max(0.55, Math.min(1.25, Math.min(w, h) / 560));
    var cx = portrait ? w * 0.58 : w * 0.7, cy = portrait ? h * 0.88 : h * 0.84;
    if (!OVM.reduz) {
      acum += dt;
      while (acum > 0.12) { acum -= 0.12; vapor.push({ x: cx + (rnd() - 0.5) * 70 * cs, y: cy - 44 * cs, a: 0, f: rnd() * 6, r: (6 + rnd() * 8) * cs, v: (26 + rnd() * 20) * cs }); }
      for (var q = vapor.length - 1; q >= 0; q--) { var v = vapor[q]; v.a += dt * 0.28; v.y -= v.v * dt; v.x += Math.sin(t * 1.3 + v.f) * 10 * dt; if (v.a >= 1) vapor.splice(q, 1); }
    }
    for (var z = 0; z < vapor.length; z++) {
      var s = vapor[z], al = Math.pow(1 - s.a, 1.6) * 0.42;
      OVM.brilho(ctx, s.x, s.y, s.r * (1 + s.a * 2.2), 'rgba(255,248,235,A)', al);
    }
    ctx.textAlign = 'left';
    xicara(ctx, cx, cy, cs);
  }
  OVM.anima(desenhar, canvas);
  desenhar(0.016, 0.5);
});

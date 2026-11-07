/* A etiqueta final: a vitrine de preços do estudo, a etiqueta coberta que vira e mostra "Jesus", e todos os preços que encolhem.
   Usada na parte 10 (interativa) e na página de conclusão (já virada). Extras (por passo): cruz de luz, trinta moedas, valor e gravidade, presente. */
(function () {
  'use strict';
  var OVM = window.OVM, PI2 = 6.2832;

  OVM.Final = function (canvas, cfg) {
    cfg = cfg || {};
    var T = OVM.tela(canvas), F = OVM.fmt, D = window.OVM_DADOS, est = OVM.estrelas(21, 230), rnd = OVM.rand(88), P = D.precos, VG = D.viagens;
    var itens = [['Café', P[0].valor], ['Refeição', P[1].valor], ['Viagem', P[3].valor], ['Carro', P[4].valor], ['Casa', P[5].valor], ['Estação Espacial', VG[2].reais], ['Marte (meta)', VG[4].reais]];
    var S = { flip: cfg.revelada ? 1 : 0, alvo: cfg.revelada ? 1 : 0, extra: cfg.extra || '', extraA: 0, faiscas: [], acum: 0, avisou: !!cfg.revelada };
    var interativo = cfg.interativo !== false && !cfg.revelada, aviso = 0;
    function curto(v) { return v < 100 ? F.n(v, 2) : v < 1000 ? F.n(Math.round(v)) : v < 1e6 ? F.n(Math.round(v / 1000)) + ' mil' : F.grande(v); }

    function etiqueta(ctx, x, y, w, h, rot, linhas, opt) {
      opt = opt || {};
      ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
      ctx.shadowColor = 'rgba(0,0,0,.4)'; ctx.shadowBlur = 12; ctx.shadowOffsetY = 4; ctx.fillStyle = opt.fundo || '#FFFBF0'; OVM.caminhoArr(ctx, -w / 2, 0, w, h, 8); ctx.fill(); ctx.shadowColor = 'transparent';
      ctx.strokeStyle = opt.borda || '#1F2A44'; ctx.lineWidth = 2; ctx.stroke(); ctx.fillStyle = '#E9DCC1'; ctx.beginPath(); ctx.arc(0, h * 0.18, Math.max(3, h * 0.07), 0, PI2); ctx.fill(); ctx.stroke();
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = opt.cor || '#1F2A44';
      linhas.forEach(function (l) { var px = l.px, mw; ctx.font = OVM.fonte(px, l.peso || 600, true); mw = ctx.measureText(l.t).width; if (mw > w * 0.9) { px = px * w * 0.9 / mw; ctx.font = OVM.fonte(px, l.peso || 600, true); } ctx.fillText(l.t, 0, h * l.y); });
      ctx.restore();
    }
    function pessoa(ctx, x, y, s, cor) {
      ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = cor;
      ctx.beginPath(); ctx.arc(0, -86, 13, 0, PI2); ctx.fill();
      ctx.beginPath(); ctx.moveTo(-15, -70); ctx.quadraticCurveTo(0, -78, 15, -70); ctx.lineTo(21, -12); ctx.lineTo(8, -12); ctx.lineTo(8, 0); ctx.lineTo(-8, 0); ctx.lineTo(-8, -12); ctx.lineTo(-21, -12); ctx.closePath(); ctx.fill();
      ctx.lineWidth = 7; ctx.lineCap = 'round'; ctx.strokeStyle = cor; ctx.beginPath(); ctx.moveTo(-14, -66); ctx.lineTo(-22, -34); ctx.moveTo(14, -66); ctx.lineTo(22, -34); ctx.stroke();
      ctx.restore();
    }

    function quadro(dt, t) {
      var w = T.w, h = T.h, ctx = T.ctx, u = Math.min(w, h), k;
      S.flip = OVM.reduz ? S.alvo : OVM.seguir(S.flip, S.alvo, 2.6, dt); if (Math.abs(S.flip - S.alvo) < 0.003) S.flip = S.alvo;
      S.extraA = OVM.seguir(S.extraA, S.extra ? 1 : 0, 4, dt); aviso = OVM.seguir(aviso, interativo && S.flip < 0.05 ? 1 : 0, 4, dt);
      if (S.flip > 0.985 && !S.avisou) { S.avisou = true; if (cfg.aoRevelar) cfg.aoRevelar(); }
      var f = S.flip, enc = OVM.suave((f - 0.35) / 0.65), brilho = OVM.suave((f - 0.5) / 0.5);
      OVM.fundoCanvas(T);
      var g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#04061A'); g.addColorStop(0.6, '#10163A'); g.addColorStop(1, '#2A1E3E'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
      OVM.pintarEstrelas(ctx, w, h, est, t, { alpha: 0.8 });
      var cx = w / 2, cy = h * 0.55, tw = Math.max(120, Math.min(w * 0.5, 300, h * 0.78)), th = tw * 0.62;
      OVM.brilho(ctx, cx, cy, tw * 1.7, 'rgba(255,214,120,A)', 0.5 * brilho);
      // a cruz de luz (passo da mão que sustenta os mundos)
      if (S.extra === 'cruz' || (S.extraA > 0.02 && S.extra === 'cruz')) { /* desenhado abaixo, com o alfa do extra */ }
      if (S.extraA > 0.02 && S.extra === 'cruz') {
        ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = S.extraA * (0.3 + 0.1 * (OVM.reduz ? 0 : Math.sin(t * 1.6)));
        var vg = ctx.createLinearGradient(0, cy - th * 1.55, 0, cy + th * 1.6); vg.addColorStop(0, 'rgba(255,240,190,0)'); vg.addColorStop(0.35, 'rgba(255,240,190,1)'); vg.addColorStop(1, 'rgba(255,240,190,0)');
        ctx.fillStyle = vg; ctx.fillRect(cx - 7, cy - th * 1.55, 14, th * 3.15);
        var hg = ctx.createLinearGradient(cx - tw * 0.85, 0, cx + tw * 0.85, 0); hg.addColorStop(0, 'rgba(255,240,190,0)'); hg.addColorStop(0.5, 'rgba(255,240,190,1)'); hg.addColorStop(1, 'rgba(255,240,190,0)'); ctx.fillStyle = hg; ctx.fillRect(cx - tw * 0.85, cy - th * 0.62 - 7, tw * 1.7, 14);
        ctx.restore();
      }
      // as etiquetas pequenas de tudo o que vimos: encolhem quando a etiqueta final é virada
      var cols = Math.max(2, Math.min(7, Math.floor(w / 100))), rows = Math.ceil(itens.length / cols), cw = w / cols, sc = 1 - 0.5 * enc, alfa = 1 - 0.35 * enc;
      itens.forEach(function (it, j) {
        var col = j % cols, row = Math.floor(j / cols), x = cw * (col + 0.5), y = h * 0.035 + row * 56 * sc * (u / 400 + 0.6) + enc * 0, rot = OVM.reduz ? 0 : Math.sin(t * 1.1 + j) * 0.05, ww = Math.min(cw * 0.86, 120) * sc, hh = 54 * sc * Math.min(1.3, u / 340);
        ctx.globalAlpha = alfa; ctx.strokeStyle = 'rgba(160,140,100,.5)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, y); ctx.stroke();
        etiqueta(ctx, x, y, ww, hh, rot, [{ t: it[0], px: 11 * sc + 2, y: 0.5, peso: 500 }, { t: 'R$ ' + curto(it[1]), px: 16 * sc + 3, y: 0.78 }]); ctx.globalAlpha = 1;
      });
      // o presente / moedas / pessoa (extras de passos)
      var ex = S.extraA;
      if (ex > 0.02 && S.extra === 'moedas') {
        ctx.save(); ctx.globalAlpha = ex; var mx = cx - tw * 0.78, my = cy + th * 0.55, r = Math.max(5, u * 0.017), n = 0;
        for (var rw = 0; rw < 7; rw++) for (var cl = 0; cl < 7 - rw && n < 28; cl++) { n++; var px = mx + (cl - (6 - rw) / 2) * r * 2.1, py = my - rw * r * 1.7; ctx.fillStyle = '#C9CED8'; ctx.beginPath(); ctx.arc(px, py, r, 0, PI2); ctx.fill(); ctx.strokeStyle = '#8A91A3'; ctx.lineWidth = 1.2; ctx.stroke(); ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.beginPath(); ctx.arc(px - r * 0.3, py - r * 0.3, r * 0.32, 0, PI2); ctx.fill(); }
        ctx.restore(); OVM.pilula(ctx, '30 moedas de prata: o preço que o mundo pôs', mx, my + r * 3, { px: 12, alpha: ex, pad: 10 });
      }
      if (ex > 0.02 && (S.extra === 'valor' || S.extra === 'pecado')) {
        var cor = S.extra === 'valor' ? '#1A1308' : '#0E0509', px2 = cx + tw * 0.78, py2 = h * 0.97, sp = Math.min(2, u / 250);
        ctx.save(); ctx.globalAlpha = ex; if (S.extra === 'valor') { OVM.brilho(ctx, px2, py2 - 50 * sp, 120 * sp, 'rgba(255,214,120,A)', 0.8); } else { OVM.brilho(ctx, px2, py2 - 50 * sp, 110 * sp, 'rgba(200,60,60,A)', 0.55); }
        pessoa(ctx, px2, py2, sp, cor); ctx.restore();
        OVM.pilula(ctx, S.extra === 'valor' ? 'você tem valor imenso' : 'o pecado é grave: custou isto', px2, py2 - 100 * sp - 16, { px: 12.5, alpha: ex, fundo: S.extra === 'valor' ? 'rgba(242,217,160,.97)' : 'rgba(100,20,30,.92)', cor: S.extra === 'valor' ? '#1F2A44' : '#FFD9D0', pad: 11 });
      }
      // faíscas de luz subindo da etiqueta
      if (brilho > 0.3 && !OVM.reduz) { S.acum += dt; while (S.acum > 0.06) { S.acum -= 0.06; S.faiscas.push({ x: cx + (rnd() - 0.5) * tw, y: cy + th * 0.5, vy: -(26 + rnd() * 50), vx: (rnd() - 0.5) * 14, a: 0, r: 1 + rnd() * 2 }); } }
      for (k = S.faiscas.length - 1; k >= 0; k--) { var s = S.faiscas[k]; s.a += dt * 0.34; s.y += s.vy * dt; s.x += s.vx * dt; if (s.a >= 1) S.faiscas.splice(k, 1); }
      for (k = 0; k < S.faiscas.length; k++) { s = S.faiscas[k]; ctx.globalAlpha = Math.sin(s.a * Math.PI) * 0.9 * brilho; ctx.fillStyle = '#FFE9A8'; ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, PI2); ctx.fill(); }
      ctx.globalAlpha = 1;
      // a etiqueta grande, que vira
      var ang = f * Math.PI, sx = Math.max(0.03, Math.abs(Math.cos(ang))), frente = f >= 0.5, bal = f < 0.02 && !OVM.reduz ? Math.sin(t * 1.6) * 0.04 : 0;
      ctx.save(); ctx.translate(cx, cy - th / 2); ctx.rotate(bal); ctx.scale(sx, 1 + 0.04 * Math.sin(ang));
      ctx.shadowColor = frente ? 'rgba(255,214,120,.7)' : 'rgba(0,0,0,.5)'; ctx.shadowBlur = frente ? 30 : 16; ctx.shadowOffsetY = 6;
      if (!frente) {
        ctx.fillStyle = '#1B2447'; OVM.caminhoArr(ctx, -tw / 2, 0, tw, th, 14); ctx.fill(); ctx.shadowColor = 'transparent'; ctx.strokeStyle = '#E0BC66'; ctx.lineWidth = 3; ctx.setLineDash([8, 7]); OVM.caminhoArr(ctx, -tw / 2 + 8, 8, tw - 16, th - 16, 10); ctx.stroke(); ctx.setLineDash([]);
        ctx.fillStyle = '#E0BC66'; ctx.beginPath(); ctx.arc(0, th * 0.1, th * 0.05, 0, PI2); ctx.fill();
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#F2D9A0'; ctx.font = OVM.fonte(th * 0.55, 500, true); ctx.fillText('?', 0, th * 0.56);
      } else {
        var gf = ctx.createLinearGradient(0, 0, 0, th); gf.addColorStop(0, '#FFF8DA'); gf.addColorStop(1, '#F4DB9C'); ctx.fillStyle = gf; OVM.caminhoArr(ctx, -tw / 2, 0, tw, th, 14); ctx.fill(); ctx.shadowColor = 'transparent';
        ctx.strokeStyle = '#8F6414'; ctx.lineWidth = 3.4; ctx.stroke(); ctx.fillStyle = '#F2E4BE'; ctx.beginPath(); ctx.arc(0, th * 0.1, th * 0.05, 0, PI2); ctx.fill(); ctx.stroke();
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#1F2A44'; ctx.font = OVM.fonte(th * 0.4, 600, true); ctx.fillText('Jesus', 0, th * 0.5);
        ctx.fillStyle = '#7A5410'; ctx.font = OVM.fonte(Math.max(10, th * 0.1), 600); ctx.fillText('O PREÇO PAGO POR VOCÊ', 0, th * 0.82);
      }
      ctx.restore();
      // presente: um laço sobre a etiqueta (recebido, não comprado)
      if (ex > 0.02 && S.extra === 'presente') {
        ctx.save(); ctx.globalAlpha = ex; ctx.translate(cx, cy - th / 2 - 4); var b = Math.min(1.4, tw / 200);
        ctx.scale(b, b); ctx.fillStyle = '#C9354A'; [-1, 1].forEach(function (d) { ctx.beginPath(); ctx.ellipse(d * 26, -16, 28, 16, d * -0.5, 0, PI2); ctx.fill(); ctx.strokeStyle = '#8F1E30'; ctx.lineWidth = 2; ctx.stroke(); });
        ctx.beginPath(); ctx.arc(0, -8, 10, 0, PI2); ctx.fill(); ctx.stroke(); ctx.fillStyle = '#C9354A'; ctx.beginPath(); ctx.moveTo(-6, 0); ctx.lineTo(-22, 36); ctx.lineTo(-8, 30); ctx.lineTo(0, 4); ctx.closePath(); ctx.fill(); ctx.beginPath(); ctx.moveTo(6, 0); ctx.lineTo(22, 36); ctx.lineTo(8, 30); ctx.lineTo(0, 4); ctx.closePath(); ctx.fill();
        ctx.restore(); OVM.pilula(ctx, 'recebido, não comprado', cx, cy + th / 2 + 30, { px: 14, alpha: ex, fundo: 'rgba(242,217,160,.97)', cor: '#1F2A44', pad: 14 });
      }
      if (aviso > 0.05) OVM.pilula(ctx, 'toque na etiqueta para virar', cx, cy + th / 2 + 32, { px: 13, alpha: aviso * (OVM.reduz ? 1 : 0.7 + 0.3 * Math.sin(t * 3)), fundo: 'rgba(242,217,160,.96)', cor: '#1F2A44', pad: 13 });
      S.caixa = { x: cx - tw / 2, y: cy - th / 2, w: tw, h: th };
    }
    OVM.anima(quadro, canvas);
    quadro(0.016, 0.5);

    var API = {
      revelar: function () { S.alvo = 1; }, desvirar: function () { S.alvo = 0; S.avisou = false; }, revelada: function () { return S.flip > 0.99; }, definirExtra: function (x) { S.extra = x || ''; if (x) S.extraA = Math.max(S.extraA, 0.0); },
      estado: S
    };
    if (interativo) {
      canvas.style.cursor = 'pointer';
      canvas.addEventListener('click', function (e) { var r = canvas.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top, c = S.caixa; if (c && x > c.x - 20 && x < c.x + c.w + 20 && y > c.y - 20 && y < c.y + c.h + 20) API.revelar(); });
    }
    return API;
  };
})();

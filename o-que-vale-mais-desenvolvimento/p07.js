/* Parte 7: onde fica o trono? A subida (motor de escala) até o limite do universo e um ponto de luz; Deus também está aqui; o anjo da ressurreição (imaginação)
   e o laboratório de luz e som (relâmpago e trovão). A velocidade do anjo NUNCA é afirmada: é imaginação marcada. */
OVM.pronto(function () {
  var D = OVM_DADOS, V = OVM_V, F = OVM.fmt, AL = D.anoLuzKm, PI2 = 6.2832, k, i;
  var cena = OVM.$('#cena'), c1 = OVM.$('#tela'), c2 = OVM.$('#tela2'), nomeEl = OVM.$('#hud-nome'), tamEl = OVM.$('#hud-tam'), pcEl = OVM.$('#hud-pc'), trilho = OVM.$('#p7-trilho'), etq = OVM.$('#p7-etq'), nota = OVM.$('#p7-nota');
  var bSubir = OVM.$('#p7-subir'), bVoltar = OVM.$('#p7-voltar'), sDist = OVM.$('#p7-dist'), oDist = OVM.$('#p7-dist-saida');
  var sKm = OVM.$('#p7-km'), oKm = OVM.$('#p7-km-saida'), bRaio = OVM.$('#p7-raio'), bSom = OVM.$('#p7-som');
  var niveis = OVM.cosmos(), n = niveis.length, modo = 'subida', luzA = 0, presA = 0, presAlvo = 0, usando = false;
  var CURTOS = ['Terra', 'Lua', 'Sistema Solar', 'Vizinhança do Sol', 'Via Láctea', 'Grupo Local', 'Laniakea', 'Universo observável'];

  // ================================================================ 1) a subida
  var cfg = { canvas: c1, niveis: niveis, aqui: 'Você está aqui', folga: 1.3, barra: function (len) { return F.distKm(len * AL); }, aoQuadro: aoQuadro, semente: 31 };
  var E, s0, sFim;
  function aoQuadro(Eng, dt, t) {
    var ctx = Eng.T.ctx, w = Eng.T.w, h = Eng.T.h, L = Math.min(w, h) * 0.94, cx = w / 2, cy = h / 2, j;
    luzA = OVM.seguir(luzA, OVM.suave((Eng.s - (Eng.sDe(n - 1) + 0.4)) / 0.5), 6, dt); presA = OVM.seguir(presA, presAlvo, 3, dt);
    // hud: a que distância da Terra a câmera está (metade do campo de visão)
    var km = Eng.campo() / 2 * AL, near = Eng.perto();
    nomeEl.textContent = km < 1e6 ? 'Perto da Terra' : 'A uns ' + F.distKm(km) + ' da Terra';
    tamEl.textContent = near > 0 ? 'passando por: ' + CURTOS[near] : '';
    pcEl.textContent = km >= AL ? F.parsecKm(km) + ' (parsecs)' : '';
    for (j = 0; j < trilho.children.length; j++) trilho.children[j].classList.toggle('passou', Eng.s >= Eng.sDe(j + 1) - 0.25);
    if (!usando && s0 !== undefined) { sDist.value = OVM.clamp((Eng.s - s0) / (sFim - s0) * 100, 0, 100); OVM.preencher(sDist); }
    oDist.textContent = F.distKm(km);
    // o ponto de luz, muito além: sem rosto e sem lugar certo (é só imaginação)
    if (luzA > 0.01) {
      var fx = cx + 0.33 * L, fy = cy - 0.3 * L, pul = OVM.reduz ? 1 : 0.85 + 0.15 * Math.sin(t * 2);
      if (presA > 0.02) { ctx.save(); var g = ctx.createLinearGradient(fx, fy, cx, cy); g.addColorStop(0, 'rgba(255,236,170,' + 0.7 * presA * luzA + ')'); g.addColorStop(1, 'rgba(255,214,120,' + 0.2 * presA * luzA + ')'); ctx.strokeStyle = g; ctx.lineWidth = 2.2; ctx.setLineDash([2, 6]); ctx.beginPath(); ctx.moveTo(fx, fy); ctx.lineTo(cx, cy); ctx.stroke(); ctx.restore(); OVM.brilho(ctx, cx, cy, 46 * presA, 'rgba(255,220,130,A)', 0.55 * presA); }
      ctx.globalAlpha = luzA; OVM.brilho(ctx, fx, fy, 56 * pul, 'rgba(255,240,200,A)', 0.9); OVM.brilho(ctx, fx, fy, 16, 'rgba(255,255,255,A)', 1); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(fx, fy, 3.4, 0, PI2); ctx.fill();
      OVM.pilula(ctx, 'imaginação: ninguém sabe onde fica', fx, fy + 30, { px: 11.5, fundo: 'rgba(80,60,10,.9)', cor: '#FFE9B8', alpha: luzA }); ctx.globalAlpha = 1;
    }
  }
  E = OVM.Escala(cfg);
  s0 = E.sDe(0); sFim = E.sDe(n - 1) + 1.1;
  E.definir(s0);
  CURTOS.forEach(function (nm, j) { if (j === 0) return; var li = document.createElement('li'); li.innerHTML = '<span class="bola"></span><span class="nome">' + nm + '<small>' + F.distKm(niveis[j].d * AL) + (niveis[j].d * AL >= AL ? ' · ' + F.parsecKm(niveis[j].d * AL) : '') + '</small></span>'; trilho.appendChild(li); });
  bSubir.addEventListener('click', function () { usando = false; E.irS(sFim, 24); });
  bVoltar.addEventListener('click', function () { usando = false; E.irS(s0, 5); });
  sDist.addEventListener('input', function () { usando = true; E.definir(OVM.lerp(s0, sFim, +sDist.value / 100)); OVM.preencher(sDist); });
  sDist.addEventListener('change', function () { usando = false; });

  // ================================================================ 2) o anjo e o relâmpago (segundo quadro)
  var T2 = OVM.tela(c2), est = OVM.estrelas(19, 160), rnd = OVM.rand(23);
  var raio = { t0: -1, km: 2, zig: [], falou: false }, abalo = 0, flash = 0, somOn = false, ac = null;
  var segmentos = []; for (i = 0; i < 12; i++) segmentos.push((rnd() - 0.5));
  function ceu(ctx, w, h, hy) {
    var g = ctx.createLinearGradient(0, 0, 0, hy); g.addColorStop(0, '#02030B'); g.addColorStop(1, modo === 'raio' ? '#1B2447' : '#0F1A3C'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    OVM.pintarEstrelas(ctx, w, h * 0.7, est, OVM.t, { alpha: modo === 'raio' ? 0.35 : 0.9 });
  }
  function pessoa(ctx, x, y, s) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = '#05070E'; ctx.beginPath(); ctx.arc(0, -34, 5.2, 0, PI2); ctx.fill();
    ctx.beginPath(); ctx.moveTo(-5, -28); ctx.lineTo(5, -28); ctx.lineTo(7, -8); ctx.lineTo(3, -8); ctx.lineTo(3, 0); ctx.lineTo(-3, 0); ctx.lineTo(-3, -8); ctx.lineTo(-7, -8); ctx.closePath(); ctx.fill(); ctx.restore();
  }
  function anjo(ctx, x, y, s, a, t) {   // uma figura de luz, sem rosto e sem detalhes: tratamento reverente
    ctx.save(); ctx.translate(x, y); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = a;
    OVM.brilho(ctx, 0, -10 * s, 120 * s, 'rgba(255,245,210,A)', 0.55);
    var g = ctx.createLinearGradient(0, -90 * s, 0, 40 * s); g.addColorStop(0, 'rgba(255,255,255,.0)'); g.addColorStop(0.35, 'rgba(255,252,235,.95)'); g.addColorStop(1, 'rgba(255,230,160,.0)'); ctx.fillStyle = g;
    ctx.beginPath(); ctx.ellipse(0, -14 * s, 9 * s, 34 * s, 0, 0, PI2); ctx.fill();
    ctx.beginPath(); ctx.arc(0, -52 * s, 7 * s, 0, PI2); ctx.fillStyle = 'rgba(255,255,250,.95)'; ctx.fill();
    [-1, 1].forEach(function (d) { ctx.beginPath(); ctx.moveTo(d * 6 * s, -34 * s); ctx.quadraticCurveTo(d * 60 * s, -80 * s - Math.sin(t * 3) * 3 * s, d * 46 * s, -4 * s); ctx.quadraticCurveTo(d * 24 * s, -24 * s, d * 6 * s, -20 * s); ctx.fillStyle = 'rgba(255,250,225,.7)'; ctx.fill(); });
    ctx.restore();
  }
  function modoAnjo(ctx, w, h, t) {
    var hy = h * 0.72, tt = t % 14, tx = w * 0.62, sh = tt > 4.15 && tt < 5.6 ? (1 - (tt - 4.15) / 1.45) * 7 : 0;
    ctx.save(); if (sh) ctx.translate((Math.random() - 0.5) * sh, (Math.random() - 0.5) * sh);
    ceu(ctx, w, h, hy);
    // colina, jardim e túmulo
    ctx.fillStyle = '#0A0C18'; ctx.beginPath(); ctx.moveTo(-10, h); ctx.lineTo(-10, hy + 6); for (var x = 0; x <= w + 10; x += 10) ctx.lineTo(x, hy + 6 - Math.sin(x / w * 3.4 + 1) * h * 0.012); ctx.lineTo(w + 10, h); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#11141F'; ctx.beginPath(); ctx.moveTo(tx - w * 0.2, hy + 10); ctx.quadraticCurveTo(tx, hy - h * 0.26, tx + w * 0.2, hy + 10); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#020306'; ctx.beginPath(); ctx.ellipse(tx, hy - 8, w * 0.045, h * 0.055, 0, Math.PI, 0); ctx.lineTo(tx + w * 0.045, hy + 12); ctx.lineTo(tx - w * 0.045, hy + 12); ctx.closePath(); ctx.fill();
    for (var o = 0; o < 4; o++) { var ox = w * (0.1 + o * 0.075), oy = hy + 4 - Math.sin(ox / w * 3.4 + 1) * h * 0.012; ctx.fillStyle = '#080A13'; ctx.fillRect(ox - 2, oy - h * 0.06, 4, h * 0.06); ctx.beginPath(); ctx.ellipse(ox, oy - h * 0.07, h * 0.04, h * 0.026, 0, 0, PI2); ctx.fill(); }
    var rolo = tt > 4.2 ? OVM.suave((tt - 4.2) / 1.6) : 0, sx = tx + w * 0.012 + rolo * w * 0.1;
    ctx.fillStyle = '#2A2D3A'; ctx.beginPath(); ctx.ellipse(sx, hy - 1, h * 0.062, h * 0.062, 0, 0, PI2); ctx.fill(); ctx.strokeStyle = '#3B3F52'; ctx.lineWidth = 2; ctx.stroke();
    pessoa(ctx, w * 0.3, hy + 8, Math.max(0.6, h / 520)); pessoa(ctx, w * 0.34, hy + 10, Math.max(0.55, h / 560));
    // a descida (imaginação)
    var a0 = 0, p = Math.min(1, tt / 4.2), ax = OVM.lerp(w * 0.92, tx - w * 0.03, p * p), ay = OVM.lerp(-h * 0.05, hy - h * 0.12, p * p), brilho = tt < 4.2 ? 0.25 + 0.75 * p : tt < 11 ? 1 : Math.max(0, 1 - (tt - 11) / 2.5);
    if (tt < 4.25) { var gl = ctx.createLinearGradient(ax, ay, w * 0.92, -h * 0.05); gl.addColorStop(0, 'rgba(255,245,200,.85)'); gl.addColorStop(1, 'rgba(255,245,200,0)'); ctx.strokeStyle = gl; ctx.lineWidth = 3 + 6 * p; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(OVM.lerp(ax, w * 0.92, 0.9), OVM.lerp(ay, -h * 0.05, 0.9)); ctx.stroke(); }
    var s = Math.max(0.55, h / 380) * (tt < 4.2 ? 0.45 + 0.55 * p : 1);
    if (brilho > 0.01) anjo(ctx, tt < 4.2 ? ax : tx - w * 0.05, tt < 4.2 ? ay : hy - h * 0.1, s, brilho, t);
    if (tt >= 4.15 && tt < 5.2) { ctx.fillStyle = 'rgba(255,255,255,' + Math.pow(1 - (tt - 4.15) / 1.05, 2) * 0.85 + ')'; ctx.fillRect(-20, -20, w + 40, h + 40); }
    ctx.restore();
    OVM.pilula(ctx, 'imaginação: a velocidade do anjo não está escrita', w / 2, h - 18, { px: 12, fundo: 'rgba(80,60,10,.92)', cor: '#FFE9B8', pad: 11 });
    if (tt > 4.4 && tt < 11) OVM.pilula(ctx, 'Mateus 28:2: houve um grande terremoto', w / 2, 24, { px: 12.5, pad: 10, alpha: OVM.clamp((tt - 4.4) / 0.6, 0, 1) });
    if (tt < 4) OVM.pilula(ctx, 'um anjo do Senhor, descendo do céu', w / 2, 24, { px: 12.5, pad: 10 });
  }
  function trovao(vol, km) {
    try {
      ac = ac || new (window.AudioContext || window.webkitAudioContext)(); if (ac.state === 'suspended') ac.resume();
      var dur = 3.6 + Math.min(2, km * 0.4), sr = ac.sampleRate, buf = ac.createBuffer(1, Math.floor(sr * dur), sr), d = buf.getChannelData(0), last = 0, j;
      for (j = 0; j < d.length; j++) { var tt = j / sr, wn = Math.random() * 2 - 1; last = (last + 0.03 * wn) / 1.03; d[j] = last * 4.2 * Math.min(1, tt / 0.06) * Math.exp(-tt / (0.9 + km * 0.12)) * (0.8 + 0.5 * Math.sin(tt * (22 + km * 3))); }
      var src = ac.createBufferSource(); src.buffer = buf; var lp = ac.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 220 + 900 / (1 + km); var gn = ac.createGain(); gn.gain.value = vol;
      src.connect(lp); lp.connect(gn); gn.connect(ac.destination); src.start();
    } catch (e) { /* sem áudio: tudo bem */ }
  }
  function modoRaio(ctx, w, h, t) {
    var hy = h * 0.78, xo = w * 0.12, t0 = raio.t0, dt = t0 < 0 ? -1 : OVM.t - t0, km = raio.km, fr = (km - 0.5) / 5.5, xb = w * 0.3 + fr * w * 0.58, esc = 1.1 - fr * 0.55, tsom = km / (D.somMs / 1000);
    var sh = dt >= tsom && dt < tsom + 0.9 ? (1 - (dt - tsom) / 0.9) * 4 : 0;
    ctx.save(); if (sh) ctx.translate((Math.random() - 0.5) * sh, (Math.random() - 0.5) * sh);
    ceu(ctx, w, h, hy);
    // nuvem de tempestade, longe
    ctx.fillStyle = 'rgba(40,48,80,.9)'; for (var c = 0; c < 9; c++) { ctx.beginPath(); ctx.ellipse(xb - w * 0.18 + c * w * 0.045, h * (0.14 + (c % 3) * 0.035), w * (0.07 + (c % 4) * 0.012) * esc, h * 0.085 * esc, 0, 0, PI2); ctx.fill(); }
    ctx.fillStyle = '#0A0D18'; ctx.beginPath(); ctx.moveTo(0, h); ctx.lineTo(0, hy); for (var x = 0; x <= w; x += 12) ctx.lineTo(x, hy - Math.sin(x / w * 5 + 1) * h * 0.01); ctx.lineTo(w, h); ctx.closePath(); ctx.fill();
    pessoa(ctx, xo, hy + 14, Math.max(0.7, h / 420));
    // marcas de distância no chão
    ctx.strokeStyle = 'rgba(255,255,255,.18)'; ctx.setLineDash([3, 6]); ctx.beginPath(); ctx.moveTo(xo, hy + 14); ctx.lineTo(xb, hy + 14); ctx.stroke(); ctx.setLineDash([]);
    OVM.pilula(ctx, F.n(km, 1) + ' km', (xo + xb) / 2, hy + 34, { px: 12, alpha: 0.9 });
    // o raio (aparece e pisca)
    if (dt >= 0 && dt < 0.5) {
      var on = dt < 0.1 || (dt > 0.17 && dt < 0.4); if (on) {
        ctx.strokeStyle = '#fff'; ctx.lineWidth = Math.max(1.5, 4 * esc); ctx.lineJoin = 'round'; ctx.shadowColor = 'rgba(190,210,255,1)'; ctx.shadowBlur = 24; ctx.beginPath();
        var yb = h * 0.2, bh = hy - yb; ctx.moveTo(xb, yb); for (var z = 1; z <= 12; z++) ctx.lineTo(xb + segmentos[z - 1] * w * 0.05 * esc, yb + bh * z / 12); ctx.stroke(); ctx.shadowBlur = 0;
        flash = dt < 0.1 ? 0.55 : 0.3;
      }
    }
    flash = OVM.seguir(flash, 0, 7, 0.016); if (flash > 0.01) { ctx.fillStyle = 'rgba(200,215,255,' + flash + ')'; ctx.fillRect(0, 0, w, h); }
    // a onda de som, andando devagar
    if (dt >= 0 && dt <= tsom + 0.4) {
      var rr = (xb - xo) * Math.min(1, dt / tsom); ctx.strokeStyle = 'rgba(255,214,120,.8)'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.ellipse(xb, hy + 14, rr, rr * 0.12, 0, 0, PI2); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,214,120,.3)'; ctx.beginPath(); ctx.ellipse(xb, hy + 14, rr * 0.85, rr * 0.1, 0, 0, PI2); ctx.stroke();
    }
    if (dt >= tsom && !raio.falou) { raio.falou = true; if (somOn) trovao(0.9 / (1 + km * 0.3), km); }
    ctx.restore();
    // placar: luz × som
    if (dt < 0) { OVM.pilula(ctx, 'Escolha a distância e toque em Relâmpago', w / 2, 24, { px: 13, pad: 11 }); }
    else {
      OVM.pilula(ctx, 'Luz: chegou na hora (o raio já foi visto)', w / 2, 24, { px: 13, pad: 11, fundo: 'rgba(40,90,60,.92)' });
      var falta = Math.max(0, tsom - dt);
      OVM.pilula(ctx, falta > 0 ? 'Som: faltam ' + F.n(falta, 1) + ' s' : 'Trovão! O som levou ' + F.n(tsom, 1) + ' s (' + F.n(km, 1) + ' km)', w / 2, 24 + 34, { px: 15, fundo: falta > 0 ? 'rgba(6,10,26,.82)' : 'rgba(242,217,160,.97)', cor: falta > 0 ? '#fff' : '#1F2A44', pad: 12 });
    }
    OVM.pilula(ctx, 'a cada 3 segundos de espera, o raio caiu a uns 1 km', w / 2, h - 16, { px: 11.5, alpha: 0.85 });
  }
  function quadro2(dt, t) {
    var w = T2.w, h = T2.h, ctx = T2.ctx; if (w < 10) return;
    OVM.fundoCanvas(T2);
    if (modo === 'raio') modoRaio(ctx, w, h, t); else modoAnjo(ctx, w, h, t);
  }
  OVM.anima(quadro2, c2);
  sKm.addEventListener('input', function () { raio.km = +sKm.value; oKm.textContent = F.n(raio.km, 1) + ' km'; OVM.preencher(sKm); });
  OVM.preencher(sKm);
  bRaio.addEventListener('click', function () { raio.t0 = OVM.t; raio.km = +sKm.value; raio.falou = false; });
  bSom.addEventListener('click', function () { somOn = !somOn; bSom.setAttribute('aria-pressed', somOn ? 'true' : 'false'); bSom.textContent = somOn ? '🔊 Som ligado' : '🔇 Som desligado'; if (somOn) { try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); ac.resume(); } catch (e) {} } });

  // ================================================================ 3) passos
  function cit(kk) { var v = V[kk]; return '<blockquote class="vers">“' + v.t + '”<cite>' + v.ref + '</cite></blockquote>'; }
  function vista(m, ctl) { modo = m; cena.setAttribute('data-modo', ctl); cena.classList.toggle('lab', m === 'anjo' || m === 'raio'); }
  function precoTag(on) { etq.style.opacity = on ? 1 : 0; }
  var passos = [
    { rotulo: 'Uma pergunta', ir: function () { vista('subida', 'subida'); presAlvo = 0; precoTag(false); nota.textContent = ''; cfg.aqui = 'Você está aqui'; usando = false; E.irS(s0, 2.5); },
      html: '<b class="grande">Onde fica o trono?</b><p>Se Deus é maior que tudo o que existe, <b>onde estaria o seu trono</b>?</p><p>A Bíblia diz só que é “nos céus”. Não diz em que lugar do universo.</p>' + cit('sl11') },
    { rotulo: 'Imagine subir', ir: function () { vista('subida', 'subida'); presAlvo = 0; precoTag(false); nota.textContent = ''; cfg.aqui = 'Você está aqui'; usando = false; E.irS(sFim, 26); },
      html: '<p>Imagine sair da Terra e <b>subir sem parar</b>, passando por cada degrau que vimos: a Lua, o Sistema Solar, as estrelas vizinhas, a galáxia, até o <b>limite do universo observável</b>.</p><p class="pequeno">É um vídeo: toque em <b>Subir</b>, ou arraste a distância. Na lateral, cada marco que você passa.</p>' },
    { rotulo: 'Além de qualquer alcance', ir: function () { vista('subida', 'subida'); presAlvo = 0; precoTag(true); nota.textContent = ''; cfg.aqui = 'Você está aqui'; usando = false; E.irS(sFim, 8); },
      html: '<p>Passamos de <b>93 bilhões de anos-luz</b> e ainda há um ponto de luz muito além. Se Deus é maior que tudo isto, o trono estaria <b>além de qualquer alcance humano</b>.</p><p>Se alguém pudesse ir até lá, seria <b>o maior preço</b> que um ser humano poderia pagar, e nenhum dinheiro compra essa viagem.</p><p class="pequeno"><span class="marca">imaginação</span> ninguém sabe onde fica; este ponto só ajuda a imaginar.</p>' },
    { rotulo: 'Mas ele também está aqui', ir: function () { vista('subida', 'subida'); presAlvo = 1; precoTag(false); cfg.aqui = 'Ele também está aqui'; usando = false; E.irS(sFim, 3); },
      html: '<p>Deus não está só lá: pelo <b>Espírito Santo</b> ele está <b>aqui</b>, sem demora e sem distância.</p>' + cit('sl139') + '<p class="pequeno">Jesus prometeu: “outro Consolador, para que fique convosco para sempre” (João 14:16).</p>' },
    { rotulo: 'E se ele quisesse vir?', ir: function () { vista('anjo', 'anjo'); presAlvo = 0; precoTag(false); nota.textContent = ''; },
      html: '<p>E se o próprio Deus quisesse enviar alguém? <b>Vai demorar?</b> Na ressurreição de Jesus, a Bíblia fala de um anjo que <b>desceu do céu</b>:</p>' + cit('mt28') + '<p class="pequeno">Ellen White: “' + V.dtn552.t + '”</p>' },
    { rotulo: 'Primeiro a luz, depois o som', ir: function () { vista('raio', 'raio'); presAlvo = 0; precoTag(false); },
      html: '<p>O anjo tinha o aspecto de um <b>relâmpago</b>. E num relâmpago acontece uma coisa curiosa: a gente vê a <b>luz primeiro</b> e ouve o <b>trovão depois</b>, porque a luz é muito mais rápida que o som.</p><p class="pequeno">Escolha a distância e toque em <b>Relâmpago</b>. Dá para ligar o som do trovão.</p>' },
    { rotulo: 'O que está escrito e o que é imaginação', ir: function () { vista('anjo', 'anjo'); },
      html: '<p><b>Está escrito:</b> o anjo desceu do céu, tinha o aspecto de um relâmpago, houve um grande terremoto. Gabriel “veio voando rapidamente” (Daniel 9:21).</p><p><span class="marca">imaginação</span> <b>A velocidade não está escrita.</b> Imagine que veio muito, muito rápido; a Bíblia não diz quanto.</p><p class="pequeno">Neste texto de Ellen White, os trovões acompanham a saída de Jesus do túmulo.</p>' },
    { rotulo: 'Longe e perto', ir: function () { vista('subida', 'subida'); presAlvo = 1; precoTag(false); cfg.aqui = 'Ele também está aqui'; usando = false; E.irS(sFim, 3); },
      html: '<p>O trono, <b>além de tudo</b>; o Espírito, <b>aqui</b>. Quem é tão grande, e ao mesmo tempo tão perto, também é grande <b>no que não dá para ver</b>.</p><p>Vamos olhar para dentro das coisas pequenas.</p>' }
  ];
  OVM.guia({ passos: passos });
});

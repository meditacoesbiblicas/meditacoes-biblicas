/* Parte 3: quanto a luz anda? Um carro a 100 km/h, a luz dando voltas na Terra, a régua do tempo (1 s … 1 ano) e o ano-luz. */
OVM.pronto(function () {
  var D = OVM_DADOS, F = OVM.fmt, PI2 = 6.2832, CL = D.c, AL = D.anoLuzKm;
  var canvas = OVM.$('#tela'), T = OVM.tela(canvas), est = OVM.estrelas(3, 240), cena = OVM.$('#cena');
  var slider = OVM.$('#p3-botao'), saida = OVM.$('#p3-saida'), chips = OVM.$$('#p3-chips .chip');
  var modo = 'estrada', am = { estrada: 1, voltas: 0, regua: 0, barras: 0 }, tAtivo = 0;
  var logT = 0, logTAlvo = 0, destaque = 0, rolagem = 0;
  var folhaTerra = document.createElement('canvas'); folhaTerra.width = folhaTerra.height = 1024; OVM.cosmos()[0].pintar(folhaTerra.getContext('2d'), OVM.rand(31));
  var REF = [{ km: D.terraCirc, t: 'volta na Terra' }, { km: D.luaKm, t: 'Lua' }, { km: D.uaKm, t: 'Sol' }, { km: 4.5e9, t: 'Netuno' }];
  var LMIN = 4.4, LMAX = 13.4;
  var CORES = ['#FFB86B', '#FFD27A', '#9DD6FF', '#B8A6FF', '#7FE0C0'];

  // ---------------------------------------------------------------- desenhos
  function carro(ctx, x, y, s, rot) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(0, 24, 66, 7, 0, 0, PI2); ctx.fill();
    ctx.fillStyle = '#E8563A'; OVM.caminhoArr(ctx, -64, -16, 128, 34, 12); ctx.fill();
    ctx.beginPath(); ctx.moveTo(-34, -16); ctx.lineTo(-20, -40); ctx.lineTo(24, -40); ctx.lineTo(42, -16); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#BFE6FF'; ctx.beginPath(); ctx.moveTo(-27, -19); ctx.lineTo(-16, -36); ctx.lineTo(-2, -36); ctx.lineTo(-2, -19); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(4, -19); ctx.lineTo(4, -36); ctx.lineTo(21, -36); ctx.lineTo(35, -19); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#FFE48A'; ctx.beginPath(); ctx.ellipse(62, -6, 4, 6, 0, 0, PI2); ctx.fill();
    ctx.fillStyle = '#C93C24'; ctx.fillRect(-64, 4, 128, 4);
    [-38, 38].forEach(function (wx) {
      ctx.save(); ctx.translate(wx, 14); ctx.fillStyle = '#23262F'; ctx.beginPath(); ctx.arc(0, 0, 15, 0, PI2); ctx.fill();
      ctx.rotate(rot); ctx.fillStyle = '#CDD2DC'; ctx.beginPath(); ctx.arc(0, 0, 8, 0, PI2); ctx.fill();
      ctx.strokeStyle = '#6D7486'; ctx.lineWidth = 2; for (var k = 0; k < 4; k++) { ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(k * 1.5708) * 8, Math.sin(k * 1.5708) * 8); ctx.stroke(); }
      ctx.restore();
    });
    ctx.restore();
  }

  function modoEstrada(ctx, w, h, t, dt, a) {
    var u = Math.min(w, h), tc = t % 5.2, p = Math.min(1, tc / 3.4), s = u / 330;
    ctx.globalAlpha = a;
    var g = ctx.createLinearGradient(0, 0, 0, h * 0.7); g.addColorStop(0, '#6BBEF3'); g.addColorStop(1, '#EAF7FF'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    OVM.brilho(ctx, w * 0.82, h * 0.2, u * 0.3, 'rgba(255,240,170,A)', 0.85); ctx.fillStyle = '#FFF2AE'; ctx.beginPath(); ctx.arc(w * 0.82, h * 0.2, u * 0.06, 0, PI2); ctx.fill();
    rolagem += dt * u * 0.75;
    function colinas(cor, base, amp, fr, vel, fase) { ctx.fillStyle = cor; ctx.beginPath(); ctx.moveTo(0, h); for (var x = 0; x <= w + 10; x += 10) ctx.lineTo(x, base - Math.sin((x + rolagem * vel) / (w * 0.22) * fr + fase) * amp - Math.sin((x + rolagem * vel) / (w * 0.09) + fase * 2) * amp * 0.35); ctx.lineTo(w, h); ctx.closePath(); ctx.fill(); }
    colinas('#9FD3A8', h * 0.56, h * 0.05, 1, 0.08, 1); colinas('#6FBE7E', h * 0.62, h * 0.04, 1.4, 0.25, 4);
    var yr0 = h * 0.66, yr1 = h * 0.84;
    ctx.fillStyle = '#58B06A'; ctx.fillRect(0, h * 0.62, w, yr0 - h * 0.62);
    ctx.fillStyle = '#464C5B'; ctx.fillRect(0, yr0, w, yr1 - yr0);
    ctx.fillStyle = '#E8ECF4'; ctx.fillRect(0, yr0, w, 3); ctx.fillRect(0, yr1 - 3, w, 3);
    var per = 64 * s * 1.6; ctx.fillStyle = '#F4D66A';
    for (var x = -per + (-rolagem % per); x < w + per; x += per) ctx.fillRect(x, (yr0 + yr1) / 2 - 2, per * 0.5, 4);
    ctx.fillStyle = '#4A9A5C'; ctx.fillRect(0, yr1, w, h - yr1);
    // árvores e placas
    for (var k = 0; k < 6; k++) { var tx = ((k * w / 5 - rolagem * 0.9) % (w * 1.2) + w * 1.2) % (w * 1.2) - w * 0.1; ctx.fillStyle = '#5B3C22'; ctx.fillRect(tx - 3 * s, yr0 - 22 * s, 6 * s, 22 * s); ctx.fillStyle = '#2F8A4B'; ctx.beginPath(); ctx.arc(tx, yr0 - 30 * s, 17 * s, 0, PI2); ctx.fill(); }
    // linhas de velocidade e o carro
    ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 2;
    for (k = 0; k < 5; k++) { var ly = yr0 + (yr1 - yr0) * (0.15 + k * 0.17), lx = ((k * 97 - rolagem * 3) % 160 + 160) % 160; ctx.beginPath(); ctx.moveTo(w * 0.1 + lx, ly); ctx.lineTo(w * 0.1 + lx + 34 * s, ly); ctx.stroke(); }
    carro(ctx, w * 0.34, (yr0 + yr1) / 2 + 6 * s, s * 1.25, rolagem / 9);
    // placar: tempo e distância
    var minutos = Math.round(60 * p), km = Math.round(100 * p), cheio = p >= 0.999;
    OVM.pilula(ctx, cheio ? '1 hora = 100 km' : 'Tempo: ' + minutos + ' min · Andou: ' + km + ' km', w / 2, h * 0.1, { px: cheio ? 17 : 14, fundo: cheio ? 'rgba(242,217,160,.96)' : 'rgba(6,10,26,.78)', cor: cheio ? '#1F2A44' : '#fff', alpha: a });
    OVM.pilula(ctx, '100 km/h', w / 2, h * 0.1 + 34, { px: 12.5, alpha: a * 0.9 });
    ctx.globalAlpha = 1;
  }

  function modoVoltas(ctx, w, h, t, dt, a) {
    var u = Math.min(w, h), cx = w / 2, cy = h * 0.5, R = u * 0.19, Rt = R * 1.6;
    ctx.globalAlpha = a;
    OVM.pintarEstrelas(ctx, w, h, est, t, { alpha: 0.85 * a });
    ctx.globalAlpha = a;
    var sz = 2 * R / 0.9; OVM.brilho(ctx, cx, cy, R * 1.5, 'rgba(110,175,255,A)', 0.3); ctx.drawImage(folhaTerra, cx - sz / 2, cy - sz / 2, sz, sz);
    ctx.strokeStyle = 'rgba(255,230,160,.28)'; ctx.lineWidth = 1.5; ctx.setLineDash([4, 7]); ctx.beginPath(); ctx.arc(cx, cy, Rt, 0, PI2); ctx.stroke(); ctx.setLineDash([]);
    var tc = t % 11, run = Math.min(1, tc / 8);
    var voltas = run * CL / D.terraCirc, ang = -Math.PI / 2 + voltas * PI2;
    for (var k = 0; k < 34; k++) {
      var f = 1 - k / 34; ctx.strokeStyle = 'rgba(255,236,170,' + (0.95 * f * f) + ')'; ctx.lineWidth = 1 + 4.5 * f; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.arc(cx, cy, Rt, ang - (k + 1) * 0.06, ang - k * 0.06); ctx.stroke();
    }
    var hx = cx + Math.cos(ang) * Rt, hy = cy + Math.sin(ang) * Rt; OVM.brilho(ctx, hx, hy, 24, 'rgba(255,240,190,A)', 0.95); ctx.fillStyle = '#FFFBE8'; ctx.beginPath(); ctx.arc(hx, hy, 4.5, 0, PI2); ctx.fill();
    var cheio = run >= 0.999;
    OVM.pilula(ctx, 'Tempo da luz: ' + F.n(run, 2) + ' s', w / 2, h * 0.09, { px: 14, alpha: a });
    OVM.pilula(ctx, cheio ? '7,5 voltas em 1 segundo' : 'Voltas na Terra: ' + F.n(voltas, 1), w / 2, h * 0.09 + 34, { px: cheio ? 16 : 14, fundo: cheio ? 'rgba(242,217,160,.96)' : 'rgba(6,10,26,.78)', cor: cheio ? '#1F2A44' : '#fff', alpha: a });
    OVM.pilula(ctx, 'câmera lenta: 1 segundo de luz passa em 8 segundos', w / 2, h * 0.93, { px: 11.5, alpha: a * 0.85 });
    OVM.pilula(ctx, 'No mesmo segundo, o carro andou 28 metros', w / 2, h * 0.93 - 27, { px: 11.5, alpha: a * 0.85, borda: 'rgba(255,184,107,.6)' });
    ctx.globalAlpha = 1;
  }

  function mapa(km, w, h, vert) {
    var f = (Math.log10(km) - LMIN) / (LMAX - LMIN);
    if (vert) { var yb = h - 26, yt = 78; return { x: Math.min(86, w * 0.22), y: yb - f * (yb - yt), f: f }; }
    var xl = 26, xr = w - 26; return { x: xl + f * (xr - xl), y: h * 0.6, f: f };
  }
  function rotuloDecada(e) { var n = Math.pow(10, e); return e < 6 ? F.n(n / 1000) + ' mil' : e < 9 ? F.grande(n) : e < 12 ? F.grande(n) : F.grande(n); }

  function modoRegua(ctx, w, h, t, dt, a) {
    var vert = w < 430 || w / h < 1.2;
    ctx.globalAlpha = a;
    OVM.pintarEstrelas(ctx, w, h, est, t, { alpha: 0.6 * a }); ctx.globalAlpha = a;
    logT = OVM.reduz ? logTAlvo : OVM.seguir(logT, logTAlvo, 4, dt);
    var km = CL * Math.pow(10, logT), q0 = mapa(Math.pow(10, LMIN), w, h, vert), q1 = mapa(Math.pow(10, LMAX), w, h, vert), qh = mapa(km, w, h, vert), e, q;
    // eixo
    var ag = vert ? ctx.createLinearGradient(0, q0.y, 0, q1.y) : ctx.createLinearGradient(q0.x, 0, q1.x, 0); ag.addColorStop(0, 'rgba(255,196,107,.9)'); ag.addColorStop(1, 'rgba(169,198,255,.9)');
    ctx.strokeStyle = 'rgba(255,255,255,.25)'; ctx.lineWidth = 2; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(q0.x, q0.y); ctx.lineTo(q1.x, q1.y); ctx.stroke();
    // o feixe: da origem até a distância
    ctx.strokeStyle = ag; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(q0.x, q0.y); ctx.lineTo(qh.x, qh.y); ctx.stroke();
    OVM.brilho(ctx, qh.x, qh.y, 26, 'rgba(255,240,190,A)', 0.95); ctx.fillStyle = '#FFFBE8'; ctx.beginPath(); ctx.arc(qh.x, qh.y, 6, 0, PI2); ctx.fill();
    // casas decimais (potências de 10)
    ctx.lineWidth = 1.6; ctx.strokeStyle = 'rgba(255,255,255,.55)';
    for (e = 5; e <= 13; e++) {
      q = mapa(Math.pow(10, e), w, h, vert);
      ctx.beginPath(); if (vert) { ctx.moveTo(q.x - 6, q.y); ctx.lineTo(q.x + 6, q.y); } else { ctx.moveTo(q.x, q.y - 6); ctx.lineTo(q.x, q.y + 6); } ctx.stroke();
      if (vert || (e % 2 === 1 || w > 640)) OVM.pilula(ctx, rotuloDecada(e) + ' km', vert ? q.x + 12 : q.x, vert ? q.y : q.y + 22, { px: 10.5, ancora: vert ? 'esq' : 'meio', alpha: 0.85, pad: 6 });
    }
    // marcos conhecidos (para sentir os números)
    REF.forEach(function (r, i) {
      q = mapa(r.km, w, h, vert); ctx.fillStyle = CORES[i + 1]; ctx.beginPath(); ctx.arc(q.x, q.y, 3.4, 0, PI2); ctx.fill();
      OVM.pilula(ctx, r.t, vert ? q.x - 10 : q.x, vert ? q.y : q.y - 20 - (i % 2) * 22, { px: 10.5, ancora: vert ? 'dir' : 'meio', cor: CORES[i + 1], alpha: 0.95, pad: 6 });
    });
    // marca do "ano-luz" quando em destaque
    if (destaque > 0.02) {
      var qa = mapa(AL, w, h, vert), g = ctx.globalAlpha; ctx.globalAlpha = g * destaque;
      ctx.strokeStyle = '#FFD878'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.arc(qa.x, qa.y, 16, 0, PI2); ctx.stroke();
      OVM.pilula(ctx, '1 ano-luz', vert ? qa.x + 24 : qa.x, vert ? qa.y : qa.y - 40, { px: 15, ancora: vert ? 'esq' : 'meio', fundo: 'rgba(242,217,160,.97)', cor: '#1F2A44', alpha: 1 });
      ctx.globalAlpha = g;
    }
    // leitura
    var tt = Math.pow(10, logT), nome = tt < 1.5 ? '1 segundo' : tt < 59.5 ? F.n(tt, 0) + ' segundos' : F.tempo(tt);
    OVM.pilula(ctx, 'Em ' + nome + ' a luz anda', vert ? w / 2 : 14 + 0, 26, { px: 13, ancora: vert ? 'meio' : 'esq', alpha: a });
    OVM.pilula(ctx, F.distKm(km), vert ? w / 2 : 14, 26 + 34, { px: 18, ancora: vert ? 'meio' : 'esq', fundo: 'rgba(242,217,160,.96)', cor: '#1F2A44', alpha: a });
    ctx.globalAlpha = 1;
  }

  function modoBarras(ctx, w, h, t, dt, a) {
    ctx.globalAlpha = a;
    OVM.pintarEstrelas(ctx, w, h, est, t, { alpha: 0.5 * a }); ctx.globalAlpha = a;
    var vs = D.velocidades, n = vs.length, top = 64, base = h - 24, hh = (base - top) / n, tm = t - tAtivo, x0 = 20, x1 = w - 20;
    OVM.pilula(ctx, 'Tempo para andar 1 ano-luz', w / 2, 26, { px: 14, alpha: a });
    for (var i = 0; i < n; i++) {
      var v = vs[i], anos = AL / v.kms / D.anoS, fr = (Math.log10(anos) + 0.7) / 9.7, ba = OVM.suave((tm - i * 0.38) / 1.1);
      var y = top + i * hh + hh * 0.5, bh = Math.min(26, hh * 0.46), len = (x1 - x0) * fr * ba;
      ctx.fillStyle = 'rgba(255,255,255,.08)'; OVM.caminhoArr(ctx, x0, y - bh / 2, x1 - x0, bh, bh / 2); ctx.fill();
      var gg = ctx.createLinearGradient(x0, 0, x1, 0); gg.addColorStop(0, CORES[i]); gg.addColorStop(1, CORES[i]);
      ctx.fillStyle = CORES[i]; OVM.caminhoArr(ctx, x0, y - bh / 2, Math.max(bh, len), bh, bh / 2); ctx.fill();
      var valor = v.id === 'luz' ? '1 ano' : (anos < 1e6 ? F.n(Math.round(anos / 100) * 100) + ' anos' : F.grande(anos) + ' de anos');
      OVM.pilula(ctx, v.nome, x0, y - bh / 2 - 11, { px: 11.5, ancora: 'esq', alpha: a * ba, pad: 7 });
      OVM.pilula(ctx, valor, Math.min(x1, x0 + Math.max(bh, len) + 8), y, { px: 12.5, ancora: 'esq', alpha: a * ba, fundo: 'rgba(6,10,26,.82)', pad: 8, cor: v.id === 'luz' ? '#FFE9B8' : '#fff' });
    }
    ctx.globalAlpha = 1;
  }

  function quadro(dt, t) {
    var w = T.w, h = T.h, ctx = T.ctx;
    OVM.fundoCanvas(T);
    var g = ctx.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#04071A'); g.addColorStop(1, '#0B1230'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    ['estrada', 'voltas', 'regua', 'barras'].forEach(function (k) { am[k] = OVM.reduz ? (k === modo ? 1 : 0) : OVM.seguir(am[k], k === modo ? 1 : 0, 6, dt); });
    destaque = OVM.seguir(destaque, destaqueAlvo, 5, dt);
    if (am.estrada > 0.01) modoEstrada(ctx, w, h, t, dt, am.estrada);
    if (am.voltas > 0.01) modoVoltas(ctx, w, h, t, dt, am.voltas);
    if (am.regua > 0.01) modoRegua(ctx, w, h, t, dt, am.regua);
    if (am.barras > 0.01) modoBarras(ctx, w, h, t, dt, am.barras);
  }
  var destaqueAlvo = 0;
  OVM.anima(quadro, canvas);
  quadro(0.016, 0.5);

  // ---------------------------------------------------------------- textos e controles
  function equiv(km) {
    var x;
    if (km < 1e6) { x = km / D.terraCirc; return '≈ ' + F.n(x, 1) + ' voltas na Terra'; }
    if (km < 1e8) { x = km / D.luaKm; return '≈ ' + F.n(x, 0) + ' vezes a distância até a Lua'; }
    if (km < 5e9) { x = km / D.uaKm; return '≈ ' + F.n(x, 1) + ' vezes a distância da Terra ao Sol'; }
    x = km / 4.5e9; return '≈ ' + F.grande(Math.round(x)) + ' vezes a distância até Netuno';
  }
  function leitura() {
    var tt = Math.pow(10, logTAlvo), km = CL * tt, el = OVM.$('#p3-leit'), eq = OVM.$('#p3-eq');
    var nome = tt < 1.5 ? '1 segundo' : tt < 59.5 ? F.n(tt, 0) + ' segundos' : F.tempo(tt);
    saida.textContent = nome;
    if (el) el.innerHTML = 'Em <b>' + nome + '</b>, a luz anda <b>' + F.distKm(km) + '</b>';
    if (eq) eq.textContent = equiv(km);
    chips.forEach(function (c) { c.classList.toggle('ativo', Math.abs(+c.getAttribute('data-v') - Math.round(logTAlvo * 100)) < 4); });
  }
  function definirT(v100) { logTAlvo = OVM.clamp(v100 / 100, 0, 7.5); slider.value = Math.round(logTAlvo * 100); OVM.preencher(slider); leitura(); }
  function irModo(m, ctrl) { modo = m; tAtivo = OVM.t; cena.setAttribute('data-modo', ctrl || m); }

  var passos = [
    { rotulo: 'Quanto anda um carro?', ir: function () { destaqueAlvo = 0; irModo('estrada'); },
      html: '<b class="grande">100 km por hora</b><p>Um carro a 100 km/h anda <b>100 km em 1 hora</b>. Para dar a volta na Terra (40.075 km), seriam <b>quase 17 dias</b> sem parar.</p><p class="pequeno">Guarde essa medida: <b>100 km/h</b>.</p>' },
    { rotulo: 'E a luz?', ir: function () { destaqueAlvo = 0; irModo('voltas'); },
      html: '<b class="grande">300 mil km por segundo</b><p>A luz anda cerca de <b>300 mil km em 1 segundo</b> (299.792 km). Em <b>1 segundo</b> ela dá <b>7,5 voltas</b> na Terra.</p><p>Nesse mesmo segundo o carro andou <b>28 metros</b>. A luz é <b>10,8 milhões de vezes</b> mais rápida.</p>' },
    { rotulo: 'A régua do tempo da luz', ir: function () { destaqueAlvo = 0; irModo('regua', 'regua'); definirT(+slider.value); },
      html: '<p>Arraste o botão e veja <b>quanto a luz anda</b> em cada tempo, de 1 segundo a 1 ano.</p><p class="p3-leit" id="p3-leit"></p><p class="p3-eq" id="p3-eq"></p>' },
    { rotulo: 'O ano-luz', ir: function () { destaqueAlvo = 1; irModo('regua', 'ano'); logTAlvo = 7.499; slider.value = 750; OVM.preencher(slider); },
      html: '<b class="grande">Ano-luz é distância</b><p>Se a luz anda sem parar por <b>1 ano</b>, ela percorre cerca de <b>9,46 trilhões de km</b>. Essa distância é <b>1 ano-luz</b>.</p><p class="pequeno">Não é tempo nem velocidade: é <b>distância</b>.</p>' },
    { rotulo: 'Quanto tempo para andar 1 ano-luz?', ir: function () { destaqueAlvo = 0; irModo('barras'); },
      html: '<p>A luz leva <b>1 ano</b>. Um avião a jato levaria <b>1,2 milhão de anos</b>; um carro, <b>10,8 milhões</b>; uma pessoa andando, <b>216 milhões</b>.</p><p>Até a sonda <b>Voyager 1</b>, a mais distante que o ser humano já mandou, levaria uns <b>17,6 mil anos</b>.</p>' },
    { rotulo: 'Agora temos uma régua', ir: function () { destaqueAlvo = 1; irModo('regua', 'ano'); },
      html: '<p>Perto, bastam <b>segundos</b> e <b>minutos</b> de luz. Longe, é preciso o <b>ano-luz</b>.</p><p>Com essa régua no bolso, dá para olhar o céu e perguntar: <b>o que está perto e o que está longe?</b></p>' }
  ];
  var g = OVM.guia({ passos: passos });
  slider.addEventListener('input', function () { definirT(+slider.value); });
  chips.forEach(function (c) { c.addEventListener('click', function () { definirT(+c.getAttribute('data-v')); }); });
});

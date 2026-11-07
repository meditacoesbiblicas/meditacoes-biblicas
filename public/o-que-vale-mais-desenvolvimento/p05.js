/* Parte 5: a escada do universo. A câmera se afasta degrau por degrau (Terra → Lua → Sistema Solar → … → universo observável); no topo, "e além disso?". */
OVM.pronto(function () {
  var D = OVM_DADOS, F = OVM.fmt, AL = D.anoLuzKm, PI2 = 6.2832;
  var niveis = OVM.cosmos(), n = niveis.length, CURTOS = ['Terra', 'Terra e Lua', 'Sistema Solar', 'Vizinhança', 'Via Láctea', 'Grupo Local', 'Laniakea', 'Universo'];
  var nomeEl = OVM.$('#hud-nome'), tamEl = OVM.$('#hud-tam'), pcEl = OVM.$('#hud-pc'), escada = OVM.$('#p5-escada'), alemEl = OVM.$('#p5-alem');
  var alem = 0, alemAlvo = 0, ultimo = -1, sd = OVM.rand(5), pergs = [], i;
  for (i = 0; i < 24; i++) pergs.push({ a: sd() * PI2, r: 0.26 + sd() * 0.62, f: sd() * 6, s: 12 + sd() * 16 });

  function atualizaHud(k) {
    var nv = niveis[k], km = nv.d * AL;
    nomeEl.textContent = nv.nome;
    tamEl.textContent = 'cerca de ' + F.distKm(km) + ' de lado a lado';
    pcEl.textContent = km >= AL ? F.parsecKm(km) + ' (parsecs)' : '';
  }
  function aoQuadro(E, dt, t) {
    var ctx = E.T.ctx, w = E.T.w, h = E.T.h, L = Math.min(w, h) * 0.94, k = E.perto(), j;
    alem = OVM.seguir(alem, alemAlvo, 3, dt);
    if (k !== ultimo) { ultimo = k; atualizaHud(k); }
    if (alem > 0.02) {
      var ru = E.px(n - 1) / 2, cx = w / 2, cy = h / 2;
      ctx.save(); ctx.lineWidth = 1.6;
      for (j = 0; j < 3; j++) { var f = ((OVM.reduz ? 0.3 : t * 0.12) + j / 3) % 1; ctx.strokeStyle = 'rgba(170,195,255,' + ((1 - f) * 0.4 * alem) + ')'; ctx.beginPath(); ctx.arc(cx, cy, ru * (1.02 + f * 1.5), 0, PI2); ctx.stroke(); }
      ctx.fillStyle = '#C9D4F2'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      for (j = 0; j < pergs.length; j++) {
        var q = pergs[j]; ctx.globalAlpha = alem * (0.1 + 0.2 * (0.5 + 0.5 * Math.sin(t * 0.9 + q.f)));
        ctx.font = OVM.fonte(q.s * (L / 400), 500, true); ctx.fillText('?', cx + Math.cos(q.a) * (ru + L * q.r * 0.55), cy + Math.sin(q.a) * (ru + L * q.r * 0.55));
      }
      ctx.restore();
    }
  }
  var E = OVM.Escala({ canvas: OVM.$('#tela'), niveis: niveis, aqui: 'Você está aqui', folga: 1.3, barra: function (len) { return F.distKm(len * AL); }, aoQuadro: aoQuadro, semente: 31 });

  // a escada (degraus clicáveis)
  var rungs = [];
  niveis.forEach(function (nv, i) {
    var li = document.createElement('li'); li.innerHTML = '<button type="button" aria-label="' + nv.nome + '"><span class="nome">' + CURTOS[i] + '</span><span class="bola"></span></button>';
    li.firstChild.addEventListener('click', function () { g.ir(i); }); escada.appendChild(li); rungs.push(li);
  });
  var top = document.createElement('li'); top.className = 'alem'; top.innerHTML = '<span class="nome">e além?</span><span class="bola">?</span>'; escada.appendChild(top); rungs.push(top);
  function marca(i) { rungs.forEach(function (li, k) { li.classList.toggle('ativo', k === i); li.classList.toggle('passou', k < i); }); }

  var TXT = [
    '<b class="grande">A Terra</b><p>Nosso ponto de partida: <b>você está aqui</b>. São <b>12.742 km</b> de ponta a ponta.</p><p class="pequeno">Cada toque em <b>Próximo</b> afasta a câmera um degrau. Ou toque nos degraus da escada.</p>',
    '<b class="grande">A Terra e a Lua</b><p>A Lua está a <b>384.400 km</b>: a luz leva <b>1,3 s</b> para chegar lá; uma nave com gente leva uns <b>3 dias</b>.</p><p class="pequeno">Na imagem, a Terra e a Lua estão maiores que o real, para dar para ver.</p>',
    '<b class="grande">O Sistema Solar</b><p>O Sol e os oito planetas cabem num círculo de uns <b>9 bilhões de km</b>. Do Sol a Netuno, a luz leva <b>cerca de 4 horas</b>.</p><p class="pequeno">As órbitas estão na escala certa; os planetas foram desenhados maiores.</p>',
    '<b class="grande">A vizinhança do Sol</b><p>Daqui em diante o quilômetro não serve mais: usamos o <b>ano-luz</b>. A estrela mais próxima, <b>Próxima do Centauro</b>, está a <b>4,2 anos-luz</b>; Sírio, a 8,6.</p><p class="pequeno">Num raio de 10 anos-luz há poucas estrelas, quase todas pequenas e fracas.</p>',
    '<b class="grande">A Via Láctea</b><p>Nossa galáxia tem uns <b>100 mil anos-luz</b> de diâmetro e <b>centenas de bilhões de estrelas</b>. O Sol está a uns <b>26 mil anos-luz</b> do centro.</p><p class="pequeno">Desenho artístico: ninguém nunca viu a galáxia de fora.</p>',
    '<b class="grande">O Grupo Local</b><p>Cerca de <b>10 milhões de anos-luz</b>. A Via Láctea e a vizinha <b>Andrômeda</b> (a 2,5 milhões de anos-luz) lideram dezenas de galáxias menores.</p>',
    '<b class="grande">O superaglomerado Laniakea</b><p>Cerca de <b>520 milhões de anos-luz</b>, com uns <b>100 mil</b> grandes galáxias, ligadas por filamentos que escorrem para um mesmo ponto central.</p><p class="pequeno">Laniakea quer dizer "céu imenso", em havaiano.</p>',
    '<b class="grande">O universo observável</b><p>Cerca de <b>93 bilhões de anos-luz</b> de lado a lado, com <b>centenas de bilhões, talvez trilhões</b>, de galáxias.</p><p class="pequeno">Até aqui chega o que a luz já pôde nos contar.</p>'
  ];
  var passos = niveis.map(function (nv, i) {
    return { rotulo: 'Degrau ' + (i + 1) + ' de ' + n, html: TXT[i], ir: function () { alemAlvo = 0; alemEl.classList.remove('on'); marca(i); E.ir(i); } };
  });
  passos.push({
    rotulo: 'No topo da escada',
    html: '<b class="grande">E além disso?</b><p>Ninguém sabe. O universo é <b>observável</b> só até certo ponto, e ele <b>se expande</b>: as galáxias se afastam umas das outras.</p><p class="pequeno">Para medir distâncias assim, os cientistas usam também o <b>parsec</b>: veja a caixa logo abaixo.</p>',
    ir: function () { alemAlvo = 1; alemEl.classList.add('on'); marca(n); E.irS(E.sDe(n - 1) + 0.5, 2.6); }
  });
  var g = OVM.guia({ passos: passos });

  // ---------------------------------------------------------------- caixa opcional: paralaxe e parsec
  (function () {
    var cv = OVM.$('#par-tela'); if (!cv) return;
    var T = OVM.tela(cv), mes = OVM.$('#par-mes'), saida = OVM.$('#par-saida'), cps = OVM.$$('#par-chips .chip'), perto = true, m = 0, fundo = OVM.estrelas(77, 46);
    function proj(ex, ey, sx, sy, yb) { return ex + (sx - ex) * (ey - yb) / (ey - sy); }
    function desenhar(dt, t) {
      var w = T.w, h = T.h, ctx = T.ctx; if (w < 10) return;
      OVM.fundoCanvas(T); ctx.fillStyle = '#070C1E'; ctx.fillRect(0, 0, w, h);
      var wl = Math.floor(w * 0.54), cx = wl / 2, cy = h * 0.66, ro = Math.min(wl * 0.36, h * 0.24), yb = 22, th = Math.PI + m / 12 * PI2;
      var ex = cx + Math.cos(th) * ro, ey = cy + Math.sin(th) * ro, kk = perto ? 2.6 : 5.4, sx = cx, sy = cy - ro * kk;
      // painel da esquerda: vista de cima
      ctx.strokeStyle = 'rgba(255,255,255,.14)'; ctx.setLineDash([3, 5]); ctx.beginPath(); ctx.arc(cx, cy, ro, 0, PI2); ctx.stroke(); ctx.setLineDash([]);
      ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.beginPath(); ctx.moveTo(8, yb); ctx.lineTo(wl - 8, yb); ctx.stroke();
      for (var i = 0; i < fundo.length; i++) { var e = fundo[i]; ctx.globalAlpha = 0.5 * e.b; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(8 + e.x * (wl - 16), yb - 6 + e.y * 5, e.r * 0.9, 0, PI2); ctx.fill(); }
      ctx.globalAlpha = 1;
      OVM.brilho(ctx, cx, cy, 20, 'rgba(255,205,90,A)', 0.9); ctx.fillStyle = '#FFE08A'; ctx.beginPath(); ctx.arc(cx, cy, 5, 0, PI2); ctx.fill();
      var xp = proj(ex, ey, sx, sy, yb);
      ctx.strokeStyle = 'rgba(255,225,150,.6)'; ctx.setLineDash([4, 5]); ctx.beginPath(); ctx.moveTo(ex, ey); ctx.lineTo(xp, yb); ctx.stroke(); ctx.setLineDash([]);
      OVM.brilho(ctx, sx, sy, 16, 'rgba(160,200,255,A)', 0.8); ctx.fillStyle = '#DDEBFF'; ctx.beginPath(); ctx.arc(sx, sy, 5, 0, PI2); ctx.fill();
      OVM.brilho(ctx, ex, ey, 14, 'rgba(110,175,255,A)', 0.8); ctx.fillStyle = '#5CA8FF'; ctx.beginPath(); ctx.arc(ex, ey, 5, 0, PI2); ctx.fill();
      OVM.pilula(ctx, 'Sol', cx, cy + 16, { px: 10.5, pad: 6 }); OVM.pilula(ctx, 'Terra', ex + (Math.cos(th) < 0 ? -26 : 26), ey + 4, { px: 10.5, pad: 6 }); OVM.pilula(ctx, 'estrela próxima', sx + 8, sy - 14, { px: 10.5, pad: 6, ancora: 'esq' });
      OVM.pilula(ctx, 'estrelas muito distantes', cx, yb + 15, { px: 10.5, pad: 6, alpha: 0.9 });
      // painel da direita: o que se vê no céu
      var xl = wl + 16, xr = w - 10, xc = (xl + xr) / 2, wr = xr - xl;
      ctx.strokeStyle = 'rgba(255,255,255,.25)'; OVM.caminhoArr(ctx, xl, h * 0.2, wr, h * 0.5, 10); ctx.stroke();
      for (i = 0; i < fundo.length; i++) { e = fundo[i]; ctx.globalAlpha = 0.6 * e.b; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(xl + 6 + e.x * (wr - 12), h * 0.2 + 6 + e.y * (h * 0.5 - 12), e.r * 1.1, 0, PI2); ctx.fill(); }
      ctx.globalAlpha = 1;
      var pa = proj(cx - ro, cy, cx, cy - ro * 2.6, yb), pb = proj(cx + ro, cy, cx, cy - ro * 2.6, yb), esc = (wr * 0.34) / (Math.abs(pb - pa) / 2), vx = xc + (xp - cx) * esc, vy = h * 0.45;
      var g0 = xc + (proj(cx - ro, cy, sx, sy, yb) - cx) * esc, g1 = xc + (proj(cx + ro, cy, sx, sy, yb) - cx) * esc;
      ctx.strokeStyle = 'rgba(221,235,255,.35)'; ctx.setLineDash([3, 4]); [g0, g1].forEach(function (gx) { ctx.beginPath(); ctx.arc(gx, vy, 7, 0, PI2); ctx.stroke(); }); ctx.setLineDash([]);
      OVM.brilho(ctx, vx, vy, 18, 'rgba(160,200,255,A)', 0.9); ctx.fillStyle = '#EAF2FF'; ctx.beginPath(); ctx.arc(vx, vy, 5.5, 0, PI2); ctx.fill();
      OVM.pilula(ctx, 'o que você vê no céu', xc, h * 0.2 - 12, { px: 11, pad: 7 });
      OVM.pilula(ctx, perto ? 'perto: muda bastante' : 'longe: muda pouco', xc, h * 0.7 + 18, { px: 11, pad: 7, fundo: 'rgba(242,217,160,.95)', cor: '#1F2A44' });
    }
    OVM.anima(desenhar, cv);
    function atualiza() { m = +mes.value / 10; saida.textContent = F.n(m, 1) + ' meses'; OVM.preencher(mes); }
    mes.addEventListener('input', atualiza); atualiza();
    cps.forEach(function (c) { c.addEventListener('click', function () { perto = c.getAttribute('data-k') === 'perto'; cps.forEach(function (o) { o.classList.toggle('ativo', o === c); }); }); });
  })();
});

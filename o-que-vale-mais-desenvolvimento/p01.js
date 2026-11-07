/* Parte 1: o botão do retorno. Seis vinhetas animadas; mexer no botão sobe o retorno e o preço juntos. */
OVM.pronto(function () {
  var P = OVM_DADOS.precos;
  var figs = OVM.$$('.vig'), box = OVM.$('#p1-vinhetas'), etq = OVM.$('#p1-etq'), valor = OVM.$('#p1-valor'), aprox = OVM.$('#p1-aprox'),
    nome = OVM.$('#p1-nome'), fioP = OVM.$('#p1-fio-preco'), fioR = OVM.$('#p1-fio-ret'), cena = OVM.$('#p1'),
    slider = OVM.$('#p1-botao'), saida = OVM.$('#p1-saida'), chips = OVM.$$('#p1-chips .chip');
  var ultimo = 0;

  function mostrar(i) {
    var p = P[i];
    box.classList.remove('mosaico');
    figs.forEach(function (f, k) { f.classList.toggle('on', k === i); });
    nome.textContent = p.nome;
    saida.textContent = p.nome;
    aprox.hidden = !p.aprox;
    OVM.contar(valor, ultimo, p.valor, p.texto, 1000);
    ultimo = p.valor;
    fioP.style.height = (OVM.clamp(Math.log10(p.valor) / 6, 0, 1) * 100) + '%';
    fioR.style.height = ((i + 1) / 6 * 100) + '%';
    cena.style.setProperty('--ret', (i + 1) / 6);
    etq.classList.remove('balanca'); void etq.offsetWidth; etq.classList.add('balanca');
    slider.disabled = false;
    slider.value = i; OVM.preencher(slider);
    chips.forEach(function (c, k) { c.classList.toggle('ativo', k === i); c.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
  }

  function resumo() {
    box.classList.add('mosaico');
    figs.forEach(function (f) { f.classList.add('on'); });
    fioP.style.height = '100%'; fioR.style.height = '100%';
    cena.style.setProperty('--ret', 1);
    slider.value = 5; OVM.preencher(slider);
    chips.forEach(function (c) { c.classList.remove('ativo'); c.setAttribute('aria-pressed', 'false'); });
  }

  function htmlItem(p) {
    return '<b class="grande">' + p.nome + '</b>' +
      '<p class="p1-linha"><span class="p1-preco">' + (p.aprox ? '<small>≈ </small>' : '') + '<small>R$ </small>' + p.texto + '</span>' +
      (p.cafes ? '<span class="p1-cafes" title="Quantas xícaras de chocolate quente, a R$ 8 cada, dá para comprar com esse valor">🍫 ' + p.cafes + '</span>' : '') + '</p>' +
      '<p class="p1-imagine">' + p.imagine + '</p>' +
      '<p class="p1-qual"><b>Dura:</b> ' + p.dura + ' · <b>Para:</b> ' + p.para + '</p>' +
      '<details class="conta"><summary>Conta e fonte</summary><p><b>' + p.nota + '</b></p><p>' + p.conta + '</p></details>';
  }

  var passos = P.map(function (p, i) {
    return { rotulo: 'O retorno · nível ' + (i + 1) + ' de 6', html: function () { return htmlItem(p); }, ir: function () { mostrar(i); } };
  });
  passos.push({
    rotulo: 'O que os seis têm em comum',
    html: '<p>Cada um entrega algo bom, e todos cobram um preço.</p>' +
      '<p>Do chocolate quente à casa, o preço subiu de cerca de <b>R$ 8</b> para cerca de <b>R$ 542 mil</b>: mais de <b>67 mil vezes</b>.</p>' +
      '<p><b>O que vale mais custa mais.</b> Para receber, é preciso pagar.</p>',
    ir: resumo
  });
  var g = OVM.guia({ passos: passos });

  slider.addEventListener('input', function () { OVM.preencher(slider); g.ir(+slider.value); });
  chips.forEach(function (c) { c.addEventListener('click', function () { g.ir(+c.getAttribute('data-i')); }); });
});

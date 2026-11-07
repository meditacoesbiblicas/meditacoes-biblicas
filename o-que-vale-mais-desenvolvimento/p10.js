/* Parte 10: a resposta. A etiqueta coberta no meio da vitrine de preços; ao virar, mostra "Jesus" e todos os outros preços encolhem.
   Depois: a mão que sustenta os mundos, nem prata nem ouro, duas conclusões equilibradas (valor imenso; pecado grave) e "recebido, não comprado". */
OVM.pronto(function () {
  var V = OVM_V, cena = OVM.$('#cena'), btn = OVM.$('#p10-virar'), chips = OVM.$$('#p10-duas .chip'), duas = 'valor', g;
  var F = OVM.Final(OVM.$('#tela'), { interativo: true, aoRevelar: function () { if (g && g.atual === 0) g.ir(1); } });
  function cit(k) { var v = V[k]; return '<blockquote class="vers">“' + v.t + '”<cite>' + v.ref + '</cite></blockquote>'; }
  function vai(modo, extra, virada) { cena.setAttribute('data-modo', modo); F.definirExtra(extra); if (virada) F.revelar(); else F.desvirar(); }
  var passos = [
    { rotulo: 'Falta uma etiqueta', ir: function () { vai('virar', '', false); },
      html: '<b class="grande">Falta uma etiqueta</b><p>Tudo o que vimos tem um preço. Mas há uma etiqueta que você ainda não consegue ler.</p><p><b>Toque nela para virar.</b></p>' },
    { rotulo: 'A resposta', ir: function () { vai('nada', '', true); },
      html: '<b class="grande">Jesus</b><p>Deus está acima de qualquer preço. Mesmo assim, <b>entregou o seu Filho</b>, que também é Deus, por você.</p>' + cit('jo316') + cit('rm58') + '<p class="pequeno">Repare: ao virar a etiqueta, todos os outros preços ficaram pequenos.</p>' },
    { rotulo: 'A mão que sustenta os mundos', ir: function () { vai('nada', 'cruz', true); },
      html: '<p>Aquele que <b>sustenta os mundos</b>, do núcleo do átomo ao limite do universo, foi quem se entregou por você.</p>' + cit('ed132') + '<p class="pequeno">“Sendo em forma de Deus… humilhou-se a si mesmo, sendo obediente até à morte e morte de cruz” (Filipenses 2:6-8).</p>' },
    { rotulo: 'Nem prata nem ouro', ir: function () { vai('nada', 'moedas', true); },
      html: cit('pe118') + '<p>O mundo avaliou Jesus em <b>30 moedas de prata</b> (Mateus 26:15). Deus o entregou pelo <b>maior valor que existe</b>: por você.</p><p class="pequeno">“Fostes comprados por bom preço” (1 Coríntios 6:20).</p>' },
    { rotulo: 'Duas conclusões', ir: function () { vai('duas', duas, true); chips.forEach(function (c) { c.classList.toggle('ativo', c.getAttribute('data-k') === duas); }); },
      html: function () {
        return duas === 'valor'
          ? '<b class="grande">Você tem valor imenso</b><p>Esse valor <b>não vem de nada que você fez ou tem</b>: vem de quem pagou por você.</p>' + cit('is43') + '<p class="pequeno">“Vede quão grande amor nos tem concedido o Pai” (1 João 3:1).</p>'
          : '<b class="grande">O pecado é grave</b><p>Só um preço tão alto pôde nos libertar dele. <b>Temer é reverência</b>: cuidado de não pecar contra quem pagou, e não medo de ser rejeitado.</p>' + cit('rm623') + '<p class="pequeno">“Mas contigo está o perdão, para que sejas temido” (Salmo 130:4).</p>';
      } },
    { rotulo: 'Recebido, não comprado', ir: function () { vai('nada', 'presente', true); },
      html: '<b class="grande">Recebido, não comprado</b><p>Existe uma única coisa que recebemos <b>sem pagar</b>, porque alguém pagou por nós.</p>' + cit('ef28') + '<p class="pequeno">“Vinde e comprai, sem dinheiro e sem preço” (Isaías 55:1).</p>' }
  ];
  g = OVM.guia({ passos: passos });
  btn.addEventListener('click', function () { F.revelar(); });
  chips.forEach(function (c) { c.addEventListener('click', function () { duas = c.getAttribute('data-k'); g.ir(4); }); });
});

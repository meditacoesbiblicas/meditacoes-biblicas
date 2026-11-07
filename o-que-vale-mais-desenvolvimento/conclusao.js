/* Conclusão: a imagem final (a etiqueta virada no meio de todos os preços) e o botão de compartilhar. */
OVM.pronto(function () {
  OVM.Final(OVM.$('#tela'), { revelada: true, interativo: false });
  var b = OVM.$('#compartilhar');
  if (b) b.addEventListener('click', function () {
    var url = location.href.split('conclusao.html')[0];
    if (navigator.share) navigator.share({ title: 'O que vale mais?', url: url }).catch(function () {});
    else if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { b.textContent = 'Link copiado ✓'; }).catch(function () {});
  });
});

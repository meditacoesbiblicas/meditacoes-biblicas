# -*- coding: utf-8 -*-
# Gera as páginas do estudo "Quanto custa?" (capa + um arquivo por ato).
# Uso: python3 scripts/quanto-custa/build.py <pasta-de-saída> [--rascunho]
#
# Regras do estudo (combinadas com o dono do site):
#  - nada nas páginas (título, capa, meta, navegação) pode adiantar o que vem nos atos seguintes;
#  - um ato por vez, só avança com a confirmação do dono;
#  - preços e fatos só entram como texto final depois de conferidos (ver ITENS: valor None = "a confirmar").
# A ilustração do Ato 1 (vitrine.jpg) foi gerada no Gemini; as áreas clicáveis estão medidas em areas_ato1.py.
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), 'estudo'))
sys.path.insert(0, AQUI)
from rascunho import gravar  # noqa: E402
import areas_ato1 as A  # noqa: E402

PASTA = 'quanto-custa'          # pasta da versão publicada (ainda não existe); a de desenvolvimento é PASTA + '-desenvolvimento'
DEST = sys.argv[1]
RASC = '--rascunho' in sys.argv
PROXIMO = None                  # próximo ato construído (ex.: 'ato-02.html'); None enquanto não existir
IMG = 'vitrine.jpg'
RAZAO = A.W / A.H               # proporção da ilustração (o CSS usa a mesma, para as áreas caírem exatamente sobre os itens)
ALT_VITRINE = ('Uma vitrine de degraus de madeira que sobem da esquerda para a direita. Sobre cada degrau há um objeto, com uma etiqueta '
               'em branco pendurada na frente: uma xícara de café, uma pequena mesa posta para a família, uma mala de viagem com chapéu '
               'de palha e mapa, livros com capelo de formatura, malas de viagem com um avião em miniatura, um carro e uma casa.')

BARRA = '''<!-- barra do site: leva de volta às Meditações; links relativos à pasta do estudo -->
<header class="site-bar">
  <div class="site-bar-inner">
    <a class="site-brand" href="../">Meditações</a>
    <nav class="site-links" aria-label="Site Meditações Bíblicas">
      <a href="../quem-sou-eu/">Quem sou eu</a>
      <a href="../sobre/">Sobre</a>
    </nav>
  </div>
</header>'''

# ----------------------------------------------------------------------------------------------------------------------
# Ato 1: a vitrine. Sete itens, do mais barato ao mais caro (nível 1 a 7).
# Todos os valores foram conferidos nas fontes em 2026-11-06 (ver `conta`). Se uma fonte for atualizada, refaça a conta aqui.
#   valor = o número mostrado no painel (pt-BR); aprox = True quando é uma conta feita sobre uma média ou uma estimativa ("≈");
#   nota = uma linha sobre o que o preço cobre; conta = a conta e a fonte (abre em "Conta e fonte");
#   recebe = o "Imagine…" (o retorno, de forma sensorial); dura / para = duas qualidades do retorno (por quanto tempo, para quem);
#   cafes = quanto isso vale em cafés de R$ 6,98 (dá a medida de quanto o preço sobe); tag = forma curta para a etiqueta da imagem (só em telas grandes).
# ----------------------------------------------------------------------------------------------------------------------
ITENS = [
    dict(nome='Um café', valor='6,98', aprox=False, tag='6,98',
         nota='Xícara de café coado, em padarias de São Paulo.',
         conta='Preço médio de uma xícara pequena de café coado em 50 padarias da cidade de São Paulo, coletado em 22 e 23 de setembro de 2026. '
               'Fonte: Procon-SP, pesquisa de preços de produtos de padaria 2026.',
         recebe='Imagine o cheiro do café fresco e uns minutos só seus.',
         dura='minutos', para='você', cafes=None),
    dict(nome='Uma refeição em família', valor='386', aprox=True, tag='386',
         nota='4 refeições completas, a R$ 96,44 cada (em 2024).',
         conta='4 pessoas × R$ 96,44 = R$ 385,76. R$ 96,44 é o preço médio da refeição completa (prato, bebida, sobremesa e café) em restaurante à la carte, '
               'numa pesquisa com mais de 4.500 restaurantes divulgada em setembro de 2024, a mais recente que encontramos. '
               'Fonte: Ticket (Edenred Brasil), Pesquisa +Valor.',
         recebe='Imagine a mesa cheia, todo mundo falando ao mesmo tempo e alguém rindo alto.',
         dura='horas', para='a família', cafes='≈ 55 cafés'),
    dict(nome='Um fim de semana fora', valor='903', aprox=True, tag='903',
         nota='2 diárias de hotel, só a hospedagem.',
         conta='2 diárias × R$ 451,71 = R$ 903,42. R$ 451,71 foi a diária média dos hotéis acompanhados pelo FOHB em maio de 2026 (amostra de 570 hotéis). '
               'Não inclui viagem, comida nem passeios. Fonte: FOHB (Fórum de Operadores Hoteleiros do Brasil), divulgado pela Panrotas em 08/07/2026.',
         recebe='Imagine acordar sem despertador, longe da rotina, com o dia todo pela frente.',
         dura='2 dias', para='quem for junto', cafes='≈ 130 cafés'),
    dict(nome='Um curso', valor='10.020', aprox=True, tag='10 mil',
         nota='Um ano de curso superior presencial.',
         conta='12 mensalidades × R$ 835 = R$ 10.020. R$ 835 é a mensalidade mediana dos cursos superiores presenciais em 2026 '
               '(metade dos cursos cobra menos, metade cobra mais). Fonte: ABMES, “Cenário de precificação da graduação – Brasil 2026”.',
         recebe='Imagine entender hoje o que ontem parecia difícil, e levar isso para a vida.',
         dura='a vida toda', para='você', cafes='≈ 1.400 cafés'),
    dict(nome='Uma viagem internacional em família', valor='41.700', aprox=True, tag='42 mil',
         nota='Estimativa: 4 pessoas, 8 dias na Disney.',
         conta='US$ 7.640 × R$ 5,46 (dólar do Banco Central em 05/11/2026) ≈ R$ 41.700. É uma estimativa para uma família de 4 pessoas em 8 dias, '
               'no cenário intermediário (passagens, hospedagem, ingressos dos parques, alimentação, transporte local, seguro e documentação), sem compras. '
               'Pode ir de cerca de R$ 32 mil a R$ 54 mil. Fonte: Catraca Livre, 13/02/2026; câmbio: Banco Central.',
         recebe='Imagine a família inteira diante de um lugar que só conhecia de foto.',
         dura='8 dias, anos de memória', para='a família', cafes='≈ 6 mil cafés'),
    dict(nome='Um carro', valor='72.490', aprox=False, tag='72 mil',
         nota='O carro novo mais barato do país (nov/2026).',
         conta='Fiat Mobi Like zero-quilômetro, preço de oferta em novembro de 2026, o mais barato entre os carros novos vendidos no Brasil. '
               'Os preços de tabela mudam com as promoções. Fonte: levantamento do UOL Carros, publicado pelo jornal A Tarde em 01/11/2026.',
         recebe='Imagine ir aonde quiser, na hora que quiser, com quem você ama.',
         dura='muitos anos', para='a família', cafes='≈ 10 mil cafés'),
    dict(nome='Uma casa', valor='542.500', aprox=True, tag='543 mil',
         nota='Imóvel de 60 m², com 2 dormitórios.',
         conta='60 m² × R$ 9.042 por m² = R$ 542.520. R$ 9.042 é o preço médio anunciado dos imóveis de 2 dormitórios nas 56 cidades acompanhadas, '
               'em outubro de 2026 (preço pedido, não o de venda). Os 60 m² são um exemplo. Fonte: Índice FipeZAP, informe de outubro de 2026.',
         recebe='Imagine abrir a porta e saber que aquele lugar é seu, e da sua família.',
         dura='décadas', para='a família', cafes='≈ 78 mil cafés'),
]
for i, it in enumerate(ITENS):
    it['nivel'] = i + 1
assert len(ITENS) == len(A.AREAS) == 7


def f(v):
    return ('%.2f' % v).rstrip('0').rstrip('.')


def pct(v, total):
    return f(v / total * 100)


def rect(r, cls='', rx=None):
    x0, y0, x1, y1 = r
    return '<rect%s x="%s" y="%s" width="%s" height="%s"%s/>' % (
        (' class="%s"' % cls) if cls else '', f(x0), f(y0), f(x1 - x0), f(y1 - y0), (' rx="%s"' % rx) if rx else '')


def overlay_svg():
    """Camada SVG sobre a ilustração (mesmo sistema de coordenadas dela): as áreas de toque e o brilho dourado de cada item."""
    g = ['<svg class="av-ov" viewBox="0 0 %d %d" preserveAspectRatio="none" role="group" aria-label="Itens da vitrine">' % (A.W, A.H)]
    for i, it in enumerate(ITENS):
        a = A.AREAS[i]
        g.append('        <g class="item" data-i="%d" tabindex="0" role="button" aria-pressed="false" aria-label="Item %d de %d: %s">'
                 % (i, i + 1, len(ITENS), it['nome']))
        for r in A.areas_de_toque(i):
            g.append('          ' + rect(r, 'hit'))
        g.append('          <g class="hl" aria-hidden="true">')
        for r, rx in ((A.pad(a['box'], 10), 26), (A.etiqueta_papel(a['tag']), 18)):
            g.append('            ' + rect(r, 'glow', rx))
            g.append('            ' + rect(r, 'ring', rx))
        g.append('          </g>')
        g.append('        </g>')
    g.append('      </svg>')
    return '\n'.join(g)


def selos_e_etiquetas():
    """✓ de item visto (no canto do objeto) e o texto que aparece na etiqueta da própria imagem."""
    out = []
    for i, it in enumerate(ITENS):
        x0, y0, x1, y1 = A.AREAS[i]['box']
        out.append('      <span class="ok" data-i="%d" aria-hidden="true" style="left:%s%%;top:%s%%;--i:%d">✓</span>' % (i, pct(x1, A.W), pct(y0, A.H), i))
    for i, it in enumerate(ITENS):
        x, y, w, h = A.AREAS[i]['tag']
        out.append('      <div class="etq" data-i="%d" aria-hidden="true" style="left:%s%%;top:%s%%;width:%s%%;height:%s%%;--i:%d">'
                   '<span class="etq-rs">R$</span><span class="etq-v">%s</span></div>'
                   % (i, pct(x, A.W), pct(y, A.H), pct(w, A.W), pct(h, A.H), i, it['tag'] or '—'))
    return '\n'.join(out)


def escreve(nome, html):
    gravar(DEST, nome, html, RASC, PASTA)


# ----------------------------------------------------------------------------------------------------------------------
# Capa
# ----------------------------------------------------------------------------------------------------------------------
def capa():
    html = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quanto custa?</title>
<meta name="description" content="Um estudo em etapas que segue uma pergunta simples, passo a passo, para ver aonde ela leva.">
<link rel="stylesheet" href="style.css">
</head>
<body class="capa">
@@BARRA@@
<div class="wrap">
  <header class="capa-hero">
    <div class="capa-texto">
      <p class="kicker">Um estudo em etapas</p>
      <h1>Quanto custa?</h1>
      <p class="lede">Tem uma pergunta que a gente faz o tempo todo, quase sem perceber. Vamos segui-la de perto, passo a passo, e ver aonde ela leva.</p>
      <div class="capa-acoes">
        <a class="botao-capa" href="ato-01.html">Começar →</a>
        <a class="qr-mini" href="qr.html" title="Ampliar o QR Code em tela cheia" aria-label="Abrir o QR Code em tela cheia"><img src="qr.svg" alt="" width="64" height="64"><span>QR Code</span></a>
      </div>
    </div>
    <figure class="capa-figura">
      <img src="@@IMG@@" alt="@@ALT@@" width="@@W@@" height="@@H@@">
    </figure>
  </header>
</div>
<!-- contagem de visitas (GoatCounter): sem JavaScript e sem cookies; o caminho em p= precisa bater com a URL publicada -->
<img src="https://meditacoesbiblicas.goatcounter.com/count?p=/meditacoes-biblicas/@@PASTA@@/" width="1" height="1" alt="">
</body>
</html>
'''
    escreve('index.html', html.replace('@@BARRA@@', BARRA).replace('@@PASTA@@', PASTA).replace('@@IMG@@', IMG)
            .replace('@@ALT@@', ALT_VITRINE).replace('@@W@@', str(A.W)).replace('@@H@@', str(A.H)))


# ----------------------------------------------------------------------------------------------------------------------
# Ato 1: Tudo tem um preço (a vitrine)
# ----------------------------------------------------------------------------------------------------------------------
JS_ATO1 = r'''
(function () {
  'use strict';
  var dados = JSON.parse(document.getElementById('dados').textContent);
  var itens = dados.itens, total = itens.length;
  var hs = [].slice.call(document.querySelectorAll('.item'));
  var oks = [].slice.call(document.querySelectorAll('.ok'));
  var etqs = [].slice.call(document.querySelectorAll('.etq'));
  var quadro = document.getElementById('quadro');
  var moldura = document.getElementById('moldura');
  var camada = document.querySelector('.av-ov');
  var dica = document.getElementById('dica-item');
  var painel = document.getElementById('painel');
  var vazio = document.getElementById('p-vazio');
  var comecar = document.getElementById('p-comecar');
  var cartao = document.getElementById('p-cartao');
  var fecho = document.getElementById('p-fecho');
  var fim = document.getElementById('av-fim');
  var et = document.getElementById('etiqueta');
  var bAnt = document.getElementById('p-ant'), bProx = document.getElementById('p-prox');
  var pontos = [].slice.call(document.querySelectorAll('.p-vistos i'));
  var reduz = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  var mouse = !!(window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches);
  var CHAVE = 'quanto-custa-ato1';
  var ZOOM = 1.45;
  var atual = -1, vistos = {}, ficha = 0, contagem = 0, ultimoPreco = 0;
  try { vistos = JSON.parse(sessionStorage.getItem(CHAVE) || '{}') || {}; } catch (e) { vistos = {}; }

  function el(id) { return document.getElementById(id); }
  function contar() { var n = 0; for (var k = 0; k < total; k++) if (vistos[k]) n++; return n; }
  function numero(v) { return parseFloat(String(v).replace(/\./g, '').replace(',', '.')); }
  function inteiro(n) { return Math.round(n).toLocaleString('pt-BR'); }

  // o preço "sobe" (ou desce) do valor do item anterior até o deste: dá a sensação de quanto ele aumenta
  function animarPreco(i) {
    var it = itens[i], alvo = numero(it.valor), node = el('et-valor'), de = ultimoPreco, meu = ++contagem;
    ultimoPreco = alvo;
    node.textContent = it.valor;
    if (reduz || de === alvo || !window.requestAnimationFrame) return;
    var t0 = null, dur = 900;
    function passo(t) {
      if (meu !== contagem) return;
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      node.textContent = p >= 1 ? it.valor : inteiro(de + (alvo - de) * e);
      if (p < 1) requestAnimationFrame(passo);
    }
    requestAnimationFrame(passo);
    setTimeout(function () { if (meu === contagem) node.textContent = it.valor; }, dur + 150);
  }

  function preencher(i) {
    var it = itens[i];
    el('et-pos').textContent = 'Item ' + (i + 1) + ' de ' + total;
    el('painel-titulo').textContent = it.nome;
    var pr = el('et-preco');
    if (!it.valor) {
      pr.className = 'et-preco pendente';
      el('et-valor').textContent = '——';
      el('et-aprox').hidden = true;
      el('et-sr').textContent = '';
      ultimoPreco = 0;
    } else {
      pr.className = 'et-preco';
      el('et-aprox').hidden = !it.aprox;
      el('et-sr').textContent = (it.aprox ? 'cerca de ' : '') + 'R$ ' + it.valor;
      animarPreco(i);
    }
    var cf = el('et-cafes');
    cf.hidden = !it.cafes;
    el('et-cafes-t').textContent = it.cafes || '';
    el('et-nota').textContent = it.nota || (it.valor ? '' : 'Preço a confirmar.');
    el('et-recebe').textContent = it.recebe || 'O que este item devolve: texto a definir.';
    el('et-chips').hidden = !(it.dura || it.para);
    el('et-dura').textContent = it.dura || '';
    el('et-para').textContent = it.para || '';
    var det = el('et-fonte');
    det.open = false;
    det.hidden = !it.conta;
    el('et-conta').textContent = it.conta || '';
    el('p-pos').textContent = (i + 1) + ' / ' + total;
    bAnt.disabled = i === 0;
    bProx.disabled = i === total - 1;
  }

  function medidores(i, animar) {
    var n = itens[i].nivel;
    [].slice.call(document.querySelectorAll('.medidor')).forEach(function (m) {
      var segs = [].slice.call(m.querySelectorAll('i'));
      var nivel = m.classList.contains('paga') ? itens[i].paga || n : itens[i].recebeNivel || n;
      m.querySelector('.m-seg').setAttribute('aria-label', (m.classList.contains('paga') ? 'Você paga: ' : 'Você recebe: ') + nivel + ' de ' + total);
      if (animar) segs.forEach(function (s) { s.style.transition = 'none'; s.classList.remove('on'); });
      void m.offsetWidth;
      segs.forEach(function (s, k) {
        s.style.transition = '';
        s.style.setProperty('--k', k);
        s.classList.toggle('on', k < nivel);
      });
    });
  }

  function marcar() {
    var n = 0;
    hs.forEach(function (h, i) {
      var v = !!vistos[i];
      oks[i].classList.toggle('on', v);
      etqs[i].classList.toggle('on', v);
      if (v) n++;
    });
    pontos.forEach(function (p, i) { p.classList.toggle('on', !!vistos[i]); });
    document.getElementById('p-vistos-n').textContent = n + ' de ' + total;
    painel.classList.toggle('completo', n === total);
    fim.hidden = !(n === total && fecho.hidden);
    comecar.hidden = n > 0;
  }

  // a imagem é maior que a janela? (mede o tamanho da caixa, que não muda com o zoom; o scrollWidth cresceria com a própria câmera)
  function rolavel() { return !!quadro && !!moldura && moldura.offsetWidth > quadro.clientWidth + 2; }

  function centrar(i) {
    // só quando a imagem é maior que a janela (celular em pé): leva o item para o meio
    if (!rolavel()) return;
    var alvo = moldura.offsetLeft + itens[i].cx * moldura.offsetWidth - quadro.clientWidth / 2;
    quadro.scrollTo({ left: alvo, behavior: reduz ? 'auto' : 'smooth' });
  }

  // a "câmera" se aproxima do item escolhido (só quando a imagem cabe inteira na janela: computador, telão, tablet e celular deitado)
  function zoomPara(i) {
    if (!moldura) return;
    if (i < 0 || reduz || rolavel()) { moldura.style.transform = ''; return; }
    var w = moldura.offsetWidth, h = moldura.offsetHeight;
    var tx = Math.min(0, Math.max(w * (1 - ZOOM), w / 2 - ZOOM * itens[i].cx * w));
    var ty = Math.min(0, Math.max(h * (1 - ZOOM), h / 2 - ZOOM * itens[i].cy * h));
    moldura.style.transformOrigin = '0 0';
    moldura.style.transform = 'translate(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px) scale(' + ZOOM + ')';
  }

  // a etiqueta do painel gira (como virar uma etiqueta de preço): sai de lado, troca o conteúdo e volta balançando, presa pelo furo
  function entra() {
    et.animate([
      { transform: 'perspective(900px) rotateY(90deg)' },
      { transform: 'perspective(900px) rotateY(0deg) rotateZ(-3deg)', offset: .7 },
      { transform: 'perspective(900px) rotateY(0deg) rotateZ(1.5deg)', offset: .85 },
      { transform: 'perspective(900px) rotateY(0deg) rotateZ(0deg)' }
    ], { duration: 460, easing: 'cubic-bezier(.2,.8,.2,1)' });
  }

  function animarEtiqueta(troca, soEntrada) {
    var meu = ++ficha;
    if (reduz || !et.animate) { troca(); return; }
    et.getAnimations().forEach(function (a) { a.cancel(); });
    if (soEntrada) { troca(); entra(); return; }
    var sai = et.animate([{ transform: 'perspective(900px) rotateY(0deg)' }, { transform: 'perspective(900px) rotateY(-90deg)' }], { duration: 170, easing: 'ease-in', fill: 'forwards' });
    sai.finished.then(function () {
      if (meu !== ficha) return;
      troca();
      sai.cancel();
      entra();
    }, function () {});
  }

  // a etiqueta que está na própria imagem vira, na primeira vez que o item é aberto
  function virarEtiquetaDaImagem(i) {
    var e = etqs[i];
    if (reduz || !e.animate) return;
    e.animate([
      { transform: 'perspective(500px) rotateY(90deg)', opacity: 0 },
      { transform: 'perspective(500px) rotateY(0deg)', opacity: 1 }
    ], { duration: 480, easing: 'cubic-bezier(.2,.8,.2,1)' });
  }

  // ao abrir o sétimo item diferente, as etiquetas (e os ✓) acendem da esquerda para a direita
  function celebrar() {
    if (reduz) return;
    moldura.classList.add('varrer');
    setTimeout(function () { moldura.classList.remove('varrer'); }, 2600);
  }

  function mostraDica(i) {
    if (!dica) return;
    dica.textContent = itens[i].nome;
    dica.style.left = itens[i].dx + '%';
    dica.style.top = itens[i].dy + '%';
    dica.hidden = false;
  }
  function escondeDica() { if (dica) dica.hidden = true; }

  function semSelecao() {
    atual = -1; ficha++;
    hs.forEach(function (h) { h.setAttribute('aria-pressed', 'false'); });
    etqs.forEach(function (e) { e.classList.remove('sel'); });
    cartao.hidden = true;
    zoomPara(-1);
  }

  function selecionar(i, vindoDoTeclado) {
    if (i < 0 || i >= total) return;
    var primeira = atual === -1, novo = !vistos[i], antes = contar();
    atual = i;
    moldura.classList.remove('convite');
    hs.forEach(function (h, k) { h.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
    etqs.forEach(function (e, k) { e.classList.toggle('sel', k === i); });
    vistos[i] = 1;
    try { sessionStorage.setItem(CHAVE, JSON.stringify(vistos)); } catch (e) {}
    vazio.hidden = true;
    fecho.hidden = true;
    cartao.hidden = false;
    animarEtiqueta(function () { preencher(i); medidores(i, true); }, primeira || !!cartao.dataset.vindoDoFecho);
    delete cartao.dataset.vindoDoFecho;
    marcar();
    if (novo) virarEtiquetaDaImagem(i);
    if (antes < total && contar() === total) celebrar();
    centrar(i);
    zoomPara(i);
    if (vindoDoTeclado) hs[i].focus({ preventScroll: true });
    if (history.replaceState) history.replaceState(null, '', '#item-' + (i + 1));
  }

  function limpar() {
    semSelecao();
    fecho.hidden = true;
    vazio.hidden = false;
    marcar();
    if (history.replaceState) history.replaceState(null, '', location.pathname);
  }

  function mostrarFecho() {
    semSelecao();
    vazio.hidden = true;
    fecho.hidden = false;
    marcar();
    if (history.replaceState) history.replaceState(null, '', '#fim');
    var t = document.getElementById('fe-titulo');
    if (t && t.focus) t.focus({ preventScroll: true });
  }

  function voltarAosItens() {
    fecho.hidden = true;
    vazio.hidden = false;
    cartao.dataset.vindoDoFecho = '1';
    marcar();
    if (history.replaceState) history.replaceState(null, '', location.pathname);
  }

  hs.forEach(function (h, i) {
    h.addEventListener('click', function () { selecionar(i); });
    h.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selecionar(i); }
      else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); selecionar(Math.min(i + 1, total - 1), true); }
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); selecionar(Math.max(i - 1, 0), true); }
    });
    if (mouse) {
      h.addEventListener('pointerenter', function () { mostraDica(i); });
      h.addEventListener('pointerleave', escondeDica);
    }
  });
  bAnt.addEventListener('click', function () { selecionar(atual - 1); });
  bProx.addEventListener('click', function () { selecionar(atual + 1); });
  comecar.addEventListener('click', function () { selecionar(0); });
  fim.addEventListener('click', mostrarFecho);
  document.getElementById('fe-voltar').addEventListener('click', voltarAosItens);
  // tocar no fundo da vitrine (fora dos itens) afasta a câmera; só quando a imagem cabe inteira na janela
  if (camada) camada.addEventListener('click', function (e) { if (e.target === camada && atual >= 0 && !rolavel()) limpar(); });
  window.addEventListener('resize', function () { if (atual >= 0) zoomPara(atual); else if (moldura) moldura.style.transform = ''; });
  // teclado e controle remoto de apresentação (setas, Page Down/Up, Home/End, Esc)
  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target && e.target.tagName;
    if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT' || t === 'BUTTON' || t === 'SUMMARY' || t === 'A') return;
    if (e.target && e.target.classList && e.target.classList.contains('item')) { if (/^(Arrow|Enter| )/.test(e.key)) return; }
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); selecionar(atual < 0 ? 0 : Math.min(atual + 1, total - 1), true); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); selecionar(atual < 0 ? 0 : Math.max(atual - 1, 0), true); }
    else if (e.key === 'Home') { e.preventDefault(); selecionar(0, true); }
    else if (e.key === 'End') { e.preventDefault(); selecionar(total - 1, true); }
    else if (e.key === 'Escape') { limpar(); escondeDica(); }
  });

  if (contar() > 0) moldura.classList.remove('convite');
  marcar();
  var m = /^#item-(\d+)$/.exec(location.hash);
  if (m && +m[1] >= 1 && +m[1] <= total) selecionar(+m[1] - 1);
  else if (location.hash === '#fim' && contar() === total) mostrarFecho();
  // celular em pé: começa com o primeiro item à vista
  if (quadro && !m) quadro.scrollLeft = 0;
})();
'''


def ato01():
    dados_itens = []
    for i, it in enumerate(ITENS):
        x0, y0, x1, y1 = A.AREAS[i]['box']
        dados_itens.append(dict(nome=it['nome'], nivel=it['nivel'], valor=it['valor'], aprox=it['aprox'], nota=it['nota'], conta=it['conta'],
                                recebe=it['recebe'], dura=it['dura'], para=it['para'], cafes=it['cafes'], tag=it['tag'],
                                cx=round((x0 + x1) / 2 / A.W, 4), cy=round((y0 + y1) / 2 / A.H, 4),
                                dx=round((x0 + x1) / 2 / A.W * 100, 2), dy=round(y0 / A.H * 100, 2)))
    dados = dict(itens=dados_itens, proximo=PROXIMO)
    pontos = ''.join('<i></i>' for _ in ITENS)
    segs = ''.join('<i></i>' for _ in range(7))
    cont = ('\n    <a class="fe-continuar" id="fe-continuar" href="%s">Levar a ideia mais longe →</a>' % PROXIMO) if PROXIMO else ''
    dev = ('\n    <p class="p-dev">Ato 1 em teste: ilustração do Gemini; valores e fontes conferidos em 06/11/2026.</p>' if RASC else '')
    fe_dev = ('\n    <p class="p-dev fe-dev">O Ato 2 só começa depois do seu teste deste ato.</p>' if (RASC and not PROXIMO) else '')
    html = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quanto custa? · Ato 1 — Tudo tem um preço</title>
<meta name="description" content="Toque nos itens da vitrine e veja quanto cada um custa e o que devolve.">
<link rel="stylesheet" href="style.css">
</head>
<body class="ato">
@@BARRA@@
<main class="av" id="av" style="--r:@@RAZAO@@">
  <section class="av-palco" aria-label="A vitrine">
    <div class="av-quadro" id="quadro">
      <div class="av-moldura convite" id="moldura">
        <img class="av-img" src="@@IMG@@" width="@@W@@" height="@@H@@" alt="@@ALT@@" fetchpriority="high">
      @@OVERLAY@@
@@SELOS@@
        <div class="dica-item" id="dica-item" hidden></div>
      </div>
    </div>
    <a class="av-voltar" href="index.html">← Início</a>
    <button type="button" class="av-fim" id="av-fim" hidden><span class="l-longo">O que os sete têm em comum</span><span class="l-curto">O que têm em comum</span> →</button>
  </section>
  <aside class="av-painel" id="painel" aria-live="polite" aria-labelledby="painel-titulo">
    <div class="p-topo">
      <p class="p-ato">Ato 1 · Tudo tem um preço</p>
      <span class="p-vistos" aria-hidden="true">@@PONTOS@@<span id="p-vistos-n" style="margin-left:4px">0 de 7</span></span>
    </div>
    <div class="p-vazio" id="p-vazio">
      <p><b><span class="so-mouse">Clique</span><span class="so-toque">Toque</span> em um item da vitrine</b> para ver a etiqueta: o preço e o que ele devolve.<span class="so-arrasta">↔ Arraste a imagem para os lados para ver todos os itens.</span></p>
      <button type="button" class="p-comecar" id="p-comecar">Começar pelo café →</button>
    </div>
    <div class="p-cartao" id="p-cartao" hidden>
      <div class="etiqueta" id="etiqueta">
        <p class="et-pos" id="et-pos"></p>
        <h2 class="et-nome" id="painel-titulo">Vitrine</h2>
        <div class="et-linha">
          <p class="et-preco" id="et-preco"><span class="aprox" aria-hidden="true" id="et-aprox" hidden>≈</span><span class="rs" aria-hidden="true">R$</span><span class="valor" id="et-valor" aria-hidden="true"></span><span class="sr-only" id="et-sr"></span></p>
          <p class="et-cafes" id="et-cafes" hidden title="Quantos cafés de R$ 6,98 dá para comprar com esse valor">☕ <span id="et-cafes-t"></span></p>
        </div>
        <p class="et-nota" id="et-nota"></p>
        <p class="et-recebe" id="et-recebe"></p>
        <p class="et-chips" id="et-chips"><span><b>Dura:</b> <i id="et-dura"></i></span><span><b>Para:</b> <i id="et-para"></i></span></p>
        <div class="medidores">
          <div class="medidor paga"><span class="m-rot">Você paga</span><span class="m-seg" role="img">@@SEGS@@</span></div>
          <div class="medidor recebe"><span class="m-rot">Você recebe</span><span class="m-seg" role="img">@@SEGS@@</span></div>
        </div>
        <p class="m-nota">Comparação entre os sete itens.</p>
        <details class="et-fonte" id="et-fonte"><summary>Conta e fonte</summary><p id="et-conta"></p></details>
      </div>
      <div class="p-nav">
        <button type="button" id="p-ant">← Anterior</button>
        <span class="p-pos" id="p-pos"></span>
        <button type="button" id="p-prox">Próximo →</button>
      </div>
    </div>
    <div class="p-fecho" id="p-fecho" hidden>
      <p class="fe-ato">Ato 1 · Tudo tem um preço</p>
      <h2 class="fe-titulo" id="fe-titulo" tabindex="-1">O que os sete têm em comum</h2>
      <p>Cada item entrega algo bom, e todos cobram um preço. Do café à casa, o preço subiu de R$ 6,98 para cerca de R$ 542 mil: mais de 77 mil vezes.</p>
      <p class="fe-ideia">Quanto mais vale o que a gente recebe, mais ele custa. <b>Para receber, é preciso pagar.</b></p>@@CONT@@
      <button type="button" class="fe-voltar" id="fe-voltar">← Rever os itens</button>@@FEDEV@@
    </div>@@DEV@@
  </aside>
</main>
<noscript><p style="position:fixed;left:0;right:0;top:0;z-index:99999;margin:0;padding:12px 16px;background:#FBEBDD;color:#9A4310;text-align:center;font:600 15px/1.4 system-ui">Esta página precisa de JavaScript para mostrar as etiquetas da vitrine.</p></noscript>
<script type="application/json" id="dados">@@DADOS@@</script>
<script>@@JS@@</script>
<!-- contagem de visitas (GoatCounter): sem JavaScript e sem cookies; o caminho em p= precisa bater com a URL publicada -->
<img src="https://meditacoesbiblicas.goatcounter.com/count?p=/meditacoes-biblicas/@@PASTA@@/ato-01.html" width="1" height="1" alt="">
</body>
</html>
'''
    html = (html.replace('@@BARRA@@', BARRA).replace('@@RAZAO@@', '%.6f' % RAZAO).replace('@@IMG@@', IMG)
            .replace('@@W@@', str(A.W)).replace('@@H@@', str(A.H)).replace('@@ALT@@', ALT_VITRINE)
            .replace('@@OVERLAY@@', overlay_svg()).replace('@@SELOS@@', selos_e_etiquetas())
            .replace('@@PONTOS@@', pontos).replace('@@SEGS@@', segs).replace('@@CONT@@', cont).replace('@@DEV@@', dev)
            .replace('@@FEDEV@@', fe_dev)
            .replace('@@DADOS@@', json.dumps(dados, ensure_ascii=False)).replace('@@JS@@', JS_ATO1)
            .replace('@@PASTA@@', PASTA))
    escreve('ato-01.html', html)


# ----------------------------------------------------------------------------------------------------------------------
# QR Code em tela cheia (para projetar). No desenvolvimento o QR abre o desenvolvimento, para testar no celular;
# na publicação (sem --rascunho) ele abre o endereço definitivo.
# ATENÇÃO ao publicar: o qr.svg do desenvolvimento NÃO pode ser copiado para a pasta publicada (ele aponta para o desenvolvimento).
# ----------------------------------------------------------------------------------------------------------------------
def qr_page():
    endereco = 'meditacoesbiblicas.github.io/meditacoes-biblicas/' + (PASTA + '-desenvolvimento' if RASC else PASTA) + '/ato-01.html'
    teste = '\n  <span class="qr-teste">QR de teste: abre o desenvolvimento. Na publicação ele passa a abrir o endereço definitivo.</span>' if RASC else ''
    html = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>QR Code · Quanto custa?</title>
<link rel="stylesheet" href="style.css">
</head>
<body class="qr">
@@BARRA@@
<main class="qr-code">
  <img class="qr-img" src="qr.svg" alt="QR Code que abre o estudo Quanto custa?">
</main>
<footer class="qr-legenda">
  <a class="qr-titulo" href="ato-01.html">Quanto custa? · Ato 1</a>
  <span>@@ENDERECO@@</span>@@TESTE@@
</footer>
</body>
</html>
'''
    escreve('qr.html', html.replace('@@BARRA@@', BARRA).replace('@@ENDERECO@@', endereco).replace('@@TESTE@@', teste))


os.makedirs(DEST, exist_ok=True)
shutil.copyfile(os.path.join(AQUI, 'qr-desenvolvimento.svg' if RASC else 'qr-producao.svg'), os.path.join(DEST, 'qr.svg'))
capa()
ato01()
qr_page()
print('quanto-custa ok:', DEST)

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
# preco/nota/recebe/tag = None  ->  "a confirmar": nada de valor inventado antes de conferir a fonte.
#   preco = número em reais (o painel mostra com vírgula e milhar); tag = forma curta para a etiqueta na imagem ("543 mil").
# ----------------------------------------------------------------------------------------------------------------------
NOMES = ['Um café', 'Uma refeição em família', 'Um fim de semana fora', 'Um curso',
         'Uma viagem internacional em família', 'Um carro', 'Uma casa']
ITENS = [dict(nome=n, nivel=i + 1, preco=None, nota=None, recebe=None, tag=None) for i, n in enumerate(NOMES)]
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
        out.append('      <span class="ok" data-i="%d" aria-hidden="true" style="left:%s%%;top:%s%%">✓</span>' % (i, pct(x1, A.W), pct(y0, A.H)))
    for i, it in enumerate(ITENS):
        x, y, w, h = A.AREAS[i]['tag']
        out.append('      <div class="etq" data-i="%d" aria-hidden="true" style="left:%s%%;top:%s%%;width:%s%%;height:%s%%">'
                   '<span class="etq-rs">R$</span><span class="etq-v">%s</span></div>'
                   % (i, pct(x, A.W), pct(y, A.H), pct(w, A.W), pct(h, A.H), it['tag'] or '—'))
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
<meta name="description" content="Um estudo em etapas para olhar de perto quanto custam as coisas e o que elas devolvem.">
<link rel="stylesheet" href="style.css">
</head>
<body class="capa">
@@BARRA@@
<div class="wrap">
  <header class="capa-hero">
    <div class="capa-texto">
      <p class="kicker">Um estudo em etapas</p>
      <h1>Quanto custa?</h1>
      <p class="lede">Quase tudo o que a gente quer tem um preço. Vamos olhar de perto o que cada coisa custa e o que ela devolve.</p>
      <a class="botao-capa" href="ato-01.html">Começar →</a>
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
  var dica = document.getElementById('dica-item');
  var painel = document.getElementById('painel');
  var vazio = document.getElementById('p-vazio');
  var cartao = document.getElementById('p-cartao');
  var et = document.getElementById('etiqueta');
  var bAnt = document.getElementById('p-ant'), bProx = document.getElementById('p-prox');
  var pontos = [].slice.call(document.querySelectorAll('.p-vistos i'));
  var reduz = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  var mouse = !!(window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches);
  var CHAVE = 'quanto-custa-ato1';
  var atual = -1, vistos = {}, ficha = 0;
  try { vistos = JSON.parse(sessionStorage.getItem(CHAVE) || '{}') || {}; } catch (e) { vistos = {}; }

  function el(id) { return document.getElementById(id); }
  function moeda(v) { return Number(v).toLocaleString('pt-BR', { minimumFractionDigits: v % 1 ? 2 : 0, maximumFractionDigits: 2 }); }

  function preencher(i) {
    var it = itens[i];
    el('et-pos').textContent = 'Item ' + (i + 1) + ' de ' + total;
    el('painel-titulo').textContent = it.nome;
    var pr = el('et-preco'), nota = el('et-nota');
    if (it.preco === null || it.preco === undefined) {
      pr.className = 'et-preco pendente';
      el('et-valor').textContent = '——';
      nota.textContent = 'Preço a confirmar.';
    } else {
      pr.className = 'et-preco';
      el('et-valor').textContent = moeda(it.preco);
      nota.textContent = it.nota || '';
    }
    el('et-recebe').textContent = it.recebe || 'O que este item devolve: texto a definir.';
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
    el('p-vistos-n').textContent = n + ' de ' + total;
    painel.classList.toggle('completo', n === total);
  }

  function centrar(i) {
    // só quando a imagem é maior que a janela (celular em pé): leva o item para o meio
    if (!quadro || quadro.scrollWidth <= quadro.clientWidth + 2) return;
    var alvo = moldura.offsetLeft + itens[i].cx * moldura.offsetWidth - quadro.clientWidth / 2;
    quadro.scrollTo({ left: alvo, behavior: reduz ? 'auto' : 'smooth' });
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

  function mostraDica(i) {
    if (!dica) return;
    dica.textContent = itens[i].nome;
    dica.style.left = itens[i].dx + '%';
    dica.style.top = itens[i].dy + '%';
    dica.hidden = false;
  }
  function escondeDica() { if (dica) dica.hidden = true; }

  function selecionar(i, vindoDoTeclado) {
    if (i < 0 || i >= total) return;
    var primeira = atual === -1, novo = !vistos[i];
    atual = i;
    hs.forEach(function (h, k) { h.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
    etqs.forEach(function (e, k) { e.classList.toggle('sel', k === i); });
    vistos[i] = 1;
    try { sessionStorage.setItem(CHAVE, JSON.stringify(vistos)); } catch (e) {}
    vazio.hidden = true;
    cartao.hidden = false;
    animarEtiqueta(function () { preencher(i); medidores(i, true); }, primeira);
    marcar();
    if (novo) virarEtiquetaDaImagem(i);
    centrar(i);
    if (vindoDoTeclado) hs[i].focus({ preventScroll: true });
    if (history.replaceState) history.replaceState(null, '', '#item-' + (i + 1));
  }

  function limpar() {
    atual = -1; ficha++;
    hs.forEach(function (h) { h.setAttribute('aria-pressed', 'false'); });
    etqs.forEach(function (e) { e.classList.remove('sel'); });
    cartao.hidden = true; vazio.hidden = false;
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
  // teclado e controle remoto de apresentação (setas, Page Down/Up, Home/End, Esc)
  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target && e.target.tagName;
    if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT' || t === 'BUTTON') return;
    if (e.target && e.target.classList && e.target.classList.contains('item')) { if (/^(Arrow|Enter| )/.test(e.key)) return; }
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); selecionar(atual < 0 ? 0 : Math.min(atual + 1, total - 1), true); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); selecionar(atual < 0 ? 0 : Math.max(atual - 1, 0), true); }
    else if (e.key === 'Home') { e.preventDefault(); selecionar(0, true); }
    else if (e.key === 'End') { e.preventDefault(); selecionar(total - 1, true); }
    else if (e.key === 'Escape') { limpar(); escondeDica(); }
  });

  marcar();
  var m = /^#item-(\d+)$/.exec(location.hash);
  if (m && +m[1] >= 1 && +m[1] <= total) selecionar(+m[1] - 1);
  // celular em pé: começa com o primeiro item à vista
  if (quadro && !m) quadro.scrollLeft = 0;
})();
'''


def ato01():
    dados_itens = []
    for i, it in enumerate(ITENS):
        x0, y0, x1, y1 = A.AREAS[i]['box']
        d = dict(nome=it['nome'], nivel=it['nivel'], preco=it['preco'], nota=it['nota'], recebe=it['recebe'], tag=it['tag'],
                 cx=round((x0 + x1) / 2 / A.W, 4), dx=round((x0 + x1) / 2 / A.W * 100, 2), dy=round(y0 / A.H * 100, 2))
        dados_itens.append(d)
    dados = dict(itens=dados_itens, proximo=PROXIMO)
    pontos = ''.join('<i></i>' for _ in ITENS)
    segs = ''.join('<i></i>' for _ in range(7))
    cont = ('\n      <a class="p-continuar" id="p-continuar" href="%s">Continuar →</a>' % PROXIMO) if PROXIMO else ''
    dev = ('\n    <p class="p-dev">Ato 1 em teste: ilustração do Gemini; textos e preços ainda a confirmar.</p>' if RASC else '')
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
      <div class="av-moldura" id="moldura">
        <img class="av-img" src="@@IMG@@" width="@@W@@" height="@@H@@" alt="@@ALT@@" fetchpriority="high">
      @@OVERLAY@@
@@SELOS@@
        <div class="dica-item" id="dica-item" hidden></div>
      </div>
    </div>
    <a class="av-voltar" href="index.html">← Início</a>
  </section>
  <aside class="av-painel" id="painel" aria-live="polite" aria-labelledby="painel-titulo">
    <div class="p-topo">
      <p class="p-ato">Ato 1 · Tudo tem um preço</p>
      <span class="p-vistos" aria-hidden="true">@@PONTOS@@<span id="p-vistos-n" style="margin-left:4px">0 de 7</span></span>
    </div>
    <p class="p-vazio" id="p-vazio"><b><span class="so-mouse">Clique</span><span class="so-toque">Toque</span> em um item da vitrine</b> para ver a etiqueta: o preço e o que ele devolve.<span class="so-arrasta">↔ Arraste a imagem para os lados para ver todos os itens.</span></p>
    <div class="p-cartao" id="p-cartao" hidden>
      <div class="etiqueta" id="etiqueta">
        <p class="et-pos" id="et-pos"></p>
        <h2 class="et-nome" id="painel-titulo">Vitrine</h2>
        <p class="et-preco" id="et-preco"><span class="rs">R$</span><span class="valor" id="et-valor"></span></p>
        <p class="et-nota" id="et-nota"></p>
        <p class="et-recebe" id="et-recebe"></p>
        <div class="medidores">
          <div class="medidor paga"><span class="m-rot">Você paga</span><span class="m-seg" role="img">@@SEGS@@</span></div>
          <div class="medidor recebe"><span class="m-rot">Você recebe</span><span class="m-seg" role="img">@@SEGS@@</span></div>
        </div>
      </div>
      <div class="p-nav">
        <button type="button" id="p-ant">← Anterior</button>
        <span class="p-pos" id="p-pos"></span>
        <button type="button" id="p-prox">Próximo →</button>
      </div>@@CONT@@
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
            .replace('@@DADOS@@', json.dumps(dados, ensure_ascii=False)).replace('@@JS@@', JS_ATO1)
            .replace('@@PASTA@@', PASTA))
    escreve('ato-01.html', html)


os.makedirs(DEST, exist_ok=True)
capa()
ato01()
print('quanto-custa ok:', DEST)

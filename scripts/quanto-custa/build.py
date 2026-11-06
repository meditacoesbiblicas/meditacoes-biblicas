# -*- coding: utf-8 -*-
# Gera as páginas do estudo "Quanto custa?" (capa + um arquivo por ato) e a ilustração provisória do Ato 1.
# Uso: python3 scripts/quanto-custa/build.py <pasta-de-saída> [--rascunho]
#
# Regras do estudo (combinadas com o dono do site):
#  - nada nas páginas (título, capa, meta, navegação) pode adiantar o que vem nos atos seguintes;
#  - um ato por vez, só avança com a confirmação do dono;
#  - preços e fatos só entram como texto final depois de conferidos (ver DADOS: valor None = "a confirmar").
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'estudo'))
from rascunho import gravar  # noqa: E402

PASTA = 'quanto-custa'          # pasta da versão publicada (ainda não existe); a de desenvolvimento é PASTA + '-desenvolvimento'
DEST = sys.argv[1]
RASC = '--rascunho' in sys.argv
PROXIMO = None                  # próximo ato construído (ex.: 'ato-02.html'); None enquanto não existir

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
# preco/nota/recebe = None  ->  o painel mostra "a confirmar": nada de valor inventado antes de conferir a fonte.
# ----------------------------------------------------------------------------------------------------------------------
ITENS = [
    dict(nome='Um café', emoji='☕', tam=84),
    dict(nome='Uma refeição em família', emoji='🍽️', tam=100),
    dict(nome='Um fim de semana fora', emoji='🧳', tam=110),
    dict(nome='Um curso', emoji='🎓', tam=124),
    dict(nome='Uma viagem internacional em família', emoji='✈️', tam=140),
    dict(nome='Um carro', emoji='🚗', tam=160),
    dict(nome='Uma casa', emoji='🏠', tam=190),
]
for i, it in enumerate(ITENS):
    it.update(nivel=i + 1, preco=None, nota=None, recebe=None)

W, H = 1536, 1024        # proporção 3:2, a mesma da ilustração final
SW, X0, Y0, DY = 176, 140, 850, 88


def geometria():
    """Posição de cada item na ilustração provisória (em px do desenho) e a área clicável (em % da imagem)."""
    saida = []
    for i, it in enumerate(ITENS):
        s = it['tam']
        xc = X0 + i * SW + SW / 2
        y = Y0 - i * DY
        topo = y - s * 1.02 - 6
        base = y + 58
        larg = s * 1.2
        saida.append(dict(xc=xc, y=y, s=s,
                          left=(xc - larg / 2) / W * 100, top=topo / H * 100,
                          width=larg / W * 100, height=(base - topo) / H * 100))
    return saida


def svg_provisorio():
    g = geometria()
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">' % (W, H, W, H),
         '<defs>'
         '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4DA"/><stop offset="1" stop-color="#F1D9A4"/></linearGradient>'
         '<radialGradient id="luz" cx="0.78" cy="0.12" r="0.7"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".85"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>'
         '<linearGradient id="madeira" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C99A55"/><stop offset="1" stop-color="#8E6431"/></linearGradient>'
         '</defs>',
         '<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H),
         '<rect width="%d" height="%d" fill="url(#luz)"/>' % (W, H)]
    for i, a in enumerate(g):
        x = X0 + i * SW
        p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#madeira)"/>' % (x, a['y'], SW + 1, H - a['y']))
        p.append('<rect x="%d" y="%d" width="%d" height="14" fill="#E8C98A"/>' % (x, a['y'], SW + 1))
        p.append('<rect x="%d" y="%d" width="2" height="%d" fill="#6E4C22" opacity=".45"/>' % (x, a['y'], H - a['y']))
    for i, a in enumerate(g):
        it = ITENS[i]
        p.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="10" fill="#000" opacity=".16"/>' % (a['xc'], a['y'] + 6, a['s'] * .5))
        p.append('<text x="%.0f" y="%.0f" font-size="%d" text-anchor="middle" '
                 'font-family="Apple Color Emoji, Segoe UI Emoji, Noto Color Emoji, sans-serif">%s</text>'
                 % (a['xc'], a['y'] - a['s'] * .12, a['s'], it['emoji']))
        # etiqueta em branco, pendurada na frente do degrau
        p.append('<path d="M%.0f %.0f Q%.0f %.0f %.0f %.0f" stroke="#1F2A44" stroke-width="1.6" fill="none"/>'
                 % (a['xc'], a['y'] + 30, a['xc'] + 9, a['y'] + 15, a['xc'] + 2, a['y'] + 3))
        p.append('<rect x="%.0f" y="%.0f" width="52" height="32" rx="5" fill="#FFF8E7" stroke="#1F2A44" stroke-width="1.6"/>'
                 % (a['xc'] - 26, a['y'] + 22))
        p.append('<circle cx="%.0f" cy="%.0f" r="3.2" fill="#fff" stroke="#1F2A44" stroke-width="1.4"/>' % (a['xc'], a['y'] + 30))
    p.append('</svg>')
    return '\n'.join(p)


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
      <img src="vitrine-provisoria.svg" alt="Uma vitrine em degraus, com um objeto em cada degrau, do menor ao maior." width="1536" height="1024">
    </figure>
  </header>
</div>
<!-- contagem de visitas (GoatCounter): sem JavaScript e sem cookies; o caminho em p= precisa bater com a URL publicada -->
<img src="https://meditacoesbiblicas.goatcounter.com/count?p=/meditacoes-biblicas/@@PASTA@@/" width="1" height="1" alt="">
</body>
</html>
'''
    escreve('index.html', html.replace('@@BARRA@@', BARRA).replace('@@PASTA@@', PASTA))


# ----------------------------------------------------------------------------------------------------------------------
# Ato 1: Tudo tem um preço (a vitrine)
# ----------------------------------------------------------------------------------------------------------------------
JS_ATO1 = r'''
(function () {
  'use strict';
  var dados = JSON.parse(document.getElementById('dados').textContent);
  var itens = dados.itens, total = itens.length;
  var hs = [].slice.call(document.querySelectorAll('.hot'));
  var quadro = document.getElementById('quadro');
  var painel = document.getElementById('painel');
  var vazio = document.getElementById('p-vazio');
  var cartao = document.getElementById('p-cartao');
  var et = document.getElementById('etiqueta');
  var bAnt = document.getElementById('p-ant'), bProx = document.getElementById('p-prox');
  var pontos = [].slice.call(document.querySelectorAll('.p-vistos i'));
  var reduz = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
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
    hs.forEach(function (h, i) { var v = !!vistos[i]; h.classList.toggle('visto', v); if (v) n++; });
    pontos.forEach(function (p, i) { p.classList.toggle('on', !!vistos[i]); });
    el('p-vistos-n').textContent = n + ' de ' + total;
    painel.classList.toggle('completo', n === total);
  }

  function centrar(i) {
    // só quando a imagem é maior que a janela (celular em pé): leva o item para o meio
    if (!quadro || quadro.scrollWidth <= quadro.clientWidth + 2) return;
    var h = hs[i], m = h.offsetParent, alvo = m.offsetLeft + h.offsetLeft + h.offsetWidth / 2 - quadro.clientWidth / 2;
    quadro.scrollTo({ left: alvo, behavior: reduz ? 'auto' : 'smooth' });
  }

  // a etiqueta gira (como virar uma etiqueta de preço): sai de lado, troca o conteúdo e volta balançando, presa pelo furo
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

  function selecionar(i, vindoDoTeclado) {
    if (i < 0 || i >= total) return;
    var primeira = atual === -1;
    atual = i;
    hs.forEach(function (h, k) { h.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
    vistos[i] = 1;
    try { sessionStorage.setItem(CHAVE, JSON.stringify(vistos)); } catch (e) {}
    vazio.hidden = true;
    cartao.hidden = false;
    animarEtiqueta(function () { preencher(i); medidores(i, true); }, primeira);
    marcar();
    centrar(i);
    if (vindoDoTeclado) hs[i].focus({ preventScroll: true });
    if (history.replaceState) history.replaceState(null, '', '#item-' + (i + 1));
  }

  function limpar() {
    atual = -1; ficha++;
    hs.forEach(function (h) { h.setAttribute('aria-pressed', 'false'); });
    cartao.hidden = true; vazio.hidden = false;
    if (history.replaceState) history.replaceState(null, '', location.pathname);
  }

  hs.forEach(function (h, i) {
    h.addEventListener('click', function () { selecionar(i); });
    h.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); selecionar(Math.min(i + 1, total - 1), true); }
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); selecionar(Math.max(i - 1, 0), true); }
    });
  });
  bAnt.addEventListener('click', function () { selecionar(atual - 1); });
  bProx.addEventListener('click', function () { selecionar(atual + 1); });
  // teclado e controle remoto de apresentação (setas, Page Down/Up, Home/End, Esc)
  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target && e.target.tagName;
    if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT') return;
    if (e.target && e.target.classList && e.target.classList.contains('hot') && /^Arrow/.test(e.key)) return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); selecionar(atual < 0 ? 0 : Math.min(atual + 1, total - 1), true); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); selecionar(atual < 0 ? 0 : Math.max(atual - 1, 0), true); }
    else if (e.key === 'Home') { e.preventDefault(); selecionar(0, true); }
    else if (e.key === 'End') { e.preventDefault(); selecionar(total - 1, true); }
    else if (e.key === 'Escape') { limpar(); }
  });

  marcar();
  var m = /^#item-(\d+)$/.exec(location.hash);
  if (m && +m[1] >= 1 && +m[1] <= total) selecionar(+m[1] - 1);
  // celular em pé: começa com o primeiro item à vista
  if (quadro) quadro.scrollLeft = 0;
})();
'''


def ato01():
    g = geometria()
    hots = []
    for i, (it, a) in enumerate(zip(ITENS, g)):
        hots.append('        <button type="button" class="hot" style="left:%.2f%%;top:%.2f%%;width:%.2f%%;height:%.2f%%" '
                    'data-nome="%s" aria-pressed="false" aria-label="Item %d de %d: %s"></button>'
                    % (a['left'], a['top'], a['width'], a['height'], it['nome'], i + 1, len(ITENS), it['nome']))
    dados = dict(itens=[dict(nome=it['nome'], nivel=it['nivel'], preco=it['preco'], nota=it['nota'], recebe=it['recebe']) for it in ITENS],
                 proximo=PROXIMO)
    pontos = ''.join('<i></i>' for _ in ITENS)
    segs = ''.join('<i></i>' for _ in range(7))
    cont = ('\n      <a class="p-continuar" id="p-continuar" href="%s">Continuar →</a>' % PROXIMO) if PROXIMO else ''
    dev = ('\n      <p class="p-dev">Protótipo do Ato 1: ilustração provisória; textos e preços ainda a confirmar.</p>' if RASC else '')
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
<main class="av" id="av">
  <section class="av-palco" aria-label="A vitrine">
    <div class="av-quadro" id="quadro">
      <div class="av-moldura" id="moldura">
        <img class="av-img" src="vitrine-provisoria.svg" width="1536" height="1024" alt="Uma vitrine em degraus que sobem da esquerda para a direita. Em cada degrau há um item com uma etiqueta: um café, uma refeição em família, um fim de semana fora, um curso, uma viagem internacional em família, um carro e uma casa.">
@@HOTS@@
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
    html = (html.replace('@@BARRA@@', BARRA).replace('@@HOTS@@', '\n'.join(hots)).replace('@@PONTOS@@', pontos)
            .replace('@@SEGS@@', segs).replace('@@CONT@@', cont).replace('@@DEV@@', dev)
            .replace('@@DADOS@@', json.dumps(dados, ensure_ascii=False)).replace('@@JS@@', JS_ATO1)
            .replace('@@PASTA@@', PASTA))
    escreve('ato-01.html', html)


os.makedirs(DEST, exist_ok=True)
with open(os.path.join(DEST, 'vitrine-provisoria.svg'), 'w', encoding='utf-8') as f:
    f.write(svg_provisorio())
capa()
ato01()
print('quanto-custa ok:', DEST)

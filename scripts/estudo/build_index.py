# -*- coding: utf-8 -*-
# Gera a página inicial do estudo: o mapa do Sermão do Monte (Mt 5:1 a 7:29), por partes, com o que está pronto e o que é "a construir".
# Uso: python3 scripts/estudo/build_index.py <pasta-de-saída> [--rascunho]
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rascunho import gravar
DEST = sys.argv[1]
RASC = '--rascunho' in sys.argv

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

# (versículos, título, descrição, arquivo ou None)
CAP5_INICIO = [('Mateus 5:1–2', 'Jesus sobe o monte', 'Jesus sobe o monte, assenta-se e ensina os discípulos.', None)]
CAP5_DEPOIS = [
    ('Mateus 5:13–16', 'Sal e luz', 'O que os bem-aventurados levam ao mundo: sal, luz e o candelabro.', 'v13-15.html'),
    ('Mateus 5:17–20', 'A lei e a justiça maior', 'Jesus não veio abolir a lei, veio cumprir. A justiça do Reino precisa exceder a dos escribas e fariseus.', 'v17-20.html'),
    ('Mateus 5:21–26', 'Raiva', 'Do “não matarás” à raiva e ao desprezo. Reconciliar-se antes de oferecer.', 'v21-26.html'),
    ('Mateus 5:27–30', 'Cobiça', 'Do “não adulterarás” ao olhar que cobiça. Arrancar o olho, cortar a mão.', 'v27-30.html'),
    ('Mateus 5:31–32', 'Divórcio', 'O ensino de Jesus sobre o divórcio.', None),
    ('Mateus 5:33–37', 'Juramentos', 'O ensino de Jesus sobre os juramentos.', None),
    ('Mateus 5:38–42', 'Olho por olho', 'Como responder ao mal.', None),
    ('Mateus 5:43–48', 'Amor aos inimigos', 'Amar os inimigos e orar pelos que perseguem.', None),
]
CAP6 = [
    ('Mateus 6:1–4', 'Dar esmolas', 'Dar sem buscar o aplauso dos homens.', None),
    ('Mateus 6:5–15', 'Oração', 'Como orar: o Pai Nosso.', None),
    ('Mateus 6:16–18', 'Jejum', 'Jejuar diante do Pai, e não diante dos homens.', None),
    ('Mateus 6:19–24', 'Tesouros e dois senhores', 'Tesouros no céu e a escolha de a quem servir.', None),
    ('Mateus 6:25–34', 'Ansiedade', 'Não andar ansioso: o cuidado do Pai.', None),
]
CAP7 = [
    ('Mateus 7:1–6', 'Julgar', 'Não julgar: o argueiro e a trave.', None),
    ('Mateus 7:7–12', 'Pedir, buscar, bater', 'A oração perseverante e a regra de ouro.', None),
    ('Mateus 7:13–14', 'A porta estreita', 'A porta estreita e o caminho estreito.', None),
    ('Mateus 7:15–20', 'Falsos profetas', 'Pelos frutos os conhecereis.', None),
    ('Mateus 7:21–23', 'Nem todo o que diz “Senhor”', 'O que importa é fazer a vontade do Pai.', None),
    ('Mateus 7:24–27', 'A casa na rocha', 'Ouvir e praticar: a casa sobre a rocha e a casa sobre a areia.', None),
    ('Mateus 7:28–29', 'Conclusão', 'As multidões se admiram do ensino de Jesus.', None),
]

PRONTAS = 1 + sum(1 for x in CAP5_DEPOIS if x[3])  # bem-aventuranças + as partes com página
TOTAL = 1 + len(CAP5_INICIO) + len(CAP5_DEPOIS) + len(CAP6) + len(CAP7)


def cartao(vs, tit, desc, href):
    if href:
        return ('      <a class="parte pronta" href="%s">\n        <span class="topo"><span class="vs">%s</span><span class="st ok">Pronto</span></span>\n'
                '        <span class="tt">%s</span>\n        <span class="ds">%s</span>\n        <span class="ir">Abrir →</span>\n      </a>' % (href, vs, tit, desc))
    return ('      <div class="parte breve">\n        <span class="topo"><span class="vs">%s</span><span class="st">A construir</span></span>\n'
            '        <span class="tt">%s</span>\n        <span class="ds">%s</span>\n      </div>' % (vs, tit, desc))


def grade(itens):
    return '    <div class="partes">\n' + '\n'.join(cartao(*i) for i in itens) + '\n    </div>'


PORTAS = ['Pobres em espírito', 'Os que choram', 'Mansos', 'Fome e sede de justiça', 'Misericordiosos', 'Puros de coração', 'Pacificadores', 'Perseguidos']
LINKS = ['v03.html#v3', 'v04.html#v4', 'v05.html#v5', 'v06.html#v6', 'v07.html#v7', 'v08.html#v8', 'v09.html#v9', 'v10-12.html#v10']
dots = '\n'.join('          <li><a href="%s" title="%s"><b>%d</b><span>%s</span></a></li>' % (LINKS[i], PORTAS[i], i + 1, PORTAS[i]) for i in range(8))

pct = round(PRONTAS * 100 / TOTAL)
html = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sermão do Monte · Mateus 5–7 — estudo</title>
<link rel="stylesheet" href="style.css">
</head>
<body class="sermao">
''' + BARRA + '''
<div class="wrap">

<header class="top sm-topo">
  <p class="kicker">Estudo bíblico · Mateus 5 a 7</p>
  <h1>Sermão do Monte</h1>
  <p>O sermão que Jesus pregou no monte (Mateus 5:1 a 7:29), estudado por partes. Escolha uma parte para abrir. As partes marcadas “A construir” ainda vão ser feitas.</p>
  <div class="progresso" role="img" aria-label="%(p)d de %(t)d partes prontas">
    <div class="barra"><span style="width:%(pct)d%%"></span></div>
    <p><b>%(p)d de %(t)d</b> partes prontas</p>
  </div>
</header>

<main class="sermao-mapa">

  <section class="cap" id="cap5" aria-labelledby="t5">
    <h2 id="t5"><span class="n5">Mateus 5</span> Bem-aventuranças, sal e luz, e a lei vista por dentro</h2>

    <div class="faixa"><span class="vs">Mateus 5:1–2</span><span class="tt">Início: Jesus sobe o monte</span><span class="ds">Jesus sobe o monte, assenta-se e ensina os discípulos.</span><span class="st">A construir</span></div>
''' % {'p': PRONTAS, 't': TOTAL, 'pct': pct} + '''

    <h3 class="grupo">As bem-aventuranças <small>Mateus 5:3–12</small></h3>
    <article class="destaque">
      <a class="foto" href="caminho.html" aria-label="O caminho e as portas: abrir a ilustração">
        <img src="caminho-mini.jpg" alt="Ilustração: o caminho estreito com as oito portas e, no alto, o juízo" width="320" height="213">
      </a>
      <div class="corpo">
        <span class="topo"><span class="vs">Mateus 5:3–12</span><span class="st ok">Pronto</span></span>
        <h4>As bem-aventuranças: oito portas no caminho</h4>
        <p>Cada bem-aventurança é uma porta do caminho cristão, que é um só. Abra a ilustração e entre por cada porta: cada uma tem a sua página, com versículos e explicação. É para a ilustração que o QR Code aponta.</p>
        <ol class="portas" aria-label="As oito portas">
''' + dots + '''
        </ol>
        <p class="acoes"><a class="botao" href="caminho.html">Abrir o caminho e as portas →</a></p>
      </div>
      <a class="qr-mini" href="qr.html" title="Ampliar o QR Code em tela cheia" aria-label="Abrir o QR Code em tela cheia"><img src="qr.svg" alt="" width="64" height="64"><span>QR Code</span></a>
    </article>

    <h3 class="grupo">Depois das bem-aventuranças <small>Mateus 5:13–48</small> <a class="ver-trilha" href="depois.html">Ver a trilha →</a></h3>
''' + grade(CAP5_DEPOIS) + '''
  </section>

  <section class="cap" id="cap6" aria-labelledby="t6">
    <h2 id="t6"><span class="n5">Mateus 6</span> Dar, orar, jejuar e confiar no Pai</h2>
''' + grade(CAP6) + '''
  </section>

  <section class="cap" id="cap7" aria-labelledby="t7">
    <h2 id="t7"><span class="n5">Mateus 7</span> Julgar, pedir, o caminho estreito e a casa na rocha</h2>
''' + grade(CAP7) + '''
  </section>

</main>
</div>
<!-- contagem de visitas (GoatCounter): sem JavaScript e sem cookies; o caminho em p= precisa bater com a URL publicada -->
<img src="https://meditacoesbiblicas.goatcounter.com/count?p=/meditacoes-biblicas/bem-aventurancas/" width="1" height="1" alt="">
<script>try{sessionStorage.setItem('origem-bem-aventurancas','ampliada')}catch(e){}</script>
</body>
</html>
'''
gravar(DEST, 'index.html', html, RASC)
print('index ok:', PRONTAS, 'de', TOTAL)

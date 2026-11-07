# -*- coding: utf-8 -*-
# Gera as páginas do estudo "O que vale mais?": capa, dez partes, conclusão, fontes e QR Code.
# Uso: python3 scripts/o-que-vale-mais/build.py <pasta-de-saída> [--rascunho]
#
# O que NÃO muda de lugar: estudo.css, estudo.js, motor.js, p01.js … p10.js (arquivos escritos à mão, na pasta de saída).
# Este script só escreve os HTML, o dados.js e o qr.svg. Regras combinadas com o dono do site:
#  - nada nas páginas antes da parte 6 (título, capa, meta, navegação) adianta o que vem depois;
#  - o objetivo do estudo só é dito no fim (parte 10 e conclusão);
#  - versículos e trechos da Ellen White vêm de fontes_cache.json e são conferidos por verify.py;
#  - "reflexão" e "imaginação" aparecem sempre marcadas como tal.
import json
import os
import shutil
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), 'estudo'))
sys.path.insert(0, AQUI)
from rascunho import gravar  # noqa: E402
import dados  # noqa: E402
import conteudo as K  # noqa: E402

PASTA = 'o-que-vale-mais'      # versão publicada (ainda não existe); a de desenvolvimento é PASTA + '-desenvolvimento'
DEST = sys.argv[1]
RASC = '--rascunho' in sys.argv
TITULO = 'O que vale mais?'
VER = str(int(time.time()))   # acrescentado aos arquivos .js/.css para o navegador não usar cópia velha

BARRA = '''<header class="site-bar">
  <div class="site-bar-inner">
    <a class="site-brand" href="../">Meditações</a>
    <nav class="site-links" aria-label="Site Meditações Bíblicas">
      <a href="../quem-sou-eu/">Quem sou eu</a>
      <a href="../sobre/">Sobre</a>
    </nav>
  </div>
</header>'''


def arq(n):
    return 'conclusao.html' if n == 11 else 'parte-%02d.html' % n


def escreve(nome, html):
    gravar(DEST, nome, html, RASC, PASTA)


def cabeca(titulo, descricao, extra=''):
    return '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<link rel="stylesheet" href="estudo.css?v=%s">
<link rel="stylesheet" href="partes.css?v=%s">%s
</head>
''' % (titulo, descricao, VER, VER, extra)


def pontos(atual):
    li = []
    for n in range(1, 11):
        cls = ' class="atual"' if n == atual else ''
        corpo = ('<a href="%s" title="Parte %d" aria-label="Parte %d"></a>' % (arq(n), n, n)) if RASC else '<span></span>'
        li.append('<li data-n="%d"%s>%s</li>' % (n, cls, corpo))
    return '<ol class="pontos" aria-label="Progresso no estudo">%s</ol>' % ''.join(li)


def devmenu(atual, classe='fixo'):
    itens = [('index.html', 'Capa', atual == 0)] + [(arq(n), 'Parte %d · %s' % (n, K.PARTES[n]['titulo']) if n in K.PARTES else 'Parte %d' % n, atual == n) for n in range(1, 11)]
    itens += [('conclusao.html', 'Conclusão', atual == 11), ('fontes.html', 'Fontes e conferência', atual == 12), ('qr.html', 'QR Code', atual == 13)]
    li = ''.join('<li%s><a href="%s">%s</a></li>' % (' class="atual"' if a else '', h, t) for h, t, a in itens)
    return '<div class="dev-menu %s"><button type="button">Menu ▾</button><ol hidden>%s</ol></div>' % (classe, li)


def rodape_comum(atual, scripts):
    dev = '<script>window.OVM_DEV=true;</script>\n' if RASC else ''
    sc = ''.join('<script src="%s?v=%s"></script>\n' % (s, VER) for s in scripts)
    return dev, sc


def pagina_parte(n):
    p = K.PARTES[n]
    tema = p.get('tema', 'noite')
    leitura = ''
    for h2, intro, cartoes in p.get('leitura', []):
        leitura += '<h2>%s</h2>\n%s%s\n' % (h2, ('<p class="intro">%s</p>\n' % intro) if intro else '', cartoes)
    prox = arq(n + 1)
    rot = 'Continuar: Parte %d →' % (n + 1) if n < 10 else 'Continuar →'
    dev, sc = rodape_comum(n, ['dados.js', 'estudo.js'] + (['motor.js'] if p.get('motor') else []) + p.get('extras', []) + [p['script']])
    html = cabeca('%s · Parte %d: %s' % (TITULO, n, p['titulo']), 'Parte %d de um estudo em etapas: %s' % (n, TITULO)) + '''<body class="parte" data-tema="%s" data-parte="%d">
%s%s
<div class="estudo-barra"><div class="estudo-barra-inner">
  <a class="voltar" href="index.html">← Início</a>
  <p class="titulo"><span class="pn">Parte %d de 10 · </span><b>%s</b></p>
  %s
  %s
</div></div>
<main>
<section class="cena %s" id="cena" aria-label="Cena interativa">
  <div class="cena-palco" id="palco">
%s
  </div>
  <div class="cena-painel">
    <p class="cena-rotulo" id="rotulo"></p>
    <div class="cena-texto" id="texto" aria-live="polite"></div>
    <div class="cena-controles" id="controles">
%s
    </div>
    <div class="cena-nav"><button type="button" id="ant">← Anterior</button><span class="pos" id="pos"></span><button type="button" id="prox">Próximo →</button></div>
  </div>
</section>
<section class="leitura" id="leitura" aria-label="Para ler e pensar">
%s</section>
<nav class="proxima" aria-label="Continuar">
  <a class="btn" href="%s">%s</a>
  <p class="aviso">Você pode voltar e rever esta parte quando quiser.</p>
</nav>
</main>
<footer class="rodape">Fontes e datas da conferência: <a href="fontes.html">Fontes</a>.</footer>
%s<noscript><p style="position:fixed;left:0;right:0;top:0;z-index:99999;margin:0;padding:12px 16px;background:#FBEBDD;color:#9A4310;text-align:center;font:600 15px/1.4 system-ui">Esta página precisa de JavaScript para funcionar.</p></noscript>
%s%s</body>
</html>
''' % (tema, n, BARRA, '', n, p['titulo'], pontos(n), devmenu(n, 'na-barra') if RASC else '', p.get('classe', 'p%02d' % n), p['palco'], p.get('controles', ''), leitura, prox, rot,
       '', dev, sc)
    escreve(arq(n), html)


def capa():
    c = K.CAPA
    dev, sc = rodape_comum(0, ['dados.js', 'estudo.js', 'capa.js'])
    html = cabeca('%s' % TITULO, c['descricao']) + '''<body class="capa" data-tema="noite" data-parte="0">
%s
<main>
<section class="capa-hero">
  <canvas id="tela" aria-hidden="true"></canvas>
  <div class="capa-texto">
    <p class="kicker">%s</p>
    <h1>%s</h1>
    <p class="lede">%s</p>
    <div class="capa-acoes">
      <a class="btn" href="parte-01.html">Começar a jornada →</a>
      <a class="qr-mini" href="qr.html" title="Ampliar o QR Code em tela cheia" aria-label="Abrir o QR Code em tela cheia"><img src="qr.svg" alt="" width="64" height="64"><span>QR Code</span></a>
    </div>
    <p class="meta">%s</p>
  </div>
</section>
</main>
%s%s%s</body>
</html>
''' % (BARRA, c['kicker'], TITULO, c['lede'], c['meta'], devmenu(0) + '\n' if RASC else '', dev, sc)
    escreve('index.html', html)


def pagina_livre(arquivo, atual, titulo, tema, corpo, scripts, descricao):
    dev, sc = rodape_comum(atual, scripts)
    html = cabeca('%s · %s' % (TITULO, titulo), descricao) + '''<body class="livre" data-tema="%s" data-parte="%d">
%s
%s
%s%s%s</body>
</html>
''' % (tema, 11 if arquivo == 'conclusao.html' else 0, BARRA, corpo, devmenu(atual) + '\n' if RASC else '', dev, sc)
    escreve(arquivo, html)


def qr_page():
    endereco = 'meditacoesbiblicas.github.io/meditacoes-biblicas/' + (PASTA + '-desenvolvimento' if RASC else PASTA) + '/'
    teste = '\n  <span class="qr-teste">QR de teste: abre o desenvolvimento. Na publicação ele passa a abrir o endereço definitivo.</span>' if RASC else ''
    html = cabeca('QR Code · %s' % TITULO, 'QR Code para abrir o estudo.') + '''<body class="qr" data-tema="dia">
%s
<main class="qr-code">
  <img class="qr-img" src="qr.svg" alt="QR Code que abre o estudo %s">
</main>
<footer class="qr-legenda">
  <a class="qr-titulo" href="index.html">%s</a>
  <span>%s</span>%s
</footer>
%s</body>
</html>
''' % (BARRA, TITULO, TITULO, endereco, teste, devmenu(13) + '\n' if RASC else '')
    escreve('qr.html', html)


def main():
    os.makedirs(DEST, exist_ok=True)
    with open(os.path.join(DEST, 'dados.js'), 'w', encoding='utf-8') as f:
        f.write('window.OVM_DADOS=' + dados.json_dados() + ';\n')
        f.write('window.OVM_V=' + json.dumps(getattr(K, 'VERSOS', {}), ensure_ascii=False, separators=(',', ':')) + ';\n')
    shutil.copyfile(os.path.join(AQUI, 'qr-desenvolvimento.svg' if RASC else 'qr-producao.svg'), os.path.join(DEST, 'qr.svg'))
    capa()
    for n in range(1, 11):
        if n in K.PARTES:
            pagina_parte(n)
    if getattr(K, 'CONCLUSAO', None):
        c = K.CONCLUSAO
        pagina_livre('conclusao.html', 11, 'Conclusão', c.get('tema', 'aurora'), c['corpo'], ['dados.js', 'estudo.js'] + c.get('extras', []) + [c['script']], 'Conclusão do estudo %s.' % TITULO)
    if getattr(K, 'FONTES_PAG', None):
        pagina_livre('fontes.html', 12, 'Fontes e conferência', 'dia', K.FONTES_PAG, ['estudo.js'], 'Fontes e datas da conferência do estudo %s.' % TITULO)
    qr_page()
    print('o-que-vale-mais ok:', DEST, '| partes:', sorted(K.PARTES))


main()

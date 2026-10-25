#!/usr/bin/env python3
"""Atualiza a cópia OFFLINE do estudo "Bem-aventuranças · Mateus 5".

Gera ~/BemAventurancas-offline/ a partir de public/bem-aventurancas/ (a versão oficial, a mesma do site).
Para abrir sem internet basta dar dois cliques em ~/BemAventurancas-offline/index.html.

O que a cópia offline muda em relação ao site:
  - as fontes (Inter e Newsreader) ficam gravadas na pasta fonts/, em vez de vir do Google Fonts;
  - o contador de visitas (GoatCounter) é removido, para o uso offline não ser contado;
  - na barra de cima, "Meditações" leva ao mapa e "Quem sou eu"/"Sobre" apontam para o site na internet;
  - o CLAUDE.md não vai.

A pasta fica fora do iCloud (na pasta pessoal) de propósito: o iCloud pode "descarregar" arquivos do
Documents quando está sem internet, justamente quando a cópia offline é necessária.

Uso:  python3 scripts/atualizar-offline.py        (roda sozinho a cada commit, pelo hook post-commit)
"""
import os
import re
import shutil
import sys
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(RAIZ, 'public', 'bem-aventurancas')
DESTINO = os.path.expanduser('~/BemAventurancas-offline')
SITE = 'https://meditacoesbiblicas.github.io/meditacoes-biblicas'
FONTES_URL = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Newsreader:wght@500;600&display=swap'
IGNORAR = {'CLAUDE.md', '.DS_Store'}
MANTER = {'fonts', 'LEIA-ME.txt'}  # coisas só da cópia offline


def baixar(url, binario=False):
    # User-Agent de navegador moderno: o Google Fonts só entrega woff2 assim
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'})
    dados = urllib.request.urlopen(req, timeout=40).read()
    return dados if binario else dados.decode('utf-8')


def preparar_fontes():
    """Baixa as fontes uma vez e devolve o CSS local (@font-face apontando para fonts/...)."""
    pasta = os.path.join(DESTINO, 'fonts')
    css_local = os.path.join(pasta, 'fonts.css')
    if os.path.exists(css_local):
        return open(css_local, encoding='utf-8').read()
    os.makedirs(pasta, exist_ok=True)
    css = baixar(FONTES_URL)
    saida = []
    # só os trechos "latin" e "latin-ext" (português cabe inteiro neles)
    for bloco in re.finditer(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, re.S):
        subconj, regra = bloco.groups()
        if subconj not in ('latin', 'latin-ext'):
            continue
        url = re.search(r'url\((https://[^)]+)\)', regra).group(1)
        nome = os.path.basename(url)
        if not nome.endswith('.woff2'):
            nome += '.woff2'
        with open(os.path.join(pasta, nome), 'wb') as f:
            f.write(baixar(url, binario=True))
        saida.append(regra.replace(url, 'fonts/' + nome))
    texto = '\n'.join(saida) + '\n'
    open(css_local, 'w', encoding='utf-8').write(texto)
    return texto


def ajustar_html(s):
    # contador de visitas fora (e o comentário que o explica)
    s = re.sub(r'<!-- contagem de visitas[^>]*-->\n?', '', s)
    s = re.sub(r'<img src="https://meditacoesbiblicas\.goatcounter\.com/[^>]*>\n?', '', s)
    # barra do site
    s = s.replace('<a class="site-brand" href="../">', '<a class="site-brand" href="index.html">')
    s = s.replace('href="../quem-sou-eu/"', 'href="%s/quem-sou-eu/" target="_blank" rel="noopener"' % SITE)
    s = s.replace('href="../sobre/"', 'href="%s/sobre/" target="_blank" rel="noopener"' % SITE)
    return s


def main():
    if not os.path.isdir(ORIGEM):
        sys.exit('Não achei ' + ORIGEM)
    os.makedirs(DESTINO, exist_ok=True)
    try:
        fontes = preparar_fontes()
    except Exception as e:  # sem internet na primeira vez: segue com as fontes do sistema
        print('Aviso: não consegui baixar as fontes (%s). Usando as fontes do sistema.' % e)
        fontes = ''

    esperados = set()
    for nome in sorted(os.listdir(ORIGEM)):
        if nome in IGNORAR:
            continue
        origem = os.path.join(ORIGEM, nome)
        if not os.path.isfile(origem):
            continue
        esperados.add(nome)
        destino = os.path.join(DESTINO, nome)
        if nome.endswith('.html'):
            texto = ajustar_html(open(origem, encoding='utf-8').read())
            open(destino, 'w', encoding='utf-8').write(texto)
        elif nome == 'style.css':
            texto = open(origem, encoding='utf-8').read()
            texto = re.sub(r'@import url\([^)]*fonts\.googleapis[^)]*\);\n?', fontes, texto, count=1)
            open(destino, 'w', encoding='utf-8').write(texto)
        else:
            shutil.copy2(origem, destino)

    # o que saiu do site também sai da cópia
    for nome in os.listdir(DESTINO):
        if nome not in esperados and nome not in MANTER and nome != '.DS_Store':
            caminho = os.path.join(DESTINO, nome)
            if os.path.isfile(caminho):
                os.remove(caminho)

    open(os.path.join(DESTINO, 'LEIA-ME.txt'), 'w', encoding='utf-8').write(
        'Estudo Bem-aventuranças · Mateus 5 — cópia para usar SEM internet.\n\n'
        'Para abrir: dê dois cliques em index.html (abre no navegador).\n'
        'Esta pasta é atualizada automaticamente toda vez que o site é atualizado; não precisa mexer nela.\n\n'
        'Sem internet, ficam sem funcionar só os links de fora: os textos completos da Bíblia (bibliaonline),\n'
        'os trechos no site da Ellen G. White e os links "Quem sou eu" e "Sobre".\n'
        'O QR Code continua levando à versão da internet (é para quem assiste, com celular).\n')
    print('Cópia offline atualizada em', DESTINO)


if __name__ == '__main__':
    main()

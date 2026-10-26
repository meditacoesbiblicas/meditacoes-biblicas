#!/usr/bin/env python3
"""Rascunho (versão em desenvolvimento) do estudo "Sermão do Monte".

Forma de trabalho combinada com o dono do site:
  1. Toda mudança nova vai primeiro para uma cópia escondida do estudo, em
         public/bem-aventurancas/<PASTA_RASCUNHO>/
     (endereço sem link em lugar nenhum, com <meta robots noindex> e uma faixa "VERSÃO EM DESENVOLVIMENTO").
  2. O dono compara o rascunho com a versão publicada.
  3. Só quando ele diz "coloca em produção" é que se roda `promover`.

Comandos:
  python3 scripts/estudo/rascunho.py criar     copia a versão publicada para o rascunho (sobrescreve o rascunho!)
  python3 scripts/estudo/rascunho.py promover  copia o rascunho para a versão publicada (e apaga da publicada o que saiu do rascunho)

As páginas HTML do rascunho diferem das publicadas só por: a meta noindex, a faixa no topo, os links da barra do site
(`../../` em vez de `../`) e o contador de visitas, que fica comentado (`<!--PIXEL ...-->`). `desrascunhar` desfaz isso.
Os geradores (build_pages.py e build_index.py) aceitam --rascunho e já gravam nessa forma.
"""
import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PUBLICADA = os.path.join(RAIZ, 'public', 'bem-aventurancas')
PASTA_RASCUNHO = 'em-desenvolvimento-k7q2'
RASCUNHO = os.path.join(PUBLICADA, PASTA_RASCUNHO)
NAO_COPIAR = {'CLAUDE.md', '.DS_Store', PASTA_RASCUNHO}

NOINDEX = '<meta name="robots" content="noindex, nofollow">\n'


def faixa(nome):
    return ('<div class="rascunho-faixa">VERSÃO EM DESENVOLVIMENTO · ainda não publicada · '
            '<a href="../%s">ver a versão publicada desta página</a></div>\n' % nome)


def rascunhar(html, nome):
    """Publicada -> rascunho."""
    if 'rascunho-faixa' in html:
        return html
    html = html.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + NOINDEX, 1)
    html = re.sub(r'(<body[^>]*>\n)', lambda m: m.group(1) + faixa(nome), html, count=1)
    # barra do site: está um nível mais fundo
    html = html.replace('<a class="site-brand" href="../">', '<a class="site-brand" href="../../">')
    html = html.replace('<a href="../quem-sou-eu/">', '<a href="../../quem-sou-eu/">')
    html = html.replace('<a href="../sobre/">', '<a href="../../sobre/">')
    # contador de visitas desligado (visitas ao rascunho não contam)
    html = re.sub(r'(<img src="https://meditacoesbiblicas\.goatcounter\.com/[^>]*>)', r'<!--PIXEL\1-->', html)
    return html


def desrascunhar(html):
    """Rascunho -> publicada (desfaz `rascunhar`)."""
    html = html.replace(NOINDEX, '', 1)
    html = re.sub(r'<div class="rascunho-faixa">.*?</div>\n', '', html, count=1, flags=re.S)
    html = html.replace('<a class="site-brand" href="../../">', '<a class="site-brand" href="../">')
    html = html.replace('<a href="../../quem-sou-eu/">', '<a href="../quem-sou-eu/">')
    html = html.replace('<a href="../../sobre/">', '<a href="../sobre/">')
    html = re.sub(r'<!--PIXEL(<img [^>]*>)-->', r'\1', html)
    return html


def gravar(pasta, nome, html, rascunho):
    """Grava uma página gerada: na forma publicada ou na do rascunho."""
    if rascunho:
        html = rascunhar(html, nome)
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, nome), 'w', encoding='utf-8') as f:
        f.write(html)


def _arquivos(pasta):
    return sorted(n for n in os.listdir(pasta) if n not in NAO_COPIAR and os.path.isfile(os.path.join(pasta, n)))


def criar():
    if os.path.isdir(RASCUNHO):
        shutil.rmtree(RASCUNHO)
    os.makedirs(RASCUNHO)
    for nome in _arquivos(PUBLICADA):
        origem = os.path.join(PUBLICADA, nome)
        destino = os.path.join(RASCUNHO, nome)
        if nome.endswith('.html'):
            gravar(RASCUNHO, nome, open(origem, encoding='utf-8').read(), True)
        else:
            shutil.copy2(origem, destino)
    print('Rascunho criado em', RASCUNHO)


def promover():
    if not os.path.isdir(RASCUNHO):
        sys.exit('Não existe rascunho.')
    novos = _arquivos(RASCUNHO)
    for nome in novos:
        origem = os.path.join(RASCUNHO, nome)
        destino = os.path.join(PUBLICADA, nome)
        if nome.endswith('.html'):
            with open(destino, 'w', encoding='utf-8') as f:
                f.write(desrascunhar(open(origem, encoding='utf-8').read()))
        else:
            shutil.copy2(origem, destino)
    for nome in _arquivos(PUBLICADA):
        if nome not in novos:
            os.remove(os.path.join(PUBLICADA, nome))
            print('Removido da publicada:', nome)
    print('Rascunho promovido para a versão publicada.')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'criar':
        criar()
    elif cmd == 'promover':
        promover()
    else:
        print(__doc__)

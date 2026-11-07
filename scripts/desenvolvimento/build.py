#!/usr/bin/env python3
"""Página-índice de tudo o que está em desenvolvimento: .../meditacoes-biblicas/desenvolvimento/

Pedido do dono (2026-11-07): para lembrar onde está cada coisa, o endereço fixo é
    <site>/desenvolvimento/            -> lista de tudo o que está sendo desenvolvido
    <site>/desenvolvimento/<nome>/     -> atalho para aquele item (redireciona para a pasta real "<pasta>-desenvolvimento")

As pastas reais continuam sendo public/<pasta>-desenvolvimento/ (os geradores, os QR Codes e o fluxo de publicação dependem delas).
Esta página e os atalhos não têm link em lugar nenhum e são noindex.

Uso:  python3 scripts/desenvolvimento/build.py [destino]      (padrão: public/desenvolvimento)
Para registrar uma coisa nova: acrescente um item em ITENS e rode de novo.
"""
import html
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
DEST = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(RAIZ, 'public', 'desenvolvimento')

# nome = parte do endereço curto; pasta = pasta real em public/ (sem o "-desenvolvimento"); publicada = endereço relativo da versão no ar, ou None
ITENS = [
    dict(nome='bem-aventurancas', pasta='bem-aventurancas', titulo='Sermão do Monte · Bem-aventuranças',
         resumo='O estudo do Sermão do Monte (Mt 5–7), com as oito portas do caminho. Aqui está a versão em desenvolvimento, com as partes que ainda não foram publicadas.',
         publicada='bem-aventurancas/'),
    dict(nome='o-que-vale-mais', pasta='o-que-vale-mais', titulo='O que vale mais?',
         resumo='A jornada em dez partes: do chocolate quente ao limite do universo e ao núcleo do átomo, até o preço que foi pago por você.',
         publicada=None),
    dict(nome='quanto-custa', pasta='quanto-custa', titulo='Quanto custa?',
         resumo='O primeiro estudo da escada de preços: a etiqueta que sobe a cada escolha.',
         publicada=None),
]

CSS = '''
:root { --navy:#1F2A44; --creme:#FAF0DD; --ouro:#C8923A; --texto:#2A2A33; --mudo:#6B5A3A; --cartao:#FFFFFF; --linha:rgba(31,42,68,.14); }
@media (prefers-color-scheme: dark) { :root { --creme:#161B2B; --texto:#ECE7DA; --mudo:#C9B98F; --cartao:#202842; --linha:rgba(255,255,255,.16); --navy:#F4E6C4; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--creme); color: var(--texto); font: 400 17px/1.55 Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
.faixa { background: #B65A2E; color: #fff; text-align: center; font: 600 13px/1.3 Inter, system-ui, sans-serif; padding: 8px 12px; }
main { max-width: 760px; margin: 0 auto; padding: 28px 16px 56px; }
.sup { margin: 0 0 6px; font: 700 12px/1.2 Inter, system-ui, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: var(--mudo); }
h1 { margin: 0 0 10px; font: 700 clamp(30px, 7vw, 42px)/1.1 Newsreader, Georgia, serif; color: var(--navy); }
.intro { margin: 0 0 26px; color: var(--mudo); }
.cartoes { display: grid; gap: 14px; padding: 0; margin: 0; list-style: none; }
.cartao { background: var(--cartao); border: 1px solid var(--linha); border-radius: 14px; padding: 18px 18px 16px; }
.cartao h2 { margin: 0 0 6px; font: 700 22px/1.2 Newsreader, Georgia, serif; color: var(--navy); }
.cartao p { margin: 0 0 12px; font-size: 16px; }
.end { margin: 0 0 14px; font: 500 13px/1.4 ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--mudo); word-break: break-all; }
.acoes { display: flex; flex-wrap: wrap; gap: 10px; }
.acoes a { display: inline-block; padding: 9px 18px; border-radius: 999px; font: 600 15px/1.2 Inter, system-ui, sans-serif; text-decoration: none; border: 1.5px solid var(--navy); color: var(--navy); }
.acoes a.principal { background: var(--navy); color: var(--creme); }
.acoes a:focus-visible { outline: 3px solid var(--ouro); outline-offset: 2px; }
.sem { font: 600 13px/1.2 Inter, system-ui, sans-serif; color: var(--mudo); align-self: center; }
'''


def esc(t):
    return html.escape(t, quote=True)


def pagina_indice():
    cartoes = []
    for it in ITENS:
        publ = ('<a href="../%s">Ver a versão publicada</a>' % esc(it['publicada'])) if it['publicada'] else '<span class="sem">Ainda não publicado</span>'
        cartoes.append(
            '<li class="cartao"><h2>%s</h2><p>%s</p><p class="end">/desenvolvimento/%s/</p>'
            '<div class="acoes"><a class="principal" href="%s/">Abrir o desenvolvimento</a>%s</div></li>'
            % (esc(it['titulo']), esc(it['resumo']), esc(it['nome']), esc(it['nome']), publ))
    return '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Em desenvolvimento · Meditações Bíblicas</title>
<style>%s</style>
</head>
<body>
<div class="faixa">EM DESENVOLVIMENTO · página de uso interno, sem link no site</div>
<main>
<p class="sup">Meditações Bíblicas</p>
<h1>Em desenvolvimento</h1>
<p class="intro">Tudo o que está sendo feito mas ainda não foi publicado fica aqui, em <b>/desenvolvimento/</b>. Cada item tem o seu endereço curto: <b>/desenvolvimento/nome-do-item/</b>.</p>
<ul class="cartoes">
%s
</ul>
</main>
</body>
</html>
''' % (CSS, '\n'.join(cartoes))


def pagina_atalho(it):
    alvo = '../../%s-desenvolvimento/' % it['pasta']
    return '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=%(alvo)s">
<title>%(titulo)s · em desenvolvimento</title>
<script>location.replace(%(alvo_js)r + location.search + location.hash);</script>
</head>
<body style="font-family: system-ui, sans-serif; padding: 24px;">
<p>Abrindo <b>%(titulo)s</b> em desenvolvimento… Se não abrir, <a href="%(alvo)s">clique aqui</a>.</p>
</body>
</html>
''' % dict(alvo=alvo, alvo_js=alvo, titulo=esc(it['titulo']))


def main():
    os.makedirs(DEST, exist_ok=True)
    # remove atalhos antigos que não estão mais na lista (só subpastas com index.html gerado por este script)
    nomes = {it['nome'] for it in ITENS}
    for nome in os.listdir(DEST):
        p = os.path.join(DEST, nome)
        if os.path.isdir(p) and nome not in nomes and os.listdir(p) == ['index.html']:
            shutil.rmtree(p)
    with open(os.path.join(DEST, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina_indice())
    for it in ITENS:
        real = os.path.join(RAIZ, 'public', it['pasta'] + '-desenvolvimento')
        if not os.path.isdir(real):
            sys.exit('pasta de desenvolvimento não existe: %s' % real)
        d = os.path.join(DEST, it['nome'])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(pagina_atalho(it))
    print('desenvolvimento ok:', DEST, '| itens:', ', '.join(it['nome'] for it in ITENS))


main()

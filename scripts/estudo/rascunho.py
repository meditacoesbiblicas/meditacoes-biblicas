#!/usr/bin/env python3
"""Rascunho (versão em desenvolvimento) e backup do estudo "Sermão do Monte".

Forma de trabalho combinada com o dono do site:
  1. Toda mudança nova vai primeiro para a versão EM DESENVOLVIMENTO, uma cópia do estudo em
         public/bem-aventurancas-desenvolvimento/
     (endereço sem link em lugar nenhum, com <meta robots noindex> e uma faixa laranja "VERSÃO EM DESENVOLVIMENTO").
  2. O dono compara com a versão publicada (public/bem-aventurancas/).
  3. Só quando ele diz "coloca em produção" se roda `promover`. Ele guarda antes, automaticamente, o BACKUP da versão
     publicada que está no ar, em
         public/bem-aventurancas-backup/
     (cada publicação sobrescreve o backup: ele é sempre "o que estava no ar antes da última publicação").

Regra de nomes: nome do original + "-desenvolvimento" e nome do original + "-backup".

Comandos:
  python3 scripts/estudo/rascunho.py criar     copia a versão publicada para o rascunho (sobrescreve o rascunho!)
  python3 scripts/estudo/rascunho.py backup    só guarda a cópia de backup da versão publicada
  python3 scripts/estudo/rascunho.py promover  faz o backup e copia o rascunho para a versão publicada, SÓ com as bem-aventuranças
                                               e a conclusão (sal e luz, a lei, raiva e cobiça ficam "A construir"); `--completo`
                                               publica tudo; `--destino DIR` faz um ensaio numa pasta qualquer (sem backup e sem
                                               tocar na publicada)

As páginas HTML do rascunho e do backup diferem das publicadas só por: a meta noindex, a faixa de aviso no rodapé da janela e o
contador de visitas, que fica comentado (`<!--PIXEL ...-->`). `desrascunhar` desfaz isso. As três pastas ficam no mesmo nível,
então os links relativos (inclusive os da barra do site, `../`) são os mesmos nas três.
Os geradores (build_pages.py e build_index.py) aceitam --rascunho e já gravam nessa forma.
"""
import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PUBLICO = os.path.join(RAIZ, 'public')
PASTA_PUBLICADA = 'bem-aventurancas'
PASTA_RASCUNHO = 'bem-aventurancas-desenvolvimento'
PASTA_BACKUP = 'bem-aventurancas-backup'
PUBLICADA = os.path.join(PUBLICO, PASTA_PUBLICADA)
RASCUNHO = os.path.join(PUBLICO, PASTA_RASCUNHO)
BACKUP = os.path.join(PUBLICO, PASTA_BACKUP)
NAO_COPIAR = {'CLAUDE.md', '.DS_Store'}

NOINDEX = '<meta name="robots" content="noindex, nofollow">\n'
CSS_FAIXA = '''
/* ---------- faixa de aviso (só existe nas cópias de rascunho e de backup) ---------- */
.rascunho-faixa { position: fixed; left: 0; right: 0; bottom: 0; z-index: 9999; padding: 7px 14px; background: #B3541E; color: #fff; text-align: center; font: 600 13px/1.3 var(--sans, system-ui); letter-spacing: .02em; box-shadow: 0 -2px 10px rgba(0, 0, 0, .25); }
.rascunho-faixa.backup { background: #3A4A73; }
.rascunho-faixa a { color: #FFE9C7; }
/* a faixa fixa não pode cobrir a dica da ilustração ampliada */
body.ampliada:has(.rascunho-faixa) { --faixa: 38px; }
@media (max-width: 760px) { body.ampliada:has(.rascunho-faixa) { --faixa: 58px; } }
'''


def faixa(nome, tipo='rascunho'):
    if tipo == 'backup':
        return ('<div class="rascunho-faixa backup">BACKUP da versão anterior · guardada antes da última publicação · '
                '<a href="../%s/%s">ver a versão atual desta página</a></div>\n' % (PASTA_PUBLICADA, nome))
    return ('<div class="rascunho-faixa">VERSÃO EM DESENVOLVIMENTO · ainda não publicada · '
            '<a href="../%s/%s">ver a versão publicada desta página</a></div>\n' % (PASTA_PUBLICADA, nome))


def rascunhar(html, nome, tipo='rascunho'):
    """Publicada -> rascunho (ou backup)."""
    if 'rascunho-faixa' in html:
        return html
    html = html.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + NOINDEX, 1)
    html = re.sub(r'(<body[^>]*>\n)', lambda m: m.group(1) + faixa(nome, tipo), html, count=1)
    # contador de visitas desligado (visitas ao rascunho/backup não contam)
    html = re.sub(r'(<img src="https://meditacoesbiblicas\.goatcounter\.com/[^>]*>)', r'<!--PIXEL\1-->', html)
    return html


def desrascunhar(html):
    """Rascunho (ou backup) -> publicada (desfaz `rascunhar`)."""
    html = html.replace(NOINDEX, '', 1)
    html = re.sub(r'<div class="rascunho-faixa[^"]*">.*?</div>\n', '', html, count=1, flags=re.S)
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


def _copiar_como(origem_dir, destino_dir, tipo):
    if os.path.isdir(destino_dir):
        shutil.rmtree(destino_dir)
    os.makedirs(destino_dir)
    for nome in _arquivos(origem_dir):
        origem = os.path.join(origem_dir, nome)
        destino = os.path.join(destino_dir, nome)
        if nome.endswith('.html'):
            gravar(destino_dir, nome, rascunhar(open(origem, encoding='utf-8').read(), nome, tipo), False)
        elif nome == 'style.css':
            css = open(origem, encoding='utf-8').read()
            if '.rascunho-faixa' not in css:
                css += CSS_FAIXA
            open(destino, 'w', encoding='utf-8').write(css)
        else:
            shutil.copy2(origem, destino)


def criar():
    _copiar_como(PUBLICADA, RASCUNHO, 'rascunho')
    print('Rascunho criado em', RASCUNHO)


def backup():
    _copiar_como(PUBLICADA, BACKUP, 'backup')
    print('Backup guardado em', BACKUP)


# páginas que o dono ainda não leu: por enquanto não vão para a versão publicada (ficam como "A construir" lá e prontas no rascunho)
EXCLUIR_PARCIAL = {'v13-15.html', 'v17-20.html', 'v21-26.html', 'v27-30.html', 'depois.html'}


def promover(destino=None, parcial=True):
    """Rascunho -> versão publicada, depois de guardar o backup da que está no ar. Com parcial=True (padrão, vontade do dono), só vão
    as bem-aventuranças e a conclusão: sal e luz, a lei, raiva e cobiça ficam "A construir" na publicada e a trilha não é publicada.
    As páginas geradas são refeitas em modo --parcial."""
    import subprocess
    import tempfile
    if not os.path.isdir(RASCUNHO):
        sys.exit('Não existe rascunho.')
    if destino is None:
        backup()
    destino = destino or PUBLICADA
    aqui = os.path.dirname(os.path.abspath(__file__))
    tmp = tempfile.mkdtemp()
    for nome in _arquivos(RASCUNHO):  # imagens etc. (a conclusão usa conclusao.jpg se existir)
        if not nome.endswith('.html'):
            shutil.copy2(os.path.join(RASCUNHO, nome), os.path.join(tmp, nome))
    extra = ['--parcial'] if parcial else []
    subprocess.check_call([sys.executable, os.path.join(aqui, 'build_pages.py'), tmp] + extra, stdout=subprocess.DEVNULL)
    subprocess.check_call([sys.executable, os.path.join(aqui, 'build_index.py'), tmp] + extra, stdout=subprocess.DEVNULL)
    geradas = {n for n in os.listdir(tmp) if n.endswith('.html')}
    os.makedirs(destino, exist_ok=True)
    finais = set()
    for nome in _arquivos(RASCUNHO):
        if parcial and nome in EXCLUIR_PARCIAL:
            continue
        origem = os.path.join(RASCUNHO, nome)
        alvo = os.path.join(destino, nome)
        if nome in geradas:
            shutil.copy2(os.path.join(tmp, nome), alvo)
        elif nome.endswith('.html'):
            with open(alvo, 'w', encoding='utf-8') as f:
                f.write(desrascunhar(open(origem, encoding='utf-8').read()))
        else:
            shutil.copy2(origem, alvo)
        finais.add(nome)
    for nome in _arquivos(destino):
        if nome not in finais:
            os.remove(os.path.join(destino, nome))
            print('Removido da publicada:', nome)
    shutil.rmtree(tmp, ignore_errors=True)
    print('Rascunho promovido para', destino, '(parcial)' if parcial else '(completo)')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'criar':
        criar()
    elif cmd == 'backup':
        backup()
    elif cmd == 'promover':
        dest = sys.argv[sys.argv.index('--destino') + 1] if '--destino' in sys.argv else None
        promover(dest, parcial='--completo' not in sys.argv)
    else:
        print(__doc__)

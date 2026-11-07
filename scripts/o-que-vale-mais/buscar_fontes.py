# -*- coding: utf-8 -*-
# Busca ao vivo os textos citados no estudo "O que vale mais?" e grava em fontes_cache.json:
#   - versículos na ARC (bibliaonline.com.br, JSON-LD de cada versículo);
#   - parágrafos da Ellen G. White em português (m.egwwritings.org/pt/book/<livro>.<parágrafo>).
# O gerador (build.py) usa o cache; o verificador (verify.py) confere de novo, ao vivo, cada trecho citado nas páginas.
# Uso: python3 scripts/o-que-vale-mais/buscar_fontes.py
import html
import json
import os
import re
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, 'fontes_cache.json')

# (livro-slug, capítulo, [versículos])
BIBLIA = [
    ('sl', 19, [1]), ('is', 40, [26, 22, 12]), ('sl', 8, [3, 4, 5]), ('gn', 1, [1, 26, 27, 28]), ('gn', 2, [2, 15]),
    ('hb', 1, [3]), ('cl', 1, [16, 17]), ('sl', 104, [30]), ('is', 65, [17]), ('ap', 21, [5]),
    ('sl', 11, [4]), ('sl', 103, [19]), ('sl', 139, [7, 8, 9, 10, 13, 14, 15, 16]),
    ('jo', 14, [16, 17]), ('mt', 28, [2, 3]), ('dn', 9, [21, 22, 23]), ('ez', 1, [14]),
    ('ex', 21, [32]), ('mt', 26, [15]), ('zc', 11, [12, 13]),
    ('jo', 3, [16]), ('rm', 5, [8]), ('rm', 8, [32]), ('1pe', 1, [17, 18, 19]), ('1co', 6, [20]), ('1co', 7, [23]),
    ('jo', 1, [1, 14]), ('fp', 2, [6, 7, 8]), ('sl', 130, [4]), ('mt', 10, [29, 30, 31]), ('1jo', 3, [1]),
    ('jo', 16, [7]), ('mt', 28, [19]),
    ('1rs', 8, [27]), ('is', 66, [1]), ('jr', 23, [23, 24]), ('is', 45, [12]), ('job', 38, [4]), ('gn', 37, [28]), ('sl', 49, [7, 8]),
    ('is', 55, [1]), ('ef', 2, [8, 9]), ('rm', 6, [23]), ('tt', 2, [14]), ('gl', 2, [20]), ('is', 43, [1, 4]),
]
# parágrafos EGW (id do livro . id do parágrafo)
EGW = ['1948.670', '1948.581', '1807.329', '11255.2247', '11125.3050', '1931.919', '11099.1756', '1806.1717', '1813.3468', '1813.3470']

UA = {'User-Agent': 'Mozilla/5.0'}


def verso(livro, cap, v):
    url = 'https://www.bibliaonline.com.br/arc/%s/%d/%d' % (livro, cap, v)
    s = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode('utf-8', 'ignore')
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        if isinstance(d, dict) and d.get('text'):
            return re.sub(r'\s+', ' ', d['text']).strip()
    return None


def egw(pid):
    s = urllib.request.urlopen(urllib.request.Request('https://m.egwwritings.org/pt/book/' + pid, headers=UA), timeout=40).read().decode('utf-8', 'ignore')
    m = re.search(r'<p class="egw_content_wrapper[^"]*"[^>]*data-para-id="%s"[^>]*>(.*?)</p>' % re.escape(pid), s, re.S)
    if not m:
        return None
    sp = re.search(r'<span class="egw_content"[^>]*>(.*?)</span>\s*<span class="egw_refcode"', m.group(1), re.S)
    ref = re.search(r'egw_refcode[^>]*>(.*?)</span>', m.group(1), re.S)
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', sp.group(1) if sp else m.group(1)))).strip()
    r = re.sub(r'<[^>]+>', '', ref.group(1)).strip() if ref else ''
    return {'texto': t, 'ref': r}


def main():
    cache = {'biblia': {}, 'egw': {}}
    if os.path.exists(SAIDA) and '--tudo' not in sys.argv:
        cache = json.load(open(SAIDA, encoding='utf-8'))
    falhas = []
    for livro, cap, vs in BIBLIA:
        for v in vs:
            k = '%s/%d/%d' % (livro, cap, v)
            if k in cache['biblia']:
                continue
            t = verso(livro, cap, v)
            if t:
                cache['biblia'][k] = t
            else:
                falhas.append(k)
    for pid in EGW:
        if pid in cache['egw']:
            continue
        r = egw(pid)
        if r:
            cache['egw'][pid] = r
        else:
            falhas.append('egw ' + pid)
    with open(SAIDA, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=1, sort_keys=True)
    print('versículos:', len(cache['biblia']), '| parágrafos EGW:', len(cache['egw']), '| falhas:', falhas)


if __name__ == '__main__':
    main()

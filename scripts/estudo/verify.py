# -*- coding: utf-8 -*-
# Confere cada trecho citado nas páginas contra o texto real (bibliaonline e EGW Writings).
import re, sys, html, json, glob, os, urllib.request

# Confere cada trecho citado nas páginas contra o texto real: versículos no bibliaonline (ARC/BKJ/ARA) e Ellen White
# no site oficial (m.egwwritings.org/pt). Uso: python3 scripts/estudo/verify.py <pasta-com-as-páginas>
PASTA = sys.argv[1]
_egw = {}


def egw_texto(pid):
    """Texto do parágrafo EGW <livro>.<parágrafo> (buscado ao vivo e guardado em memória)."""
    if pid not in _egw:
        s = urllib.request.urlopen(urllib.request.Request('https://m.egwwritings.org/pt/book/' + pid, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read().decode('utf-8', 'ignore')
        m = re.search(r'<p class="egw_content_wrapper[^"]*"[^>]*data-para-id="%s"[^>]*>(.*?)</p>' % re.escape(pid), s, re.S)
        txt = ''
        if m:
            sp = re.search(r'<span class="egw_content"[^>]*>(.*?)</span>\s*<span class="egw_refcode"', m.group(1), re.S)
            txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', sp.group(1) if sp else m.group(1)))).strip()
        _egw[pid] = txt
    return _egw[pid]


cache = {}
def verso(ver, livro, cap, v):
    k = (ver, livro, cap, v)
    if k not in cache:
        url = f'https://www.bibliaonline.com.br/{ver}/{livro}/{cap}/{v}'
        s = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read().decode('utf-8', 'ignore')
        txt = None
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try: d = json.loads(m.group(1))
            except Exception: continue
            if isinstance(d, dict) and d.get('text'): txt = d['text']; break
        cache[k] = txt
    return cache[k]

def norm(t):
    t = html.unescape(t)
    t = t.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    t = re.sub(r'\s+', ' ', t).strip().casefold()
    return t

def pedacos(h):
    h = re.sub(r'<span class="n">\d+</span>', '', h)
    h = re.sub(r'</?mark>', '', h)
    h = re.sub(r'<[^>]+>', '', h)
    out = []
    for p in re.split(r'…', h):
        p = norm(p).strip(' .,;:!?"')
        if len(p) >= 4: out.append(p)
    return out

erros = 0; checados = 0
for arq in sorted(glob.glob(os.path.join(PASTA, 'v*.html')) + glob.glob(os.path.join(PASTA, 'conclusao.html')) + glob.glob(os.path.join(PASTA, 'de-cima.html'))):
    s = open(arq, encoding='utf-8').read()
    for art in re.findall(r'<article class="note [a-z]+"[^>]*>.*?</article>', s, re.S):
        h3 = re.sub(r'<[^>]+>', '', re.search(r'<h3[^>]*>(.*?)</h3>', art, re.S).group(1)).strip()
        cor = re.search(r'class="note ([a-z]+)"', art).group(1)
        bq = re.search(r'<blockquote class="text">(.*?)</blockquote>', art, re.S)
        if not bq or cor == 'gray':
            continue
        paras = re.findall(r'<p>(.*?)</p>', bq.group(1), re.S)
        link = re.search(r'href="(https://[^"]+)"', art).group(1)
        m = re.match(r'https://www\.bibliaonline\.com\.br/(arc|bkj|ara)/([^/]+)/(\d+)/(\d+)\+', link)
        if m:
            ver, livro, cap, v0 = m.groups()
            for p in paras:
                nl = re.search(r'<span class="n">(\d+)</span>', p)
                v = nl.group(1) if nl else v0
                texto = verso(ver, livro, cap, v)
                alvo = norm(texto or '')
                for pe in pedacos(p):
                    checados += 1
                    if pe not in alvo:
                        erros += 1
                        print(f'  ✗ {os.path.basename(arq)} | {h3} ({ver} {livro} {cap}:{v}) | não achei: "{pe[:90]}"')
            continue
        m = re.match(r'https://m\.egwwritings\.org/pt/book/([0-9.]+)', link)
        if m:
            alvo = norm(egw_texto(m.group(1)))
            for p in paras:
                for pe in pedacos(p):
                    checados += 1
                    if pe not in alvo:
                        erros += 1
                        print(f'  ✗ {os.path.basename(arq)} | {h3} (EGW {m.group(1)}) | não achei: "{pe[:90]}"')
print(f'\n{checados} trechos conferidos; {erros} divergência(s).')

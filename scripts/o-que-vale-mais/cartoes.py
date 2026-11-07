# -*- coding: utf-8 -*-
# Cartões de leitura do estudo "O que vale mais?": versículos (ARC), Ellen G. White (português), dados conferidos, reflexões e imaginação.
# Os textos vêm de fontes_cache.json (buscados ao vivo por buscar_fontes.py) e são conferidos de novo por verify.py.
import html as H
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
CACHE = json.load(open(os.path.join(AQUI, 'fontes_cache.json'), encoding='utf-8'))

NOMES = {'sl': 'Salmo', 'is': 'Isaías', 'gn': 'Gênesis', 'hb': 'Hebreus', 'cl': 'Colossenses', 'ap': 'Apocalipse', 'jo': 'João', 'mt': 'Mateus',
         'dn': 'Daniel', 'ez': 'Ezequiel', 'ex': 'Êxodo', 'zc': 'Zacarias', 'rm': 'Romanos', '1pe': '1 Pedro', '1co': '1 Coríntios',
         'fp': 'Filipenses', '1jo': '1 João', '1rs': '1 Reis', 'jr': 'Jeremias', 'job': 'Jó', 'ef': 'Efésios', 'tt': 'Tito', 'gl': 'Gálatas'}


def esc(s):
    return H.escape(s, quote=False)


def _marcar(txt, marcas):
    out = esc(txt)
    for m in marcas or []:
        me = esc(m)
        assert me in out, 'trecho a marcar não existe: %r em %r' % (m, txt)
        out = out.replace(me, '<mark>' + me + '</mark>', 1)
    return out


def referencia(chaves):
    """['sl/139/7','sl/139/8'] -> 'Salmo 139:7–8'"""
    livro, cap, _ = chaves[0].split('/')
    vs = [int(c.split('/')[2]) for c in chaves]
    partes = []
    ini = prev = vs[0]
    for v in vs[1:] + [None]:
        if v is not None and v == prev + 1:
            prev = v
            continue
        partes.append(str(ini) if ini == prev else '%d–%d' % (ini, prev) if prev - ini > 1 else '%d, %d' % (ini, prev))
        if v is not None:
            ini = prev = v
    return '%s %s:%s' % (NOMES[livro], cap, ', '.join(partes))


def biblia(chaves, marcas=None, antes=None, titulo=None, tag='Bíblia · ARC'):
    """Cartão de versículo(s) da ARC. `chaves` = ['sl/19/1', ...] (mesmo capítulo); `marcas` = {chave: [trechos a destacar]}."""
    marcas = marcas or {}
    livro, cap, v1 = chaves[0].split('/')
    paras = []
    for c in chaves:
        n = c.split('/')[2]
        txt = CACHE['biblia'][c]
        paras.append('<p><span class="n">%s</span>%s</p>' % (n, _marcar(txt, marcas.get(c))))
    corpo = '\n      '.join(paras)
    ref = referencia(chaves)
    return ('''<article class="cartao biblia" data-ref="%s">
  <span class="tag">%s</span>
  <h3>%s</h3>%s
  <blockquote>
      %s
  </blockquote>
  <a class="fonte" href="https://www.bibliaonline.com.br/arc/%s/%s/%s+" target="_blank" rel="noopener">Ler o texto completo na ARC ↗</a>
</article>''' % (','.join(chaves), tag, esc(titulo or ref), ('\n  <p class="antes">%s</p>' % antes) if antes else '', corpo, livro, cap, v1))


def egw(pid, titulo, marcas=None, trecho=None, antes=None):
    """Cartão da Ellen G. White: sempre trecho literal em português, com o link do parágrafo no site oficial."""
    d = CACHE['egw'][pid]
    txt = trecho or d['texto']
    if trecho:
        assert trecho in d['texto'], 'trecho não está no parágrafo %s' % pid
    pre = '… ' if trecho and not d['texto'].startswith(trecho) else ''
    pos = ' …' if trecho and not d['texto'].endswith(trecho) else ''
    corpo = '<p>%s%s%s</p>' % (pre, _marcar(txt, marcas), pos)
    return ('''<article class="cartao egw" data-egw="%s">
  <span class="tag">Ellen G. White</span>
  <h3>%s</h3>%s
  <blockquote>
      %s
  </blockquote>
  <a class="fonte" href="https://m.egwwritings.org/pt/book/%s" target="_blank" rel="noopener">Abrir o trecho no site do Ellen G. White ↗</a>
</article>''' % (pid, esc(titulo), ('\n  <p class="antes">%s</p>' % antes) if antes else '', corpo, pid))


def _simples(classe, tag, titulo, corpo, fontes=None, extra=''):
    links = ''.join('\n  <a class="fonte" href="%s" target="_blank" rel="noopener">%s ↗</a>' % (u, esc(l)) for l, u in (fontes or []))
    return '''<article class="cartao %s"%s>
  <span class="tag">%s</span>
  <h3>%s</h3>
  %s%s
</article>''' % (classe, extra, tag, esc(titulo), corpo, links)


def fato(titulo, corpo, fontes=None, obs=None):
    """Dado conferido, com a fonte e a data da conferência."""
    c = corpo + (('\n  <p class="obs">%s</p>' % obs) if obs else '')
    return _simples('fato', 'Dado conferido', titulo, c, fontes)


def reflexao(titulo, corpo):
    """Ideia do estudo que NÃO é ensino direto da Bíblia nem de Ellen White: sempre marcada como reflexão."""
    return _simples('reflexao', 'Reflexão (não é afirmação da Bíblia)', titulo, corpo)


def imaginacao(titulo, corpo):
    """Cena imaginada: nunca apresentada como fato."""
    return _simples('imaginacao', 'Imaginação (não está escrito)', titulo, corpo)


def curiosos(titulo, corpo):
    return '<details class="curiosos">\n  <summary>%s</summary>\n  <div>%s</div>\n</details>' % (esc(titulo), corpo)


def grade(cartoes, um=False):
    return '<div class="cartoes%s">\n%s\n</div>' % (' um' if um else '', '\n'.join(cartoes))

# -*- coding: utf-8 -*-
# Gera as páginas de detalhe do estudo (bem-aventuranças, sal e luz, a lei, raiva, cobiça) e a trilha (depois.html).
# Conteúdo para o público, sem descrição de marcas do dono.
# Uso: python3 scripts/estudo/build_pages.py <pasta-de-saída> [--rascunho]
#   --rascunho: grava na forma do rascunho (noindex, faixa, contador desligado); ver rascunho.py.
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

# uma página por bem-aventurança (a porta N do caminho)
PAGINAS = [
    ('v03.html', '1 · v.3'), ('v04.html', '2 · v.4'), ('v05.html', '3 · v.5'), ('v06.html', '4 · v.6'),
    ('v07.html', '5 · v.7'), ('v08.html', '6 · v.8'), ('v09.html', '7 · v.9'), ('v10-12.html', '8 · v.10–12'),
]
DEPOIS = [
    ('depois.html', 'Trilha'), ('v13-15.html', 'Sal e luz'), ('v17-20.html', 'A lei'),
    ('v21-26.html', 'Raiva'), ('v27-30.html', 'Cobiça'),
]


def pixel(arq):
    return ('<!-- contagem de visitas (GoatCounter): sem JavaScript e sem cookies; o caminho em p= precisa bater com a URL publicada -->\n'
            '<img src="https://meditacoesbiblicas.goatcounter.com/count?p=/meditacoes-biblicas/bem-aventurancas/%s" width="1" height="1" alt="">' % arq)


def crumbs(atual):
    li = []
    for arq, rot in PAGINAS + [('conclusao.html', 'Conclusão')]:
        cur = ' aria-current="page"' if arq == atual else ''
        li.append('    <li><a href="%s"%s>%s</a></li>' % (arq, cur, rot))
    for i, (arq, rot) in enumerate(DEPOIS):
        cur = ' aria-current="page"' if arq == atual else ''
        cls = ' class="after"' if i == 0 else ''
        li.append('    <li%s><a href="%s"%s>%s</a></li>' % (cls, arq, cur, rot))
    voltar = '<a class="back" href="index.html">← Sermão do Monte</a>'
    if atual in [a for a, _ in PAGINAS] + [('conclusao.html', '')]:
        # nas páginas das bem-aventuranças, o 2º botão volta para a ilustração de onde o leitor veio (ampliada ou página do caminho); o script abaixo troca o destino
        voltar += '\n    <a class="back" id="voltar-origem" href="caminho-ampliado.html">← A ilustração das portas</a>'
    return ('<nav class="crumbs" aria-label="Navegação">\n  <div class="voltares">\n    ' + voltar + '\n  </div>\n  <ul class="pages">\n'
            + '\n'.join(li) + '\n  </ul>\n</nav>')


def pager(prev, nxt):
    return ('<nav class="pager" aria-label="Anterior e próxima">\n'
            '  <a class="prev" href="%s"><span class="dir">%s</span>%s</a>\n'
            '  <a class="next" href="%s"><span class="dir">%s</span>%s</a>\n</nav>'
            % (prev[0], prev[1], prev[2], nxt[0], nxt[1], nxt[2]))


def bq(*paras):
    if len(paras) == 1:
        return '<blockquote class="text"><p>%s</p></blockquote>' % paras[0]
    return '<blockquote class="text">\n' + '\n'.join('        <p>%s</p>' % p for p in paras) + '\n      </blockquote>'


def n(num, txt):
    return '<span class="n">%s</span>%s' % (num, txt)


def arc(ref):
    return ('<a class="full" href="https://www.bibliaonline.com.br/arc/%s+" target="_blank" rel="noopener">'
            'Ler o texto completo na ARC ↗</a>' % ref)


def bkj(ref):
    return ('<a class="full" href="https://www.bibliaonline.com.br/bkj/%s+" target="_blank" rel="noopener">'
            'Ler o texto completo na King James ↗</a>' % ref)


def ara(ref):
    return ('<a class="full" href="https://www.bibliaonline.com.br/ara/%s+" target="_blank" rel="noopener">'
            'Ler o texto completo na ARA ↗</a>' % ref)


def egw(par):
    return ('<a class="full" href="https://m.egwwritings.org/pt/book/%s" target="_blank" rel="noopener">'
            'Abrir o trecho no site do Ellen G. White ↗</a>' % par)


KJ = ' <span class="ver">King James</span>'
ARA = ' <span class="ver">ARA</span>'


def card(cor, tag, h3, corpo=None, obs=None, link=None, extra_p=None, antes=None):
    partes = ['    <article class="note %s">' % cor,
              '      <span class="tag">%s</span>' % tag,
              '      <h3>%s</h3>' % h3]
    if antes:
        # explicação ANTES do versículo, para quem não vê de cara a ligação com a bem-aventurança
        partes.append('      <p class="antes">%s</p>' % antes)
    if corpo:
        partes.append('      ' + corpo)
    for p in (extra_p or []):
        partes.append('      <p>%s</p>' % p)
    if obs:
        partes.append('      <p class="obs">%s</p>' % obs)
    if link:
        partes.append('      ' + link)
    partes.append('    </article>')
    return '\n'.join(partes)


# cada bem-aventurança é uma porta do caminho (ver caminho.html): v.3 = porta 1 ... v.10 = porta 8
PORTA = {'v3': 1, 'v4': 2, 'v5': 3, 'v6': 4, 'v7': 5, 'v8': 6, 'v9': 7, 'v10': 8}


def grupo(gid, ref, h2, bible_html, notas, subs=None):
    """notas: lista de strings (cards) ou ('sub', 'texto') para h4."""
    corpo = []
    for x in notas:
        if isinstance(x, tuple):
            corpo.append('    <h4 class="sub">%s</h4>' % x[1])
        else:
            corpo.append(x)
    if gid in PORTA:
        ref = '<b class="no">%d</b>Porta %d · %s' % (PORTA[gid], PORTA[gid], ref)
    return ('<section class="group" id="%s">\n  <aside class="verse">\n    <span class="ref">%s</span>\n    <h2>%s</h2>\n    %s\n  </aside>\n  <div class="notes">\n\n'
            % (gid, ref, h2, bible_html) + '\n\n'.join(corpo) + '\n\n  </div>\n</section>')


ORIGEM = '''<script>
/* lembra de onde o leitor veio (ilustração ampliada ou página do caminho) para os botões "voltar à imagem" levarem ao lugar certo */
try{var o=sessionStorage.getItem('origem-bem-aventurancas'),m=o==='caminho'?['caminho.html','O caminho e as portas']:['caminho-ampliado.html','A ilustração das portas'];
var b=document.getElementById('voltar-origem');if(b){b.href=m[0];b.textContent='← '+m[1];}
var v=document.getElementById('volta-imagem');if(v){v.href=m[0];}
var p=document.getElementById('prev-origem');if(p){p.href=m[0];p.lastChild.textContent=m[1];}}catch(e){}
</script>'''


# quem chega pela animação da porta (caminho-ampliado.html) entra na página saindo da mesma luz; a classe vai no <html> antes de a página aparecer
ENTRADA = '''<script>try{var t=+sessionStorage.getItem('porta-aberta');if(t){sessionStorage.removeItem('porta-aberta');if(Date.now()-t<8000)document.documentElement.className+=' entrando';}}catch(e){}</script>
'''


def pagina(arq, titulo, kicker, h1, sub, grupos, pg, comentario='', final=''):
    cab = '<header class="top">\n  <p class="kicker">%s</p>\n  <h1>%s</h1>' % (kicker, h1)
    if sub:
        cab += '\n  <p>%s</p>' % sub
    cab += '\n</header>'
    html = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<link rel="stylesheet" href="style.css">\n%s</head>\n<body>\n%s\n<div class="wrap">\n\n%s\n\n%s\n\n%s'
            % (titulo, ENTRADA if arq in [a for a, _ in PAGINAS] else '', BARRA, crumbs(arq), cab, comentario))
    html += '\n'.join(['\n' + g + '\n' for g in grupos])
    extra = ('\n' + ORIGEM) if arq in [a for a, _ in PAGINAS] else ''
    html += '\n%s\n\n%s\n\n</div>\n%s%s\n</body>\n</html>\n' % (final, pg, pixel(arq), extra)
    gravar(DEST, arq, html, RASC)


# botão no fim de cada bem-aventurança: volta à ilustração (a imagem é usada na palestra)
VOLTA = '''<div class="volta-imagem">
  <a class="botao-volta" id="volta-imagem" href="caminho-ampliado.html">← Voltar à imagem das portas</a>
</div>'''


# fim da porta 8: leva à conclusão de todas as bem-aventuranças (só quem chegou até aqui a lê) e à imagem
FINAL8 = '''<aside class="cc-convite" aria-labelledby="cc-conv-t">
  <div class="cc-conv-sinal" aria-hidden="true"><span class="p">(</span><span class="pts"><i></i><i></i><i></i><i></i><i></i><i></i></span><span class="p">)</span></div>
  <div class="cc-conv-texto">
    <p class="cc-conv-kicker">Você chegou à última porta</p>
    <h2 id="cc-conv-t">Conclusão das bem-aventuranças</h2>
    <p>Olhe para as oito de uma vez: a moldura que a primeira e a última formam, o que cresce entre elas e o que cada ponta tem de oposto.</p>
    <a class="cc-conv-botao" href="conclusao.html">Ler a conclusão →</a>
  </div>
</aside>
<div class="volta-imagem fim">
  <a class="botao-volta" id="volta-imagem" href="caminho-ampliado.html">← Voltar à imagem das portas</a>
</div>'''


def bible(*paras):
    if len(paras) == 1:
        return '<blockquote class="bible"><p>%s</p></blockquote>' % paras[0]
    return '<blockquote class="bible">\n' + '\n'.join('      <p>%s</p>' % p for p in paras) + '\n    </blockquote>'


# =====================================================================================
# As oito bem-aventuranças: UMA PÁGINA POR PORTA (v.3 a v.10-12), com os versículos em ordem
# do mais simples ao mais difícil e uma explicação antes dos versículos que não são óbvios.
# =====================================================================================
COMENT_V03 = '''<!-- Para enriquecer: copie um bloco <article class="note ..."> e troque a cor (blue, orange, green, purple ou gray), o título e o texto.
     Para destacar a parte do versículo que explica a bem-aventurança, envolva-a em <mark>...</mark>.
     Para explicar um versículo antes de citá-lo, coloque <p class="antes">...</p> logo abaixo do título do cartão.
     Texto bíblico: ARC (Almeida Revista e Corrigida); onde o cartão traz o selo "King James", é a BKJ. O link "Ler o texto completo" leva ao versículo inteiro. -->

'''

# ---------- porta 1 · v.3 ----------
v3 = grupo('v3', 'Mateus 5:3', 'Pobres em espírito',
    bible('bem-aventurados <mark>os pobres de espírito</mark>, porque <mark>deles é o Reino dos céus</mark>;'),
    [
    ('sub', 'Quem é o pobre de espírito?'),
    card('blue', 'Paralelo', 'Salmos 51:17',
         antes='Pobre de espírito é quem reconhece a própria necessidade diante de Deus: tem o espírito quebrantado, sem orgulho.',
         corpo=bq('Os sacrifícios para Deus são <mark>o espírito quebrantado</mark>; a um <mark>coração quebrantado e contrito</mark> não desprezarás, ó Deus.'),
         link=arc('sl/51/17')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 7.1',
         corpo=bq('Jesus apresentara a taça de bênçãos aos que se julgavam ricos e de nada carecidos (Apocalipse 3:17)… <mark>O orgulho não sente necessidade</mark>, fechando, pois, o coração a Cristo e às bênçãos infinitas que Ele veio dar.',
                  '…Os que sabem que não se podem salvar a si mesmos… são os que apreciam o auxílio que Cristo pode conceder. <mark>São eles os pobres de espírito, aos quais Ele declara bem-aventurados.</mark>'),
         link=egw('1956.76')),
    ('sub', 'O que Deus faz pelos humildes'),
    card('blue', 'Paralelo', 'Isaías 57:15',
         antes='Deus, que é santo e habita nas alturas, também habita com o humilde.',
         corpo=bq('Em um alto e santo lugar habito e também com <mark>o contrito e abatido de espírito</mark>, para vivificar o espírito dos abatidos…'),
         link=arc('is/57/15')),
    card('blue', 'Paralelo', 'Tiago 4:10',
         corpo=bq('<mark>Humilhai-vos perante o Senhor</mark>, e ele <mark>vos exaltará</mark>.'),
         link=arc('tg/4/10')),
    ('sub', 'O oposto: o orgulho'),
    card('orange', 'Contraste', 'Provérbios 16:18',
         corpo=bq('A <mark>soberba</mark> precede a ruína, e a <mark>altivez do espírito</mark> precede a queda.'),
         link=arc('pv/16/18')),
    card('orange', 'Contraste', 'Apocalipse 3:17',
         antes='Laodiceia é a igreja que se achava rica e sem falta de nada: o oposto exato do pobre de espírito. Jesus mostra o que ela era de verdade.',
         corpo=bq('Como dizes: <mark>Rico sou, e estou enriquecido, e de nada tenho falta</mark>…',
                  '(e não sabes que és um desgraçado, e miserável, e <mark>pobre</mark>, e cego, e nu)'),
         link=arc('ap/3/17')),
    card('orange', 'Contraste', '1 Timóteo 3:6' + KJ,
         antes='Paulo diz como escolher um líder: não alguém recém-chegado, para que o orgulho não o derrube, como derrubou o diabo.',
         corpo=bq('não um principiante, para que, <mark>envaidecendo-se com orgulho</mark>, não caia na condenação do diabo.'),
         link=bkj('1tm/3/6')),
    card('gray', 'Conclusão', 'Pobre de espírito: quem reconhece a sua necessidade',
         extra_p=['A versão Almeida Revista e Atualizada (ARA) traduz “humildes de espírito”. Quem se humilha diante de Deus é exaltado por Ele (Tg 4:10), e Deus habita com o contrito (Is 57:15). O contrário é o orgulho (Pv 16:18) e a igreja de Laodiceia, que se achava rica e sem falta de nada (Ap 3:17).'],
         obs='E repare no tempo do verbo: “deles é o Reino” está no presente. A mesma promessa fecha a lista na <a href="v10-12.html#v10">porta 8</a>.'),
    ])
pagina('v03.html', 'Mateus 5:3 · Pobres em espírito — Sermão do Monte', 'Mateus 5:3 · porta 1', 'Pobres em espírito', None, [v3],
       pager(('caminho-ampliado.html', '← Voltar', 'A ilustração das portas'), ('v04.html', 'Próxima →', 'Porta 2 · Os que choram')).replace('<a class="prev" href="caminho-ampliado.html">', '<a class="prev" id="prev-origem" href="caminho-ampliado.html">'),
       comentario=COMENT_V03, final=VOLTA)

# ---------- porta 2 · v.4 ----------
v4 = grupo('v4', 'Mateus 5:4', 'Os que choram',
    bible('bem-aventurados <mark>os que choram</mark>, porque eles <mark>serão consolados</mark>;'),
    [
    ('sub', 'Que choro é esse?'),
    card('blue', 'Paralelo', '2 Coríntios 7:10',
         antes='Há dois tipos de tristeza, e só uma é a que Jesus abençoa: a tristeza segundo Deus, que leva ao arrependimento.',
         corpo=bq('…a tristeza <mark>segundo Deus</mark> opera <mark>arrependimento para a salvação</mark>… mas a tristeza do mundo opera a morte.'),
         link=arc('2co/7/10')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 9.2',
         corpo=bq('<mark>O pranto aqui apresentado é a sincera tristeza de coração pelo pecado.</mark>… Vemos que foi o pecado que açoitou e crucificou o Senhor da glória.'),
         link=egw('1956.86')),
    ('sub', 'Chorar pelos próprios pecados'),
    card('green', 'Exemplo', 'Lucas 22:61,62',
         antes='Pedro tinha negado a Jesus três vezes. Quando Jesus o olha, ele entende o que fez e chora.',
         corpo=bq(n('61', 'E, virando-se o Senhor, <mark>olhou para Pedro</mark>, e Pedro lembrou-se da palavra do Senhor…'),
                  n('62', 'E, saindo Pedro para fora, <mark>chorou amargamente</mark>.')),
         link=arc('lc/22/61')),
    card('blue', 'Paralelo', 'Tiago 4:9,10',
         antes='Tiago também chama ao pranto por causa do pecado, e promete que quem se humilha será exaltado (compare com a <a href="v03.html#v3">porta 1</a>).',
         corpo=bq(n('9', 'Senti as vossas misérias, e <mark>lamentai, e chorai</mark>; converta-se o vosso riso em pranto, e o vosso gozo, em tristeza.'),
                  n('10', 'Humilhai-vos perante o Senhor, e ele vos exaltará.')),
         link=arc('tg/4/9')),
    ('sub', 'Chorar pelos pecados dos outros'),
    card('green', 'Exemplo', 'Filipenses 3:18,19',
         antes='Aqui Paulo chora, mas não pelos pecados dele: chora pelos que vivem como inimigos da cruz de Cristo. O pranto segundo Deus também sofre pelo pecado dos outros.',
         corpo=bq(n('18', '…muitas vezes vos disse e agora também digo, <mark>chorando</mark>, que são inimigos da cruz de Cristo.'),
                  n('19', 'O fim deles é a perdição, o deus deles é o ventre…')),
         link=arc('fp/3/18')),
    card('green', 'Exemplo', 'Ezequiel 9:4–6',
         antes='Antes de um juízo sobre Jerusalém, Deus manda marcar na testa quem sofre pelo pecado ao redor. Os que têm o sinal são poupados. Chorar pelo pecado, o próprio e o dos outros, é o que marca quem é de Deus.',
         corpo=bq(n('4', '…marca com um sinal as testas dos homens <mark>que suspiram e que gemem</mark> por causa de todas as abominações que se cometem no meio dela.'),
                  n('6', '…mas <mark>a todo o homem que tiver o sinal não vos chegueis</mark>…')),
         link=arc('ez/9/4')),
    ('sub', 'A tristeza que não é segundo Deus'),
    card('orange', 'Contraste', '1 Pedro 4:15,16' + KJ,
         antes='Nem todo sofrimento é o que Deus consola. Padecer por fazer o mal não é tristeza segundo Deus. Mas padecer por ser cristão não é vergonha, e sim motivo para glorificar a Deus (o mesmo trecho aparece na <a href="v10-12.html#v10">porta 8</a>, a dos perseguidos).',
         corpo=bq(n('15', 'Mas que nenhum de vós padeça <mark>como homicida, ou como ladrão, ou como malfeitor</mark>…'),
                  n('16', 'Porém, se algum homem <mark>padece como cristão</mark>, que não se envergonhe, antes glorifique a Deus nisto.')),
         link=bkj('1pe/4/15')),
    card('gray', 'Conclusão', 'A tristeza que Deus consola',
         extra_p=['Nem toda tristeza é a que o v.4 abençoa. A tristeza “segundo Deus” nasce do pecado e leva ao arrependimento: foi a de Pedro (Lc 22:62), é a do que se humilha (Tg 4:9,10) e é a de Paulo, que chora também pelos inimigos da cruz (Fp 3:18). Os que gemem pelas abominações são marcados por Deus (Ez 9:4). A tristeza do mundo opera a morte (2Co 7:10). É a primeira que será consolada.']),
    ])
pagina('v04.html', 'Mateus 5:4 · Os que choram — Sermão do Monte', 'Mateus 5:4 · porta 2', 'Os que choram', None, [v4],
       pager(('v03.html', '← Anterior', 'Porta 1 · Pobres em espírito'), ('v05.html', 'Próxima →', 'Porta 3 · Mansos')), final=VOLTA)

# ---------- porta 3 · v.5 ----------
v5 = grupo('v5', 'Mateus 5:5', 'Mansos',
    bible('bem-aventurados <mark>os mansos</mark>, porque eles <mark>herdarão a terra</mark>;'),
    [
    ('sub', 'Quem é o manso?'),
    card('blue', 'Paralelo', 'Mateus 11:29',
         antes='Jesus descreve a si mesmo com as mesmas palavras: manso e humilde.',
         corpo=bq('Tomai sobre vós o meu jugo, e <mark>aprendei de mim, que sou manso e humilde de coração</mark>, e encontrareis descanso para a vossa alma.'),
         link=arc('mt/11/29')),
    card('blue', 'Paralelo', 'Provérbios 16:32' + KJ,
         antes='Manso não é fraco. É quem governa o próprio espírito, e isso vale mais do que a força.',
         corpo=bq('<mark>Aquele que é tardio em se irar</mark> é melhor do que o poderoso, e <mark>o que domina o seu espírito</mark> do que aquele que toma uma cidade.'),
         link=bkj('pv/16/32')),
    ('sub', 'O que Deus faz pelos mansos'),
    card('blue', 'Paralelo', 'Salmos 25:9',
         corpo=bq('Guiará <mark>os mansos</mark> retamente; e aos <mark>mansos</mark> ensinará o seu caminho.'),
         link=arc('sl/25/9')),
    card('blue', 'Paralelo', 'Salmos 149:4',
         corpo=bq('…o Senhor se agrada do seu povo; ele <mark>adornará os mansos com a salvação</mark>.'),
         link=arc('sl/149/4')),
    card('gray', 'Conclusão', 'Mansidão é domínio próprio',
         extra_p=['O manso governa o seu próprio espírito (Pv 16:32), é guiado e ensinado por Deus (Sl 25:9) e é adornado por Ele com a salvação (Sl 149:4). Jesus é o modelo: manso e humilde de coração (Mt 11:29). É esse domínio que herda a terra.']),
    ])
pagina('v05.html', 'Mateus 5:5 · Mansos — Sermão do Monte', 'Mateus 5:5 · porta 3', 'Mansos', None, [v5],
       pager(('v04.html', '← Anterior', 'Porta 2 · Os que choram'), ('v06.html', 'Próxima →', 'Porta 4 · Fome e sede de justiça')), final=VOLTA)

# ---------- porta 4 · v.6 ----------
v6 = grupo('v6', 'Mateus 5:6', 'Fome e sede de justiça',
    bible('bem-aventurados <mark>os que têm fome e sede de justiça</mark>, porque eles <mark>serão fartos</mark>;'),
    [
    ('sub', 'Ter fome e sede'),
    card('blue', 'Paralelo', 'Salmos 42:1,2',
         antes='Fome e sede são necessidades que não se adiam. Assim a alma busca a Deus.',
         corpo=bq(n('1', 'Como o cervo brama pelas correntes das águas, assim suspira a minha alma por ti, ó Deus!'),
                  n('2', 'A minha alma <mark>tem sede de Deus</mark>, do Deus vivo…')),
         link=arc('sl/42/1')),
    card('blue', 'Paralelo', 'João 6:35',
         corpo=bq('Eu sou o pão da vida; aquele que vem a mim <mark>não terá fome</mark>; e quem crê em mim <mark>nunca terá sede</mark>.'),
         link=arc('jo/6/35')),
    ('sub', 'O que sacia: a justiça que vem de Deus'),
    card('blue', 'Paralelo', 'Isaías 55:1,2',
         antes='Deus convida os sedentos. E pergunta por que gastar a vida naquilo que não alimenta.',
         corpo=bq(n('1', 'Ó vós todos os que <mark>tendes sede</mark>, vinde às águas…'),
                  n('2', 'Por que gastais o dinheiro naquilo que <mark>não é pão</mark>? E o produto do vosso trabalho naquilo que <mark>não pode satisfazer</mark>?')),
         link=arc('is/55/1')),
    card('blue', 'Paralelo', 'Filipenses 3:9',
         antes='A justiça de que Jesus fala não é a que a pessoa produz, e sim a que vem de Deus, pela fé.',
         corpo=bq('…não tendo a minha justiça que vem da lei, mas <mark>a que vem pela fé em Cristo</mark>, a saber, <mark>a justiça que vem de Deus</mark>, pela fé;'),
         link=arc('fp/3/9')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 18.2',
         corpo=bq('<mark>Não é por meio de penosas lutas ou fatigante lida, nem de dádivas ou sacrifícios, que alcançamos a justiça; ela é, porém, gratuitamente dada a toda alma que dela tem fome e sede.</mark>'),
         link=egw('1956.131')),
    ('sub', 'O que não sacia: a justiça própria'),
    card('orange', 'Contraste', 'Romanos 10:3',
         corpo=bq('…não conhecendo a justiça de Deus e <mark>procurando estabelecer a sua própria justiça</mark>, não se sujeitaram à justiça de Deus.'),
         link=arc('rm/10/3')),
    card('orange', 'Contraste', 'Isaías 64:6',
         corpo=bq('…<mark>todas as nossas justiças</mark>, como trapo da imundícia;…'),
         link=arc('is/64/6')),
    card('gray', 'Conclusão', 'Justiça própria não sacia',
         extra_p=['Quem tenta se fartar com a própria justiça continua com fome: ela não é pão (Is 55:2), não submete a Deus (Rm 10:3) e não passa de “trapo da imundícia” (Is 64:6). A justiça que sacia vem de Deus, pela fé em Cristo (Fp 3:9), e é dada a quem tem fome e sede dela. Por isso só Cristo, o pão da vida, farta (Jo 6:35).']),
    ])
pagina('v06.html', 'Mateus 5:6 · Fome e sede de justiça — Sermão do Monte', 'Mateus 5:6 · porta 4', 'Fome e sede de justiça', None, [v6],
       pager(('v05.html', '← Anterior', 'Porta 3 · Mansos'), ('v07.html', 'Próxima →', 'Porta 5 · Misericordiosos')), final=VOLTA)

# ---------- porta 5 · v.7 ----------
v7 = grupo('v7', 'Mateus 5:7', 'Misericordiosos',
    bible('bem-aventurados <mark>os misericordiosos</mark>, porque eles alcançarão <mark>misericórdia</mark>;'),
    [
    ('sub', 'Ser misericordioso'),
    card('blue', 'Paralelo', 'Lucas 6:36,38',
         antes='O modelo da misericórdia é o próprio Pai. E a medida que usamos com os outros é a que será usada conosco.',
         corpo=bq(n('36', 'Sede, pois, <mark>misericordiosos</mark>, como também vosso Pai é misericordioso.'),
                  n('38', '…porque <mark>com a mesma medida com que medirdes também vos medirão de novo</mark>.')),
         link=arc('lc/6/36')),
    ('sub', 'A misericórdia volta'),
    card('blue', 'Paralelo', 'Salmos 18:25',
         antes='Deus trata cada um conforme a pessoa trata os outros: com o benigno, benigno.',
         corpo=bq('Com <mark>o benigno</mark> te mostrarás <mark>benigno</mark>; e com o homem sincero te mostrarás sincero;'),
         link=arc('sl/18/25')),
    card('green', 'Exemplo', 'Mateus 18:33',
         antes='Na parábola, um servo teve toda a dívida perdoada pelo seu senhor e depois não quis perdoar uma dívida pequena de um companheiro. Esta é a pergunta do senhor a ele.',
         corpo=bq('Não devias tu, igualmente, <mark>ter compaixão do teu companheiro</mark>, como eu também <mark>tive misericórdia de ti</mark>?'),
         link=arc('mt/18/33')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 23.2',
         corpo=bq('Os misericordiosos “alcançarão misericórdia”… Há uma doce paz para o espírito compassivo, uma bendita satisfação na vida de esquecimento de si mesmo em benefício de outros… <mark>Haveis de ceifar aquilo que semeardes.</mark>'),
         link=egw('1956.157')),
    ('sub', 'Quem não faz misericórdia'),
    card('orange', 'Contraste', 'Tiago 2:13',
         corpo=bq('Porque o juízo será <mark>sem misericórdia sobre aquele que não fez misericórdia</mark>; e <mark>a misericórdia triunfa sobre o juízo</mark>.'),
         link=arc('tg/2/13')),
    card('gray', 'Conclusão', 'A misericórdia volta',
         extra_p=['A misericórdia funciona nos dois sentidos: quem a pratica a recebe (Sl 18:25; Lc 6:38), e o juízo é sem misericórdia para quem não a usou (Tg 2:13). Quem foi perdoado deve ter compaixão do outro (Mt 18:33), e “a misericórdia triunfa sobre o juízo”.']),
    ])
pagina('v07.html', 'Mateus 5:7 · Misericordiosos — Sermão do Monte', 'Mateus 5:7 · porta 5', 'Misericordiosos', None, [v7],
       pager(('v06.html', '← Anterior', 'Porta 4 · Fome e sede de justiça'), ('v08.html', 'Próxima →', 'Porta 6 · Puros de coração')), final=VOLTA)

# ---------- porta 6 · v.8 ----------
v8 = grupo('v8', 'Mateus 5:8', 'Puros de coração',
    bible('bem-aventurados <mark>os limpos de coração</mark>, porque eles <mark>verão a Deus</mark>;'),
    [
    ('sub', 'Quem é o puro de coração?'),
    card('blue', 'Paralelo', 'Salmos 24:3,4',
         corpo=bq(n('3', 'Quem subirá ao monte do Senhor ou quem estará no seu lugar santo?'),
                  n('4', 'Aquele que é <mark>limpo de mãos e puro de coração</mark>, que não entrega a sua alma à vaidade, nem jura enganosamente.')),
         link=arc('sl/24/3')),
    card('blue', 'Paralelo', 'Salmos 15:1,2',
         antes='O Salmo 15 pergunta quem pode habitar na presença de Deus (uma imagem de quem será salvo). A resposta começa no coração: quem anda em sinceridade e fala a verdade “segundo o seu coração”.',
         corpo=bq(n('1', 'Senhor, quem <mark>habitará no teu tabernáculo</mark>? Quem <mark>morará no teu santo monte</mark>?'),
                  n('2', 'Aquele que <mark>anda em sinceridade</mark>, e pratica a justiça, e fala verazmente <mark>segundo o seu coração</mark>;')),
         link=arc('sl/15/1')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 25.1',
         corpo=bq('…não somente puros no sentido em que o mundo entende a pureza, livres do que é sensual, puros de concupiscências, mas <mark>fiéis nos íntimos desígnios e motivos da alma, isentos de orgulho e de interesse egoísta</mark>, humildes, abnegados, semelhantes a uma criança.'),
         obs='Sobre as palavras de Jesus “bem-aventurados os limpos de coração”.',
         link=egw('1956.166')),
    ('sub', 'A esperança de ver a Deus'),
    card('blue', 'Paralelo', '1 João 3:1–3',
         antes='Quem espera ver a Cristo como Ele é começa, desde agora, a se purificar.',
         corpo=bq(n('2', '…porque assim como é <mark>o veremos</mark>.'),
                  n('3', 'E qualquer que nele tem esta esperança <mark>purifica-se a si mesmo, como também ele é puro</mark>.')),
         link=arc('1jo/3/1')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 24.3',
         corpo=bq('Jesus não menciona essa pureza cerimonial como uma das condições de entrar em Seu reino, mas indica a necessidade da pureza de coração… Na cidade de Deus não entrará coisa alguma que contamine. <mark>Todos quantos houverem de ser seus moradores, hão de se ter tornado aqui puros de coração.</mark>'),
         link=egw('1956.163')),
    ('sub', 'O oposto: limpo por fora, contaminado por dentro'),
    card('orange', 'Contraste', 'Mateus 23:25,26',
         antes='O contrário do coração limpo não é só o que é sensual: é também quem cuida do que aparece e deixa o interior sujo. Jesus disse isto aos fariseus.',
         corpo=bq(n('25', 'Ai de vós, escribas e fariseus, hipócritas! Pois que <mark>limpais o exterior do copo e do prato</mark>, mas <mark>o interior está cheio de rapina e de iniquidade</mark>.'),
                  n('26', 'Fariseu cego! <mark>Limpa primeiro o interior</mark> do copo e do prato, para que também o exterior fique limpo.')),
         link=arc('mt/23/25')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 24.2',
         corpo=bq('Tinham o espírito preocupado com regras e restrições e o temor de contaminação exterior, e <mark>não percebiam a mancha que o egoísmo e a malícia comunicavam à alma</mark>.'),
         obs='Sobre os judeus no tempo de Jesus, que cuidavam da limpeza cerimonial.',
         link=egw('1956.162')),
    card('orange', 'Contraste', 'Tiago 4:8',
         antes='“Duplo ânimo” é o coração dividido, que quer Deus e quer o pecado ao mesmo tempo. Tiago manda purificar o coração.',
         corpo=bq('Chegai-vos a Deus, e ele se chegará a vós. Limpai as mãos, pecadores; e, vós de <mark>duplo ânimo</mark>, <mark>purificai o coração</mark>.'),
         link=arc('tg/4/8')),
    ('sub', 'A raiz: o orgulho que quis o lugar de Deus'),
    card('orange', 'Contraste', 'Isaías 14:13,14',
         antes='Este é o coração que quis tomar o lugar de Deus. Quando diz “serei semelhante ao Altíssimo”, não quer imitar a Deus como modelo: quer usurpar, tomar à força, a honra que pertence só a Ele. É a raiz do orgulho, do qual o coração limpo é livre.',
         corpo=bq(n('13', 'E tu dizias <mark>no teu coração</mark>: Eu subirei ao céu, e, acima das estrelas de Deus, <mark>exaltarei o meu trono</mark>,'),
                  n('14', '…e <mark>serei semelhante ao Altíssimo</mark>.')),
         link=arc('is/14/13')),
    card('purple', 'Ellen White', 'Patriarcas e Profetas, p. 9.3',
         corpo=bq('Se bem que toda a sua glória proviesse de Deus, este poderoso anjo veio a considerá-la como pertencente a si próprio. Não contente com sua posição… <mark>arriscou-se a cobiçar a homenagem devida unicamente ao Criador.</mark>'),
         obs='Sobre Lúcifer. O próprio parágrafo cita Isaías 14:13,14.',
         link=egw('1815.78')),
    card('gray', 'Conclusão', 'A pureza vem de dentro',
         extra_p=['Ser limpo de coração é ser fiel nos motivos da alma, sem orgulho e sem interesse egoísta (MDC 25.1). Sobe ao monte do Senhor quem é “limpo de mãos e puro de coração” (Sl 24:3,4), e quem espera ver a Cristo se purifica desde agora (1Jo 3:3).',
                  'O oposto não é só o sensual: é o limpo por fora e contaminado por dentro (Mt 23:25,26), o de duplo ânimo (Tg 4:8) e, na raiz, o orgulho que quer o lugar de Deus (Is 14:13,14). A pureza vai de dentro para fora; não basta parecer certo por fora.']),
    ])
pagina('v08.html', 'Mateus 5:8 · Puros de coração — Sermão do Monte', 'Mateus 5:8 · porta 6', 'Puros de coração', None, [v8],
       pager(('v07.html', '← Anterior', 'Porta 5 · Misericordiosos'), ('v09.html', 'Próxima →', 'Porta 7 · Pacificadores')), final=VOLTA)

# ---------- porta 7 · v.9 ----------
v9 = grupo('v9', 'Mateus 5:9', 'Pacificadores',
    bible('bem-aventurados <mark>os pacificadores</mark>, porque eles serão chamados <mark>filhos de Deus</mark>;'),
    [
    ('sub', 'Procurar a paz'),
    card('blue', 'Paralelo', 'Romanos 12:18',
         antes='A paz depende de nós até onde for possível. O pacificador faz a sua parte.',
         corpo=bq('Se for possível, quanto estiver em vós, <mark>tende paz com todos os homens</mark>.'),
         link=arc('rm/12/18')),
    card('blue', 'Paralelo', 'Provérbios 20:3' + KJ,
         corpo=bq('<mark>É uma honra para um homem cessar os conflitos</mark>…'),
         link=bkj('pv/20/3')),
    ('sub', 'Por que são chamados filhos de Deus'),
    card('blue', 'Paralelo', '2 Coríntios 5:18',
         antes='Os pacificadores são chamados filhos de Deus porque continuam a obra do Pai: reconciliar.',
         corpo=bq('E tudo isso provém de Deus, que <mark>nos reconciliou consigo mesmo</mark> por Jesus Cristo e nos deu <mark>o ministério da reconciliação</mark>,'),
         link=arc('2co/5/18')),
    card('gray', 'Conclusão', 'Depois de pacificar, vem a perseguição',
         extra_p=['O pecado separou o homem de Deus; a morte de Cristo trouxe a reconciliação. O pacificador reconcilia as pessoas com Deus e entre si, em Deus e por meio de Deus. Nem toda “paz” é a que Deus abençoa.',
                  'E há um “depois disto”: depois de ser pacificador e chamado filho de Deus, vem a perseguição (<a href="v10-12.html#v10">porta 8</a>). Foi assim com Abel: Caim o perseguiu porque as obras dele eram justas e as suas, más (1Jo 3:12,13).']),
    ])
pagina('v09.html', 'Mateus 5:9 · Pacificadores — Sermão do Monte', 'Mateus 5:9 · porta 7', 'Pacificadores', None, [v9],
       pager(('v08.html', '← Anterior', 'Porta 6 · Puros de coração'), ('v10-12.html', 'Próxima →', 'Porta 8 · Perseguidos')), final=VOLTA)

# ---------- porta 8 · v.10–12 ----------
v10 = grupo('v10', 'Mateus 5:10–12', 'Perseguidos',
    bible(n('10', 'bem-aventurados os que sofrem <mark>perseguição</mark> por causa da justiça, porque <mark>deles é o Reino dos céus</mark>;'),
          n('11', 'bem-aventurados sois vós quando vos injuriarem, e <mark>perseguirem</mark>, e, mentindo, disserem todo o mal contra vós, por minha causa.'),
          n('12', 'Exultai e alegrai-vos, porque é grande o vosso galardão nos céus; porque assim <mark>perseguiram</mark> os profetas…')),
    [
    ('sub', 'Por que o justo é perseguido'),
    card('blue', 'Paralelo', 'João 15:19',
         corpo=bq('…porque não sois do mundo, antes eu vos escolhi do mundo, por isso é que <mark>o mundo vos aborrece</mark>.'),
         link=arc('jo/15/19')),
    card('green', 'Exemplo', '1 João 3:12,13',
         antes='Caim perseguiu Abel porque as obras de Abel eram justas e as suas, más. O mundo aborrece quem faz o bem, e isso não é motivo para espanto.',
         corpo=bq(n('12', 'E por que causa o matou? Porque as suas obras eram más, e <mark>as de seu irmão, justas</mark>.'),
                  n('13', 'Meus irmãos, não vos maravilheis, se <mark>o mundo vos aborrece</mark>.')),
         link=arc('1jo/3/12')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 8.1',
         corpo=bq('…<mark>Seus súditos são os humildes de espírito, os mansos, os perseguidos por causa da justiça.</mark> Deles é o reino dos Céus. Conquanto não se tenha ainda realizado plenamente, iniciou-se neles a obra que os tornará “idôneos para participar da herança dos santos na luz”.'),
         link=egw('1956.80')),
    ('sub', 'Perseguidos: exemplos'),
    card('green', 'Exemplo', 'Lucas 4:28–30',
         antes='Jesus, em Nazaré, foi expulso da cidade por dizer a verdade.',
         corpo=bq(n('28', 'E todos, na sinagoga, ouvindo essas coisas, <mark>se encheram de ira</mark>.'),
                  n('29', '…<mark>o expulsaram da cidade</mark> e o levaram até ao cume do monte… <mark>para dali o precipitarem</mark>.'),
                  n('30', 'Ele, porém, passando pelo meio deles, retirou-se.')),
         link=arc('lc/4/28')),
    card('green', 'Exemplo', '2 Samuel 16:5–14',
         antes='Simei amaldiçoou o rei Davi e lhe atirou pedras (v.5–8). Davi não revidou: entregou a causa ao Senhor.',
         corpo=bq(n('11', '…<mark>Deixai-o; que amaldiçoe</mark>, porque o Senhor lho disse.'),
                  n('12', 'Porventura, o Senhor olhará para a minha miséria e o Senhor <mark>me pagará com bem a sua maldição deste dia</mark>.')),
         link=arc('2sm/16/5')),
    ('sub', 'O oposto do perseguido: o morno'),
    card('orange', 'Contraste', 'Apocalipse 3:16',
         antes='É o oposto do v.10: o morno, que se diz de Cristo mas não se decide, é rejeitado por Ele. O perseguido é o contrário: está decidido, e por isso o mundo tenta expulsá-lo, como expulsaram Jesus da cidade (Lc 4:29).',
         corpo=bq('Assim, porque és <mark>morno</mark> e não és frio nem quente, vomitar-te-ei da minha boca.'),
         link=arc('ap/3/16')),
    ('sub', 'Os v.11–12: perseguido como cristão'),
    card('blue', 'Paralelo', '1 Pedro 4:14–18' + KJ,
         antes='É o que Jesus diz no v.11: ser vituperado por causa de Cristo é bem-aventurança, e sofrer “como cristão” é motivo para glorificar a Deus, não para se envergonhar.',
         corpo=bq(n('14', 'Se sois censurados pelo nome de Cristo, <mark>felizes sois</mark>, porque o Espírito de glória e de Deus repousa sobre vós…'),
                  n('16', 'Porém, se algum homem <mark>padece como cristão</mark>, que não se envergonhe, antes glorifique a Deus nisto.')),
         link=bkj('1pe/4/14')),
    card('orange', 'Contraste', '1 Pedro 4:15' + KJ,
         antes='Há o sofrimento que vem de fazer o mal e o que vem de fazer a vontade de Deus. Só o segundo é a perseguição bem-aventurada (v.16).',
         corpo=bq('Mas que nenhum de vós padeça <mark>como homicida, ou como ladrão, ou como malfeitor</mark>…'),
         link=bkj('1pe/4/15')),
    card('gray', 'Conclusão', 'Uma só bem-aventurança, em três passos',
         extra_p=['Jesus repete a perseguição três vezes seguidas (v.10, 11 e 12), mas não são três bem-aventuranças: é uma só, que vai se completando.',
                  'No v.10 vem a causa: ser perseguido “por causa da justiça”. No v.11, como isso acontece: injúrias, perseguição e mentiras, “por minha causa”. No v.12, o que fazer e o que esperar: exultar e se alegrar, porque é grande o galardão nos céus e os profetas também foram perseguidos.',
                  'Quem ouve já sabe, desde o início, que isso pode acontecer, e sabe também por que vale a pena.']),
    ])
pagina('v10-12.html', 'Mateus 5:10–12 · Perseguidos — Sermão do Monte', 'Mateus 5:10–12 · porta 8', 'Perseguidos por causa da justiça', 'O v.10 é a bem-aventurança; os v.11–12 a ampliam.', [v10],
       pager(('v09.html', '← Anterior', 'Porta 7 · Pacificadores'), ('conclusao.html', 'Próxima →', 'Conclusão das bem-aventuranças')), final=FINAL8)

# =====================================================================================
# conclusao.html — conclusão de TODAS as bem-aventuranças (página própria, largura total; só quem chegou à porta 8 chega aqui)
# =====================================================================================
def conclusao():
    TAB = [
        ('1', 'Pobres em espírito', 'v03.html#v3', 'deles é o Reino dos céus', 'presente'),
        ('2', 'Os que choram', 'v04.html#v4', 'serão consolados', 'futuro'),
        ('3', 'Mansos', 'v05.html#v5', 'herdarão a terra', 'futuro'),
        ('4', 'Fome e sede de justiça', 'v06.html#v6', 'serão fartos', 'futuro'),
        ('5', 'Misericordiosos', 'v07.html#v7', 'alcançarão misericórdia', 'futuro'),
        ('6', 'Puros de coração', 'v08.html#v8', 'verão a Deus', 'futuro'),
        ('7', 'Pacificadores', 'v09.html#v9', 'serão chamados filhos de Deus', 'futuro'),
        ('8', 'Perseguidos', 'v10-12.html#v10', 'deles é o Reino dos céus', 'presente'),
    ]
    meio = '\n'.join('        <li><a href="%s"><span class="num">%s</span><b>%s</b><span class="prom">%s</span></a></li>' % (h, n_, nome, prom)
                     for n_, nome, h, prom, q in TAB[1:7])
    linhas = '\n'.join('        <tr class="%s"><td><a href="%s"><span class="num">%s</span></a></td><td><a href="%s">%s</a></td><td>%s</td><td><span class="tempo %s">%s</span></td></tr>'
                       % (q, h, n_, h, nome, prom, q, 'agora' if q == 'presente' else 'depois') for n_, nome, h, prom, q in TAB)
    img = ''
    if os.path.exists(os.path.join(DEST, 'conclusao.jpg')):
        img = '''
  <figure class="cc-imagem">
    <img src="conclusao.jpg" alt="Ilustração: as oito portas em fila; a primeira e a última, maiores e douradas, abraçam as seis do meio como dois parênteses.">
    <figcaption>Ilustração criada com IA</figcaption>
  </figure>'''
    corpo = '''
<header class="cc-hero">
  <div class="cc-hero-texto">
    <p class="kicker">Mateus 5:3–12 · as oito portas</p>
    <h1>Conclusão das bem-aventuranças</h1>
    <p class="lede">Você passou pelas oito portas. Vista de cima, a lista tem uma forma: a primeira e a última se fecham uma na outra, como parênteses, e guardam entre elas tudo o que nasce da humildade.</p>
  </div>@@IMG@@
</header>

<section class="cc-sec" aria-labelledby="cc-moldura">
  <h2 id="cc-moldura">A moldura: dois parênteses</h2>
  <p class="cc-intro">A primeira e a última bem-aventurança têm a <b>mesma promessa</b>, e no presente: “deles é o Reino dos céus”. Elas abrem e fecham a lista, e as seis do meio ficam dentro desses parênteses.</p>
  <div class="moldura">
    <a class="paren esq" href="v03.html#v3"><span class="num">1</span><b>Pobres em espírito</b><span class="prom">“deles é o Reino dos céus”</span><span class="quando">já no presente</span></a>
    <div class="meio">
      <ol>
@@MEIO@@
      </ol>
      <p class="rotulo-meio">Seis promessas para o futuro</p>
    </div>
    <a class="paren dir" href="v10-12.html#v10"><span class="num">8</span><b>Perseguidos</b><span class="prom">“deles é o Reino dos céus”</span><span class="quando">já no presente</span></a>
  </div>
</section>

<section class="cc-sec" aria-labelledby="cc-dentro">
  <h2 id="cc-dentro">Dentro dos parênteses: uma progressão</h2>
  <p class="cc-intro">Quem é pobre de espírito (porta 1) reconhece a sua necessidade, e isso o leva a chorar pelo pecado (porta 2). Ver o pecado e querer ser livre dele leva a aprender a ser manso (porta 3), e assim por diante: uma coisa leva à outra, e a pessoa vai crescendo.</p>
  <article class="note purple cc-cartao">
    <span class="tag">Ellen White</span>
    <h3>O Maior Discurso de Cristo, p. 13.2</h3>
    <blockquote class="text"><p>Há, através das bem-aventuranças, <mark>uma progressão na experiência cristã</mark>. Os que sentiram sua necessidade de Cristo, os que choraram por causa do pecado, e se sentaram com Cristo na escola da aflição, hão de, com o divino Mestre, <mark>aprender a ser mansos</mark>.</p></blockquote>
    <a class="full" href="https://m.egwwritings.org/pt/book/1956.106" target="_blank" rel="noopener">Abrir o trecho no site do Ellen G. White ↗</a>
  </article>
  <p class="cc-intro">Repare no verbo: “hão de aprender”. Não é automático. É uma escola, em que se aprende aos poucos, e a pessoa pode cair, voltar ao caminho e aprender só em parte. Pelo caminho há quem ajude: os misericordiosos (porta 5) levantam quem caiu, e os pacificadores (porta 7) reconciliam. As promessas das seis do meio estão no futuro, e quem passa por elas não desiste: continua até alcançá-las.</p>
  <p class="cc-intro">E o perseguido (porta 8) precisa da humildade e de todas as outras para suportar. A humildade, no fim, termina em perseguição.</p>
</section>

<section class="cc-sec" aria-labelledby="cc-laodiceia">
  <h2 id="cc-laodiceia">O oposto de cada ponta: Laodiceia</h2>
  <p class="cc-intro">A carta à igreja de Laodiceia mostra o contrário das duas portas que fecham a moldura.</p>
  <div class="cc-par">
    <article class="note orange cc-cartao">
      <span class="tag">Contraste da porta 1</span>
      <h3>Apocalipse 3:17</h3>
      <p class="antes">Quem se acha rico e sem falta de nada é o oposto do pobre de espírito.</p>
      <blockquote class="text"><p>Como dizes: <mark>Rico sou, e estou enriquecido, e de nada tenho falta</mark>… e não sabes que és um desgraçado, e miserável, e <mark>pobre</mark>, e cego, e nu</p></blockquote>
      <a class="full" href="https://www.bibliaonline.com.br/arc/ap/3/17+" target="_blank" rel="noopener">Ler o texto completo na ARC ↗</a>
    </article>
    <article class="note orange cc-cartao">
      <span class="tag">Contraste da porta 8</span>
      <h3>Apocalipse 3:16</h3>
      <p class="antes">O morno, que não se decide, é o oposto do perseguido, que está decidido e por isso é expulso.</p>
      <blockquote class="text"><p>Assim, porque és <mark>morno</mark> e não és frio nem quente, vomitar-te-ei da minha boca.</p></blockquote>
      <a class="full" href="https://www.bibliaonline.com.br/arc/ap/3/16+" target="_blank" rel="noopener">Ler o texto completo na ARC ↗</a>
    </article>
  </div>
</section>

<section class="cc-fecho" aria-labelledby="cc-fim">
  <article class="note gray">
    <span class="tag">Conclusão</span>
    <h3 id="cc-fim">Um só caminho, oito portas</h3>
    <p>As oito bem-aventuranças não são oito caminhos: são oito portas de um só caminho, e quem vai para o Reino passa por todas. Ele começa na humildade, que reconhece a necessidade (porta 1), e termina em perseguição por causa da justiça (porta 8). Passando por todas elas, da primeira à oitava, Deus forma o caráter, e as promessas de cada porta se cumprem no futuro.</p>
    <p class="obs">E a primeira e a última guardam a mesma promessa: “deles é o Reino dos céus”.</p>
  </article>
  <div class="volta-imagem fim">
    <a class="botao-conclusao" href="v13-15.html">Continuar: sal e luz →</a>
    <a class="botao-volta" id="volta-imagem" href="caminho-ampliado.html">← Voltar à imagem das portas</a>
  </div>
</section>
'''
    corpo = corpo.replace('@@IMG@@', img).replace('@@MEIO@@', meio).replace('@@LINHAS@@', linhas)
    html = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>Conclusão das bem-aventuranças · Mateus 5:3–12 — Sermão do Monte</title>\n<link rel="stylesheet" href="style.css">\n' + ENTRADA + '</head>\n<body class="conclusao">\n'
            + BARRA + '\n<div class="wrap">\n\n' + crumbs('conclusao.html') + '\n' + corpo + '\n'
            + pager(('v10-12.html', '← Anterior', 'Porta 8 · Perseguidos'), ('v13-15.html', 'Próxima →', 'Sal e luz · v.13–16'))
            + '\n\n</div>\n' + pixel('conclusao.html') + '\n' + ORIGEM + '\n</body>\n</html>\n')
    gravar(DEST, 'conclusao.html', html, RASC)


conclusao()

# =====================================================================================
# v.13–16  Sal e luz
# =====================================================================================
v13 = grupo('v13', 'Mateus 5:13', 'Sal da terra',
    bible(n('13', 'Vós sois <mark>o sal</mark> da terra; e, <mark>se o sal for insípido</mark>, com que se há de salgar? Para nada mais presta, senão para se lançar fora e ser pisado pelos homens.')),
    [
    card('gray', 'Conclusão', 'De bem-aventurados a sal e luz',
         bq(n('11', 'bem-aventurados <mark>sois vós</mark> quando vos injuriarem…'),
            n('13', '<mark>Vós sois</mark> o sal da terra…')),
         extra_p=['Quem é insultado por causa de Cristo é o sal e a luz: Jesus diz “bem-aventurados sois vós” (v.11) e logo em seguida “vós sois o sal da terra” (v.13). O que os bem-aventurados vivem nas bem-aventuranças, eles levam ao mundo.']),
    card('blue', 'Paralelo', 'Colossenses 4:6',
         bq('A vossa palavra seja sempre agradável, <mark>temperada com sal</mark>, para que saibais como vos convém responder a cada um.'),
         link=arc('cl/4/6')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 53.2',
         bq('A dura, rígida ortodoxia dos fariseus, destituída de contrição, ternura ou amor… Eles eram como <mark>o sal que se tornara insípido</mark>; pois sua influência não tinha poder algum para preservar o mundo da corrupção.'),
         obs='Sobre os fariseus: o sal que perdeu o sabor, e com ele a utilidade (v.13).',
         link=egw('1956.297')),
    card('orange', 'Contraste', 'Provérbios 18:8' + ARA,
         bq('As palavras do maldizente são <mark>doces bocados</mark> que descem para o mais interior do ventre.'),
         link=ara('pv/18/8')),
    card('gray', 'Conclusão', 'O sal e o doce',
         extra_p=['A palavra do maldizente é doce: “doces bocados” que agradam, são engolidos com gosto e descem até o mais íntimo (Pv 18:8). O doce agrada sem limite, engana e adoece. O sal é o contrário: na medida certa dá sabor, sem ele faz falta, e demais estraga.',
                  'Quem passou pelas bem-aventuranças — pobre de espírito, que chorou pelo pecado, manso, com fome e sede de justiça, misericordioso, puro de coração, pacificador e perseguido — é o sal da terra. Não fala para agradar: dá sabor, com a palavra certa na hora certa, sem faltar e sem passar da medida. É a palavra temperada (Cl 4:6).']),
    ])

v14 = grupo('v14', 'Mateus 5:14–16', 'Luz do mundo',
    bible(n('14', 'Vós sois <mark>a luz do mundo</mark>; não se pode esconder uma cidade edificada sobre um monte;'),
          n('15', 'nem se acende <mark>a candeia</mark> e se coloca debaixo do alqueire, mas, <mark>no velador</mark>, e dá luz a todos que estão na casa.'),
          n('16', 'Assim <mark>resplandeça a vossa luz</mark> diante dos homens, para que vejam as vossas <mark>boas obras</mark> e <mark>glorifiquem o vosso Pai</mark>, que está nos céus.')),
    [
    ('sub', 'Luz e trevas'),
    card('blue', 'Paralelo', 'João 8:12',
         bq('Eu sou <mark>a luz do mundo</mark>; quem me segue <mark>não andará em trevas</mark>, mas terá a luz da vida.'),
         obs='No v.14 Jesus diz “vós sois a luz do mundo”: a luz dos discípulos vem dEle, que é a luz.',
         link=arc('jo/8/12')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 39.2',
         bq('<mark>Jesus, o Salvador, é a única luz que pode iluminar a escuridão de um mundo imerso no pecado.</mark>… Foi recebendo de Sua luz que os discípulos se puderam tornar portadores de luz.'),
         link=egw('1956.233')),
    card('blue', 'Paralelo', 'Efésios 5:8',
         bq('Porque, noutro tempo, <mark>éreis trevas</mark>, mas, agora, <mark>sois luz no Senhor</mark>; andai como filhos da luz'),
         link=arc('ef/5/8')),
    card('blue', 'Paralelo', 'Filipenses 2:15',
         bq('…filhos de Deus inculpáveis no meio duma geração corrompida e perversa, entre a qual <mark>resplandeceis como astros no mundo</mark>;'),
         link=arc('fp/2/15')),
    card('blue', 'Paralelo', 'Isaías 60:1,2',
         bq(n('1', 'Levanta-te, <mark>resplandece</mark>, porque já vem a tua luz…'),
            n('2', 'Porque eis que <mark>as trevas cobriram a terra</mark>, e a escuridão, os povos; mas sobre ti o Senhor virá surgindo, e a sua glória se verá sobre ti.')),
         link=arc('is/60/1')),
    card('orange', 'Contraste', 'João 3:19,20',
         bq(n('19', 'E a condenação é esta: Que a luz veio ao mundo, e os homens <mark>amaram mais as trevas do que a luz</mark>, porque as suas obras eram más.'),
            n('20', 'Porque todo aquele que faz o mal <mark>aborrece a luz</mark> e não vem para a luz para que as suas obras não sejam reprovadas.')),
         obs='Luz e trevas se medem pelas obras: as boas aparecem na luz (v.16); as más fogem dela.',
         link=arc('jo/3/19')),
    card('orange', 'Contraste', '1 João 1:5–7',
         bq(n('5', '…que Deus é luz, e <mark>não há nele treva nenhuma</mark>.'),
            n('6', 'Se dissermos que temos comunhão com ele e <mark>andarmos em trevas, mentimos</mark> e não praticamos a verdade.'),
            n('7', 'Mas, se <mark>andarmos na luz</mark>, como ele na luz está, temos comunhão uns com os outros…')),
         link=arc('1jo/1/5')),
    card('orange', 'Contraste', 'Provérbios 4:18,19',
         bq(n('18', 'Mas a vereda dos justos é como <mark>a luz da aurora</mark>, que vai brilhando mais e mais até ser dia perfeito.'),
            n('19', 'O caminho dos ímpios é como <mark>a escuridão</mark>; nem conhecem aquilo em que tropeçam.')),
         link=arc('pv/4/18')),
    ('sub', 'v.16: as boas obras'),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 41.1',
         bq('Mas Jesus não pediu aos discípulos: “Esforçai-vos por fazer resplandecer a vossa luz”; Ele disse: “Resplandeça.” <mark>Se Cristo habita no coração, é impossível esconder a luz de Sua presença.</mark>'),
         link=egw('1956.239')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 44.4',
         bq('As provações suportadas com paciência, as bênçãos recebidas com gratidão… a mansidão, a bondade, misericórdia e amor manifestados habitualmente, <mark>são luzes que resplandecem no caráter</mark>, em contraste com <mark>as trevas do coração egoísta</mark>, em que nunca brilhou a luz da vida.'),
         link=egw('1956.254')),
    card('gray', 'Conclusão', 'A luz que mostra o Pai',
         extra_p=['A luz são as boas obras (v.16), e elas não chamam a atenção para quem as faz, e sim para o Pai: “glorifiquem o vosso Pai”. Do outro lado ficam as trevas, que são as obras más escondidas, porque quem faz o mal aborrece a luz (Jo 3:19,20).',
                  'Mais adiante Jesus mostra o oposto: quem faz as obras “a fim de serem vistos pelos homens” (Mt 23:5), como os escribas e fariseus (<a href="v17-20.html#v20">v.20</a>).']),
    ('sub', 'O candelabro (v.15–16)'),
    card('blue', 'Paralelo', 'Êxodo 25:31,37',
         bq(n('31', 'Também farás <mark>um castiçal de ouro puro</mark>; de ouro batido se fará este castiçal…'),
            n('37', 'Também lhe farás <mark>sete lâmpadas</mark>, as quais se acenderão para alumiar defronte dele.')),
         obs='A ARC diz “castiçal”; a NAA e a King James dizem “candelabro”.',
         link=arc('ex/25/31')),
    card('purple', 'Ellen White', 'Patriarcas e Profetas, p. 247.3',
         bq('No primeiro compartimento, ou lugar santo, estavam a mesa dos pães da proposição, <mark>o castiçal ou candelabro</mark>, e o altar de incenso.',
            'Do lado do sul estava o castiçal de sete ramos, com as suas sete lâmpadas… e o todo era feito de uma peça de ouro maciço. Não havendo janelas no tabernáculo, <mark>nunca ficavam apagadas todas as lâmpadas a um tempo, mas espargiam sua luz dia e noite</mark>.'),
         link=egw('1815.1428')),
    card('blue', 'Paralelo', 'Zacarias 4:2,6',
         bq(n('2', '…eis <mark>um castiçal todo de ouro</mark>, e <mark>um vaso de azeite</mark> no cimo, com as suas sete lâmpadas…'),
            n('6', '…Não por força, nem por violência, mas <mark>pelo meu Espírito</mark>, diz o Senhor dos Exércitos.')),
         link=arc('zc/4/2')),
    card('blue', 'Paralelo', 'Apocalipse 1:12,13,20',
         bq(n('12', '…vi <mark>sete castiçais de ouro</mark>;'),
            n('13', 'e, <mark>no meio dos sete castiçais</mark>, um semelhante ao Filho do Homem…'),
            n('20', '…e os sete castiçais, que viste, <mark>são as sete igrejas</mark>.')),
         link=arc('ap/1/12')),
    card('purple', 'Ellen White', 'Patriarcas e Profetas, p. 254.1',
         bq('…contemplou ele ali “sete lâmpadas de fogo” (Apocalipse 4:5) que ardiam diante do trono… viu ali as “sete lâmpadas de fogo” e o “altar de ouro” <mark>representados pelo castiçal de ouro</mark> e o altar de incenso no santuário terrestre.'),
         obs='Sobre o santuário do céu, que o santuário terrestre representava.',
         link=egw('1815.1468')),
    card('orange', 'Contraste', 'Apocalipse 2:5',
         bq('Lembra-te, pois, de onde caíste, e arrepende-te, e pratica as primeiras obras; quando não, brevemente a ti virei e <mark>tirarei do seu lugar o teu castiçal</mark>, se não te arrependeres.'),
         obs='Como o sal que perde o sabor (v.13), o castiçal que não cumpre a sua função é tirado do lugar.',
         link=arc('ap/2/5')),
    card('gray', 'Conclusão', 'O candelabro: luz que não se apaga',
         extra_p=['No santuário, o candelabro ficava no lugar santo, com as sete lâmpadas de ouro sempre acesas, de dia e de noite. No Apocalipse, Cristo anda no meio dos sete castiçais de ouro, que são as igrejas (Ap 1:12,13,20), e Zacarias liga o castiçal e o azeite à promessa “pelo meu Espírito” (Zc 4:2,6).',
                  'É a imagem do v.16: o povo de Deus é o candelabro, a luz vem de Cristo e do Espírito, e acesa deve ficar “no velador”, onde dá luz a todos que estão na casa (v.15).']),
    ])
pagina('v13-15.html', 'Mateus 5:13–16 · Sal e luz — Sermão do Monte', 'Mateus 5:13–16 · o que fazem os bem-aventurados', 'Sal e luz', None, [v13, v14],
       pager(('v10-12.html', '← Anterior', 'v.10–12 · Perseguidos'), ('v17-20.html', 'Próxima →', 'v.17–20 · A lei e a justiça maior')))

# =====================================================================================
# v.17–20  A lei
# =====================================================================================
v17 = grupo('v17', 'Mateus 5:17–19', 'A lei não é abolida',
    bible(n('17', 'Não cuideis que vim destruir a lei ou os profetas; não vim <mark>ab-rogar, mas cumprir</mark>.'),
          n('18', 'Porque em verdade vos digo que, até que o céu e a terra passem, <mark>nem um jota ou um til</mark> se omitirá da lei sem que tudo seja cumprido.'),
          n('19', 'Qualquer, pois, que <mark>violar um destes menores mandamentos</mark> e assim ensinar aos homens <mark>será chamado o menor</mark> no Reino dos céus; aquele, porém, que os <mark>cumprir e ensinar</mark> será chamado grande no Reino dos céus.')),
    [
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 48.3',
         bq('Falando da lei, Jesus disse: “Não vim ab-rogar, mas cumprir.” Ele emprega aqui a palavra “cumprir” no mesmo sentido em que a usou quando declarou a João Batista Seu desígnio de “cumprir toda a justiça” (Mateus 3:15); isto é, <mark>encher a medida do reclamo da lei</mark>, dar um exemplo de perfeita conformidade com a vontade de Deus.'),
         link=egw('1956.273')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 49.3',
         bq('Por Sua própria obediência à lei, Cristo testificou do <mark>caráter imutável</mark> da mesma… Enquanto o céu e a Terra durarem, <mark>os santos princípios da santa lei de Deus permanecerão</mark>.'),
         link=egw('1956.278')),
    card('blue', 'Paralelo', 'Tiago 2:10',
         bq(n('10', 'Porque qualquer que guardar toda a lei e <mark>tropeçar em um só ponto tornou-se culpado de todos</mark>.')),
         obs='Por isso não existe mandamento “pequeno” (v.19).',
         link=arc('tg/2/10')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 51.2',
         bq('<mark>Isto é, não terá lugar ali.</mark> Pois aquele que voluntariamente violar um mandamento, não observa, em espírito e verdade, a nenhum deles.'),
         obs='Sobre o “menor no reino dos Céus” do v.19.',
         link=egw('1956.287')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 51.3',
         bq('Não é a grandeza do ato de desobediência que constitui o pecado mas <mark>a discordância com a vontade expressa de Deus no mínimo particular</mark>…'),
         link=egw('1956.288')),
    card('gray', 'Conclusão', 'Cumprir é dar a lei por inteiro',
         extra_p=['Jesus não veio abolir a lei, veio cumpri-la, e ela permanece enquanto durar o céu e a terra (v.17,18). Por isso nenhum mandamento é pequeno: quem viola um deles e ensina os outros a fazer o mesmo é o “menor”; quem cumpre e ensina é “grande” no Reino dos céus (v.19).',
                  'E nem um jota ou um til: a menor letra e o menor traço da lei não passam sem que tudo se cumpra.']),
    ])
v20 = grupo('v20', 'Mateus 5:20', 'Uma justiça que excede',
    bible(n('20', 'Porque vos digo que, se <mark>a vossa justiça não exceder</mark> a dos <mark>escribas e fariseus</mark>, de modo nenhum entrareis no Reino dos céus.')),
    [
    ('sub', 'Como eram os escribas e fariseus'),
    card('orange', 'Contraste', 'Mateus 23:1–3',
         bq(n('1', 'Então, falou Jesus <mark>à multidão e aos seus discípulos</mark>,'),
            n('2', '…Na cadeira de Moisés, estão assentados os escribas e fariseus.'),
            n('3', 'Observai, pois, e praticai tudo o que vos disserem; mas não procedais em conformidade com as suas obras, porque <mark>dizem e não praticam</mark>.')),
         obs='O ensino podia estar certo. O que faltava era a vida.',
         link=arc('mt/23/1')),
    card('orange', 'Contraste', 'Mateus 23:5',
         bq('E fazem todas as obras <mark>a fim de serem vistos pelos homens</mark>, pois trazem largos filactérios, e alargam as franjas das suas vestes,'),
         obs='No v.16 as obras aparecem para que o Pai seja glorificado. Aqui, para que eles sejam vistos.',
         link=arc('mt/23/5')),
    card('orange', 'Contraste', 'Mateus 23:27,28',
         bq(n('27', '…Pois que sois semelhantes aos <mark>sepulcros caiados</mark>, que por fora realmente parecem formosos, mas <mark>interiormente estão cheios de ossos de mortos</mark> e de toda imundícia.'),
            n('28', 'Assim, também vós <mark>exteriormente pareceis justos</mark> aos homens, mas <mark>interiormente estais cheios de hipocrisia e de iniquidade</mark>.')),
         link=arc('mt/23/27')),
    card('blue', 'Paralelo', '1 Samuel 16:7',
         bq('…Não atentes para a sua aparência… porque o Senhor não vê como vê o homem. Pois <mark>o homem vê o que está diante dos olhos, porém o Senhor olha para o coração</mark>.'),
         link=arc('1sm/16/7')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 53.1',
         bq('Declarou que a justiça a que os fariseus davam tão grande valor, nada valia… Todas as suas pretensões de piedade, suas invenções e cerimônias humanas, e mesmo <mark>o cumprimento das exigências exteriores da lei</mark>, não os podiam tornar santos. <mark>Não eram puros de coração</mark> ou nobres e semelhantes a Cristo no caráter.'),
         link=egw('1956.296')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 54.2',
         bq('Os discípulos de Cristo precisam alcançar <mark>a justiça de um caráter diverso</mark> daquela dos fariseus, se querem entrar no reino do Céu. Em Seu Filho, Deus lhes oferecia a perfeita justiça da lei.'),
         link=egw('1956.302')),
    card('gray', 'Conclusão', 'A justiça que excede vem de dentro',
         extra_p=['Os escribas e fariseus ensinavam a lei, mas viviam para ser vistos (Mt 23:3,5) e cuidavam só do lado de fora, como sepulcros caiados (Mt 23:27,28). A justiça que “excede” não é fazer mais coisas: é a que vem de dentro, onde só Deus vê (1Sm 16:7).',
                  'E ela não nasce de esforço próprio: é a justiça que vem de Deus pela fé em Cristo (Fp 3:9, no <a href="v06.html#v6">v.6</a>). Por isso as bem-aventuranças vêm primeiro: quem tem fome e sede de justiça a recebe.'],
         obs='Nos próximos versículos Jesus amplia a lei, do ato para o coração: o “não matarás” (<a href="v21-26.html#v21">v.21–26</a>) e o “não adulterarás” (<a href="v27-30.html#v27">v.27–30</a>).'),
    ])
pagina('v17-20.html', 'Mateus 5:17–20 · A lei e a justiça maior — Sermão do Monte', 'Mateus 5:17–20 · depois das bem-aventuranças', 'A lei e a justiça maior', None, [v17, v20],
       pager(('v13-15.html', '← Anterior', 'Sal e luz · v.13–16'), ('v21-26.html', 'Próxima →', 'v.21–26 · Da morte à raiva')))

# =====================================================================================
# v.21–26  Raiva
# =====================================================================================
v21 = grupo('v21', 'Mateus 5:21–22', 'Do assassinato à raiva',
    bible(n('21', 'Ouvistes que foi dito aos antigos: <mark>Não matarás</mark>; mas qualquer que matar será réu de juízo.'),
          n('22', 'Eu, porém, vos digo que qualquer que, <mark>sem motivo, se encolerizar</mark> contra seu irmão será réu de juízo, e qualquer que chamar a seu irmão de <mark>raca</mark> será réu do Sinédrio; e qualquer que lhe chamar de <mark>louco</mark> será réu do fogo do inferno.')),
    [
    ('sub', 'O coração e o sentimento'),
    card('blue', 'Paralelo', '1 Samuel 16:7',
         bq('…o homem vê o que está diante dos olhos, <mark>porém o Senhor olha para o coração</mark>.'),
         obs='A lei de fora vê o ato. Deus vê a raiva que ainda não virou ato.',
         link=arc('1sm/16/7')),
    card('blue', 'Paralelo', 'Hebreus 4:12',
         bq('…a palavra de Deus é viva, e eficaz, e mais penetrante do que qualquer espada de dois gumes… e é <mark>apta para discernir os pensamentos e intenções do coração</mark>.'),
         link=arc('hb/4/12')),
    card('blue', 'Paralelo', 'Salmos 139:23,24',
         bq(n('23', '<mark>Sonda-me, ó Deus, e conhece o meu coração</mark>; prova-me e conhece os meus pensamentos.'),
            n('24', 'E vê se há em mim algum caminho mau e guia-me pelo caminho eterno.')),
         link=arc('sl/139/23')),
    card('blue', 'Paralelo', 'Filipenses 2:5–8',
         bq(n('5', 'De sorte que haja em vós <mark>o mesmo sentimento que houve também em Cristo Jesus</mark>,'),
            n('6', 'que, sendo em forma de Deus, <mark>não teve por usurpação ser igual a Deus</mark>;'),
            n('7', 'Mas <mark>aniquilou-se a si mesmo</mark>, tomando a forma de servo…'),
            n('8', 'e, achado na forma de homem, <mark>humilhou-se a si mesmo</mark>, sendo obediente até à morte e morte de cruz.')),
         obs='O “sentimento” que Jesus pede é o de Cristo: humilhar-se, em vez de se exaltar (compare o <a href="v03.html#v3">v.3</a>).',
         link=arc('fp/2/5')),
    card('orange', 'Contraste', 'Isaías 14:13',
         bq('E tu dizias <mark>no teu coração</mark>: Eu subirei ao céu, e, acima das estrelas de Deus, <mark>exaltarei o meu trono</mark>,'),
         obs='A raiz do conflito: querer usurpar, tomar à força, o lugar que é de Deus. Cristo fez o contrário: “não teve por usurpação ser igual a Deus” (Fp 2:6).',
         link=arc('is/14/13')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 56.2',
         bq('<mark>O espírito de ódio e de vingança originou-se com Satanás</mark>… No pensamento de vingança jaz encoberta a má ação, da mesma maneira que <mark>a árvore está na semente</mark>.'),
         link=egw('1956.312')),
    ('sub', 'v.22: ira e desprezo'),
    card('orange', 'Contraste', 'Romanos 12:14',
         bq('<mark>abençoai</mark> aos que vos perseguem; <mark>abençoai e não amaldiçoeis</mark>.'),
         obs='A raiva amaldiçoa; o discípulo abençoa, até a quem o persegue.',
         link=arc('rm/12/14')),
    card('blue', 'Paralelo', 'Isaías 53:3',
         bq('Era <mark>desprezado</mark> e o mais indigno entre os homens, homem de dores… e, como um de quem os homens escondiam o rosto, <mark>era desprezado, e não fizemos dele caso algum</mark>.'),
         obs='“Raca” é desprezo. Foi assim que Cristo foi tratado.',
         link=arc('is/53/3')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 56.3',
         bq('No dom de Seu Filho para nossa redenção, Deus mostrou quão alto valor dá Ele a toda alma humana, e <mark>não dá direito a homem algum de falar desprezivelmente de outro</mark>.'),
         link=egw('1956.313')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 57.2',
         bq('Jesus diz que quem quer que condene seu irmão como apóstata ou desprezador de Deus, <mark>mostra ser ele mesmo digno da mesma condenação</mark>.'),
         obs='Sobre o “louco” do v.22.',
         link=egw('1956.317')),
    card('gray', 'Conclusão', 'A raiva é a semente do assassinato',
         extra_p=['A lei olhava o ato (“não matarás”); Jesus olha a raiz. A raiva sem motivo, o desprezo (“raca”) e a ofensa (“louco”) já são o espírito do assassino (1Jo 3:15, no <a href="#v23">v.23–26</a>).',
                  'Quem tem o sentimento de Cristo (Fp 2:5–8) abençoa em vez de amaldiçoar (Rm 12:14), e pede a Deus: “sonda-me” (Sl 139:23,24).']),
    ])
v23 = grupo('v23', 'Mateus 5:23–26', 'Reconciliar-se antes de oferecer',
    bible(n('23', 'Portanto, se trouxeres a tua oferta ao altar e aí te lembrares de que <mark>teu irmão tem alguma coisa contra ti</mark>,'),
          n('24', 'deixa ali diante do altar a tua oferta, e vai <mark>reconciliar-te primeiro com teu irmão</mark>, e depois vem, e apresenta a tua oferta.'),
          n('25', 'Concilia-te <mark>depressa</mark> com o teu adversário, enquanto estás no caminho com ele, para que não aconteça que o adversário te entregue ao juiz…'),
          n('26', 'Em verdade te digo que, de maneira nenhuma, sairás dali, enquanto não pagares o último ceitil.')),
    [
    card('blue', 'Paralelo', '1 João 3:10,15',
         bq(n('10', 'Nisto são manifestos os filhos de Deus e os filhos do diabo: qualquer que <mark>não pratica a justiça e não ama a seu irmão</mark> não é de Deus.'),
            n('15', 'Qualquer que <mark>aborrece a seu irmão é homicida</mark>. E vós sabeis que nenhum homicida tem permanente nele a vida eterna.')),
         link=arc('1jo/3/10')),
    card('orange', 'Contraste', 'Salmos 101:3',
         bq('Não porei <mark>coisa má diante dos meus olhos</mark>; <mark>aborreço as ações</mark> daqueles que se desviam; nada se me pegará.'),
         obs='Há um aborrecer certo: o das ações más, não o do irmão (compare 1Jo 3:15).',
         link=arc('sl/101/3')),
    card('blue', 'Paralelo', 'Marcos 11:25',
         bq('E, quando estiverdes orando, <mark>perdoai, se tendes alguma coisa contra alguém</mark>, para que vosso Pai, que está nos céus, vos perdoe as vossas ofensas.'),
         link=arc('mc/11/25')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 58.2',
         bq('A oferta sacrifical exprimia fé em que, mediante Cristo, o ofertante se havia tornado participante da misericórdia e do amor de Deus. Mas, <mark>que uma pessoa exprimisse fé no amor perdoador de Deus, enquanto, por sua vez, condescendia com um espírito de desamor, seria simplesmente uma farsa</mark>.'),
         link=egw('1956.324')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 58.3',
         bq('Talvez nosso irmão nos tenha feito um maior agravo do que nós a ele, mas <mark>isto não diminui a nossa responsabilidade</mark>… cumpre-nos deixar a nossa oferta de oração, ou de ações de graças, ou a oferta voluntária, e ir ter com o irmão com quem estamos em desinteligência'),
         link=egw('1956.325')),
    card('gray', 'Conclusão', 'Antes de oferecer, reconciliar',
         extra_p=['Quem odeia o irmão não pode oferecer nada a Deus: o culto sem amor ao irmão é uma farsa. Por isso Jesus manda deixar a oferta diante do altar e ir primeiro reconciliar-se, e depressa (v.24,25).',
                  'Reconciliar-se é a obra do pacificador (<a href="v09.html#v9">v.9</a>) e o fruto de quem é misericordioso (<a href="v07.html#v7">v.7</a>).']),
    ])
pagina('v21-26.html', 'Mateus 5:21–26 · Da morte à raiva — Sermão do Monte', 'Mateus 5:21–26 · depois das bem-aventuranças', 'Da morte à raiva', None, [v21, v23],
       pager(('v17-20.html', '← Anterior', 'v.17–20 · A lei e a justiça maior'), ('v27-30.html', 'Próxima →', 'v.27–30 · Do adultério à cobiça')))

# =====================================================================================
# v.27–30  Cobiça
# =====================================================================================
v27 = grupo('v27', 'Mateus 5:27–28', 'Do adultério à cobiça',
    bible(n('27', 'Ouvistes que foi dito aos antigos: <mark>Não cometerás adultério</mark>.'),
          n('28', 'Eu porém, vos digo que qualquer que <mark>atentar numa mulher para a cobiçar</mark> já <mark>em seu coração</mark> cometeu adultério com ela.')),
    [
    card('blue', 'Paralelo', 'Tiago 2:11–13',
         bq(n('11', 'Porque aquele que disse: <mark>Não cometerás adultério, também disse: Não matarás</mark>. Se tu, pois, não cometeres adultério, mas matares, estás feito transgressor da lei.'),
            n('12', 'Assim falai e assim procedei, como devendo ser julgados <mark>pela lei da liberdade</mark>.'),
            n('13', 'Porque o juízo será <mark>sem misericórdia</mark> sobre aquele que não fez misericórdia; e <mark>a misericórdia triunfa sobre o juízo</mark>.')),
         obs='Os dois mandamentos que Jesus amplia vêm do mesmo Legislador: o “não matarás” (<a href="v21-26.html#v21">v.21</a>) e o “não adulterarás”.',
         link=arc('tg/2/11')),
    ('sub', 'O desejo nasce no coração'),
    card('blue', 'Paralelo', '1 Samuel 16:7',
         bq('…<mark>o Senhor olha para o coração</mark>.'),
         obs='Como no <a href="v21-26.html#v21">v.21</a>: a lei de fora vê o ato; Deus vê o desejo.',
         link=arc('1sm/16/7')),
    card('blue', 'Paralelo', 'Mateus 15:18,19',
         bq(n('18', 'Mas o que sai da boca <mark>procede do coração</mark>, e isso contamina o homem.'),
            n('19', 'Porque do coração procedem os <mark>maus pensamentos, mortes, adultérios</mark>, prostituição, furtos, falsos testemunhos e blasfêmias.')),
         obs='Mortes e adultérios, os dois mandamentos ampliados, saem do mesmo lugar.',
         link=arc('mt/15/18')),
    card('blue', 'Paralelo', 'Tiago 1:14,15',
         bq(n('14', 'Mas cada um é tentado, quando atraído e engodado pela sua própria <mark>concupiscência</mark>.'),
            n('15', 'Depois, havendo a concupiscência concebido, <mark>dá à luz o pecado</mark>; e o pecado, sendo consumado, gera a morte.')),
         obs='Concupiscência é o desejo mau.',
         link=arc('tg/1/14')),
    card('blue', 'Paralelo', 'Isaías 14:13',
         bq('E tu dizias <mark>no teu coração</mark>: Eu subirei ao céu…'),
         obs='O desejo de ter o que não é seu, cobiçar, nasce “no coração” e fala ali, antes de qualquer ato (compare o <a href="v08.html#v8">v.8</a>).',
         link=arc('is/14/13')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 59.3',
         bq('Os judeus orgulhavam-se de sua moralidade, e olhavam com horror às práticas sensuais dos pagãos… mas qual não foi seu espanto ao escutarem <mark>palavras que punham a descoberto o mal de seus próprios corações</mark>!'),
         link=egw('1956.331')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 60.1',
         bq('Quando o pensamento do mal é amado e nutrido, embora secretamente, disse Jesus, isso mostra que o pecado ainda reina no coração… O período de tentação… <mark>não cria o mal revelado, mas apenas desenvolve ou torna manifesto aquilo que estava oculto e latente no coração</mark>.'),
         link=egw('1956.334')),
    ('sub', 'O que fazer com os pensamentos'),
    card('blue', 'Paralelo', 'Filipenses 4:8',
         bq('Quanto ao mais, irmãos, tudo o que é verdadeiro, tudo o que é honesto, tudo o que é justo, tudo o que é puro, tudo o que é amável, tudo o que é de boa fama, se há alguma virtude, e se há algum louvor, <mark>nisso pensai</mark>.'),
         link=arc('fp/4/8')),
    card('blue', 'Paralelo', 'Isaías 55:7,8',
         bq(n('7', 'Deixe o ímpio o seu caminho, e o homem maligno, <mark>os seus pensamentos</mark> e se converta ao Senhor, que se compadecerá dele…'),
            n('8', 'Porque <mark>os meus pensamentos não são os vossos pensamentos</mark>, nem os vossos caminhos, os meus caminhos, diz o Senhor.')),
         link=arc('is/55/7')),
    card('blue', 'Paralelo', '1 Crônicas 29:17,18',
         bq(n('17', 'E bem sei eu, Deus meu, que <mark>tu provas os corações</mark> e que <mark>da sinceridade te agradas</mark>…'),
            n('18', 'Senhor, Deus de nossos pais Abraão, Isaque e Israel, <mark>conserva isso para sempre no intento dos pensamentos do coração</mark> de teu povo; e encaminha o seu coração para ti.')),
         link=arc('1cr/29/17')),
    card('green', 'Exemplo', 'Jó 31:1',
         bq('<mark>Fiz concerto com os meus olhos</mark>; como, pois, os fixaria numa virgem?'),
         obs='Jó decidiu de antemão para onde não olharia. “Concerto” é pacto, compromisso.',
         link=arc('job/31/1')),
    card('gray', 'Conclusão', 'O desejo é a semente',
         extra_p=['Os fariseus se orgulhavam de não fazer o que os pagãos faziam. Jesus mostra que o pecado já está onde ninguém vê: no desejo. A tentação não cria o mal, apenas o faz aparecer (MDC 60.1).',
                  'Por isso a defesa começa no que se pensa (Fp 4:8), no que se deixa Deus examinar (1Cr 29:17; Sl 139:23,24) e no que se decide não olhar (Jó 31:1; Sl 101:3).']),
    ])
v29 = grupo('v29', 'Mateus 5:29–30', 'Arrancar o olho, cortar a mão',
    bible(n('29', 'Portanto, se o teu <mark>olho direito</mark> te escandalizar, <mark>arranca-o</mark> e atira-o para longe de ti, pois te é melhor que se perca um dos teus membros do que todo o teu corpo seja lançado no inferno.'),
          n('30', 'E, se a tua <mark>mão direita</mark> te escandalizar, <mark>corta-a</mark> e atira-a para longe de ti, porque te é melhor que um dos teus membros se perca do que todo o teu corpo seja lançado no inferno.')),
    [
    card('blue', 'Paralelo', 'Mateus 18:8,9',
         bq(n('8', 'Portanto, se a tua mão ou o teu pé te escandalizar, <mark>corta-o</mark> e atira-o para longe de ti; <mark>melhor te é entrar na vida coxo ou aleijado</mark>…'),
            n('9', 'E, se o teu olho te escandalizar, <mark>arranca-o</mark>, e atira-o para longe de ti. <mark>Melhor te é entrar na vida com um só olho</mark>…')),
         link=arc('mt/18/8')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 61.1',
         bq('É mediante a vontade que o pecado retém seu domínio sobre nós. <mark>A entrega da vontade é representada como arrancar o olho ou cortar a mão.</mark> Afigura-se-nos muitas vezes que, sujeitar a vontade a Deus é o mesmo que consentir em atravessar a vida mutilado ou aleijado. É melhor, porém, diz Cristo, que o eu seja mutilado, ferido, aleijado, contanto que possais entrar na vida.'),
         link=egw('1956.340')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 60.2',
         bq('A fim de impedir que a doença se alastre ao corpo e destrua a vida, um homem se submeteria mesmo a separar-se de sua mão direita. <mark>Muito mais deve ele estar pronto a entregar aquilo que põe em risco a vida da alma.</mark>'),
         link=egw('1956.336')),
    card('purple', 'Ellen White', 'O Maior Discurso de Cristo, p. 62.2',
         bq('Exigirá um sacrifício o entregar-se a Deus; é, porém, <mark>um sacrifício do inferior pelo mais elevado, do terreno pelo espiritual, do perecível pelo eterno</mark>.'),
         link=egw('1956.345')),
    card('gray', 'Conclusão', 'Renunciar é cortar o que leva ao pecado',
         extra_p=['Ninguém é chamado a se mutilar: o que Jesus pede é a entrega da vontade (MDC 61.1). Mas a renúncia precisa ser tão radical quanto arrancar um olho: o que faz tropeçar não pode ficar, por mais precioso que seja.',
                  'O que parece perda é, nas palavras de Ellen White, “a porta para um mais elevado bem”. E o preço de ficar com o que faz tropeçar é todo o corpo no inferno (v.29,30).']),
    ])
pagina('v27-30.html', 'Mateus 5:27–30 · Do adultério à cobiça — Sermão do Monte', 'Mateus 5:27–30 · depois das bem-aventuranças', 'Do adultério à cobiça', None, [v27, v29],
       pager(('v21-26.html', '← Anterior', 'v.21–26 · Da morte à raiva'), ('depois.html', 'Voltar →', 'A trilha · depois das bem-aventuranças')),
       final='<aside class="em-construcao">\n  <span class="selo">A construir</span>\n  <p>Este é, por enquanto, o último trecho estudado do Sermão do Monte. O restante (Mateus 5:31 em diante) está marcado como “A construir” no <a href="index.html">mapa do sermão</a>.</p>\n</aside>')

# =====================================================================================
# depois.html — a trilha: o que vem depois das bem-aventuranças (página própria, layout diferente)
# =====================================================================================
def passo(num, href, vs, titulo, texto, fora, dentro, chips):
    return ('    <li class="passo">\n'
            '      <span class="marca" aria-hidden="true">%s</span>\n'
            '      <a class="cartao" href="%s">\n'
            '        <span class="vs">%s</span>\n'
            '        <span class="tt">%s</span>\n'
            '        <span class="tx">%s</span>\n'
            '        <span class="fd"><span class="fora"><b>Por fora</b>%s</span><span class="seta" aria-hidden="true">→</span><span class="dentro"><b>Por dentro</b>%s</span></span>\n'
            '        <span class="chips">%s</span>\n'
            '        <span class="ir">Abrir este passo →</span>\n'
            '      </a>\n'
            '    </li>' % (num, href, vs, titulo, texto, fora, dentro,
                           ''.join('<span>%s</span>' % c for c in chips)))


HUB_PASSOS = '\n'.join([
    passo('1', 'v13-15.html#v14', 'Mateus 5:13–16', 'Sal e luz',
          'O que os bem-aventurados vivem, eles levam ao mundo: dão sabor, iluminam e deixam ver as boas obras, para que o Pai seja glorificado.',
          'obras que se veem', 'para glorificar o Pai, não a si', ['sal × doce', 'luz × trevas', 'o candelabro']),
    passo('2', 'v17-20.html#v17', 'Mateus 5:17–20', 'A lei e a justiça maior',
          'Jesus não veio abolir a lei, veio cumprir. Nenhum mandamento é pequeno, e a justiça do Reino precisa exceder a dos escribas e fariseus.',
          'os escribas e fariseus: dizem e não fazem', 'uma justiça que vem de dentro', ['jota e til', 'o menor no reino', 'sepulcros caiados']),
    passo('3', 'v21-26.html#v21', 'Mateus 5:21–26', 'Da morte à raiva',
          'O assassinato começa no coração: a raiva, o desprezo e a ofensa. E o culto sem amor ao irmão não vale: primeiro reconciliar-se.',
          '“Não matarás”', 'nem a raiva, nem o desprezo', ['raca', 'sonda-me', 'reconciliar-se']),
    passo('4', 'v27-30.html#v27', 'Mateus 5:27–30', 'Do adultério à cobiça',
          'O adultério também começa por dentro, no olhar que cobiça. Por isso Jesus pede uma renúncia radical, como arrancar o olho e cortar a mão.',
          '“Não adulterarás”', 'nem o olhar que cobiça', ['o desejo', 'os pensamentos', 'arrancar o olho']),
])

def passo_breve(num, vs, titulo, texto):
    return ('    <li class="passo breve">\n'
            '      <span class="marca" aria-hidden="true">%s</span>\n'
            '      <div class="cartao">\n'
            '        <span class="vs">%s · <b class="st">A construir</b></span>\n'
            '        <span class="tt">%s</span>\n'
            '        <span class="tx">%s</span>\n'
            '      </div>\n'
            '    </li>' % (num, vs, titulo, texto))


HUB_BREVES = '\n'.join([
    passo_breve('5', 'Mateus 5:31–32', 'Divórcio', 'O ensino de Jesus sobre o divórcio.'),
    passo_breve('6', 'Mateus 5:33–37', 'Juramentos', 'O ensino de Jesus sobre os juramentos.'),
    passo_breve('7', 'Mateus 5:38–42', 'Olho por olho', 'Como responder ao mal.'),
    passo_breve('8', 'Mateus 5:43–48', 'Amor aos inimigos', 'Amar os inimigos e orar pelos que perseguem.'),
])

HUB = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
       '<title>Depois das bem-aventuranças · Mateus 5:13–48 — Sermão do Monte</title>\n<link rel="stylesheet" href="style.css">\n</head>\n<body class="depois">\n'
       + BARRA + '\n<div class="wrap">\n\n' + crumbs('depois.html') + '''

<header class="dp-hero">
  <p class="kicker">Sermão do Monte · Mateus 5:13–48</p>
  <h1>Depois das bem-aventuranças</h1>
  <p class="lede">Jesus acabou de dizer quem é bem-aventurado. Agora mostra o que isso muda na vida: o que os bem-aventurados levam ao mundo (sal e luz) e como a lei deve ser vivida, não só por fora, mas por dentro.</p>
  <blockquote class="chave">
    <span class="rotulo">O fio da trilha · Mateus 5:20</span>
    <p><span class="n">20</span>Porque vos digo que, se <mark>a vossa justiça não exceder</mark> a dos <mark>escribas e fariseus</mark>, de modo nenhum entrareis no Reino dos céus.</p>
  </blockquote>
</header>

<p class="dp-guia">Do 1 ao 4, os passos já estão prontos. Do 5 ao 8, ainda vão ser feitos. Em cada passo, Jesus tira a lei do <b>lado de fora</b> e a leva para o <b>coração</b>.</p>

<ol class="trilha">
''' + HUB_PASSOS + '''
''' + HUB_BREVES + '''
</ol>

<section class="dp-fecho" aria-labelledby="fecho">
  <article class="note gray">
    <span class="tag">Conclusão</span>
    <h3 id="fecho">De fora para dentro</h3>
    <p>Os escribas e fariseus cuidavam da aparência: obras para serem vistos, palavras sem prática, sepulcros caiados por fora. Jesus pede a justiça que começa onde só Deus vê, e que ninguém produz sozinho: ela é dada por Deus a quem tem fome e sede dela.</p>
    <p class="obs">É por isso que as bem-aventuranças vêm primeiro: o pobre de espírito reconhece que precisa dela, e a recebe.</p>
    <p class="obs">Para fechar a mensagem: <a href="caminho-ampliado.html">rever o caminho e as portas</a>. Para ver o sermão inteiro: <a href="index.html">mapa do Sermão do Monte</a>.</p>
  </article>
</section>

</div>
''' + pixel('depois.html') + '\n</body>\n</html>\n')
gravar(DEST, 'depois.html', HUB, RASC)

print('ok')

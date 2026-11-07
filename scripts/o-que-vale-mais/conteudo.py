# -*- coding: utf-8 -*-
# Conteúdo das páginas do estudo "O que vale mais?" (textos, cenas e cartões de leitura).
# Regra de ouro: até a parte 5 nada fala de Deus; a primeira menção é na parte 6; o objetivo só é dito na parte 10 e na conclusão.
import dados as D
import vinhetas as V
from cartoes import biblia, egw, fato, reflexao, imaginacao, curiosos, grade, referencia, CACHE

PARTES = {}
VERSOS = {}   # nome -> {ref, t}: versículos e trechos citados nos painéis (texto literal do cache; vai para dados.js como OVM_V)


def regv(nome, *chaves):
    VERSOS[nome] = {'ref': referencia(list(chaves)) + ' (ARC)', 't': ' '.join(CACHE['biblia'][c] for c in chaves)}


def regegw(nome, pid, trecho, obra):
    d = CACHE['egw'][pid]
    assert trecho in d['texto'], 'trecho não está no parágrafo %s' % pid
    VERSOS[nome] = {'ref': 'Ellen G. White, %s (%s)' % (obra, d['ref']), 't': trecho}

CAPA = dict(
    descricao='Um estudo em etapas que começa numa xícara de café e vai muito longe.',
    kicker='Um estudo em etapas',
    lede='Quase toda escolha que a gente faz esconde uma pergunta. Esta jornada começa numa xícara de café e vai muito, muito longe.',
    meta='10 partes · uns 40 minutos · melhor no celular, em pé ou deitado',
)

# ======================================================================================================================
# PARTE 1 — Tudo o que a gente quer tem um preço  (o botão do retorno)
# ======================================================================================================================
NOMES_CURTOS = ['☕ Café', '🍽️ Refeição', '🏖️ Fim de semana', '✈️ Viagem', '🚗 Carro', '🏠 Casa']
vigs = []
for i, svg in enumerate(V.TODAS):
    svg = svg.replace('<svg class="vinheta', '<svg preserveAspectRatio="xMidYMid slice" class="vinheta', 1)
    p = D.PRECOS[i]
    vigs.append('<figure class="vig" data-i="%d">%s<figcaption><b>R$ %s</b><span>%s</span></figcaption></figure>' % (i, svg, p['texto'], p['nome']))

P1_PALCO = '''<div class="p1-cena" id="p1">
  <div class="p1-vinhetas" id="p1-vinhetas">
%s
  </div>
  <div class="p1-brilho" id="p1-brilho"></div>
  <div class="p1-termos" aria-hidden="true">
    <div class="termo preco"><span class="rot" title="Preço">R$</span><div class="barra"><i id="p1-fio-preco"></i></div></div>
    <div class="termo retorno"><span class="rot" title="Retorno">✦</span><div class="barra"><i id="p1-fio-ret"></i></div></div>
  </div>
  <div class="p1-etiqueta" id="p1-etq" aria-hidden="true"><span class="furo"></span><span class="aprox" id="p1-aprox" hidden>≈</span><span class="rs">R$</span><b id="p1-valor">6,98</b></div>
  <p class="p1-nome" id="p1-nome" aria-hidden="true">Um café</p>
</div>''' % '\n'.join(vigs)

P1_CONTROLES = '''<label class="ctrl-rotulo" for="p1-botao"><span>O botão do retorno</span><output id="p1-saida">Um café</output></label>
<input type="range" id="p1-botao" min="0" max="5" step="1" value="0" aria-describedby="rotulo">
<ul class="chips" id="p1-chips">%s</ul>''' % ''.join('<li><button type="button" class="chip" data-i="%d">%s</button></li>' % (i, n) for i, n in enumerate(NOMES_CURTOS))

RAZAO = D.PRECOS[-1]['valor'] / D.PRECOS[0]['valor']
assert RAZAO > 77000

P1_LEITURA = [(
    'Para pensar',
    'Estes números foram conferidos em novembro de 2026. Cada conta e cada fonte está em "Conta e fonte", dentro da cena.',
    grade([
        fato('Do café à casa, quanto o preço sobe?',
             '<p>Um café custa cerca de <b>R$ 7</b>. Uma casa de 60 m² custa cerca de <b>R$ 542 mil</b>. A casa custa <b>mais de 77 mil vezes</b> o preço do café: dá para tomar mais de 77 mil cafés pelo preço de uma casa.</p>',
             obs='Conta: R$ 542.520 ÷ R$ 6,98 ≈ 77.725.'),
        reflexao('O que vale mais custa mais',
                 '<p>Repare no que cada coisa devolve: o café, uns minutos; a refeição, algumas horas; o fim de semana, dois dias; a viagem, anos de lembrança; o carro, muitos anos; a casa, décadas. '
                 'Quanto mais tempo dura o que recebemos, e quanto mais gente alcança, mais caro costuma ser.</p>'
                 '<p>Essa é a ideia que vai nos acompanhar: <b>para receber, é preciso pagar</b>, e o que vale mais custa mais.</p>'),
    ]) + '\n' + curiosos('Como os preços foram conferidos',
             '<p>Café: Procon-SP, setembro de 2026. Refeição: Ticket/Edenred, 2024. Fim de semana: FOHB, maio de 2026. Viagem: Catraca Livre, fevereiro de 2026, com o dólar do Banco Central de 5/11/2026. '
             'Carro: UOL Carros, novembro de 2026. Casa: Índice FipeZAP, outubro de 2026. Detalhes em <a href="fontes.html">Fontes</a>.</p>'),
)]

PARTES[1] = dict(titulo='Tudo o que a gente quer tem um preço', tema='dia', script='p01.js', palco=P1_PALCO, controles=P1_CONTROLES, leitura=P1_LEITURA)

# ======================================================================================================================
# PARTE 2 — A viagem mais cara  (foguete e preços)
# ======================================================================================================================
P2_PALCO = '''<div class="p2-cena" id="p2">
  <canvas id="tela" aria-hidden="true"></canvas>
  <div class="p1-etiqueta" id="p2-etq" aria-hidden="true" style="opacity:0"></div>
  <p class="p2-alt" id="p2-alt" aria-hidden="true"></p>
</div>'''

P2_CONTROLES = '''<label class="ctrl-rotulo" for="p2-botao"><span>Até onde ir?</span><output id="p2-saida">Na plataforma</output></label>
<input type="range" id="p2-botao" min="0" max="4" step="1" value="0" aria-describedby="rotulo">
<ul class="chips" id="p2-chips">%s</ul>''' % ''.join('<li><button type="button" class="chip" data-i="%d">%s</button></li>' % (i, v['chip']) for i, v in enumerate(D.VIAGENS))

P2_LEITURA = [(
    'Para pensar',
    'Preços conferidos em novembro de 2026, com o dólar do Banco Central de 05/11/2026 (R$ 5,46). Cada conta e cada fonte está em "Conta e fonte", dentro da cena.',
    grade([
        fato('Sair do planeta custa milhões',
             '<p>Perto da beira do espaço, um assento anunciado custou <b>US$ 750 mil</b> (cerca de R$ 4,1 milhões); numa estação em órbita, algo como <b>US$ 55 a 70 milhões</b> (mais de R$ 300 milhões). '
             'Para a Lua não existe passagem à venda. Para Marte existe só uma <b>meta</b>: menos de US$ 500 mil, "um dia".</p>',
             obs='Conta: US$ 65 milhões × R$ 5,4621 ≈ R$ 355 milhões. Os valores mudam; o que fica é a ideia.'),
        reflexao('Quanto mais longe, mais caro (ou impossível de comprar)',
                 '<p>Na parte 1, o preço subiu junto com o que se recebe. Aqui ele sobe junto com a <b>distância</b>: cada parada é muito mais longe, e muito mais cara, que a anterior.</p>'
                 '<p>Mas ficou no ar uma pergunta: <b>quanto é "longe"?</b> Para responder, precisamos de uma régua.</p>'),
    ]) + '\n' + curiosos('Como os preços foram conferidos',
             '<p>Beira do espaço: Virgin Galactic (março e agosto de 2026); Blue Origin, assento leiloado em 2021 por US$ 28 milhões. Estação Espacial: reportagens sobre a Axiom Space (US$ 55 milhões nas primeiras missões; US$ 59 a 70 milhões na Ax-4, 2025). '
             'Marte: Elon Musk, em 2019 e 2022, falou em menos de US$ 500 mil e em US$ 100 mil como exemplo; é meta, não preço, e ainda não existe viagem tripulada. Câmbio: Banco Central. Detalhes em <a href="fontes.html">Fontes</a>.</p>'),
)]

PARTES[2] = dict(titulo='A viagem mais cara', tema='noite', script='p02.js', motor=True, palco=P2_PALCO, controles=P2_CONTROLES, leitura=P2_LEITURA)

# ======================================================================================================================
# PARTE 3 — Quanto a luz anda?  (carro, voltas na Terra, régua do tempo, ano-luz)
# ======================================================================================================================
P3_PALCO = '''<div class="p3-cena" id="p3">
  <canvas id="tela" aria-hidden="true"></canvas>
</div>'''

TEMPOS3 = [('1 segundo', 0), ('1 minuto', 1.778), ('1 hora', 3.556), ('1 dia', 4.936), ('1 mês', 6.42), ('1 ano', 7.499)]
P3_CONTROLES = '''<label class="ctrl-rotulo" for="p3-botao"><span>Quanto tempo a luz anda?</span><output id="p3-saida">1 segundo</output></label>
<input type="range" id="p3-botao" min="0" max="750" step="1" value="0" aria-describedby="rotulo">
<ul class="chips" id="p3-chips">%s</ul>''' % ''.join('<li><button type="button" class="chip" data-v="%d">%s</button></li>' % (round(v * 100), n) for n, v in TEMPOS3)

P3_LEITURA = [(
    'Para pensar',
    'Os números desta parte são medidas oficiais e contas simples. Dá para refazer cada uma na calculadora.',
    grade([
        fato('A velocidade da luz',
             '<p>A luz, no vácuo, anda <b>299.792.458 metros por segundo</b>: é o valor exato adotado pelo Sistema Internacional de Unidades (cerca de 300 mil km por segundo). Em 1 segundo ela dá <b>7,5 voltas</b> na Terra '
             '(299.792 km ÷ 40.075 km da circunferência no Equador).</p>',
             obs='Um carro a 100 km/h anda 27,8 m em 1 segundo. Razão: 299.792 km/s ÷ (100 km ÷ 3.600 s) ≈ 10,8 milhões de vezes.'),
        fato('O ano-luz',
             '<p>Um <b>ano-luz</b> é a distância que a luz percorre em um ano: cerca de <b>9,46 trilhões de km</b> (299.792 km/s × 31.557.600 s, o ano de 365,25 dias). É medida de <b>distância</b>, não de tempo.</p>',
             obs='A sonda Voyager 1, a mais distante que o ser humano já mandou, anda a cerca de 17 km/s: levaria uns 17,6 mil anos para andar 1 ano-luz.'),
    ]),
)]

PARTES[3] = dict(titulo='Quanto a luz anda?', tema='noite', script='p03.js', motor=True, palco=P3_PALCO, controles=P3_CONTROLES, leitura=P3_LEITURA)

# ======================================================================================================================
# PARTE 4 — Perto e longe  (o tempo que a luz leva até cada lugar; Voyager 1)
# ======================================================================================================================
P4_PALCO = '''<div class="p4-cena" id="p4">
  <canvas id="tela" aria-hidden="true"></canvas>
</div>'''

NOMES4 = [('lua', '🌕 Lua'), ('sol', '☀️ Sol'), ('venus', '♀ Vênus'), ('marte', '🔴 Marte'), ('jupiter', '🪐 Júpiter'), ('netuno', '🔵 Netuno'), ('voyager', '🛰️ Voyager 1'), ('proxima', '⭐ Próxima')]
P4_CONTROLES = '''<p class="ctrl-dica" id="p4-dica">Toque num lugar no mapa, ou escolha aqui:</p>
<ul class="chips" id="p4-chips">%s</ul>''' % ''.join('<li><button type="button" class="chip" data-c="%s">%s</button></li>' % (c, n) for c, n in NOMES4)

P4_LEITURA = [(
    'Para pensar',
    'Distâncias de fichas técnicas da NASA e do Sistema Internacional. A posição da Voyager 1 vem da página oficial da missão (conferida em 6 de novembro de 2026).',
    grade([
        fato('A Voyager 1 e o "dia-luz"',
             '<p>A NASA informa que, em <b>18 de novembro de 2026</b>, a <b>Voyager 1</b> chegará a <b>1 dia-luz</b> da Terra: cerca de <b>25,9 bilhões de km</b>, a distância que a luz percorre em 24 horas. Lançada em 1977, ela levou cerca de <b>49 anos</b> para chegar onde a luz chega em 1 dia.</p>'
             '<p>Por isso, um comando enviado para ela leva cerca de 1 dia para chegar, e a resposta, outro dia.</p>',
             fontes=[('NASA: o que é um dia-luz (Voyager 1)', 'https://science.nasa.gov/mission/voyager/voyager-1/voyager-1-what-is-a-light-day/')],
             obs='Conta de conferência: 25,9 bilhões de km ÷ 17 km/s ≈ 1,5 bilhão de segundos ≈ 48 anos (a velocidade média da viagem foi um pouco diferente de 17 km/s).'),
        fato('Ainda longe da estrela mais próxima',
             '<p>A estrela mais próxima do Sol, <b>Próxima do Centauro</b>, está a <b>4,2 anos-luz</b>. A Voyager 1 percorreu, em quase 50 anos, cerca de <b>0,06%</b> desse caminho; no ritmo atual, levaria uns <b>75 mil anos</b> para chegar lá.</p>',
             obs='Conta: 1 dia-luz ÷ 4,25 anos-luz ≈ 0,064%. 4,25 anos-luz ÷ 17 km/s ≈ 75 mil anos.'),
    ]) + '\n' + curiosos('De onde vêm os números',
             '<p>Distâncias da Terra: Lua 363.300 a 405.500 km; Sol 147,1 a 152,1 milhões de km; Vênus 38 a 261 milhões; Marte 55 a 401 milhões; Júpiter 588 a 968 milhões; Netuno 4,3 a 4,7 bilhões (NASA, fichas dos planetas). '
             'O tempo da luz é a distância dividida por 299.792 km/s. Como os planetas se movem, mostramos uma <b>faixa</b> (da mais perto à mais longe). Detalhes em <a href="fontes.html">Fontes</a>.</p>'),
)]

PARTES[4] = dict(titulo='Perto e longe', tema='noite', script='p04.js', motor=True, palco=P4_PALCO, controles=P4_CONTROLES, leitura=P4_LEITURA)

# ======================================================================================================================
# PARTE 5 — A escada do universo  (zoom out por degraus; parsec numa caixa opcional)
# ======================================================================================================================
P5_PALCO = '''<div class="p5-cena" id="p5">
  <canvas id="tela" aria-hidden="true"></canvas>
  <div class="p5-hud" aria-hidden="true"><b id="hud-nome"></b><span id="hud-tam"></span><small id="hud-pc"></small></div>
  <ol class="p5-escada" id="p5-escada" aria-label="Degraus da escada do universo"></ol>
  <p class="p5-alem" id="p5-alem" aria-hidden="true">e além disso?</p>
</div>'''

def _lista_niveis():
    li = []
    for i, n, al, o in D.NIVEIS:
        km = al * D.ANO_LUZ_KM
        if km < 1e6:
            t = '%s km' % ('{:,.0f}'.format(km).replace(',', '.'))
        elif km < D.ANO_LUZ_KM * 0.1:
            t = '%s de km' % ('9 bilhões' if i == 'sistema' else '769 mil')
        else:
            t = '{} anos-luz'.format({'vizinhanca': '20', 'galaxia': '100 mil', 'grupo': '10 milhões de', 'super': '520 milhões de', 'universo': '93 bilhões de'}[i])
        if i == 'lua':
            t = '769 mil km'
        li.append('<li><b>%s:</b> %s</li>' % (n, t.replace('anos-luz', 'de anos-luz') if False else t))
    return '<ul class="lista">%s</ul>' % ''.join(li)

P5_PARALAXE = '''<p>Para medir estrelas <b>próximas</b>, os astrônomos usam a <b>paralaxe</b>. A Terra gira em volta do Sol; por isso, uma estrela próxima parece mudar de lugar contra o fundo de estrelas distantes. Quanto <b>menor</b> o deslocamento, <b>mais longe</b> está a estrela.</p>
<div class="par-box">
  <canvas id="par-tela" aria-label="A Terra na órbita e a estrela que parece se deslocar"></canvas>
  <label class="ctrl-rotulo" for="par-mes"><span>Posição da Terra na órbita</span><output id="par-saida">0 meses</output></label>
  <input type="range" id="par-mes" min="0" max="120" step="1" value="0">
  <ul class="chips" id="par-chips"><li><button type="button" class="chip ativo" data-k="perto">Estrela mais perto</button></li><li><button type="button" class="chip" data-k="longe">Estrela mais longe</button></li></ul>
</div>
<p><b>Parsec</b> é a distância em que uma estrela mostraria <b>1 segundo de arco</b> (1/3.600 de grau) de paralaxe. 1 parsec = <b>3,26 anos-luz</b> = 30,9 trilhões de km. Não é "um ano-luz um pouco maior": é uma régua que <b>nasce do método de medir</b>.</p>
<p>O parsec ganha sentido nos múltiplos: <b>quiloparsec</b> (mil parsecs), <b>megaparsec</b> (um milhão) e <b>gigaparsec</b> (um bilhão). O universo observável tem cerca de <b>28,5 gigaparsecs</b> de diâmetro, os mesmos 93 bilhões de anos-luz.</p>'''

P5_LEITURA = [(
    'Para pensar',
    'Todos os tamanhos vêm de fontes científicas (NASA, Nature, União Astronômica Internacional) e estão resumidos em "Fontes".',
    grade([
        fato('Os degraus da escada', '<p>Do menor para o maior, de lado a lado:</p>' + _lista_niveis(),
             obs='As distâncias ficam cada vez mais difíceis de imaginar: por isso a régua certa deixa de ser o quilômetro e passa a ser o ano-luz.'),
        fato('Quantas galáxias?', '<p>As estimativas variam de <b>centenas de bilhões</b> até cerca de <b>2 trilhões</b> de galáxias no universo observável. Só o superaglomerado Laniakea, onde a nossa galáxia mora, tem uns <b>100 mil</b> grandes galáxias.</p>',
             fontes=[('Tully et al., Nature (2014): Laniakea', 'https://www.nature.com/articles/nature13674'), ('NASA: censo de galáxias do Hubble', 'https://science.nasa.gov/missions/hubble/hubble-reveals-observable-universe-contains-10-times-more-galaxies-than-previously-thought/')]),
        fato('Por que "observável"?', '<p>Só vemos o que a luz teve tempo de chegar até nós desde o começo do universo (cerca de 13,8 bilhões de anos). Com a expansão do espaço, a borda do que dá para ver está hoje a uns <b>46,5 bilhões de anos-luz</b> de nós, em todas as direções: daí os <b>93 bilhões</b> de diâmetro. <b>O que há além disso ninguém sabe.</b></p>',
             fontes=[('Observable universe (Wikipédia)', 'https://en.wikipedia.org/wiki/Observable_universe')]),
        fato('Constelações não são lugares', '<p>As constelações são <b>desenhos</b> que vemos do céu da Terra. As estrelas de um mesmo desenho podem estar a distâncias muito diferentes: no Cruzeiro do Sul, a estrela Gacrux fica a uns <b>88</b> anos-luz; a Mimosa, a uns <b>350</b>. Por isso elas não entram na escada: não são degraus, são figuras.</p>',
             fontes=[('Crux (Wikipédia)', 'https://en.wikipedia.org/wiki/Crux')], obs='Os valores variam um pouco conforme o catálogo de estrelas.'),
    ]) + '\n' + curiosos('Como os astrônomos medem? A paralaxe e o parsec', P5_PARALAXE),
)]

PARTES[5] = dict(titulo='A escada do universo', tema='noite', script='p05.js', motor=True, palco=P5_PALCO, controles='', leitura=P5_LEITURA)

# ======================================================================================================================
# PARTE 6 — Quem fez tudo isto?  (primeira menção a Deus; o céu, as estrelas chamadas pelo nome)
# ======================================================================================================================
regv('sl19', 'sl/19/1'); regv('is4026', 'is/40/26'); regv('sl8', 'sl/8/3', 'sl/8/4'); regv('cl1617', 'cl/1/16', 'cl/1/17'); regv('hb13', 'hb/1/3'); regv('gn11', 'gn/1/1')
regegw('egw_atomo', '11099.1756', 'Este mundo é apenas pequenino átomo no vasto domínio sobre o qual Deus preside', 'Testemunhos para Ministros e Obreiros Evangélicos, p. 324')
regegw('egw_estrela', '11255.2247', 'Não há nenhuma estrela, que embeleze o céu, que por Ele não haja sido criada.', 'A Ciência do Bom Viver, p. 424')

P6_PALCO = '''<div class="p6-cena" id="p6">
  <canvas id="tela" aria-hidden="true"></canvas>
</div>'''

P6_CONTROLES = '''<label class="ctrl-rotulo" for="p6-olhos"><span>Levante os olhos</span><output id="p6-saida">um pouco</output></label>
<input type="range" id="p6-olhos" min="0" max="100" step="1" value="40">
<p class="leitura-chamada"><button type="button" class="btn sec" id="p6-chamar">✨ Chamar pelo nome</button></p>'''

P6_LEITURA = [(
    'Para ler e pensar',
    'Textos da Bíblia (versão Almeida Revista e Corrigida) e de Ellen G. White, copiados do texto original e conferidos ao vivo nos sites de origem. As partes destacadas são as que a cena usa.',
    grade([
        biblia(['sl/19/1']),
        biblia(['is/40/26'], marcas={'is/40/26': ['quem a todas chama pelo seu nome', 'nenhuma faltará']}),
        biblia(['sl/8/3', 'sl/8/4'], marcas={'sl/8/4': ['que é o homem mortal para que te lembres dele?']}),
        biblia(['gn/1/1']),
        biblia(['cl/1/16', 'cl/1/17'], marcas={'cl/1/17': ['todas as coisas subsistem por ele']}),
        biblia(['hb/1/3'], marcas={'hb/1/3': ['sustentando todas as coisas pela palavra do seu poder']}),
        egw('11255.2247', 'A Ciência do Bom Viver, p. 424', trecho='Não há nenhuma estrela, que embeleze o céu, que por Ele não haja sido criada.', marcas=['Não há nenhuma estrela']),
        egw('11099.1756', 'Testemunhos para Ministros e Obreiros Evangélicos, p. 324', trecho='Este mundo é apenas pequenino átomo no vasto domínio sobre o qual Deus preside', marcas=['pequenino átomo']),
        egw('1807.329', 'Caminho a Cristo (nova edição), p. 53', trecho='E Deus cuida de tudo e sustenta tudo o que criou.', marcas=['sustenta tudo o que criou']),
    ]) + '\n<h2>Uma reflexão, marcada como reflexão</h2>\n' + grade([
        reflexao('Deus continua agindo?',
                 '<p>A Bíblia e Ellen White afirmam que Deus <b>sustenta</b> o universo o tempo todo (Hb 1:3; Cl 1:17), que Ele <b>terminou</b> a obra da criação (Gn 2:2) e que fará <b>novos céus e nova terra</b> (Is 65:17; Ap 21:5).</p>'
                 '<p>Daí podemos <b>imaginar</b> que o universo em expansão fala de um Deus que não para de agir. Mas <b>nenhum dos dois textos diz</b> que o universo se expande porque Deus continua criando: isso é reflexão, não ensino.</p>'),
        biblia(['is/40/22'], antes='Aqui o profeta diz que Deus "estende" os céus. Ligar isso à expansão do universo é interpretação, não está escrito.'),
        biblia(['is/45/12']),
        biblia(['gn/2/2'], antes='A Bíblia diz que Deus concluiu a obra da criação.'),
        biblia(['is/65/17'], antes='E que haverá uma nova criação:'),
        biblia(['ap/21/5']),
        reflexao('Feitos à imagem do Criador',
                 '<p>Fomos feitos "à imagem de Deus" (Gn 1:26-27) e recebemos algo para <b>cultivar e guardar</b> (Gn 2:15). É razoável pensar que Deus não nos fez para ficarmos parados: aprender, cuidar, explorar e criar combina com a imagem do Criador.</p><p>Isso é <b>aplicação</b> do texto, não afirmação direta dele.</p>'),
    ]) + '\n' + curiosos('As distâncias das estrelas da cena',
             '<p>A luz que você vê hoje saiu de cada uma há muito tempo: ' + '; '.join('%s, há cerca de %s anos' % (n, ('{:.1f}'.format(a) if a < 10 else '{:.0f}'.format(a)).replace('.', ',')) for n, a in D.ESTRELAS) + '.</p><p>Distâncias conforme o catálogo Gaia/Hipparcos, via Wikipédia, conferidas em 6/11/2026; podem variar um pouco entre catálogos. Detalhes em <a href="fontes.html">Fontes</a>.</p>'),
)]

PARTES[6] = dict(titulo='Quem fez tudo isto?', tema='noite', script='p06.js', palco=P6_PALCO, controles=P6_CONTROLES, leitura=P6_LEITURA)

# ======================================================================================================================
# PARTE 7 — Onde fica o trono?  (subida até o limite do universo; presença; o anjo; luz e som)
# ======================================================================================================================
regv('sl11', 'sl/11/4'); regv('sl103', 'sl/103/19'); regv('is66', 'is/66/1'); regv('sl139', 'sl/139/7', 'sl/139/8', 'sl/139/9', 'sl/139/10')
regv('jr23', 'jr/23/23', 'jr/23/24'); regv('jo14', 'jo/14/16', 'jo/14/17'); regv('mt28', 'mt/28/2', 'mt/28/3'); regv('dn921', 'dn/9/21'); regv('ez114', 'ez/1/14'); regv('rs827', '1rs/8/27')
regegw('dtn552', '1813.3468', 'Vestido com a armadura de Deus, deixou este anjo as cortes celestiais. Os brilhantes raios da glória divina o precediam, iluminando-lhe o caminho.', 'O Desejado de Todas as Nações, p. 552')
regegw('dtn5524', '1813.3470', 'Aquele que vencera a morte, e a sepultura, saiu do túmulo com o passo do vencedor, por entre o cambalear da terra, o fuzilar dos relâmpagos e o ribombar dos trovões.', 'O Desejado de Todas as Nações, p. 552')

P7_PALCO = '''<div class="p7-cena" id="p7">
  <canvas id="tela" aria-hidden="true"></canvas>
  <canvas id="tela2" aria-hidden="true"></canvas>
  <div class="p5-hud" id="p7-hud" aria-hidden="true"><b id="hud-nome">A Terra</b><span id="hud-tam"></span><small id="hud-pc"></small></div>
  <ol class="p7-trilho" id="p7-trilho" aria-hidden="true"></ol>
  <div class="p1-etiqueta" id="p7-etq" aria-hidden="true" style="opacity:0"><span class="furo"></span><b class="sem">nenhum preço paga essa viagem</b></div>
  <p class="p7-nota" id="p7-nota" aria-hidden="true"></p>
</div>'''

P7_CONTROLES = '''<div class="ctl" id="ctl-subida">
  <p class="leitura-chamada"><button type="button" class="btn sec" id="p7-subir">▶ Subir</button><button type="button" class="btn sec" id="p7-voltar">↺ Voltar à Terra</button></p>
  <label class="ctrl-rotulo" for="p7-dist"><span>Distância da Terra</span><output id="p7-dist-saida">—</output></label>
  <input type="range" id="p7-dist" min="0" max="100" step="0.1" value="0">
</div>
<div class="ctl" id="ctl-raio">
  <label class="ctrl-rotulo" for="p7-km"><span>A que distância caiu o raio?</span><output id="p7-km-saida">2 km</output></label>
  <input type="range" id="p7-km" min="0.5" max="6" step="0.1" value="2">
  <p class="leitura-chamada"><button type="button" class="btn" id="p7-raio">⚡ Relâmpago!</button><button type="button" class="btn sec" id="p7-som" aria-pressed="false">🔇 Som desligado</button></p>
</div>'''

P7_LEITURA = [(
    'Para ler e pensar',
    'Textos da Bíblia (ARC) e de Ellen G. White copiados do original e conferidos ao vivo nos sites de origem. O que é imaginação vem sempre marcado como imaginação.',
    grade([
        biblia(['sl/11/4']), biblia(['sl/103/19']),
        biblia(['is/66/1'], antes='A Bíblia diz que o trono está "nos céus", mas não diz em que lugar do universo. Nem este estudo diz.'),
        biblia(['1rs/8/27'], marcas={'1rs/8/27': ['os céus e até o céu dos céus te não poderiam conter']}),
        biblia(['sl/139/7', 'sl/139/8', 'sl/139/9', 'sl/139/10'], marcas={'sl/139/7': ['Para onde me irei do teu Espírito']}),
        biblia(['jr/23/23', 'jr/23/24'], marcas={'jr/23/24': ['não encho eu os céus e a terra?']}),
        biblia(['jo/14/16', 'jo/14/17'], marcas={'jo/14/16': ['outro Consolador, para que fique convosco para sempre']}),
    ]) + '\n<h2>O anjo da ressurreição</h2>\n' + grade([
        biblia(['mt/28/2', 'mt/28/3'], marcas={'mt/28/2': ['um anjo do Senhor, descendo do céu'], 'mt/28/3': ['como um relâmpago']}),
        egw('1813.3468', 'O Desejado de Todas as Nações, p. 552', trecho='Vestido com a armadura de Deus, deixou este anjo as cortes celestiais. Os brilhantes raios da glória divina o precediam, iluminando-lhe o caminho.', marcas=['Os brilhantes raios da glória divina o precediam']),
        egw('1813.3470', 'O Desejado de Todas as Nações, p. 552', trecho='Aquele que vencera a morte, e a sepultura, saiu do túmulo com o passo do vencedor, por entre o cambalear da terra, o fuzilar dos relâmpagos e o ribombar dos trovões.', marcas=['o fuzilar dos relâmpagos e o ribombar dos trovões'], antes='Repare: neste texto, o estrondo de trovões acompanha a saída de Jesus do túmulo, não a descida do anjo.'),
        biblia(['dn/9/21'], marcas={'dn/9/21': ['veio voando rapidamente']}, antes='Outro anjo, Gabriel, "veio voando rapidamente".'),
        biblia(['ez/1/14'], antes='E, na visão de Ezequiel, os seres celestiais se moviam "à semelhança dos relâmpagos".'),
        imaginacao('A velocidade do anjo',
                   '<p><b>O que está escrito:</b> ele desceu do céu, tinha o aspecto de um relâmpago e houve um grande terremoto. <b>O que não está escrito:</b> a que velocidade ele veio.</p>'
                   '<p>Imagine que veio rápido, muito mais rápido que qualquer coisa que conhecemos: quando algo assim "pousa", a terra treme. Na física, nada com massa alcança a velocidade da luz; anjos são seres espirituais, então a comparação é só para ilustrar. <b>Isto é imaginação, não fato.</b></p>'),
        fato('Luz e som: por que o relâmpago vem antes',
             '<p>A luz anda <b>299.792 km por segundo</b>; o som no ar, uns <b>343 m por segundo</b>. A luz é cerca de <b>874 mil vezes</b> mais rápida. Por isso a gente vê o relâmpago e <b>só depois</b> ouve o trovão: a cada <b>3 segundos</b> de espera, o raio caiu a uns <b>1 km</b>.</p>',
             obs='Conta: 1.000 m ÷ 343 m/s ≈ 2,9 s por quilômetro (som a 20 °C).'),
    ]) + '\n' + curiosos('O maior preço, e a pergunta que ficou',
             '<p><b>Reflexão (não é afirmação da Bíblia):</b> se alguém pudesse ir até onde fica o trono, seria o maior preço que um ser humano poderia pagar, e nenhum dinheiro compra essa viagem. A pergunta que fica é a que vem depois: se tudo tem preço, e Deus está acima de qualquer um, <b>como é possível que Ele se aproxime de nós?</b></p>'),
)]

PARTES[7] = dict(titulo='Onde fica o trono?', tema='noite', script='p07.js', motor=True, palco=P7_PALCO, controles=P7_CONTROLES, leitura=P7_LEITURA)

# ======================================================================================================================
# PARTE 8 — A grandeza no pequeno  (zoom para dentro: mão, pele, células, núcleo, DNA, átomo, núcleo do átomo)
# ======================================================================================================================
regv('sl139_14', 'sl/139/14'); regv('sl139_16', 'sl/139/16'); regv('mt1030', 'mt/10/30')
regegw('ed114', '1948.581', 'A perfeição existe tanto nas menores como nas maiores obras de Deus. A mão que sustém os mundos no espaço, é a que modela as flores do campo.', 'Educação, p. 114')
regegw('cc53', '1807.329', 'Desde as estrelas que, em seus inexplicáveis trajetos através do espaço, percorrem, século após século, os caminhos a elas designados, até o minúsculo átomo, as coisas da natureza obedecem à vontade do Criador.', 'Caminho a Cristo (nova edição), p. 53')

P8_PALCO = '''<div class="p8-cena" id="p8">
  <canvas id="tela" aria-hidden="true"></canvas>
  <div class="p5-hud" aria-hidden="true"><b id="hud-nome"></b><span id="hud-tam"></span><small id="hud-pc"></small></div>
  <ol class="p5-escada p8-escada" id="p8-escada" aria-label="Degraus para dentro"></ol>
</div>'''

P8_CONTROLES = '''<div class="ctl" id="ctl-modelo">
  <p class="ctrl-dica">Como desenhar o átomo?</p>
  <ul class="chips" id="p8-modelo"><li><button type="button" class="chip ativo" data-m="nuvem">Modelo atual: nuvem</button></li><li><button type="button" class="chip" data-m="orbitas">Modelo antigo: sistema solar</button></li></ul>
</div>
<div class="ctl" id="ctl-zoom">
  <label class="ctrl-rotulo" for="p8-zoom"><span>Zoom</span><output id="p8-zoom-saida">20 cm</output></label>
  <input type="range" id="p8-zoom" min="0" max="100" step="0.1" value="0">
</div>'''

P8_LEITURA = [(
    'Para ler e pensar',
    'Tamanhos de fontes científicas (NASA, Wikipédia e livros-texto) e textos da Bíblia e de Ellen G. White copiados do original. As imagens são desenhos artísticos, não fotografias.',
    grade([
        biblia(['sl/139/13', 'sl/139/14', 'sl/139/15', 'sl/139/16'], marcas={'sl/139/14': ['maravilhosas são as tuas obras']}),
        biblia(['mt/10/29', 'mt/10/30', 'mt/10/31'], marcas={'mt/10/30': ['os cabelos da vossa cabeça estão todos contados']}),
        egw('1948.581', 'Educação, p. 114', trecho='A perfeição existe tanto nas menores como nas maiores obras de Deus. A mão que sustém os mundos no espaço, é a que modela as flores do campo.', marcas=['tanto nas menores como nas maiores obras de Deus']),
        egw('1807.329', 'Caminho a Cristo (nova edição), p. 53', trecho='Desde as estrelas que, em seus inexplicáveis trajetos através do espaço, percorrem, século após século, os caminhos a elas designados, até o minúsculo átomo, as coisas da natureza obedecem à vontade do Criador.', marcas=['até o minúsculo átomo']),
        fato('O DNA de uma célula tem uns 2 metros',
             '<p>O conjunto de DNA de uma célula humana (duas cópias) tem uns <b>6 bilhões de pares de bases</b>. Cada par ocupa cerca de <b>0,34 nm</b> da escada. Esticado, o fio teria <b>cerca de 2 metros</b>, dentro de um núcleo de uns 8 milésimos de milímetro. O corpo tem uns <b>30 trilhões</b> de células.</p>',
             obs='Conta: 6,2 bilhões × 0,34 nm ≈ 2,1 m. Um conjunto (haploide) do genoma humano tem cerca de 3,1 bilhões de pares de bases.', fontes=[('Human genome (Wikipédia)', 'https://en.wikipedia.org/wiki/Human_genome')]),
        fato('O átomo é quase todo espaço vazio',
             '<p>O núcleo de um átomo é de <b>dezenas de milhares de vezes menor</b> que o átomo (cerca de 27 mil a 60 mil, conforme o átomo). Se o átomo fosse um estádio de 100 m, o núcleo seria um <b>grão de areia</b> de uns 2 mm no meio do campo.</p>',
             obs='Conta: 100 m ÷ 50.000 = 2 mm.', fontes=[('Atomic nucleus (Wikipédia)', 'https://en.wikipedia.org/wiki/Atomic_nucleus')]),
        fato('Do maior ao menor: mais de 40 degraus',
             '<p>O universo observável tem cerca de <b>10<sup>27</sup> metros</b> de diâmetro; o núcleo de um átomo, cerca de <b>10<sup>−15</sup> metros</b>. Entre os dois cabem <b>mais de 40 potências de dez</b>: a criação é grande para os dois lados.</p>',
             obs='Conta: 8,8 × 10²⁶ m ÷ 5 × 10⁻¹⁵ m ≈ 1,8 × 10⁴¹.'),
        reflexao('O átomo é um "mini sistema solar"?',
                 '<p>Muita gente compara o átomo a um sistema solar, e a imagem é bonita. Mas é um <b>modelo antigo e superado</b>: os elétrons não giram como planetas, formam uma <b>nuvem</b> de probabilidade. A semelhança que existe de verdade é outra: <b>os dois são quase todo espaço vazio</b>.</p><p>Use como <b>analogia</b>, não como fato.</p>'),
        reflexao('Um universo no pequeno?',
                 '<p>Dá para pensar que existe "um universo" no grande e outro no minúsculo, e que a mesma sabedoria aparece nos dois. A Bíblia e Ellen White afirmam que a <b>perfeição está nas menores obras de Deus</b>; a ideia de "mini universo" é uma figura nossa, não um ensino.</p>'),
    ]),
)]

PARTES[8] = dict(titulo='A grandeza no pequeno', tema='noite', script='p08.js', motor=True, palco=P8_PALCO, controles=P8_CONTROLES, leitura=P8_LEITURA)

# ======================================================================================================================
# PARTE 9 — Os preços voltam  (etiquetas, o preço das pessoas no mundo, a balança que não se mexe, a pergunta)
# Mt 26:15 (trinta moedas de prata por Jesus) NÃO entra aqui: fica para a parte 10, para o clímax não vazar.
# ======================================================================================================================
regv('gn3728', 'gn/37/28'); regv('ex2132', 'ex/21/32'); regv('sl49', 'sl/49/7', 'sl/49/8')
TOTAL9 = sum([p['valor'] for p in D.PRECOS if p['id'] != 'fim']) + D.VIAGENS[2]['usd'] * D.PTAX + D.VIAGENS[4]['usd'] * D.PTAX

P9_PALCO = '''<div class="p9-cena" id="p9">
  <canvas id="tela" aria-hidden="true"></canvas>
</div>'''

P9_CONTROLES = '''<div class="ctl" id="ctl-balanca">
  <p class="ctrl-dica">Tente pagar: toque nos itens para pôr no prato.</p>
  <ul class="chips" id="p9-itens"></ul>
  <p class="leitura-chamada"><button type="button" class="btn sec" id="p9-tudo">Somar tudo</button><button type="button" class="btn sec" id="p9-limpar">Esvaziar</button></p>
</div>'''

P9_LEITURA = [(
    'Para ler e pensar',
    'Os versículos vêm da Bíblia (ARC), conferidos ao vivo. As contas usam os preços das partes 1 e 2 (com as fontes e datas em cada uma).',
    grade([
        biblia(['gn/37/28'], marcas={'gn/37/28': ['venderam José por vinte moedas de prata']}, antes='Um jovem vendido pelos próprios irmãos:'),
        biblia(['ex/21/32'], marcas={'ex/21/32': ['trinta siclos de prata']}, antes='A lei da época fixava o preço de um servo ou de uma serva assim:'),
        biblia(['sl/49/7', 'sl/49/8'], marcas={'sl/49/7': ['nenhum deles, de modo algum, pode remir a seu irmão ou dar a Deus o resgate dele'], 'sl/49/8': ['a redenção da sua alma é caríssima']}),
        fato('Tudo o que vimos, somado',
             '<p>Se pusermos no prato <b>um de cada</b>: o café, a refeição, a viagem em família, o carro, a casa, a viagem até a Estação Espacial e a meta de Marte, a conta chega a cerca de <b>R$ 358 milhões</b>.</p><p>Ainda assim, nenhum desses preços alcança o de quem está acima de todos.</p>',
             obs='Conta (preços das partes 1 e 2, sem o fim de semana): ≈ R$ %s.' % ('{:,.0f}'.format(TOTAL9).replace(',', '.'))),
        reflexao('A conta que o mundo faz',
                 '<p>No mundo, o valor de alguém quase sempre é medido pelo que a pessoa <b>tem</b> ou pelo que pode <b>oferecer em troca</b>, e nem sempre é dinheiro: pode ser simpatia, utilidade, influência. Quando a gente não tem nada para oferecer, bate a dúvida: <b>"que valor eu tenho?"</b></p>'
                 '<p>Pessoas já foram vendidas como mercadoria por preços irrisórios. <b>Isso nunca foi o valor delas</b>: foi o que o mundo, errado, chegou a cobrar.</p>'),
    ]),
)]

PARTES[9] = dict(titulo='Os preços voltam', tema='dia', script='p09.js', palco=P9_PALCO, controles=P9_CONTROLES, leitura=P9_LEITURA)

# ======================================================================================================================
# PARTE 10 — A resposta  (a etiqueta que vira; o preço; duas conclusões equilibradas; recebido, não comprado)
# O objetivo do estudo SÓ é dito aqui e na conclusão.
# ======================================================================================================================
def trecho_de(pid, ini, fim):
    t = CACHE['egw'][pid]['texto']
    a = t.index(ini)
    b = t.index(fim, a) + len(fim)
    return t[a:b]


T_ED132 = trecho_de('1948.670', 'A mão que sustém os mundos', 'foi pregada por nós.')
T_PJ96A = trecho_de('1931.919', 'Este mundo é apenas um átomo', 'se desviaram do redil.')
T_PJ96B = trecho_de('1931.919', 'Deus Se entregou a Si mesmo', 'ovelha que se perdera.')
T_CBV = trecho_de('11255.2247', 'Ele foi pregado na cruz', 'Deus - o homem.')
regv('jo316', 'jo/3/16'); regv('rm58', 'rm/5/8'); regv('pe118', '1pe/1/18', '1pe/1/19'); regv('co620', '1co/6/20'); regv('mt2615', 'mt/26/15'); regv('is43', 'is/43/4'); regv('jo31', '1jo/3/1')
regv('rm623', 'rm/6/23'); regv('sl1304', 'sl/130/4'); regv('tt214', 'tt/2/14'); regv('ef28', 'ef/2/8', 'ef/2/9'); regv('is551', 'is/55/1'); regv('gl220', 'gl/2/20'); regv('fp26', 'fp/2/6', 'fp/2/7', 'fp/2/8')
regegw('ed132', '1948.670', T_ED132, 'Educação, p. 132'); regegw('pj96', '1931.919', T_PJ96B, 'Parábolas de Jesus, p. 96')

P10_PALCO = '''<div class="p10-cena" id="p10">
  <canvas id="tela" aria-label="Uma etiqueta coberta no meio da vitrine de preços"></canvas>
</div>'''

P10_CONTROLES = '''<div class="ctl" id="ctl-virar">
  <p class="leitura-chamada"><button type="button" class="btn" id="p10-virar">Virar a etiqueta</button></p>
</div>
<div class="ctl" id="ctl-duas">
  <ul class="chips" id="p10-duas"><li><button type="button" class="chip ativo" data-k="valor">1 · Valor imenso</button></li><li><button type="button" class="chip" data-k="pecado">2 · Pecado grave</button></li></ul>
</div>'''

P10_LEITURA = [(
    'O preço',
    'Textos da Bíblia (ARC) e de Ellen G. White, copiados do original e conferidos ao vivo nos sites de origem; as partes destacadas são as que a cena usa.',
    grade([
        biblia(['jo/3/16'], marcas={'jo/3/16': ['deu o seu Filho unigênito']}),
        biblia(['rm/5/8'], marcas={'rm/5/8': ['Cristo morreu por nós']}),
        biblia(['rm/8/32'], marcas={'rm/8/32': ['o entregou por todos nós']}),
        biblia(['jo/1/1'], marcas={'jo/1/1': ['o Verbo era Deus']}, antes='Quem foi entregue?'),
        biblia(['fp/2/6', 'fp/2/7', 'fp/2/8'], marcas={'fp/2/6': ['sendo em forma de Deus'], 'fp/2/8': ['obediente até à morte e morte de cruz']}),
        egw('1948.670', 'Educação, p. 132', trecho=T_ED132, marcas=['é a que na cruz foi pregada por nós']),
        egw('1931.919', 'Parábolas de Jesus, p. 96', trecho=T_PJ96B, marcas=['Deus Se entregou a Si mesmo em Seu Filho']),
    ]) + '\n<h2>Nem prata nem ouro</h2>\n' + grade([
        biblia(['1pe/1/18', '1pe/1/19'], marcas={'1pe/1/18': ['como prata ou ouro'], '1pe/1/19': ['o precioso sangue de Cristo']}),
        biblia(['1co/6/20'], marcas={'1co/6/20': ['fostes comprados por bom preço']}),
        biblia(['1co/7/23'], marcas={'1co/7/23': ['Fostes comprados por bom preço']}),
        biblia(['mt/26/15'], marcas={'mt/26/15': ['trinta moedas de prata']}, antes='O mundo avaliou Jesus assim:'),
        biblia(['zc/11/12', 'zc/11/13'], marcas={'zc/11/13': ['esse belo preço em que fui avaliado por eles']}, antes='O profeta Zacarias já tinha falado desse preço:'),
    ]) + '\n<h2>Você tem valor imenso para Deus</h2>\n' + grade([
        biblia(['is/43/1', 'is/43/4'], marcas={'is/43/1': ['eu te remi', 'tu és meu'], 'is/43/4': ['foste precioso aos meus olhos']}),
        biblia(['1jo/3/1'], marcas={'1jo/3/1': ['quão grande amor nos tem concedido o Pai']}),
        biblia(['gl/2/20'], marcas={'gl/2/20': ['se entregou a si mesmo por mim']}),
        biblia(['mt/10/31'], marcas={'mt/10/31': ['mais valeis vós do que muitos passarinhos']}),
        egw('1931.919', 'Parábolas de Jesus, p. 96', trecho=T_PJ96A, marcas=['é mais precioso a Seus olhos']),
        egw('11255.2247', 'A Ciência do Bom Viver, p. 424', trecho=T_CBV, marcas=['Ele foi pregado na cruz']),
        reflexao('De onde vem esse valor?',
                 '<p>Não vem do que você fez, do que você tem, nem do que pode oferecer em troca: <b>vem de quem pagou por você</b>. Por isso ele não aumenta quando você vai bem e não diminui quando você erra.</p>'),
    ]) + '\n<h2>O pecado é grave</h2>\n' + grade([
        biblia(['rm/6/23'], marcas={'rm/6/23': ['o salário do pecado é a morte', 'o dom gratuito de Deus']}),
        biblia(['tt/2/14'], marcas={'tt/2/14': ['para nos remir de toda iniquidade']}),
        biblia(['sl/130/4'], marcas={'sl/130/4': ['para que sejas temido']}),
        biblia(['1pe/1/17'], marcas={'1pe/1/17': ['andai em temor']}),
        reflexao('O que quer dizer "temer"',
                 '<p>Aqui o temor <b>não é medo de ser rejeitado</b>: quem foi comprado por tão alto preço não precisa temer a rejeição. É <b>reverência</b> e cuidado de não pecar contra quem pagou esse preço. Se foi preciso entregar o Filho para nos libertar do pecado, o pecado é grave.</p>'),
    ]) + '\n<h2>Recebido, não comprado</h2>\n' + grade([
        biblia(['ef/2/8', 'ef/2/9'], marcas={'ef/2/8': ['é dom de Deus'], 'ef/2/9': ['Não vem das obras']}),
        biblia(['is/55/1'], marcas={'is/55/1': ['sem dinheiro e sem preço']}),
    ]),
)]

PARTES[10] = dict(titulo='A resposta', tema='aurora', script='p10.js', extras=['final.js'], palco=P10_PALCO, controles=P10_CONTROLES, leitura=P10_LEITURA)

# ======================================================================================================================
# (as demais partes são acrescentadas abaixo, uma a uma)
# ======================================================================================================================

# ======================================================================================================================
# CONCLUSÃO — página final (imagem final, as duas conclusões, versículos, perguntas, QR Code)
# ======================================================================================================================
CONCL_CORPO = '''<main class="concl">
  <section class="concl-hero" aria-label="A etiqueta final">
    <canvas id="tela" aria-label="A etiqueta final: Jesus, o preço pago por você, no meio de todos os preços do estudo"></canvas>
  </section>
  <section class="concl-texto">
    <p class="kicker">Conclusão</p>
    <h1>O que vale mais?</h1>
    <p class="lede">Passamos de uma xícara de café ao limite do universo, e do universo ao núcleo do átomo. Tudo o que vimos tem preço. Só Deus está acima de qualquer preço, e foi ele quem pagou, <b>por você</b>, o preço mais alto que existe.</p>
    <div class="concl-duas">
      <article class="cartao fato"><span class="tag">Primeira conclusão</span><h3>Você tem valor imenso</h3><p>O valor que Deus dá a você <b>não vem de nada que você fez ou tem</b>. Vem de quem pagou por você.</p></article>
      <article class="cartao reflexao"><span class="tag">Segunda conclusão</span><h3>O pecado é grave</h3><p>Só um preço tão alto pôde nos libertar dele. Temer é <b>reverência</b>: cuidado de não pecar contra quem pagou, não medo de ser rejeitado.</p></article>
    </div>
    <h2>Palavras para guardar</h2>
    ''' + grade([
        biblia(['jo/3/16'], marcas={'jo/3/16': ['deu o seu Filho unigênito']}),
        biblia(['1pe/1/18', '1pe/1/19'], marcas={'1pe/1/18': ['como prata ou ouro'], '1pe/1/19': ['o precioso sangue de Cristo']}),
        biblia(['rm/5/8'], marcas={'rm/5/8': ['Cristo morreu por nós']}),
        egw('1948.670', 'Educação, p. 132', trecho=T_ED132, marcas=['é a que na cruz foi pregada por nós']),
    ]) + '''
    <h2>Para pensar com calma</h2>
    <ul class="perguntas">
      <li>Onde eu tenho tentado <b>comprar</b> o valor que já me foi dado?</li>
      <li>O que muda em mim ao saber que fui comprado com o maior preço que existe?</li>
      <li>Como posso responder, com gratidão e cuidado, a quem pagou por mim?</li>
    </ul>
    <p class="acoes"><a class="btn" href="index.html">Rever o estudo</a><button type="button" class="btn sec" id="compartilhar">Compartilhar</button><a class="btn sec" href="qr.html">QR Code</a><a class="btn sec" href="fontes.html">Fontes</a></p>
    <p class="rodape-concl">O QR Code abre o início do estudo, para você passar a quem quiser.</p>
  </section>
</main>'''

CONCLUSAO = dict(tema='aurora', script='conclusao.js', extras=['final.js'], corpo=CONCL_CORPO)

FONTES_PAG = '''<main class="concl"><section class="concl-texto">
<p class="kicker">Fontes e conferência</p>
<h1>De onde vêm os números e os textos</h1>
<p class="lede">Tudo foi conferido em <b>6 de novembro de 2026</b>. Os preços mudam com o tempo; os textos da Bíblia e de Ellen G. White foram copiados ao vivo dos sites de origem, e o gerador do estudo se recusa a montar a página se um trecho destacado não existir no texto original.</p>
<h2>Preços (partes 1, 2 e 9)</h2>
<ul class="lista">
<li><b>Café:</b> Procon-SP, pesquisa de preços de produtos de padaria 2026 (22 e 23/09/2026).</li>
<li><b>Refeição em família:</b> Ticket (Edenred Brasil), Pesquisa +Valor, setembro de 2024 (a mais recente encontrada).</li>
<li><b>Fim de semana fora:</b> FOHB, divulgado pela Panrotas em 08/07/2026.</li>
<li><b>Viagem internacional em família (estimativa):</b> Catraca Livre, 13/02/2026; câmbio do Banco Central (PTAX, venda, 05/11/2026: R$ 5,4621).</li>
<li><b>Carro:</b> levantamento do UOL Carros, publicado pelo jornal A Tarde em 01/11/2026.</li>
<li><b>Casa:</b> Índice FipeZAP, informe de outubro de 2026.</li>
<li><b>Viagens espaciais:</b> Virgin Galactic (março e agosto de 2026); Blue Origin (assento leiloado em 2021 por US$ 28 milhões); Axiom Space (valores não oficiais, segundo reportagens); Elon Musk (2019 e 2022: é meta, não preço).</li>
</ul>
<h2>Ciência (partes 3 a 5 e 8)</h2>
<ul class="lista">
<li><b>Velocidade da luz:</b> 299.792.458 m/s, valor exato do Sistema Internacional de Unidades.</li>
<li><b>Dia-luz e Voyager 1:</b> <a href="https://science.nasa.gov/mission/voyager/voyager-1/voyager-1-what-is-a-light-day/" target="_blank" rel="noopener">NASA, "What Is a Light-Day?"</a> (18 de novembro de 2026; Lua 384.400 km; Sol 8 min 20 s; Marte de 3 a 22 minutos; Netuno 4 h 10 min).</li>
<li><b>Distâncias do Sistema Solar:</b> fichas técnicas da NASA para a Lua, o Sol e os planetas.</li>
<li><b>Superaglomerado Laniakea:</b> <a href="https://www.nature.com/articles/nature13674" target="_blank" rel="noopener">Tully et al., Nature (2014)</a>.</li>
<li><b>Número de galáxias:</b> <a href="https://science.nasa.gov/missions/hubble/hubble-reveals-observable-universe-contains-10-times-more-galaxies-than-previously-thought/" target="_blank" rel="noopener">NASA, censo de galáxias do Hubble</a>.</li>
<li><b>Universo observável (93 bilhões de anos-luz, 28,5 Gpc):</b> <a href="https://en.wikipedia.org/wiki/Observable_universe" target="_blank" rel="noopener">Wikipédia</a>.</li>
<li><b>Parsec:</b> <a href="https://en.wikipedia.org/wiki/Parsec" target="_blank" rel="noopener">Wikipédia</a> (definição da União Astronômica Internacional: 648.000/π unidades astronômicas).</li>
<li><b>Estrelas do céu da parte 6:</b> página de cada estrela na Wikipédia (catálogos Gaia e Hipparcos). <b>Cruzeiro do Sul:</b> <a href="https://en.wikipedia.org/wiki/Crux" target="_blank" rel="noopener">Wikipédia</a>.</li>
<li><b>DNA e átomo:</b> <a href="https://en.wikipedia.org/wiki/Human_genome" target="_blank" rel="noopener">genoma humano</a> (cerca de 3,1 bilhões de pares de bases); <a href="https://en.wikipedia.org/wiki/Atomic_nucleus" target="_blank" rel="noopener">núcleo atômico</a> (de 27 mil a 60 mil vezes menor que o átomo).</li>
</ul>
<h2>Bíblia e Ellen G. White</h2>
<ul class="lista">
<li><b>Bíblia:</b> Almeida Revista e Corrigida (ARC), no site <a href="https://www.bibliaonline.com.br/arc" target="_blank" rel="noopener">bibliaonline.com.br</a>.</li>
<li><b>Ellen G. White (português):</b> <a href="https://m.egwwritings.org/pt/book/1948" target="_blank" rel="noopener">Educação</a>, <a href="https://m.egwwritings.org/pt/book/1931" target="_blank" rel="noopener">Parábolas de Jesus</a>, <a href="https://m.egwwritings.org/pt/book/1813" target="_blank" rel="noopener">O Desejado de Todas as Nações</a>, <a href="https://m.egwwritings.org/pt/book/11099" target="_blank" rel="noopener">Testemunhos para Ministros</a>, <a href="https://m.egwwritings.org/pt/book/11255" target="_blank" rel="noopener">A Ciência do Bom Viver</a> e <a href="https://m.egwwritings.org/pt/book/1807" target="_blank" rel="noopener">Caminho a Cristo</a>, no site oficial da Ellen G. White Estate.</li>
</ul>
<h2>O que é reflexão ou imaginação (e vem sempre marcado)</h2>
<ul class="lista">
<li>"Deus continua agindo" e "feitos à imagem do Criador" (parte 6): aplicações, não afirmações diretas dos textos.</li>
<li>O ponto de luz e a velocidade do anjo (parte 7): imaginação; a velocidade não está escrita. Nada com massa alcança a velocidade da luz.</li>
<li>O átomo como "mini sistema solar" (parte 8): modelo antigo e superado, só como analogia.</li>
<li>O Salmo 139:16 diante do DNA (parte 8): aplicação, o Salmo não fala de DNA.</li>
</ul>
<p class="acoes"><a class="btn" href="index.html">Voltar ao início</a></p>
</section></main>'''

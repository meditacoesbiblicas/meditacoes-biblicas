# -*- coding: utf-8 -*-
# Conteúdo das páginas do estudo "O que vale mais?" (textos, cenas e cartões de leitura).
# Regra de ouro: até a parte 5 nada fala de Deus; a primeira menção é na parte 6; o objetivo só é dito na parte 10 e na conclusão.
import dados as D
import vinhetas as V
from cartoes import biblia, egw, fato, reflexao, imaginacao, curiosos, grade

PARTES = {}

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
# (as demais partes são acrescentadas abaixo, uma a uma)
# ======================================================================================================================

CONCLUSAO = None
FONTES_PAG = None

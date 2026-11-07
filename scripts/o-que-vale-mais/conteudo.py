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
# (as demais partes são acrescentadas abaixo, uma a uma)
# ======================================================================================================================

CONCLUSAO = None
FONTES_PAG = None

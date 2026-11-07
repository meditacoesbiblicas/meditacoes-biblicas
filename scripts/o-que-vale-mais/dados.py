# -*- coding: utf-8 -*-
# Constantes, contas e dados do estudo "O que vale mais?": fonte única para os textos (Python) e para as animações (dados.js).
# Cada número tem a sua fonte registrada em FONTES (mostrada na página "Fontes e conferência"). Conferidos em 2026-11-06.
import json
import math

# ---------------------------------------------------------------- constantes físicas
C_KM_S = 299792.458                      # velocidade da luz no vácuo (valor exato do SI)
ANO_S = 365.25 * 86400                   # ano juliano (o ano usado para o ano-luz)
ANO_LUZ_KM = C_KM_S * ANO_S              # 9,4607 trilhões de km
UA_KM = 149597870.7                      # unidade astronômica (valor exato, UAI 2012)
PARSEC_KM = 648000 / math.pi * UA_KM     # 3,0857e13 km
PARSEC_AL = PARSEC_KM / ANO_LUZ_KM       # 3,2616 anos-luz
TERRA_CIRC_KM = 40075.017                # circunferência no equador (NASA/WGS-84)
LUA_KM = 384400                          # distância média Terra-Lua
SOM_M_S = 343                            # som no ar a 20 °C
VOYAGER_KM_S = 17.0                      # NASA/JPL: cerca de 17 km/s (61 mil km/h)
DIA_LUZ_KM = C_KM_S * 86400              # 25,9 bilhões de km (Voyager 1 chega aqui em nov/2026)
PTAX = 5.4621                            # dólar PTAX (Banco Central), venda, 05/11/2026

# ---------------------------------------------------------------- distâncias (em km, quando a luz leva tempo conhecido)
# (id, nome, distância típica em km, mínima, máxima, observação)
CORPOS = [
    ('lua', 'Lua', LUA_KM, 363300, 405500, 'distância média; de 363.300 a 405.500 km'),
    ('sol', 'Sol', UA_KM, 147.1e6, 152.1e6, '1 unidade astronômica (média)'),
    ('venus', 'Vênus', 41e6, 38.2e6, 261.0e6, 'de 38 a 261 milhões de km, conforme a posição'),
    ('marte', 'Marte', 225e6, 54.6e6, 401.4e6, 'de 55 a 401 milhões de km; média de 225 milhões'),
    ('jupiter', 'Júpiter', 778e6, 588.5e6, 968.0e6, 'de 588 a 968 milhões de km'),
    ('netuno', 'Netuno', 4.5e9, 4.306e9, 4.687e9, 'de 4,3 a 4,7 bilhões de km'),
    ('voyager', 'Voyager 1', DIA_LUZ_KM, None, None, '1 dia-luz em novembro de 2026'),
    ('proxima', 'Próxima do Centauro', 4.2465 * ANO_LUZ_KM, None, None, 'a estrela mais próxima do Sol'),
]

# ---------------------------------------------------------------- estrelas para o céu da parte 6 (nome, distância em anos-luz; conferidas na Wikipédia/Gaia em 2026-11-06)
ESTRELAS = [
    ('Alfa do Centauro', 4.34), ('Sírio', 8.61), ('Prócion', 11.46), ('Altair', 16.73), ('Vega', 25.04), ('Fomalhaut', 25.13),
    ('Pólux', 33.78), ('Arcturo', 36.7), ('Capela', 42.92), ('Aldebarã', 67), ('Régulo', 79.3), ('Espiga', 250),
]

# ---------------------------------------------------------------- velocidades (id, nome, km/s)
VELOCIDADES = [
    ('pe', 'Uma pessoa andando', 5 / 3600),
    ('carro', 'Um carro a 100 km/h', 100 / 3600),
    ('aviao', 'Um avião a jato', 900 / 3600),
    ('voyager', 'A sonda Voyager 1', VOYAGER_KM_S),
    ('luz', 'A luz', C_KM_S),
]

# ---------------------------------------------------------------- escada do universo (diâmetros em anos-luz)
NIVEIS = [
    ('terra', 'A Terra', 12742 / ANO_LUZ_KM, 'cerca de 12.742 km de diâmetro'),
    ('lua', 'A Terra e a Lua', 2 * LUA_KM / ANO_LUZ_KM, 'a Lua gira a cerca de 384 mil km da Terra: a órbita tem uns 769 mil km de lado a lado'),
    ('sistema', 'O Sistema Solar', 2 * 4.5e9 / ANO_LUZ_KM, 'até a órbita de Netuno: cerca de 9 bilhões de km de lado a lado'),
    ('vizinhanca', 'A vizinhança do Sol', 20, 'estrelas num raio de 10 anos-luz (a mais próxima está a 4,2)'),
    ('galaxia', 'A Via Láctea', 100000, 'cerca de 100 mil anos-luz de diâmetro, com centenas de bilhões de estrelas'),
    ('grupo', 'O Grupo Local', 10e6, 'cerca de 10 milhões de anos-luz, com a Via Láctea, Andrômeda e dezenas de galáxias'),
    ('super', 'O superaglomerado Laniakea', 520e6, 'cerca de 520 milhões de anos-luz, com cerca de 100 mil galáxias'),
    ('universo', 'O universo observável', 93e9, 'cerca de 93 bilhões de anos-luz de diâmetro'),
]

# ---------------------------------------------------------------- preços (parte 1) — conferidos em 2026-11-06
PRECOS = [
    dict(id='cafe', nome='Um chocolate quente', valor=8.0, texto='8', aprox=True, nota='Uma xícara de chocolate quente, em padaria (valor de referência).',
         conta='Valor de referência: R$ 8, o meio do caminho entre o chocolate quente pequeno (R$ 7,20) e o grande (R$ 8,90) do cardápio de uma padaria. '
               'Não encontramos uma pesquisa oficial de preço para esse item, então é uma estimativa; o preço real varia de lugar para lugar. Fonte: cardápio da Padaria Brasil (Cardápio Seguro).',
         imagine='Imagine o cheiro do chocolate quente e uns minutos só seus, numa manhã fria.', dura='minutos', para='você'),
    dict(id='refeicao', nome='Uma refeição em família', valor=385.76, texto='386', aprox=True, nota='4 refeições completas, a R$ 96,44 cada (em 2024).',
         conta='4 pessoas × R$ 96,44 = R$ 385,76. R$ 96,44 é o preço médio da refeição completa (prato, bebida, sobremesa e café) em restaurante à la carte, '
               'numa pesquisa com mais de 4.500 restaurantes divulgada em setembro de 2024, a mais recente que encontramos. Fonte: Ticket (Edenred Brasil), Pesquisa +Valor.',
         imagine='Imagine a mesa cheia, todo mundo falando ao mesmo tempo e alguém rindo alto.', dura='horas', para='a família'),
    dict(id='fim', nome='Um fim de semana fora', valor=903.42, texto='903', aprox=True, nota='2 diárias de hotel, só a hospedagem.',
         conta='2 diárias × R$ 451,71 = R$ 903,42. R$ 451,71 foi a diária média dos hotéis acompanhados pelo FOHB em maio de 2026 (amostra de 570 hotéis). '
               'Não inclui viagem, comida nem passeios. Fonte: FOHB (Fórum de Operadores Hoteleiros do Brasil), divulgado pela Panrotas em 08/07/2026.',
         imagine='Imagine acordar sem despertador, longe da rotina, com o dia todo pela frente.', dura='2 dias', para='quem for junto'),
    dict(id='viagem', nome='Uma viagem internacional em família', valor=41714.4, texto='41.700', aprox=True, nota='Estimativa: 4 pessoas, 8 dias na Disney.',
         conta='US$ 7.640 × R$ 5,46 (dólar do Banco Central em 05/11/2026) ≈ R$ 41.700. É uma estimativa para uma família de 4 pessoas em 8 dias, no cenário '
               'intermediário (passagens, hospedagem, ingressos dos parques, alimentação, transporte local, seguro e documentação), sem compras. '
               'Pode ir de cerca de R$ 32 mil a R$ 54 mil. Fonte: Catraca Livre, 13/02/2026; câmbio: Banco Central.',
         imagine='Imagine a família inteira diante de um lugar que só conhecia de foto.', dura='8 dias, anos de memória', para='a família'),
    dict(id='carro', nome='Um carro', valor=72490, texto='72.490', aprox=False, nota='O carro novo mais barato do país (nov/2026).',
         conta='Fiat Mobi Like zero-quilômetro, preço de oferta em novembro de 2026, o mais barato entre os carros novos vendidos no Brasil. '
               'Os preços de tabela mudam com as promoções. Fonte: levantamento do UOL Carros, publicado pelo jornal A Tarde em 01/11/2026.',
         imagine='Imagine ir aonde quiser, na hora que quiser, com quem você ama.', dura='muitos anos', para='a família'),
    dict(id='casa', nome='Uma casa', valor=542520, texto='542.500', aprox=True, nota='Imóvel de 60 m², com 2 dormitórios.',
         conta='60 m² × R$ 9.042 por m² = R$ 542.520. R$ 9.042 é o preço médio anunciado dos imóveis de 2 dormitórios nas 56 cidades acompanhadas, '
               'em outubro de 2026 (preço pedido, não o de venda). Os 60 m² são um exemplo. Fonte: Índice FipeZAP, informe de outubro de 2026.',
         imagine='Imagine abrir a porta e saber que aquele lugar é seu, e da sua família.', dura='décadas', para='a família'),
]
CAFES = ['≈ 48 xícaras', '≈ 110 xícaras', '≈ 5 mil xícaras', '≈ 9 mil xícaras', '≈ 68 mil xícaras']

# ---------------------------------------------------------------- viagens espaciais (parte 2): US$ e R$ ao câmbio PTAX
def reais(usd):
    return usd * PTAX


VIAGENS = [
    dict(id='plataforma', nome='Na plataforma', chip='🚀 Plataforma', alt_km=0, rotulo='A viagem começa aqui'),
    dict(id='karman', nome='Beira do espaço', chip='🌍 Beira do espaço', alt_km=100, imagine='Imagine ver a curvatura da Terra e flutuar por alguns minutos.', rotulo='Linha de Kármán: 100 km',
         usd=750e3, preco='US$ 750 mil por assento', tempo='alguns minutos sem peso',
         nota='Virgin Galactic anunciou US$ 750 mil por assento em março de 2026 e, em agosto, retirou esse preço, com novos valores maiores a caminho e o primeiro voo comercial adiado para fevereiro de 2027. '
              'Na Blue Origin, o único preço conhecido é o de um assento leiloado em junho de 2021: US$ 28 milhões.'),
    dict(id='estacao', nome='Estação Espacial', chip='🛰️ Estação', alt_km=400, imagine='Imagine dar uma volta na Terra a cada hora e meia e ver o sol nascer 16 vezes por dia.', rotulo='Órbita da Estação Espacial: 400 km',
         usd=65e6, preco='cerca de US$ 55 a 70 milhões', tempo='cerca de 1 dia até chegar; 10 a 14 dias lá',
         nota='A Axiom Space não divulga o preço oficialmente; as reportagens falam em cerca de US$ 55 milhões nas primeiras missões e US$ 59 a 70 milhões na Ax-4 (2025).'),
    dict(id='lua', nome='Lua', chip='🌕 Lua', alt_km=LUA_KM, imagine='Imagine ver a Terra do tamanho de uma bolinha azul no céu preto.', rotulo='Lua: 384.400 km', usd=None, preco='nenhum bilhete à venda', tempo='cerca de 3 dias (como na missão Artemis II, segundo a NASA)',
         nota='Não existe passagem comercial para a Lua. Os astronautas da missão Artemis II levaram cerca de 3 dias para chegar lá (NASA).'),
    dict(id='marte', nome='Marte', chip='🔴 Marte', alt_km=225e6, imagine='Imagine pisar numa terra vermelha e ver a Terra como uma estrela azul.', rotulo='Marte: 225 milhões de km (em média)', usd=500e3, preco='meta: menos de US$ 500 mil', tempo='cerca de 7 meses (como a sonda Perseverance)',
         nota='Elon Musk disse em 2019 que um bilhete para Marte custaria um dia menos de US$ 500 mil e, em 2022, falou em US$ 100 mil como exemplo. É meta declarada, não preço: ainda não existe viagem tripulada a Marte.'),
]


def json_dados():
    d = dict(
        c=C_KM_S, anoS=ANO_S, anoLuzKm=ANO_LUZ_KM, uaKm=UA_KM, parsecKm=PARSEC_KM, parsecAl=PARSEC_AL, terraCirc=TERRA_CIRC_KM, luaKm=LUA_KM,
        somMs=SOM_M_S, voyagerKms=VOYAGER_KM_S, diaLuzKm=DIA_LUZ_KM, ptax=PTAX,
        corpos=[dict(id=i, nome=n, km=k, min=mn, max=mx, obs=o) for i, n, k, mn, mx, o in CORPOS],
        velocidades=[dict(id=i, nome=n, kms=v) for i, n, v in VELOCIDADES],
        estrelas=[dict(nome=n, al=a) for n, a in ESTRELAS],
        niveis=[dict(id=i, nome=n, al=a, obs=o) for i, n, a, o in NIVEIS],
        precos=[dict(id=p['id'], nome=p['nome'], valor=p['valor'], texto=p['texto'], aprox=p['aprox'], nota=p['nota'], conta=p['conta'],
                     imagine=p['imagine'], dura=p['dura'], para=p['para'], cafes=(CAFES[i - 1] if i > 0 else None)) for i, p in enumerate(PRECOS)],
        viagens=[dict(v, reais=(reais(v['usd']) if v.get('usd') else None)) for v in VIAGENS],
    )
    return json.dumps(d, ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
    print('ano-luz = %.4e km | parsec = %.4e km = %.4f al | dia-luz = %.4e km' % (ANO_LUZ_KM, PARSEC_KM, PARSEC_AL, DIA_LUZ_KM))
    print('voltas por segundo (luz):', C_KM_S / TERRA_CIRC_KM)
    print('Voyager até Próxima (anos):', 4.2465 * ANO_LUZ_KM / VOYAGER_KM_S / ANO_S)
    print('Voyager até Andrômeda (anos):', 2.5e6 * ANO_LUZ_KM / VOYAGER_KM_S / ANO_S)
    print('Lua (s):', LUA_KM / C_KM_S, '| Sol (s):', UA_KM / C_KM_S, '| Netuno (h):', 4.5e9 / C_KM_S / 3600)
    print('som: s por km =', 1000 / SOM_M_S)

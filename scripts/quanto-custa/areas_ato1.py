# -*- coding: utf-8 -*-
# Medidas (em pixels da imagem vitrine.jpg, 2000x1342) das áreas clicáveis do Ato 1.
# Foram lidas sobre a ilustração do Gemini: as 7 etiquetas brancas por detecção de cor (todas 81x117),
# as arestas dos degraus por gradiente, e as caixas dos objetos conferidas com uma grade de coordenadas.
# Se a ilustração for trocada, é aqui que se recalibra (e o verificador `conferir_areas.py` mostra o resultado).
W, H = 2000, 1342

# col = (x0, x1) do degrau; box = (x0, y0, x1, y1) do objeto em cima dele; tag = (x, y, largura, altura) do retângulo branco da etiqueta.
AREAS = [
    dict(col=(61, 330),    box=(138, 820, 288, 1052),  tag=(149, 1182, 81, 117)),
    dict(col=(330, 600),   box=(360, 798, 590, 965),   tag=(420, 1085, 81, 117)),
    dict(col=(600, 872),   box=(626, 672, 856, 863),   tag=(696, 979, 81, 116)),
    dict(col=(872, 1145),  box=(902, 566, 1104, 753),  tag=(973, 867, 81, 117)),
    dict(col=(1145, 1415), box=(1139, 467, 1390, 643), tag=(1245, 765, 81, 116)),
    dict(col=(1415, 1685), box=(1386, 381, 1632, 522), tag=(1517, 641, 81, 116)),
    dict(col=(1685, 1937), box=(1597, 157, 1953, 404), tag=(1785, 522, 81, 118)),
]
CHAO = 1293          # linha onde os degraus encostam no chão


def pad(box, p):
    x0, y0, x1, y1 = box
    return (x0 - p, y0 - p, x1 + p, y1 + p)


def etiqueta_papel(tag):
    """Retângulo da etiqueta de papel inteira (com argola e margens), a partir do retângulo branco."""
    x, y, w, h = tag
    return (x - 16, y - 46, x + w + 16, y + h + 16)


def areas_de_toque(i):
    """Retângulos que respondem ao clique/toque no item i: o degrau inteiro (do alto do objeto até o chão) e a caixa do objeto
    (que pode passar um pouco da largura do degrau, como o chapéu e a base da casa)."""
    a = AREAS[i]
    cx0, cx1 = a['col']
    x0, y0, x1, y1 = a['box']
    degrau = (cx0, y0, cx1, CHAO)
    objeto = (x0, y0, x1, y1)
    if i == len(AREAS) - 1:   # a base da casa passa por cima do degrau 6: só a parte de cima, para não roubar o toque do carro
        objeto = (x0, y0, x1, 381)
        degrau = (cx0, 381, cx1, CHAO)
        return [objeto, (x0 + 43, 381, x1, y1), degrau]
    return [degrau, objeto]

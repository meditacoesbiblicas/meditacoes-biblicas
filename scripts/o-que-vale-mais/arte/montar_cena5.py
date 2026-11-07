# -*- coding: utf-8 -*-
"""Cena 5 (carro): prepara as camadas.
 - fundo sem a cerca (a cerca passa a ser desenhada em código, para se mover como o resto do cenário);
 - tira cada árvore/poste/arbusto da faixa magenta e monta duas faixas de paralaxe (árvores de longe; postes de perto);
 - recorta os dois discos das rodas do carro (para girarem por cima do carro)."""
import numpy as np
from PIL import Image, ImageFilter
from collections import deque
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, '../../../public/o-que-vale-mais-desenvolvimento/img/')

# 1) fundo sem cerca: copia a faixa de pasto logo acima sobre a faixa da cerca, com bordas suaves
f = Image.open(f'{BASE}/cena5/01-fundo.png').convert('RGB')
a = np.array(f).astype(np.float32)
y0, y1 = 592, 690            # faixa da cerca (px originais, 1536x1024)
src = a[y0 - 92:y1 - 92].copy()
h = y1 - y0
w = np.ones(h, np.float32); w[:10] = np.linspace(0, 1, 10); w[-10:] = np.linspace(1, 0, 10)
a[y0:y1] = a[y0:y1] * (1 - w[:, None, None]) + src * w[:, None, None]
f2 = Image.fromarray(a.astype(np.uint8)); f2 = f2.resize((1280, round(1280 * f2.height / f2.width)), Image.LANCZOS)
f2.save(OUT + 'cena5-fundo.jpg', quality=84, optimize=True)

# 2) elementos da faixa magenta
t = np.array(Image.open(f'{BASE}/cena5/03-arvores.png').convert('RGB')).astype(np.float32)
r, g, b = t[..., 0], t[..., 1], t[..., 2]
gn = np.minimum(r, b) - g
puro = np.clip((gn - 170) / 50, 0, 1); soft = np.clip((gn - 40) / 90, 0, 1)
bgm = Image.fromarray(((puro > .5) * 255).astype(np.uint8))
near = np.array(bgm.filter(ImageFilter.MaxFilter(9))).astype(np.float32) / 255
alpha = 1 - np.maximum(puro, soft * near)
band = np.array(bgm.filter(ImageFilter.MaxFilter(15))).astype(np.float32) / 255 > .5
t[..., 0] = np.where(band, np.minimum(r, g + 8), r); t[..., 2] = np.where(band, np.minimum(b, g + 8), b)
rgba = Image.fromarray(np.clip(t, 0, 255).astype(np.uint8)).convert('RGBA'); rgba.putalpha(Image.fromarray((alpha * 255).astype(np.uint8)))
al = (alpha > .3)
# componentes conexos (em 1/4 de resolução)
sm = np.array(Image.fromarray((al * 255).astype(np.uint8)).resize((384, 256), Image.BILINEAR)) > 40
sm = np.array(Image.fromarray((sm * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0
lab = np.zeros(sm.shape, int); n = 0
for sy in range(sm.shape[0]):
    for sx in range(sm.shape[1]):
        if sm[sy, sx] and not lab[sy, sx]:
            n += 1; q = deque([(sy, sx)]); lab[sy, sx] = n
            while q:
                y, x = q.popleft()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < sm.shape[0] and 0 <= xx < sm.shape[1] and sm[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n; q.append((yy, xx))
els = []
for k in range(1, n + 1):
    ys, xs = np.where(lab == k)
    if len(ys) < 40: continue
    x0, x1, yb0, yb1 = xs.min() * 4 - 4, xs.max() * 4 + 8, ys.min() * 4 - 4, ys.max() * 4 + 8
    crop = rgba.crop((max(x0, 0), max(yb0, 0), x1, yb1))
    # zera pixels de outros componentes na caixa (vizinhos que encostam na caixa)
    els.append((x0, crop))
els.sort(key=lambda e: e[0])
print('componentes:', [(e[0], e[1].size) for e in els])
Image.new('RGB', (1, 1)).save('/dev/null', 'PNG')

def kind(img):
    w_, h_ = img.size
    return 'poste' if (h_ > 2.2 * w_ and w_ < 130 + 0) or w_ < 110 and h_ > 280 else ('arbusto' if h_ < 140 else 'arvore')
import json
info = []
for i, (x, im) in enumerate(els):
    k = kind(im); info.append((i, k, im.size)); im.save(f'{BASE}/cena5/el{i:02d}-{k}.png')
print(info)

# 3) faixas de paralaxe (2x a resolução em unidades do viewBox 480x320)
def el(i): return Image.open(f'{BASE}/cena5/el{i:02d}-{info[i][1]}.png')
def faixa(largura_vb, altura_vb, itens, s):
    S = 2
    img = Image.new('RGBA', (largura_vb * S, altura_vb * S), (0, 0, 0, 0))
    for i, x, dy in itens:
        e = el(i); k = s * S
        e = e.resize((max(1, round(e.width * k)), max(1, round(e.height * k))), Image.LANCZOS)
        img.alpha_composite(e, (round(x * S), img.height - e.height + round(dy * S)))
    return img
arv = faixa(560, 140, [(0, 8, 2), (1, 95, 3), (3, 112, 1), (4, 205, 2), (5, 296, 3), (6, 350, 1), (8, 435, 2), (9, 540, 3)], .30)
arv.save(OUT + 'cena5-arvores-longe.webp', 'WEBP', quality=88, method=6)
pos = faixa(480, 135, [(2, 90, 0), (9, 200, 0), (7, 330, 0), (1, 430, 0)], .36)
pos.save(OUT + 'cena5-postes-perto.webp', 'WEBP', quality=88, method=6)
print('faixas', arv.size, pos.size)

# 4) discos das rodas (giram por cima do carro)
car = np.array(Image.open(f'{BASE}/cena5/02-carro.png').convert('RGB')).astype(np.float32)
R = 90
yy, xx = np.mgrid[0:car.shape[0], 0:car.shape[1]]
for nome, cx, cy in (('tras', 267, 748), ('frente', 1259, 748)):
    d = np.hypot(xx - cx, yy - cy)
    tile = car[cy - R - 2:cy + R + 2, cx - R - 2:cx + R + 2].copy()
    gr = (tile[..., 1] - np.maximum(tile[..., 0], tile[..., 2])) > 60     # verde do fundo visto entre os raios
    tile[gr] = (38, 34, 31)
    m = np.clip((R + .5 - d[cy - R - 2:cy + R + 2, cx - R - 2:cx + R + 2]) / 1.5, 0, 1)
    o = Image.fromarray(tile.astype(np.uint8)).convert('RGBA'); o.putalpha(Image.fromarray((m * 255).astype(np.uint8)))
    o.save(OUT + f'cena5-roda-{nome}.webp', 'WEBP', quality=90, method=6); print('roda', nome, o.size)

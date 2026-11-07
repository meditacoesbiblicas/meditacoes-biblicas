# -*- coding: utf-8 -*-
"""Recorte por chroma key puro (sem a máscara do Vision), para objetos com partes claras/finas
(chaves na mão, calçada de pedra, janelas do carro). Preserva folhagem verde por dentro: só some o que for fundo puro
e uma franja de poucos pixels em volta dele.
uso: python3 recortar_chave.py origem.png saida.webp largura_final [--magenta] [--prev prev.jpg]"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, out, wfinal = sys.argv[1], sys.argv[2], int(sys.argv[3])
mag = '--magenta' in sys.argv
a = np.array(Image.open(src).convert('RGB')).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
gn = (np.minimum(r, b) - g) if mag else (g - np.maximum(r, b))
tol = float(sys.argv[sys.argv.index('--tol') + 1]) if '--tol' in sys.argv else 170
puro = np.clip((gn - tol) / 50, 0, 1)
soft = np.clip((gn - 40) / 90, 0, 1)
bgmask = Image.fromarray(((puro > .5) * 255).astype(np.uint8))
near = np.array(bgmask.filter(ImageFilter.MaxFilter(9))).astype(np.float32) / 255
alpha = 1 - np.maximum(puro, soft * near)
if '--verde-global' in sys.argv:   # objetos sem nada verde (ex.: pessoas): some qualquer resto esverdeado
    alpha = alpha * (1 - np.clip((gn - 12) / 30, 0, 1))
# descontamina a franja
band = np.array(bgmask.filter(ImageFilter.MaxFilter(15))).astype(np.float32) / 255 > .5
if mag:
    a[..., 0] = np.where(band, np.minimum(r, g + 8), r); a[..., 2] = np.where(band, np.minimum(b, g + 8), b)
else:
    a[..., 1] = np.where(band, np.minimum(g, np.maximum(r, b) + 5), g)
al = Image.fromarray((np.clip(alpha, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7))
rgba = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); rgba.putalpha(al)
bb = rgba.getbbox(); rgba = rgba.crop(bb)
rgba = rgba.resize((wfinal, round(rgba.height * wfinal / rgba.width)), Image.LANCZOS)
rgba.save(out, 'WEBP', quality=88, method=6)
print(out, 'bbox', bb, 'final', rgba.size)
if '--prev' in sys.argv:
    p = sys.argv[sys.argv.index('--prev') + 1]
    bg = Image.new('RGBA', rgba.size, (60, 70, 110, 255)); bg.alpha_composite(rgba); bg.convert('RGB').save(p, quality=88)

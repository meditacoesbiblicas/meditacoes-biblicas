# -*- coding: utf-8 -*-
"""Recorta um objeto sobre fundo verde chroma (#00FF00) do Gemini.
uso: python3 recortar.py origem.jpg mascara_vision.png saida.webp largura_final [--prev prev.jpg]
Alfa = verde-chave suave nas bordas + miolo da máscara do Vision (preserva saladas/arbustos verdes por dentro)."""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, vis_p, out, wfinal = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
im = Image.open(src).convert('RGB')
a = np.array(im).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
vis = np.array(Image.open(vis_p).convert('L')).astype(np.float32) / 255
visb = Image.fromarray((vis > .5).astype(np.uint8) * 255)
core = np.array(visb.filter(ImageFilter.MinFilter(13))).astype(np.float32) / 255   # miolo (~6px para dentro)
grn = g - np.maximum(r, b)
key = 1 - np.clip((grn - 28) / 70, 0, 1)                # 0 = fundo verde puro
outer = np.array(visb.filter(ImageFilter.MaxFilter(9))).astype(np.float32) / 255      # só aceita perto do objeto
alpha = np.maximum(key * outer, core)
# buracos de fundo verde puro dentro do objeto (entre pernas, cadeiras, colunas)
puro = np.clip(((g - 175) / 40), 0, 1) * np.clip(((95 - r) / 30), 0, 1) * np.clip(((95 - b) / 30), 0, 1)
alpha = alpha * (1 - puro)
# descontamina verde nas bordas (fora do miolo)
band = (core < .5)
lim = np.maximum(r, b) + 6
g2 = np.where(band & (g > lim), lim, g)
a[..., 1] = g2
al = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.9))
rgba = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); rgba.putalpha(al)
bb = rgba.getbbox(); rgba = rgba.crop(bb)
h = round(rgba.height * wfinal / rgba.width)
rgba = rgba.resize((wfinal, h), Image.LANCZOS)
rgba.save(out, 'WEBP', quality=88, method=6)
print(out, 'bbox_original', bb, 'final', rgba.size)
if '--prev' in sys.argv:
    p = sys.argv[sys.argv.index('--prev') + 1]
    bg = Image.new('RGBA', rgba.size, (60, 70, 110, 255)); bg.alpha_composite(rgba); bg.convert('RGB').save(p, quality=88)

# -*- coding: utf-8 -*-
# Desenha as áreas de areas_ato1.py por cima da ilustração, para conferir a calibração a olho.
# Uso: python3 scripts/quanto-custa/conferir_areas.py <imagem.jpg> <saida.jpg>
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import areas_ato1 as A  # noqa: E402

im = Image.open(sys.argv[1]).convert('RGB')
d = ImageDraw.Draw(im, 'RGBA')
cores = [(255, 0, 0), (0, 160, 0), (0, 90, 255), (200, 0, 200), (230, 130, 0), (0, 170, 170), (120, 60, 0)]
for i in range(len(A.AREAS)):
    c = cores[i]
    for r in A.areas_de_toque(i):
        d.rectangle(r, fill=c + (38,), outline=c + (255,), width=3)
    d.rounded_rectangle(A.pad(A.AREAS[i]['box'], 10), radius=22, outline=(255, 255, 255, 255), width=5)
    d.rounded_rectangle(A.etiqueta_papel(A.AREAS[i]['tag']), radius=16, outline=(255, 255, 0, 255), width=5)
im.save(sys.argv[2], quality=88)
print('ok')

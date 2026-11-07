from PIL import Image, ImageDraw, ImageFilter
import numpy as np
SRC='/Users/prlt/Documents/code/meditacoes-biblicas/scripts/o-que-vale-mais/arte/cena1/02-caneca.jpg'
im=Image.open(SRC).convert('RGB'); W,H=im.size
a=np.array(im).astype(np.float32)
vis=np.array(Image.open('caneca_recorte.png.mask.png').convert('L')).astype(np.float32)/255
SS=2
def ell(cx,cy,rx,ry):
    m=Image.new('L',(W*SS,H*SS),0); ImageDraw.Draw(m).ellipse([(cx-rx)*SS,(cy-ry)*SS,(cx+rx)*SS,(cy+ry)*SS],fill=255)
    return np.array(m.resize((W,H),Image.LANCZOS)).astype(np.float32)/255
yy,xx=np.mgrid[0:H,0:W]
outer=ell(980,310,362,86); inner=ell(980,313,336,68)
# 1) limpa a máscara do Vision acima do aro (cortina) e junta o aro
vis2=vis.copy(); vis2[(yy<340)&(outer<0.5)]=0
# 2) pires: elipse (o Vision ficou irregular na esquerda)
saucer=ell(992,938,632,234)
# corpo: Vision abaixo do aro; pires: elipse (só abaixo/ao redor do corpo)
body=vis2.copy(); body[(a[...,1]>a[...,0]+40)&(a[...,1]>a[...,2]+40)]=0; body[(yy>690)&(xx<640)]=0   # tira a borda irregular do pires à esquerda
mask=np.clip(np.maximum.reduce([body,outer,saucer]),0,1)
# 3) repinta o aro de trás (à esquerda) e o líquido, que sumiram na cortina
liq_zone=inner*np.clip((860-xx)/40,0,1)*(yy<378)
ring_zone=np.clip(outer-inner,0,1)*(yy<312)*(xx<1180)
# cores amostradas
def mean(x0,y0,x1,y1): return a[y0:y1,x0:x1].reshape(-1,3).mean(0)
rim_col=mean(1230,236,1290,262)   # aro claro, lado direito
liq_col=np.array([112.,66.,46.])   # chocolate
print('aro',rim_col,'liq',liq_col)
rng=np.random.default_rng(3); noise=np.array(Image.fromarray((rng.random((H//6+1,W//6+1))*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)).astype(np.float32)/255-0.5
t=np.clip((xx-620)/360,0,1)[...,None]
liq=(liq_col*(0.82+0.3*t)+noise[...,None]*14)
rim=(rim_col*(0.88+0.12*t)+noise[...,None]*10)
out=a.copy()
lz=liq_zone[...,None]; out=out*(1-lz)+liq*lz
rz=ring_zone[...,None]; out=out*(1-rz)+rim*rz
# 4) tira o verde das bordas (descontaminação)
r,g,b=out[...,0],out[...,1],out[...,2]
lim=np.maximum(r,b)+8
over=g>lim
g2=np.where(over,lim,g)
out[...,1]=g2
alpha=Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
rgba=Image.fromarray(np.clip(out,0,255).astype(np.uint8)).convert('RGBA'); rgba.putalpha(alpha)
rgba.save('caneca_final.png')
bg=Image.new('RGBA',rgba.size,(40,60,120,255)); bg.alpha_composite(rgba)
bg.convert('RGB').resize((1000,671)).save('prev_final.jpg',quality=88)
print(rgba.getbbox())

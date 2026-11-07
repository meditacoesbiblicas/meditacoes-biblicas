# -*- coding: utf-8 -*-
# Seis vinhetas animadas (SVG) da parte 1: o que cada coisa "devolve". As animações estão em partes.css (classes .vinheta ...).

CAFE = '''<svg class="vinheta v-cafe" viewBox="0 0 480 320" role="img" aria-label="Uma caneca de chocolate quente fumegante, com marshmallows, sobre uma mesa de madeira, numa cozinha com a luz da manhã entrando pela janela">
<defs><filter id="c-sombra" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="3.2"/></filter></defs>
<image href="img/cena1-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<g opacity=".62"><image class="raio mistura" href="img/cena1-raio.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/></g>
<ellipse cx="271.2" cy="284.9" rx="43.6" ry="9" fill="#2E1A0A" opacity=".38" filter="url(#c-sombra)"/>
<image href="img/cena1-caneca.webp" x="187.5" y="161.0" width="169.6" height="125.8"/>
<g class="vapores"><image class="vp a mistura" href="img/cena1-vapor.jpg" x="212.6" y="70.4" width="112" height="108.3"/><image class="vp b mistura" href="img/cena1-vapor.jpg" x="212.6" y="70.4" width="112" height="108.3"/><image class="vp c mistura" href="img/cena1-vapor.jpg" x="212.6" y="70.4" width="112" height="108.3"/></g>
<g fill="#FFF3C4" class="motas"><circle class="mota m1" cx="86" cy="70" r="1.3"/><circle class="mota m2" cx="132" cy="104" r="1"/><circle class="mota m3" cx="176" cy="150" r="1.5"/><circle class="mota m4" cx="112" cy="168" r="1.1"/><circle class="mota m5" cx="214" cy="92" r="1.2"/><circle class="mota m6" cx="60" cy="122" r="1"/></g>
</svg>'''

REFEICAO = '''<svg class="vinheta v-refeicao" viewBox="0 0 480 320" role="img" aria-label="Uma família de quatro pessoas conversando e rindo em volta de uma mesa num restaurante aconchegante, enquanto o garçom chega com pratos vegetarianos e uma jarra de água com limão">
<defs><radialGradient id="r-brilho" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFD98A" stop-opacity=".9"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient>
<filter id="r-sombra" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="3.4"/></filter></defs>
<image href="img/cena2-restaurante-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<ellipse class="brilho-lampada mistura" cx="240" cy="52" rx="140" ry="74" fill="url(#r-brilho)"/>
<ellipse cx="203" cy="298" rx="112" ry="8" fill="#2A1408" opacity=".42" filter="url(#r-sombra)"/>
<ellipse cx="355" cy="292" rx="30" ry="4.5" fill="#2A1408" opacity=".4" filter="url(#r-sombra)"/>
<image class="familia-img" href="img/cena2-restaurante-familia.webp" x="91" y="106.6" width="224" height="191.4"/>
<image class="garcom-img" href="img/cena2-garcom.webp" x="325" y="189.5" width="60" height="102.5"/>
<g class="vapores"><image class="vp a mistura" href="img/cena1-vapor.jpg" x="150.5" y="144.5" width="44" height="42.5"/><image class="vp b mistura" href="img/cena1-vapor.jpg" x="210" y="142.5" width="44" height="42.5"/><image class="vp c mistura" href="img/cena1-vapor.jpg" x="354" y="171.5" width="28" height="27"/></g>
<g fill="#E0526A"><path class="coracao h1" d="M130 120c-8-10-22 1-12 12l12 11 12-11c10-11-4-22-12-12z"/><path class="coracao h2" d="M290 112c-7-9-19 1-10 10l10 10 10-10c9-10-3-19-10-10z"/><path class="coracao h3" d="M250 96c-6-8-16 1-8 9l8 8 8-8c8-9-2-17-8-9z"/></g>
</svg>'''

FIM = '''<svg class="vinheta v-fim" viewBox="0 0 480 320" role="img" aria-label="Uma família descalça na grama de um hotel fazenda, dando capim a um cavalinho e rindo com as galinhas, com o casarão do hotel e a piscina ao fundo e nuvens passando">
<image href="img/cena3-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<g class="nuvens-g"><image class="nuvens mistura" href="img/cena3-nuvens.jpg" x="-10" y="-10" width="500" height="197.8" opacity=".95"/></g>
<image href="img/cena3-casarao.webp" x="262" y="123.6" width="125" height="66.4"/>
<image href="img/cena3-piscina.webp" x="96" y="132.3" width="100" height="55.7"/>
<g fill="#FFFFFF" class="brilhos"><circle class="tw t1" cx="141" cy="155" r="1.8"/><circle class="tw t2" cx="160" cy="163" r="1.4"/><circle class="tw t3" cx="127" cy="167" r="1.6"/></g>
<ellipse cx="190" cy="304" rx="82" ry="6.5" fill="#1F3A12" opacity=".35" style="filter: blur(3px)"/>
<image class="familia-img" href="img/cena3-familia.webp" x="95" y="141.5" width="190" height="166.5"/>
</svg>'''

VIAGEM = '''<svg class="vinheta v-viagem" viewBox="0 0 480 320" role="img" aria-label="Uma família brasileira com malas diante da Torre Eiffel, em Paris, no fim da tarde, enquanto um avião cruza o céu">
<defs><radialGradient id="p-sol" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFE3A0" stop-opacity=".95"/><stop offset="1" stop-color="#FFE3A0" stop-opacity="0"/></radialGradient>
<linearGradient id="p-rastro" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".75"/></linearGradient>
<filter id="p-sombra" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="3"/></filter></defs>
<image href="img/cena4-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<ellipse class="brilho-sol mistura" cx="262" cy="176" rx="64" ry="46" fill="url(#p-sol)"/>
<g class="aviao-g"><rect x="-64" y="63" width="66" height="2.6" rx="1.3" fill="url(#p-rastro)"/><image href="img/cena4-aviao.webp" x="0" y="52" width="72" height="17.4"/></g>
<g fill="#FFE9A8" class="fagulhas mistura"><circle class="tw t1" cx="240" cy="52" r="2.2"/><circle class="tw t2" cx="236" cy="98" r="1.8"/><circle class="tw t3" cx="245" cy="120" r="1.8"/><circle class="tw t1" cx="228" cy="164" r="2"/><circle class="tw t2" cx="254" cy="168" r="1.8"/><circle class="tw t3" cx="240" cy="142" r="1.6"/></g>
<ellipse cx="236" cy="305" rx="62" ry="6" fill="#4A3320" opacity=".38" filter="url(#p-sombra)"/>
<image class="familia-img" href="img/cena4-familia.webp" x="171" y="194" width="130" height="111.8"/>
</svg>'''

CARRO = '''<svg class="vinheta v-carro" viewBox="0 0 480 320" role="img" aria-label="Um carro em uma estrada aberta, em um dia de sol, com a paisagem passando">
<defs>
<linearGradient id="k-ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7EC8F5"/><stop offset="1" stop-color="#E8F6FF"/></linearGradient>
</defs>
<rect width="480" height="320" fill="url(#k-ceu)"/>
<circle cx="392" cy="62" r="30" fill="#FFE57A"/><circle cx="392" cy="62" r="46" fill="#FFE57A" opacity=".25"/>
<g class="nuvens"><ellipse class="nv n1" cx="90" cy="60" rx="46" ry="14" fill="#FFFFFF" opacity=".9"/><ellipse class="nv n2" cx="260" cy="38" rx="36" ry="11" fill="#FFFFFF" opacity=".85"/></g>
<g class="morros longe"><path d="M0 214L70 156L140 206L220 140L300 208L380 150L460 204L540 160V236H0Z" fill="#8BB6C9"/><path d="M-480 214L-410 156L-340 206L-260 140L-180 208L-100 150L-20 204L60 160V236H-480Z" fill="#8BB6C9"/></g>
<g class="morros perto"><path d="M0 236L90 190L190 232L290 184L390 232L480 196V256H0Z" fill="#5E9A6C"/><path d="M-480 236L-390 190L-290 232L-190 184L-90 232L0 196V256H-480Z" fill="#5E9A6C"/></g>
<rect y="244" width="480" height="76" fill="#4A4F5C"/><rect y="244" width="480" height="6" fill="#6A7080"/>
<g class="faixas" fill="#FFE9A0"><rect x="0" y="286" width="50" height="6" rx="3"/><rect x="100" y="286" width="50" height="6" rx="3"/><rect x="200" y="286" width="50" height="6" rx="3"/><rect x="300" y="286" width="50" height="6" rx="3"/><rect x="400" y="286" width="50" height="6" rx="3"/><rect x="500" y="286" width="50" height="6" rx="3"/></g>
<g class="carro-corpo">
<path d="M118 262L124 232Q130 218 150 214L200 208L238 186Q252 178 272 178H318Q344 180 356 200L384 214Q404 220 406 240L408 262Z" fill="#E24B3B"/>
<path d="M246 192L274 186H318Q336 188 346 204L248 208Z" fill="#CFEAFB"/><path d="M296 186V206" stroke="#E24B3B" stroke-width="5"/>
<rect x="120" y="244" width="290" height="10" rx="4" fill="#B93A2E"/><rect x="394" y="226" width="14" height="10" rx="3" fill="#FFF3B0"/><rect x="118" y="230" width="9" height="10" rx="3" fill="#FFB1A8"/>
<polygon class="farol" points="408,230 480,208 480,258 408,238" fill="#FFF3B0" opacity=".28"/>
<g class="roda r1"><circle cx="176" cy="264" r="25" fill="#23252D"/><circle cx="176" cy="264" r="13" fill="#B8BDC9"/><path d="M176 253V275M165 264H187M168 256L184 272M184 256L168 272" stroke="#6E7484" stroke-width="3"/></g>
<g class="roda r2"><circle cx="352" cy="264" r="25" fill="#23252D"/><circle cx="352" cy="264" r="13" fill="#B8BDC9"/><path d="M352 253V275M341 264H363M344 256L360 272M360 256L344 272" stroke="#6E7484" stroke-width="3"/></g>
</g>
<g class="vento" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity=".7"><path class="vt a" d="M30 206H86"/><path class="vt b" d="M10 226H60"/><path class="vt c" d="M46 190H92"/></g>
</svg>'''

CASA = '''<svg class="vinheta v-casa" viewBox="0 0 480 320" role="img" aria-label="Uma casa ao entardecer, de janelas acesas, com a família lá dentro">
<defs>
<linearGradient id="h-ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#262A66"/><stop offset=".6" stop-color="#8E5C9A"/><stop offset="1" stop-color="#F2A06A"/></linearGradient>
<radialGradient id="h-luz" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFE9A0" stop-opacity=".95"/><stop offset="1" stop-color="#FFE9A0" stop-opacity="0"/></radialGradient>
</defs>
<rect width="480" height="320" fill="url(#h-ceu)"/>
<g fill="#FFFFFF"><circle class="est e1" cx="60" cy="40" r="1.6"/><circle class="est e2" cx="130" cy="72" r="1.3"/><circle class="est e3" cx="210" cy="30" r="1.7"/><circle class="est e1" cx="400" cy="46" r="1.5"/><circle class="est e2" cx="448" cy="92" r="1.2"/><circle class="est e3" cx="330" cy="64" r="1.4"/></g>
<circle cx="52" cy="92" r="16" fill="#FFF3CF"/><circle cx="46" cy="88" r="16" fill="#262A66" opacity=".0"/>
<path d="M0 262Q120 238 240 252Q360 238 480 258V320H0Z" fill="#2F5A3C"/>
<path d="M200 320Q214 286 238 270H262Q286 286 300 320Z" fill="#D9C79F" opacity=".9"/>
<rect x="146" y="162" width="188" height="108" fill="#EAD7B8"/>
<polygon points="128,166 240,92 352,166" fill="#8B3A2F"/><rect x="296" y="102" width="20" height="40" fill="#6E2E26"/>
<g class="fumaca-casa" fill="#FFFFFF" opacity=".55"><circle class="fm f1" cx="306" cy="96" r="7"/><circle class="fm f2" cx="310" cy="86" r="6"/><circle class="fm f3" cx="304" cy="76" r="5"/></g>
<rect x="222" y="206" width="36" height="64" rx="3" fill="#6B4226"/><circle cx="250" cy="240" r="2.6" fill="#E9C56B"/>
<circle class="aura a1" cx="188" cy="204" r="52" fill="url(#h-luz)"/><circle class="aura a2" cx="292" cy="204" r="52" fill="url(#h-luz)"/><circle class="aura a3" cx="240" cy="150" r="34" fill="url(#h-luz)"/>
<rect class="janela j1" x="166" y="186" width="44" height="40" rx="3" fill="#FFD670" stroke="#8A5A34" stroke-width="4"/><path d="M188 186V226M166 206H210" stroke="#8A5A34" stroke-width="3"/>
<rect class="janela j2" x="270" y="186" width="44" height="40" rx="3" fill="#FFD670" stroke="#8A5A34" stroke-width="4"/><path d="M292 186V226M270 206H314" stroke="#8A5A34" stroke-width="3"/>
<circle class="janela j3" cx="240" cy="140" r="14" fill="#FFD670" stroke="#8A5A34" stroke-width="4"/>
<g class="familia" fill="#6B3F2E"><circle cx="180" cy="208" r="6"/><path d="M171 226Q172 214 180 214Q188 214 189 226Z"/><circle cx="196" cy="212" r="4.6"/><path d="M189 226Q190 218 196 218Q202 218 203 226Z"/></g>
<g class="familia2" fill="#5A3328"><circle cx="286" cy="210" r="6"/><path d="M277 226Q278 214 286 214Q294 214 295 226Z"/></g>
<path d="M396 320V232" stroke="#4A3A2C" stroke-width="5"/><circle cx="396" cy="226" r="8" fill="#FFE9A0"/><circle cx="396" cy="226" r="34" fill="url(#h-luz)" opacity=".7"/>
<ellipse cx="72" cy="244" rx="30" ry="40" fill="#2A5A38"/><rect x="68" y="266" width="8" height="26" fill="#4A3426"/>
<g class="vagalumes" fill="#FFF28A"><circle class="vg v1" cx="130" cy="262" r="2.2"/><circle class="vg v2" cx="360" cy="270" r="2.2"/><circle class="vg v3" cx="110" cy="290" r="2"/></g>
</svg>'''

TODAS = [CAFE, REFEICAO, FIM, VIAGEM, CARRO, CASA]

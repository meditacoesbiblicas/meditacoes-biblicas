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

REFEICAO = '''<svg class="vinheta v-refeicao" viewBox="0 0 480 320" role="img" aria-label="Uma família de quatro pessoas conversando e sorrindo em volta de uma mesa posta, sob uma lâmpada acesa">
<defs><radialGradient id="r-brilho" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFD98A" stop-opacity=".9"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient>
<filter id="r-sombra" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="3.4"/></filter></defs>
<image href="img/cena2-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<ellipse class="brilho-lampada mistura" cx="240" cy="96" rx="150" ry="110" fill="url(#r-brilho)"/>
<ellipse cx="240" cy="299.6" rx="149.4" ry="9" fill="#2A1408" opacity=".4" filter="url(#r-sombra)"/>
<image class="familia-img" href="img/cena2-familia.webp" x="81.1" y="94.2" width="317.8" height="205.3"/>
<g class="vapores"><image class="vp a mistura" href="img/cena1-vapor.jpg" x="209.0" y="149.2" width="62" height="59.9"/><image class="vp b mistura" href="img/cena1-vapor.jpg" x="209.0" y="149.2" width="62" height="59.9"/></g>
<g fill="#E0526A"><path class="coracao h1" d="M150 120c-8-10-22 1-12 12l12 11 12-11c10-11-4-22-12-12z"/><path class="coracao h2" d="M340 106c-7-9-19 1-10 10l10 10 10-10c9-10-3-19-10-10z"/><path class="coracao h3" d="M300 84c-6-8-16 1-8 9l8 8 8-8c8-9-2-17-8-9z"/></g>
</svg>'''

FIM = '''<svg class="vinheta v-fim" viewBox="0 0 480 320" role="img" aria-label="Uma família descalça na grama de um hotel fazenda, dando capim a um cavalinho e rindo com as galinhas, com a sede da fazenda ao fundo e nuvens passando">
<image href="img/cena3-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<g class="nuvens-g"><image class="nuvens mistura" href="img/cena3-nuvens.jpg" x="-10" y="-10" width="500" height="197.8" opacity=".95"/></g>
<image href="img/cena3-sede.webp" x="305.5" y="141.4" width="105.0" height="48.6"/>
<g class="fumacas"><image class="vp a mistura" href="img/cena1-vapor.jpg" x="363.9" y="130.7" width="18" height="17.4"/><image class="vp b mistura" href="img/cena1-vapor.jpg" x="363.9" y="130.7" width="18" height="17.4"/></g>
<ellipse cx="231.0" cy="303.0" rx="90.3" ry="7" fill="#1F3A12" opacity=".35" style="filter: blur(3px)"/>
<image class="familia-img" href="img/cena3-familia.webp" x="117.5" y="119.6" width="215.0" height="188.4"/>
</svg>'''

VIAGEM = '''<svg class="vinheta v-viagem" viewBox="0 0 480 320" role="img" aria-label="Um avião cruzando o globo de uma cidade a outra, em direção a lugares novos">
<defs>
<linearGradient id="g-ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101A4A"/><stop offset="1" stop-color="#3A5AB8"/></linearGradient>
<radialGradient id="g-globo" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#7FC2F0"/><stop offset=".6" stop-color="#2A6FB8"/><stop offset="1" stop-color="#143C7A"/></radialGradient>
</defs>
<rect width="480" height="320" fill="url(#g-ceu)"/>
<g fill="#FFFFFF"><circle class="tw t1" cx="52" cy="48" r="1.6"/><circle class="tw t2" cx="140" cy="86" r="1.2"/><circle class="tw t3" cx="396" cy="40" r="1.8"/><circle class="tw t1" cx="440" cy="102" r="1.2"/><circle class="tw t2" cx="220" cy="30" r="1.4"/><circle class="tw t3" cx="330" cy="74" r="1.1"/></g>
<circle cx="240" cy="430" r="266" fill="#8FD0FF" opacity=".28"/><circle cx="240" cy="430" r="250" fill="url(#g-globo)"/><g fill="#FFFFFF" opacity=".55"><ellipse cx="150" cy="226" rx="34" ry="6"/><ellipse cx="330" cy="214" rx="40" ry="6"/><ellipse cx="240" cy="236" rx="48" ry="5"/><ellipse cx="410" cy="250" rx="26" ry="5"/></g>
<path d="M120 250q30-26 70-18q34 8 50-8q26-20 66 6q34 22 70 6l20 30q-70 20-130 6q-60-14-146 8z" fill="#5BA86A" opacity=".85"/>
<path d="M300 232q18-10 36 0q10 14-6 22q-22 4-30-22z" fill="#6DB879" opacity=".9"/>
<path id="g-rota" d="M96 206Q240 20 384 206" fill="none" stroke="#FFE08A" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round"/>
<circle cx="96" cy="206" r="7" fill="#FF7A59"/><circle cx="384" cy="206" r="7" fill="#FF7A59"/>
<path d="M84 206l12-44l12 44z" fill="#2C2540" opacity=".85"/><path d="M366 206h36v-22l-6-8v-10h-6v10h-12v-10h-6v10l-6 8z" fill="#2C2540" opacity=".85"/>
<g><path transform="scale(-1 1)" d="M-18 0l6-3 22-12 4 1-12 14 14 1 6-5 3 1-3 6 3 6-3 1-6-5-14 1 12 14-4 1-22-12-6-3z" fill="#FFFFFF"><animateMotion dur="7s" repeatCount="indefinite" rotate="auto"><mpath href="#g-rota"/></animateMotion></path></g>
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

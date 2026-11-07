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
<ellipse cx="191" cy="298" rx="99" ry="7.5" fill="#2A1408" opacity=".42" filter="url(#r-sombra)"/>
<ellipse cx="353" cy="296" rx="40" ry="5.5" fill="#2A1408" opacity=".4" filter="url(#r-sombra)"/>
<image class="familia-img" href="img/cena2-restaurante-familia.webp" x="91" y="126.5" width="200" height="171.0"/>
<image class="garcom-img" href="img/cena2-garcom.webp" x="283" y="106" width="103" height="187.6"/>
<g class="vapores"><image class="vp a mistura" href="img/cena1-vapor.jpg" x="143.8" y="159" width="40" height="38.6"/><image class="vp b mistura" href="img/cena1-vapor.jpg" x="196.8" y="158" width="40" height="38.6"/><image class="vp c mistura" href="img/cena1-vapor.jpg" x="289" y="88" width="46" height="44.4"/></g>
<g fill="#E0526A"><path class="coracao h1" d="M130 140c-8-10-22 1-12 12l12 11 12-11c10-11-4-22-12-12z"/><path class="coracao h2" d="M262 128c-7-9-19 1-10 10l10 10 10-10c9-10-3-19-10-10z"/><path class="coracao h3" d="M214 118c-6-8-16 1-8 9l8 8 8-8c8-9-2-17-8-9z"/></g>
</svg>'''

FIM = '''<svg class="vinheta v-fim" viewBox="0 0 480 320" role="img" aria-label="Uma família descalça na grama de um hotel fazenda, dando capim a um cavalinho e rindo com as galinhas, com o casarão do hotel e a piscina ao fundo e nuvens passando">
<image href="img/cena3-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<g class="nuvens-g"><image class="nuvens mistura" href="img/cena3-nuvens.jpg" x="150" y="0" width="170" height="67.2" opacity=".8"/></g>
<image href="img/cena3-casarao.webp" x="262" y="123.6" width="125" height="66.4"/>
<ellipse cx="190" cy="304" rx="82" ry="6.5" fill="#1F3A12" opacity=".35" style="filter: blur(3px)"/>
<image class="familia-img" href="img/cena3-familia.webp" x="95" y="141.5" width="190" height="166.5"/>
</svg>'''

VIAGEM = '''<svg class="vinheta v-viagem" viewBox="0 0 480 320" role="img" aria-label="Uma família brasileira com malas diante da Torre Eiffel, em Paris, no fim da tarde, enquanto um avião distante sobe pelo céu, bem longe da torre">
<defs><radialGradient id="p-sol" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFE3A0" stop-opacity=".95"/><stop offset="1" stop-color="#FFE3A0" stop-opacity="0"/></radialGradient>
<linearGradient id="p-rastro" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".75"/></linearGradient>
<filter id="p-sombra" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="3"/></filter></defs>
<image href="img/cena4-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<ellipse class="brilho-sol mistura" cx="262" cy="176" rx="64" ry="46" fill="url(#p-sol)"/>
<g class="aviao-g"><rect x="-40" y="4.2" width="42" height="1.8" rx=".9" fill="url(#p-rastro)"/><image href="img/cena4-aviao.webp" x="0" y="0" width="44" height="10.6"/></g>
<g fill="#FFE9A8" class="fagulhas mistura"><circle class="tw t1" cx="240" cy="52" r="2.2"/><circle class="tw t2" cx="236" cy="98" r="1.8"/><circle class="tw t3" cx="245" cy="120" r="1.8"/><circle class="tw t1" cx="228" cy="164" r="2"/><circle class="tw t2" cx="254" cy="168" r="1.8"/><circle class="tw t3" cx="240" cy="142" r="1.6"/></g>
<ellipse cx="236" cy="305" rx="62" ry="6" fill="#4A3320" opacity=".38" filter="url(#p-sombra)"/>
<image class="familia-img" href="img/cena4-familia.webp" x="171" y="194" width="130" height="111.8"/>
</svg>'''

CARRO = '''<svg class="vinheta v-carro" viewBox="0 0 480 320" role="img" aria-label="Uma família num carro vermelho novo, passeando por uma estrada de interior num dia de sol, com árvores e postes passando ao lado">
<image href="img/cena5-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<g class="nuvens-g"><image class="nuvens mistura" href="img/cena3-nuvens.jpg" x="110" y="-6" width="260" height="102.9" opacity=".85"/></g>
<g class="arvores-g"><image href="img/cena5-arvores-longe.webp" x="0" y="67" width="560" height="140"/><image href="img/cena5-arvores-longe.webp" x="560" y="67" width="560" height="140"/></g>
<g class="cerca-g"><g stroke="#2B2A26" stroke-width=".7" fill="none"><path d="M0 193.7H1160"/><path d="M0 203.1H1160"/></g><rect x="0" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="2.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="64" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="66.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="128" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="130.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="192" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="194.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="256" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="258.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="320" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="322.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="384" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="386.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="448" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="450.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="512" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="514.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="576" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="578.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="640" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="642.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="704" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="706.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="768" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="770.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="832" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="834.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="896" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="898.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="960" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="962.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="1024" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="1026.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/><rect x="1088" y="188.5" width="3.4" height="22.8" fill="#7A5B3B"/><rect x="1090.2" y="188.5" width="1.2" height="22.8" fill="#5B4129"/></g>
<g class="postes-g"><image href="img/cena5-postes-perto.webp" x="0" y="89" width="480" height="135"/><image href="img/cena5-postes-perto.webp" x="480" y="89" width="480" height="135"/></g>
<rect x="0" y="239.8" width="480" height="5.4" fill="#6A6668"/>
<g class="tracos" fill="#F2C230"><rect x="10" y="241.2" width="48" height="2"/><rect x="120" y="241.2" width="48" height="2"/><rect x="230" y="241.2" width="48" height="2"/><rect x="340" y="241.2" width="48" height="2"/><rect x="450" y="241.2" width="48" height="2"/><rect x="560" y="241.2" width="48" height="2"/></g>
<g class="carro-g"><image class="carro-img" href="img/cena5-carro.webp" x="117" y="154.5" width="250" height="107.5"/><image class="roda r1" href="img/cena5-roda-tras.webp" x="142.95" y="225.2" width="30.6" height="30.6"/><image class="roda r2" href="img/cena5-roda-frente.webp" x="307.9" y="225.2" width="30.6" height="30.6"/></g>
</svg>'''

CASA = '''<svg class="vinheta v-casa" viewBox="0 0 480 320" role="img" aria-label="Uma família abraçada, de costas, mostra as chaves diante da casa própria ao entardecer, com as janelas acesas e passarinhos voltando para casa">
<defs><radialGradient id="k-luz" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFC24D" stop-opacity=".95"/><stop offset="1" stop-color="#FFC24D" stop-opacity="0"/></radialGradient></defs>
<image href="img/cena6-fundo.jpg" x="0" y="0" width="480" height="320" preserveAspectRatio="xMidYMid slice"/>
<g class="nuvens-g"><image class="nuvens mistura" href="img/cena6-nuvens.jpg" x="245" y="0" width="110" height="73.3" opacity=".85"/></g>
<g class="passaros" fill="none" stroke="#3B2742" stroke-width="1.4" stroke-linecap="round"><g class="passaro p1" transform="translate(250 44)"><path class="asa" d="M0 0q4-4 8 0q4-4 8 0"/></g><g class="passaro p2" transform="translate(270 56)"><path class="asa" d="M0 0q3-3 6 0q3-3 6 0"/></g><g class="passaro p3" transform="translate(292 38)"><path class="asa" d="M0 0q3-3 6 0q3-3 6 0"/></g></g>
<image href="img/cena6-casa.webp" x="105" y="72.6" width="270" height="179.4"/>
<g class="brilhos-janela mistura"><ellipse class="janela-brilho j1" cx="210.6" cy="112.8" rx="30" ry="19" fill="url(#k-luz)"/><ellipse class="janela-brilho j2" cx="282.7" cy="111.9" rx="30" ry="19" fill="url(#k-luz)"/><ellipse class="janela-brilho j3" cx="190.8" cy="174.1" rx="30" ry="19" fill="url(#k-luz)"/><ellipse class="janela-brilho j4" cx="293.5" cy="174.1" rx="30" ry="19" fill="url(#k-luz)"/><ellipse class="janela-brilho j5" cx="262.9" cy="162.4" rx="14" ry="12" fill="url(#k-luz)"/></g>
<g class="vagalumes mistura" fill="#FFF3A0"><circle class="vaga v1" cx="130" cy="262" r="1.5"/><circle class="vaga v2" cx="168" cy="278" r="1.2"/><circle class="vaga v3" cx="330" cy="268" r="1.5"/><circle class="vaga v4" cx="360" cy="282" r="1.2"/><circle class="vaga v5" cx="112" cy="240" r="1.3"/><circle class="vaga v6" cx="372" cy="244" r="1.3"/></g>
<image class="familia-img" href="img/cena6-familia.webp" x="184" y="187.3" width="112" height="104.7"/>
</svg>'''

TODAS = [CAFE, REFEICAO, FIM, VIAGEM, CARRO, CASA]

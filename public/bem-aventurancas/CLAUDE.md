# Sermão do Monte (Mt 5–7) — site de estudo, em construção

Site estático (HTML + CSS puro) de estudo bíblico, projetado na igreja. **O estudo é o Sermão do Monte (Mt 5–7), em construção**: começa pelas bem-aventuranças (Mt 5:3–12) e já segue pela trilha até Mt 5:30; o resto virá aos poucos (o site diz isso no mapa, com o selo "Em construção", e no último passo da trilha). A pasta e a URL continuam `bem-aventurancas` (a URL não muda). Sem JavaScript, sem build. O dono pede melhorias uma por vez; responder sempre em português do Brasil.

## Arquivos

- `index.html` — mapa do estudo (um ramo por versículo/grupo), legenda dos cartões e o quadro "O que o conjunto mostra".
- `v03.html`, `v04-05.html`, `v06-08.html`, `v09.html`, `v10-12.html` — as bem-aventuranças.
- `depois.html` — a **trilha** "Depois das bem-aventuranças" (Mt 5:13–30), página de layout próprio (hero azul-marinho com o v.20 como chave, 4 passos numa linha do tempo; cada passo mostra "Por fora → Por dentro"). No mapa ela é o banner `.depois-banner` logo abaixo da árvore ("E depois das bem-aventuranças?"), que substituiu o antigo cartão "Sal e luz".
- `v13-15.html` — "Sal e luz" (v.13–16; o nome do arquivo é mantido por causa da URL): grupos `#v13` (sal) e `#v14` (luz: luz×trevas, boas obras e o candelabro/santuário).
- `v17-20.html` — a lei (v.17–19, grupo `#v17`) e a justiça que excede a dos escribas e fariseus (v.20, grupo `#v20`).
- `v21-26.html` — da morte à raiva (`#v21`) e reconciliar-se antes de oferecer (`#v23`).
- `v27-30.html` — do adultério à cobiça (`#v27`) e arrancar o olho/cortar a mão (`#v29`).
- `style.css` — único CSS. Fontes via `@import` do Google Fonts (Inter e Newsreader), com fallback do sistema.

## Estrutura do estudo

- **Numeração das portas (1 a 8):** v.3=1, v.4=2, v.5=3, v.6=4, v.7=5, v.8=6, v.9=7, v.10–12=8. Aparece nos ramos do mapa (`<b class="no">`), no cabeçalho de cada grupo ("Porta N · Mateus 5:x") e nas pílulas. Bate com a ilustração `caminho.html` (cada bem-aventurança é uma porta do caminho único; o juízo no fim). Ao criar grupo novo de bem-aventurança, atualize o `PORTA` do script e os ramos.
- `caminho.html` (+ `caminho.jpg`, `caminho-mini.jpg`): **página de abertura, e é para onde o QR Code aponta** (pedido do dono: quem escaneia vê a ilustração, as 8 portas clicáveis — cada uma leva ao ramo da bem-aventurança — e o botão "Ver o mapa do estudo →", que continua o estudo). No PC: imagem grande à esquerda + painel azul-marinho com as portas à direita (no celular: imagem em cima e portas em pílulas; o celular é a referência de qualidade, o PC tem que ficar no mesmo nível). A imagem abre o `caminho.jpg` inteiro. Criada com IA (Gemini) a partir de roteiro do dono. **Tem o pixel de visitas** (é a entrada do QR). No mapa (PC), o cartão `.caminho-card` fica **ao lado do QR (QR à esquerda, caminho à direita), com a mesma largura e a mesma altura** (`.top-lado`, 2 colunas de 188px); no celular ficam empilhados; os dois abrem, respectivamente, `qr.html` e `caminho.html`. Link também no fim da trilha.

- As bem-aventuranças são Mt 5:3–12: oito (v.3–10); os v.11–12 ampliam a oitava, no mesmo tópico (`v10-12.html`).
- Depois delas vem a trilha (`depois.html`): Sal e luz (v.13–16) → A lei e a justiça maior (v.17–20) → Da morte à raiva (v.21–26) → Do adultério à cobiça (v.27–30). O fio é Mt 5:20: a justiça que excede a dos escribas e fariseus, "de fora para dentro" (a lei vista pelo ato × Jesus olhando o coração).
- O mapa usa âncoras: `#v3`, `#v4`, `#v5`, `#v6`, `#v7`, `#v8`, `#v9`, `#v10`; a trilha usa `#v13`, `#v14`, `#v17`, `#v20`, `#v21`, `#v23`, `#v27`, `#v29`. Cada `<section class="group" id="vN">` da página de detalhe tem o id correspondente.

## Barra do site (em TODAS as páginas: o mapa, a trilha, as de detalhe e o `qr.html`)

- `<header class="site-bar">` logo depois de `<body>`, fora do `.wrap`: Meditações (`../`), Quem sou eu (`../quem-sou-eu/`) e Sobre (`../sobre/`). Serve para voltar ao site principal com um clique, de qualquer página.
- Só HTML e CSS (sem JavaScript). **Ao criar página nova, copie a barra.** Se as rotas do site principal mudarem, atualize os 3 links.
- Abrindo por `file://`, esses 3 links não funcionam (saem da pasta); no site publicado funcionam.

## Navegação (repetida em todas as páginas de detalhe)

- Topo: `<nav class="crumbs">` com o botão "← Mapa" e as pílulas: v.3, v.4–5, v.6–8, v.9, v.10–12 e, separadas, "Trilha", "Sal e luz", "A lei", "Raiva" e "Cobiça". A página atual leva `aria-current="page"`.
- Rodapé: `<nav class="pager">` com Anterior/Próxima. A primeira página volta ao Mapa; o fim da cadeia (`v27-30.html`) volta para a trilha (`depois.html`). A trilha em si não tem pager.
- **Ao criar ou renomear uma página, atualize TODAS** (pílulas de todas as páginas, pager das vizinhas, ramo no `index.html`).

## Card (cartão) de conteúdo

```html
<article class="note blue|orange|green|purple|gray">
  <span class="tag">Paralelo | Contraste | Exemplo | Ellen White | Conclusão</span>
  <h3>Livro por extenso + referência <span class="ver">King James</span></h3>
  <blockquote class="text"><p>… <mark>parte que explica a bem-aventurança</mark> …</p></blockquote>
  <p class="obs">uma frase de conclusão, em linguagem para o público</p>
  <a class="full" href="https://www.bibliaonline.com.br/arc/{livro}/{capitulo}/{versiculo}+" target="_blank" rel="noopener">Ler o texto completo na ARC ↗</a>
</article>
```

- Cores: azul = Paralelo, laranja = Contraste, verde = Exemplo, roxo = Ellen White (Espírito de Profecia), cinza = Conclusão.
- O selo `<span class="ver">King James</span>` (ou `<span class="ver">ARA</span>`) entra no `<h3>` só dos cartões que não são ARC. Cartão sem selo = ARC.
- Versículos numerados dentro da citação: `<span class="n">12</span>`.
- Cartão cinza "Conclusão": sem citação; só o título e 1–3 frases (`<p>`), no máximo uma `p.obs` de ligação.
- As páginas de detalhe foram geradas por script a partir de uma lista de cartões. Para editar, mexa direto nos HTML (é o texto oficial).

## Conteúdo

- **O site é para o público.** Nunca descreva as marcas do dono (circulado, sublinhado, seta, margem, lápis, cores, "posição incerta", "leitura minha"). O dono explica as anotações na conversa e a conclusão vai para o site, já em linguagem para o público. Nada de "Sua nota".
- A Bíblia se explica sozinha: comentário mínimo. Conclusão só onde o dono pediu ou explicou o raciocínio; tom claro e direto. Se usar palavra difícil, repita ao lado com um sinônimo entre vírgulas (ex.: "usurpar, tomar à força").
- **Não invente referência.** Versículos extras (além dos que o dono anotou) só quando ele pedir; liste-os para ele na resposta.
- **Texto bíblico.** Padrão: ARC (Almeida Revista e Corrigida, © Sociedade Bíblica do Brasil). O dono lê a **King James** em português, que é a **BKJ** do bibliaonline (`https://www.bibliaonline.com.br/bkj/{livro}/{capitulo}/{versiculo}+`); use-a só onde ele pedir (hoje: Pv 16:32, 1Tm 3:6, 1Pe 4:14–18, 1Pe 4:15, Pv 20:3). **Pv 18:8 está em ARA** (selo "ARA", link `https://www.bibliaonline.com.br/ara/pv/18/8+`, "doces bocados"): não volte para a King James. O Sl 15 fica em ARC (preferência dele). Quando ele pedir outra passagem em King James ou ARA, troque o texto, o selo e o link.
- Cite só o trecho-chave (até cerca de 125 caracteres por citação, com … nas omissões), nunca capítulos inteiros. **Confira a redação exata no bibliaonline antes de inserir, nunca de memória.** O texto completo do versículo está no JSON-LD (`"text"`) da página do versículo.
- **Ellen White (Espírito de Profecia).** Só citação **literal** em português, de m.egwwritings.org/pt, com link do **parágrafo exato**: `https://m.egwwritings.org/pt/book/<livro>.<parágrafo>` (O Maior Discurso de Cristo = 1956, ex.: 1956.131 = MDC 18.2; Patriarcas e Profetas = 1815, ex.: 1815.78 = PP 9.3). Cartão roxo, título "Livro, p. N.N". O link de "trecho marcado" do site só se cria logado; se o dono mandar um, troque. Se não achar trecho adequado, não invente.

## Técnica

- Sem JavaScript e sem build. Só links relativos. Precisa abrir por `file://` e dentro de subpasta do GitHub Pages.
- Projetado na igreja: texto grande e legível. Teste em tela larga (1280px ou mais) e estreita (390px), sem rolagem horizontal.
- Planejado: QR Code para quem assiste à mensagem. **A URL não pode mudar depois de publicada: não renomeie a pasta nem os arquivos.**

## Publicação

- A versão oficial fica no repositório da página de meditações (`meditacoes-biblicas`), em `public/bem-aventurancas/`. Editar ali, commit e push a cada pedido.
- URL final: https://meditacoesbiblicas.github.io/meditacoes-biblicas/bem-aventurancas/
- O GitHub Pages publica o branch `gh-pages`, que um workflow (`.github/workflows/deploy.yml`) reconstrói a cada push em `main`. Leva alguns minutos.
- Este arquivo (`CLAUDE.md`) não vai para o site público: o `angular.json` do repositório o ignora na publicação.
- A entrada na lista da home está em `src/app/data/meditations.ts` (id `bem-aventurancas`, campo `url`). Entradas com `url` abrem a página estática em vez do leitor de markdown.

## Cópia offline (para usar sem internet)

- Pasta `~/BemAventurancas-offline/` (fora do iCloud de propósito, para o iCloud não descarregar os arquivos sem internet). Abre com dois cliques em `index.html`. Gerada por `scripts/atualizar-offline.py` a partir desta pasta (`public/bem-aventurancas/`).
- **Regra do dono: toda vez que o estudo for atualizado, a cópia offline também.** Um hook `post-commit` (e `post-merge`) em `.git/hooks/` roda o script a cada commit; mesmo assim, **depois de qualquer alteração, rode `python3 scripts/atualizar-offline.py`** se o hook não tiver rodado (hooks não vão no git: em outra máquina, recrie).
- A cópia muda só: fontes locais (`fonts/`), sem contador de visitas, barra do site com "Meditações" → `index.html` e "Quem sou eu"/"Sobre" apontando para a internet; sem `CLAUDE.md`. Não edite a pasta offline à mão: ela é sobrescrita.

## QR Code

- **Cartão no mapa:** no canto superior direito do `index.html` há um cartão (`.qr-card`, no estilo dos outros cartões) com o QR em miniatura. Ele leva ao `qr.html`. No celular o cartão vem abaixo do texto de abertura.
- **`qr.html`:** só a barra do site, o QR e, embaixo, o título (que é link para o mapa) e o endereço. O QR ocupa a janela inteira **sem rolagem** (testado de 390px a 1920px). Para isso ele é posicionado de forma absoluta na área livre entre a barra e a legenda; não troque por `height: 100%` em flex/SVG, porque o Safari estoura a altura.
- **`qr.svg`:** a imagem do QR (usada no cartão e no `qr.html`). Aponta para `.../bem-aventurancas/caminho.html`. Foi gerada com a biblioteca npm `qrcode` (correção de erro Q, margem de 4 módulos) e conferida decodificando de volta para a URL. **Se a URL do estudo mudar, gere de novo.** (A regra é a URL não mudar.)
- O `qr.html` não tem o pixel de visitas de propósito: é só a tela de projeção. Quem conta a visita do QR é o `caminho.html`.

## Contagem de visitas

- Cada página termina com um pixel do GoatCounter (`<img src=".../count?p=/meditacoes-biblicas/bem-aventurancas/<arquivo>">`): sem JavaScript e sem cookies. O valor de `p=` precisa bater com o caminho publicado da página.
- **Ao criar uma página nova, copie o pixel e troque o caminho em `p=`.** Se renomear/criar arquivo sem isso, ela não é contada.
- Abrir as páginas por `file://` também envia a visita (com o caminho fixo em `p=`). Visitas de teste podem ser apagadas em GoatCounter → Settings → Manage pageviews.

## Pendências e notas

- O dono ainda vai mandar mais anotações (fotos). Ele pede melhorias uma por vez e prefere ver o resultado no site para comentar depois.
- A "luz" (Mt 5:14–16) e a trilha (v.17–30) foram montadas a partir da foto da Bíblia dele (anotações dos v.16–30). Os versículos além dos anotados (Êx 25:31,37; Zc 4:2,6; Ap 1:12,13,20; Ap 2:5; Jo 8:12; Ef 5:8; Fp 2:15; Is 60:1,2; Jo 3:19,20; 1Jo 1:5–7; Pv 4:18,19; Tg 2:10; Mt 23:5,27,28; Mt 15:18,19; Tg 1:14,15; Mc 11:25; Mt 18:8,9; Jó 31:1) e os trechos de Ellen White (PP 247.3, PP 254.1 e MDC 39–62) foram escolhidos por mim; ele pode retirar o que não quiser.
- Sobre o "menor no reino dos céus" (v.19), a Ellen White diz: "Isto é, não terá lugar ali" (MDC 51.2).
- Pv 20:3 foi para a King James porque o dono leu o verso nela; se ele preferir ARC, volte o texto e o link.
- Os v.6 e v.7 ganharam versículos e trechos de Ellen White escolhidos a pedido do dono; ele pode retirar o que não quiser.

# Bem-aventuranças · Mateus 5 — site de estudo

Site estático (HTML + CSS puro) de estudo bíblico, projetado na igreja. Sem JavaScript, sem build. O dono pede melhorias uma por vez; responder sempre em português do Brasil.

## Arquivos

- `index.html` — mapa do estudo (um ramo por versículo/grupo), legenda dos cartões e o quadro "O que o conjunto mostra".
- `v03.html`, `v04-05.html`, `v06-08.html`, `v09.html`, `v10-12.html` — as bem-aventuranças.
- `v13-15.html` — "Sal e luz": o que fazem os bem-aventurados (fora das bem-aventuranças). No mapa é um cartão comum, clicável (sem pontilhado nem seta).
- `style.css` — único CSS. Fontes via `@import` do Google Fonts (Inter e Newsreader), com fallback do sistema.

## Estrutura do estudo

- As bem-aventuranças são Mt 5:3–12: oito (v.3–10); os v.11–12 ampliam a oitava, no mesmo tópico (`v10-12.html`).
- "Sal e luz" (v.13–15) é outra seção, fora das bem-aventuranças.
- O mapa usa âncoras: `#v3`, `#v4`, `#v5`, `#v6`, `#v7`, `#v8`, `#v9`, `#v10`, `#v13`. Cada `<section class="group" id="vN">` da página de detalhe tem o id correspondente.

## Barra do site (em TODAS as 8 páginas: o mapa, as 6 de detalhe e o `qr.html`)

- `<header class="site-bar">` logo depois de `<body>`, fora do `.wrap`: Meditações (`../`), Quem sou eu (`../quem-sou-eu/`) e Sobre (`../sobre/`). Serve para voltar ao site principal com um clique, de qualquer página.
- Só HTML e CSS (sem JavaScript). **Ao criar página nova, copie a barra.** Se as rotas do site principal mudarem, atualize os 3 links.
- Abrindo por `file://`, esses 3 links não funcionam (saem da pasta); no site publicado funcionam.

## Navegação (repetida em todas as páginas de detalhe)

- Topo: `<nav class="crumbs">` com o botão "← Mapa" e as 6 pílulas (v.3, v.4–5, v.6–8, v.9, v.10–12 e "Sal e luz · v.13–15"). A página atual leva `aria-current="page"`.
- Rodapé: `<nav class="pager">` com Anterior/Próxima. A primeira página volta ao Mapa; a última ("Sal e luz") tem "Voltar → Mapa".
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
- O selo `<span class="ver">King James</span>` entra no `<h3>` só dos cartões que não são ARC. Cartão sem selo = ARC.
- Versículos numerados dentro da citação: `<span class="n">12</span>`.
- Cartão cinza "Conclusão": sem citação; só o título e 1–3 frases (`<p>`), no máximo uma `p.obs` de ligação.
- As páginas de detalhe foram geradas por script a partir de uma lista de cartões. Para editar, mexa direto nos HTML (é o texto oficial).

## Conteúdo

- **O site é para o público.** Nunca descreva as marcas do dono (circulado, sublinhado, seta, margem, lápis, cores, "posição incerta", "leitura minha"). O dono explica as anotações na conversa e a conclusão vai para o site, já em linguagem para o público. Nada de "Sua nota".
- A Bíblia se explica sozinha: comentário mínimo. Conclusão só onde o dono pediu ou explicou o raciocínio; tom claro e direto. Se usar palavra difícil, repita ao lado com um sinônimo entre vírgulas (ex.: "usurpar, tomar à força").
- **Não invente referência.** Versículos extras (além dos que o dono anotou) só quando ele pedir; liste-os para ele na resposta.
- **Texto bíblico.** Padrão: ARC (Almeida Revista e Corrigida, © Sociedade Bíblica do Brasil). O dono lê a **King James** em português, que é a **BKJ** do bibliaonline (`https://www.bibliaonline.com.br/bkj/{livro}/{capitulo}/{versiculo}+`); use-a só onde ele pedir (hoje: Pv 16:32, 1Tm 3:6, 1Pe 4:14–18, 1Pe 4:15, Pv 18:8, Pv 20:3). O Sl 15 fica em ARC (preferência dele). Quando ele pedir outra passagem em King James, troque o texto, o selo e o link.
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

## QR Code

- **Cartão no mapa:** no canto superior direito do `index.html` há um cartão (`.qr-card`, no estilo dos outros cartões) com o QR em miniatura. Ele leva ao `qr.html`. No celular o cartão vem abaixo do texto de abertura.
- **`qr.html`:** só a barra do site, o QR e, embaixo, o título (que é link para o mapa) e o endereço. O QR ocupa a janela inteira **sem rolagem** (testado de 390px a 1920px). Para isso ele é posicionado de forma absoluta na área livre entre a barra e a legenda; não troque por `height: 100%` em flex/SVG, porque o Safari estoura a altura.
- **`qr.svg`:** a imagem do QR (usada no cartão e no `qr.html`). Aponta para a URL publicada do estudo. Foi gerada com a biblioteca npm `qrcode` (correção de erro Q, margem de 4 módulos) e conferida decodificando de volta para a URL. **Se a URL do estudo mudar, gere de novo.** (A regra é a URL não mudar.)
- O `qr.html` não tem o pixel de visitas de propósito: é só a tela de projeção.

## Contagem de visitas

- Cada página termina com um pixel do GoatCounter (`<img src=".../count?p=/meditacoes-biblicas/bem-aventurancas/<arquivo>">`): sem JavaScript e sem cookies. O valor de `p=` precisa bater com o caminho publicado da página.
- **Ao criar uma página nova, copie o pixel e troque o caminho em `p=`.** Se renomear/criar arquivo sem isso, ela não é contada.
- Abrir as páginas por `file://` também envia a visita (com o caminho fixo em `p=`). Visitas de teste podem ser apagadas em GoatCounter → Settings → Manage pageviews.

## Pendências e notas

- O dono ainda vai mandar mais anotações (fotos). Ele pede melhorias uma por vez e prefere ver o resultado no site para comentar depois.
- A "luz" (Mt 5:14–15) ainda não tem comentário; o dono vai detalhar.
- Pv 20:3 foi para a King James porque o dono leu o verso nela; se ele preferir ARC, volte o texto e o link.
- Os v.6 e v.7 ganharam versículos e trechos de Ellen White escolhidos a pedido do dono; ele pode retirar o que não quiser.

# Bem-aventuranças · Mateus 5 — site de estudo

Site estático (HTML + CSS puro) de estudo bíblico, projetado na igreja. Sem JavaScript, sem build. O dono pede melhorias uma por vez; responder sempre em português do Brasil.

## Arquivos

- `index.html` — mapa do estudo (um ramo por versículo/grupo), legenda das anotações e a seção "Padrões que você marcou".
- `v03.html`, `v04-05.html`, `v06-08.html`, `v09.html`, `v10-12.html` — as bem-aventuranças.
- `v13-15.html` — "Sal e luz", outro ensino (fora das bem-aventuranças).
- `style.css` — único CSS. Fontes via `@import` do Google Fonts (Inter e Newsreader), com fallback do sistema.

## Estrutura do estudo

- As bem-aventuranças são Mt 5:3–12: oito (v.3–10); os v.11–12 ampliam a oitava, no mesmo tópico (`v10-12.html`).
- "Sal e luz" (v.13–15) é outra seção, fora das bem-aventuranças.
- O mapa usa âncoras: `#v3`, `#v4`, `#v5`, `#v6`, `#v7`, `#v8`, `#v9`, `#v10`, `#v13`. Cada `<section class="group" id="vN">` da página de detalhe tem o id correspondente.

## Barra do site (em TODAS as 7 páginas, inclusive o mapa)

- `<header class="site-bar">` logo depois de `<body>`, fora do `.wrap`: Meditações (`../`), Quem sou eu (`../quem-sou-eu/`) e Sobre (`../sobre/`). Serve para voltar ao site principal com um clique, de qualquer página.
- Só HTML e CSS (sem JavaScript). **Ao criar página nova, copie a barra.** Se as rotas do site principal mudarem, atualize os 3 links.
- Abrindo por `file://`, esses 3 links não funcionam (saem da pasta); no site publicado funcionam.

## Navegação (repetida em todas as páginas de detalhe)

- Topo: `<nav class="crumbs">` com o botão "← Mapa" e as 6 pílulas (v.3, v.4–5, v.6–8, v.9, v.10–12 e "Sal e luz · v.13–15"). A página atual leva `aria-current="page"`.
- Rodapé: `<nav class="pager">` com Anterior/Próxima. A primeira página volta ao Mapa; a última ("Sal e luz") tem "Voltar → Mapa".
- **Ao criar ou renomear uma página, atualize TODAS** (pílulas de todas as páginas, pager das vizinhas, ramo no `index.html`).

## Card de anotação

```html
<article class="note blue|orange|green|gray">
  <span class="tag">Paralelo | Contraste | Exemplo | Sua nota</span>
  <h3>Livro por extenso + referência</h3>
  <blockquote class="text"><p>… <mark>parte que explica a bem-aventurança</mark> …</p></blockquote>
  <p class="obs">só marcas minhas ou leituras incertas</p>
  <a class="full" href="https://www.bibliaonline.com.br/arc/{livro}/{capitulo}/{versiculo}+" target="_blank" rel="noopener">Ler o texto completo na ARC ↗</a>
</article>
```

- Cores: azul = Paralelo, laranja = Contraste, verde = Exemplo, cinza = Sua nota.
- Exemplo de link: `https://www.bibliaonline.com.br/arc/tg/4/10+`.
- Versículos numerados dentro da citação: `<span class="n">12</span>`.

## Conteúdo

- A Bíblia se explica sozinha: comentário mínimo. Interpretação minha ou incerta leva "Leitura minha" (em `p.obs`).
- Só entram versículos que o dono anotou. **Não invente referência.**
- Texto bíblico: ARC (Almeida Revista e Corrigida, © Sociedade Bíblica do Brasil). Cite só o trecho-chave (até cerca de 125 caracteres por citação, com … nas omissões), nunca capítulos inteiros. Confira a redação exata em bibliaonline.com.br/arc antes de inserir, nunca de memória.

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

## QR Code em tela cheia

- `qr.html`: página só com o QR Code ocupando a tela (para projetar na igreja), com o título e o endereço embaixo. Aponta para a URL publicada do estudo. O mapa (`index.html`) tem o botão "QR Code em tela cheia" que leva a ela; o link de volta fica invisível e só aparece ao passar o mouse.
- O QR é um SVG embutido na própria página (sem JavaScript). Foi gerado com a biblioteca npm `qrcode` (correção de erro Q, margem de 4 módulos) e conferido decodificando de volta para a URL. **Se a URL do estudo mudar, gere o QR de novo.** (A regra é a URL não mudar.)
- A página não tem o pixel de visitas de propósito: é só a tela de projeção.

## Contagem de visitas

- Cada página termina com um pixel do GoatCounter (`<img src=".../count?p=/meditacoes-biblicas/bem-aventurancas/<arquivo>">`): sem JavaScript e sem cookies. O valor de `p=` precisa bater com o caminho publicado da página.
- **Ao criar uma página nova, copie o pixel e troque o caminho em `p=`.** Se renomear/criar arquivo sem isso, ela não é contada.
- Abrir as páginas por `file://` também envia a visita (com o caminho fixo em `p=`). Visitas de teste podem ser apagadas em GoatCounter → Settings → Manage pageviews.

## A conferir (conhecido, ainda não corrigido)

- `v06-08.html`, card "Isaías 14:12,13": o título diz 12,13, mas os trechos citados estão numerados 13 e 14. Conferir a referência certa em bibliaonline.com.br/arc antes de mexer.

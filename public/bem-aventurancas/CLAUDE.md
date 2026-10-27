# Sermão do Monte (Mt 5–7) — site de estudo

Site estático (HTML + CSS puro) de estudo bíblico, projetado na igreja. **O estudo é o Sermão do Monte (Mt 5:1 a 7:29), feito por partes e ainda incompleto.** O foco é o sermão; as bem-aventuranças são só a primeira parte (e a ilustração do caminho e das portas é delas). O que ainda não foi feito aparece, em cada lugar, com o selo **"A construir"** (não "em construção"): nos cartões de `index.html`, nos passos 5–8 de `depois.html` e na caixa do fim de `v27-30.html`. Na lista da home o título é "Sermão do Monte" e o versículo-chave "Mateus 5–7". A pasta e a URL continuam `bem-aventurancas` (a URL não muda). Sem JavaScript, sem build. O dono pede melhorias uma por vez; responder sempre em português do Brasil.

## Forma de trabalho: RASCUNHO primeiro, produção só quando o dono mandar

- **Toda mudança nova vai primeiro para o rascunho** (versão em desenvolvimento): pasta `public/bem-aventurancas/em-desenvolvimento-k7q2/` (cópia completa do estudo, sem link em lugar nenhum, `noindex`, com uma faixa laranja "VERSÃO EM DESENVOLVIMENTO" no rodapé da janela e o contador de visitas desligado). Endereço: `https://meditacoesbiblicas.github.io/meditacoes-biblicas/bem-aventurancas/em-desenvolvimento-k7q2/index.html`. O dono compara com a versão publicada (a faixa tem o link da página publicada equivalente).
- **Só publique na versão de verdade quando ele disser "coloca em produção".** Aí rode `python3 scripts/estudo/rascunho.py promover` (copia o rascunho para a versão publicada, desfazendo a forma de rascunho, e apaga da publicada o que saiu do rascunho), depois commit/push e confira ao vivo. `python3 scripts/estudo/rascunho.py criar` recria o rascunho a partir da publicada (**sobrescreve** o rascunho).
- **Geradores** (no repositório): `scripts/estudo/build_pages.py <pasta> [--rascunho]` (todas as páginas de detalhe e `depois.html`), `scripts/estudo/build_index.py <pasta> [--rascunho]` (`index.html`) e `scripts/estudo/verify.py <pasta>` (confere cada citação no bibliaonline e no site da Ellen White). Páginas feitas à mão (`caminho.html`, `caminho-ampliado.html`, `qr.html`, `style.css`, redirecionamentos) editam-se direto na pasta do rascunho.
- Depois de promover, a cópia offline também é atualizada (o hook de commit já faz isso).
- Não cite nem divulgue o endereço do rascunho em lugar público; só ao dono.
- **QUANDO O DONO MANDAR PUBLICAR (e só então), faça isto, nesta ordem** (combinado em 2026-10-26; o dono não gostou do endereço `em-desenvolvimento-k7q2` porque é difícil de lembrar):
  1. **Backup da versão publicada ANTES de promover:** copie a versão publicada atual (como está agora, sem as mudanças) para `public/bem-aventurancas-backup/` (endereço: `https://meditacoesbiblicas.github.io/meditacoes-biblicas/bem-aventurancas-backup/`), na forma de rascunho/backup (noindex, faixa de aviso "BACKUP da versão anterior", contador desligado). Pasta ao lado de `bem-aventurancas/`, não dentro dela.
  2. **Promova** o rascunho para a publicada (`rascunho.py promover`).
  3. **Troque o endereço do rascunho** de `bem-aventurancas/em-desenvolvimento-k7q2/` para `public/bem-aventurancas-desenvolvimento/` (endereço: `.../bem-aventurancas-desenvolvimento/`): o nome do original + `-desenvolvimento`. Ajuste o `rascunho.py` (pasta fora de `bem-aventurancas/`, links da barra do site voltam a ser `../`, link da faixa vira `../bem-aventurancas/<arquivo>`) e remova a pasta antiga.
  **Publicação PARCIAL (decisão do dono em 2026-10-26):** na publicada vão **só as bem-aventuranças e a conclusão**. Sal e luz, A lei, Raiva e Cobiça (já prontos no rascunho, mas que ele ainda não leu) ficam **"A construir" na publicada** e a trilha (`depois.html`, `v13-15`, `v17-20`, `v21-26`, `v27-30`) **não é publicada**; no rascunho continuam prontos. `rascunho.py promover` já faz isso (usa `--parcial` nos geradores; `--completo` publica tudo; `--destino DIR` faz um ensaio sem tocar na publicada). Quando o dono disser que leu uma dessas partes, tire-a de `EXCLUIR_PARCIAL` (e do ajuste parcial nos geradores) para ela ir à publicada.
  **O backup** guarda sempre a versão publicada de **antes** de cada nova publicação (é sobrescrito a cada publicação).
  4. Mande ao dono os dois links novos (desenvolvimento e backup) e atualize esta seção.
  Regra de nomes para qualquer versão futura: **original + `-desenvolvimento`** para o rascunho e **original + `-backup`** para o backup. **Não faça nada disso antes de ele pedir para publicar.**

## O que está SÓ NO RASCUNHO (ainda não publicado) — atualizado em 2026-10-26

Quando o dono mandar publicar, passe cada item para as seções certas deste arquivo e apague esta lista. Detalhes de cada um estão nos geradores (`scripts/estudo/`) e nos comentários dos HTML do rascunho.
- **Uma página por bem-aventurança** (`v03`, `v04`, `v05`, `v06`, `v07`, `v08`, `v09`, `v10-12`); `v04-05.html`, `v06-08.html` e `mapa.html` viram redirecionamentos; versículos em blocos com subtítulos, do mais simples ao mais difícil, com explicação ANTES do versículo (`<p class="antes">`); o **mapa foi removido**; botão "← Voltar à imagem das portas" no fim de cada porta.
- **`conclusao.html`**: conclusão de todas as bem-aventuranças (a moldura em forma de parênteses, "tudo nasce da humildade" com EGW MDC 13.2, tabela presente × futuro, o oposto Laodiceia). Só se chega a ela pelo fim da porta 8. Quando existir `conclusao.jpg` na pasta, o gerador a coloca no cabeçalho (o dono está gerando a imagem; o script dela foi entregue na conversa).
- **QR Code direto na ilustração:** `qr.svg` aponta para `.../bem-aventurancas/caminho-ampliado.html` (e não mais para `caminho.html`); `qr.html` mostra esse endereço. Gerador: `scripts/estudo/gerar_qr.mjs`. QRs antigos (para `caminho.html`) continuam funcionando.
- **A porta que se abre** (`caminho-ampliado.html`): ao abrir uma porta (clique no PC; 2º toque no celular), duas folhas giram, a luz divina enche a tela e só então carrega a página da bem-aventurança, que nasce da mesma luz (`html.entrando`, ligada por um script no `<head>` das páginas das portas e da conclusão, via `sessionStorage['porta-aberta']`). Web Animations API; ~1,6 s; clicar de novo pula; `prefers-reduced-motion` vai direto; trata o botão "voltar" do navegador (`pageshow`). As folhas/luz são CSS (`.porta-*`), posicionadas sobre o vão do arco a partir da área clicável (`.hot`): se a ilustração for trocada, ajuste as áreas (`.hot`) **e** os recuos do vão no script (0,19/0,20/0,62/0,76).
- **Sem redundância na página inicial:** o cartão das bem-aventuranças em `index.html` vai **direto** para `caminho-ampliado.html` (sem lista de portas nem segundo botão); o botão do topo da ilustração é só "← Sermão do Monte". No fim da porta 8 há um convite grande para `conclusao.html` (`.cc-convite`, com os parênteses e as seis luzes). Na conclusão os títulos **não têm número** (para não se confundir com as portas 1 a 8) e a seção "presente e futuro" saiu.
- `caminho-ampliado.html` ganhou o botão "Sermão do Monte" e **o contador de visitas** (é a entrada do QR); no celular a imagem abre centralizada nas portas.

## Arquivos (três níveis: o sermão → as partes → os detalhes)

- `index.html` — **página inicial = mapa do Sermão do Monte (Mt 5:1 a 7:29)**, por capítulos (Mateus 5, 6 e 7) e por partes. Cada parte é um cartão: **"Pronto"** (azul-marinho, abre a página) ou **"A construir"** (pontilhado, sem link). Tem a barra de progresso ("5 de 22 partes prontas"; o número sai do script `build_index.py`, não é manual). A parte das bem-aventuranças é um cartão em destaque com a ilustração. **Ao fazer uma parte nova: tire o "A construir" dela e ligue o cartão à página.** Esta é a URL que não pode mudar.
- `mapa.html` — **o mapa das bem-aventuranças** (Mt 5:3–12): a árvore com um ramo por versículo/grupo, a legenda dos cartões, o QR Code e o cartão "O caminho e as portas" no canto do cabeçalho, o quadro "O que as bem-aventuranças mostram" e o banner "Depois das bem-aventuranças" (leva à trilha). Botão "← Sermão do Monte" no topo. Antes isto era o `index.html`.
- `v03.html`, `v04-05.html`, `v06-08.html`, `v09.html`, `v10-12.html` — as bem-aventuranças (detalhe).
- `depois.html` — a **trilha "Depois das bem-aventuranças" (Mt 5:13–48)**: hero azul-marinho com o v.20 como fio, linha do tempo de 8 passos. Os passos 1–4 (sal e luz, a lei, raiva, cobiça) estão prontos e levam às páginas; os passos 5–8 (divórcio, juramentos, olho por olho, amor aos inimigos) estão "A construir". Cada passo pronto mostra "Por fora → Por dentro".
- `v13-15.html` — "Sal e luz" (v.13–16; o nome do arquivo é mantido por causa da URL): grupos `#v13` (sal) e `#v14` (luz: luz×trevas, boas obras e o candelabro/santuário).
- `v17-20.html` — a lei (v.17–19, grupo `#v17`) e a justiça que excede a dos escribas e fariseus (v.20, grupo `#v20`).
- `v21-26.html` — da morte à raiva (`#v21`) e reconciliar-se antes de oferecer (`#v23`).
- `v27-30.html` — do adultério à cobiça (`#v27`) e arrancar o olho/cortar a mão (`#v29`). No fim tem a caixa "A construir" (o restante, Mt 5:31 em diante).
- `caminho.html` — página de abertura da ilustração (é para onde o QR Code aponta) e `caminho-ampliado.html` — a imagem ampliada com as portas clicáveis; ver abaixo.
- `style.css` — único CSS. Fontes via `@import` do Google Fonts (Inter e Newsreader), com fallback do sistema.

## Estrutura do estudo

- **Numeração das portas (1 a 8):** v.3=1, v.4=2, v.5=3, v.6=4, v.7=5, v.8=6, v.9=7, v.10–12=8. Aparece nos ramos do mapa (`<b class="no">`), no cabeçalho de cada grupo ("Porta N · Mateus 5:x") e nas pílulas. Bate com a ilustração `caminho.html` (cada bem-aventurança é uma porta do caminho único; o juízo no fim). Ao criar grupo novo de bem-aventurança, atualize o `PORTA` do script e os ramos.
- **QR Code pequeno em mais lugares (`.qr-mini`):** além do cartão do `mapa.html`, há um QR minúsculo no canto inferior direito do cartão azul das bem-aventuranças em `index.html` e uma linha "QR Code desta página" no painel de `caminho.html`; todos abrem `qr.html` em tela cheia. (Se mudar o cartão azul, o QR não pode cobrir os rótulos das portas.)
- **Ilustração ampliada com portas clicáveis (`caminho-ampliado.html`) e "voltar para onde veio":** em `caminho.html` a imagem **não** tem áreas clicáveis (o painel ao lado já tem os links das portas); clicar nela abre `caminho-ampliado.html` (dica ao pousar o mouse: "Clique para ampliar e acessar cada porta"). A página ampliada mostra só a imagem na janela (sem legenda), com botão "← O caminho e as portas" e, em cada uma das 8 portas, uma área `<a class="hot">` posicionada em % sobre a imagem 3:2: ao pousar o mouse a porta acende e mostra "Porta N · nome". No celular a imagem fica na altura da tela e se arrasta para o lado, e as portas funcionam em **dois toques** (1º seleciona: acende e mostra o nome; 2º abre; tocar fora desfaz), por um pequeno script que só age em telas sem mouse (`hover: none`); no PC um clique abre. **Se a ilustração (`caminho.jpg`) for trocada, confira/refaça as posições** dessas áreas (`left/top/width/height` em % + `--rv`, o raio vertical do topo arredondado, para a seleção acompanhar o arco sem cortar o numeral; um overlay num recorte ampliado da imagem ajuda a calibrar). As páginas das bem-aventuranças (`v03`…`v10-12`) têm o botão `#voltar-origem` ("← Mapa das bem-aventuranças", "← O caminho e as portas" ou "← A ilustração das portas") e, no `v03`, o `#prev-origem` do rodapé: um pequeno script inline lê `sessionStorage['origem-bem-aventurancas']` (gravado por `index.html`/`mapa.html` = "mapa", `caminho.html` = "caminho", `caminho-ampliado.html` = "ampliada") e troca o destino. **É a única exceção à regra "sem JavaScript"**; sem o script (ou sem `sessionStorage`) o botão volta ao mapa.
- `caminho.html` (+ `caminho.jpg`, `caminho-mini.jpg`): **página de abertura, e é para onde o QR Code aponta** (pedido do dono: quem escaneia vê a ilustração, as 8 portas clicáveis — cada uma leva ao ramo da bem-aventurança — e o botão "Ver o mapa das bem-aventuranças →", que leva ao `mapa.html`). No PC: imagem grande à esquerda + painel azul-marinho com as portas à direita (no celular: imagem em cima e portas em pílulas; o celular é a referência de qualidade, o PC tem que ficar no mesmo nível). A imagem abre o `caminho.jpg` inteiro. Criada com IA (Gemini) a partir de roteiro do dono. **Tem o pixel de visitas** (é a entrada do QR). No `mapa.html` (PC), o cartão `.caminho-card` fica **ao lado do QR (QR à esquerda, caminho à direita), com a mesma largura e a mesma altura** (`.top-lado`, 2 colunas de 188px); no celular ficam empilhados; os dois abrem, respectivamente, `qr.html` e `caminho.html`. Link também no fim da trilha.

- As bem-aventuranças são Mt 5:3–12: oito (v.3–10); os v.11–12 ampliam a oitava, no mesmo tópico (`v10-12.html`).
- Depois delas vem a trilha (`depois.html`): Sal e luz (v.13–16) → A lei e a justiça maior (v.17–20) → Da morte à raiva (v.21–26) → Do adultério à cobiça (v.27–30). O fio é Mt 5:20: a justiça que excede a dos escribas e fariseus, "de fora para dentro" (a lei vista pelo ato × Jesus olhando o coração).
- O mapa das bem-aventuranças usa âncoras: `#v3`, `#v4`, `#v5`, `#v6`, `#v7`, `#v8`, `#v9`, `#v10`; a trilha usa `#v13`, `#v14`, `#v17`, `#v20`, `#v21`, `#v23`, `#v27`, `#v29`. Cada `<section class="group" id="vN">` da página de detalhe tem o id correspondente.

## Barra do site (em TODAS as páginas: o mapa, a trilha, as de detalhe e o `qr.html`)

- `<header class="site-bar">` logo depois de `<body>`, fora do `.wrap`: Meditações (`../`), Quem sou eu (`../quem-sou-eu/`) e Sobre (`../sobre/`). Serve para voltar ao site principal com um clique, de qualquer página.
- Só HTML e CSS (sem JavaScript). **Ao criar página nova, copie a barra.** Se as rotas do site principal mudarem, atualize os 3 links.
- Abrindo por `file://`, esses 3 links não funcionam (saem da pasta); no site publicado funcionam.

## Navegação (repetida em todas as páginas de detalhe)

- Topo: `<nav class="crumbs">` com o botão "← Sermão do Monte" (volta para `index.html`) e as pílulas: "Mapa" (`mapa.html`), 1 · v.3, v.4–5, v.6–8, v.9, v.10–12 e, separadas, "Trilha", "Sal e luz", "A lei", "Raiva" e "Cobiça". A página atual leva `aria-current="page"`.
- Rodapé: `<nav class="pager">` com Anterior/Próxima. A primeira página (`v03.html`) volta ao `mapa.html`; o fim da cadeia (`v27-30.html`) volta para a trilha (`depois.html`). A trilha em si não tem pager.
- **Ao criar ou renomear uma página, atualize TODAS** (pílulas de todas as páginas, pager das vizinhas, ramo no `mapa.html` e cartão no `index.html`).

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
- **Nenhuma referência bíblica fica solta no texto corrido** (conclusões, explicações, observações): o gerador (`refs_biblia` em `build_pages.py`) transforma cada "Sl 24:3,4", "Mt 23:25,26" em link (menções sem versículo, como "Salmo 15", ficam sem link, por pedido do dono) — para o cartão com o versículo, se ele está na mesma página (o cartão ganha moldura dourada ao chegar), ou, se não está, para o versículo na Bíblia Online (ARC, nova aba). Se escrever um texto novo, use as abreviações da tabela `ABREV` do script e rode o gerador.
- **No texto corrido não use siglas** (nada de "MDC 25.1"): escreva "O Maior Discurso de Cristo, p. 25.1"; o gerador faz isso sozinho e, se o cartão com o trecho está na mesma página, a menção vira link para ele (`id="egw-25-1"`). **Ao mencionar um versículo que não aparece na página, mostre um pedaço dele** (ex.: 1Tm 3:6, "ensoberbecendo-se, não caia na condenação do diabo") e não afirme mais do que o texto diz (1Tm 3:6 não diz que o orgulho derrubou o diabo; diz que o orgulho pode levar à mesma condenação).
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

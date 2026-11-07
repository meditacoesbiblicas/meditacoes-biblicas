# Estudo "Quanto custa?" — como funciona

Estudo em atos, na mesma família visual do Sermão do Monte (`scripts/estudo/`), mas com gerador próprio.

- **Desenvolvimento:** `public/quanto-custa-desenvolvimento/` (sem link em lugar nenhum, `noindex`, faixa laranja). A versão publicada será `public/quanto-custa/` (ainda não existe).
- **Gerar as páginas:** `python3 scripts/quanto-custa/build.py public/quanto-custa-desenvolvimento --rascunho`
  (sem `--rascunho` gera a forma publicada: sem faixa, sem `noindex`, com o contador de visitas ligado e o QR definitivo).
- **Arquivos:** `build.py` (páginas, textos e valores dos itens), `areas_ato1.py` (medidas das áreas clicáveis sobre `vitrine.jpg`),
  `conferir_areas.py` (desenha as áreas sobre a imagem para conferir), `gerar_qr.mjs` + `qr-*.svg` (QR Codes).
- **Imagem nova no Ato 1:** salve como `vitrine.jpg`, refaça as medidas em `areas_ato1.py` e confira com `conferir_areas.py`.
- **QR:** `qr-desenvolvimento.svg` abre o desenvolvimento (para testar no celular); `qr-producao.svg` abre o endereço definitivo.
  `build.py` copia o certo como `qr.svg`. **Ao publicar, o `qr.svg` do desenvolvimento NÃO pode ir para a pasta publicada.**
- **Valores e fontes:** todos os valores do Ato 1 foram conferidos nas fontes citadas em cada item (campo `conta`); quem atualizar um valor
  deve refazer a conta e a fonte no mesmo lugar.
- **Regras combinadas com o dono do site:** nada nas páginas (título, capa, meta description, navegação) pode adiantar o que vem nos atos
  seguintes; um ato por vez, o próximo só depois do teste e da confirmação do dono; este estudo não entra na lista de Meditações
  (`src/app/data/meditations.ts`) até ele mandar publicar.

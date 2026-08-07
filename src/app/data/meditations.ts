export type Meditacao = {
  id: string;
  titulo: string;
  versoChave: string;
  resumo: string;
  arquivoMd: string;
  referencias: string[];
  tema: string;
  data: string;
};

export const MEDITACOES: Meditacao[] = [
  {
    id: "quando-obedecer-a-deus-custa-a-aprovacao-de-alguem-que-amamos",
    data: "2026-08-07",
    tema: "Obediência a Deus",
    titulo: "⚔️ Quando Obedecer a Deus Custa a Aprovação de Alguém que Amamos",
    versoChave: "Atos 5:29",
    resumo: "Gideão nos ensina que honrar pai e mãe nunca significa participar do pecado deles.",
    arquivoMd: "quando-obedecer-a-deus-custa-a-aprovacao-de-alguem-que-amamos.md",
    referencias: ["At 5:29", "Êx 20:3", "Êx 20:12", "Jz 6:25", "Jz 6:31"]
  },

  {
    id: "o-poder-da-lingua-vida-ou-morte",
    data: "2026-01-05",
    tema: "Relacionamentos",
    titulo: "🗣️ O poder da língua: vida ou morte",
    versoChave: "Provérbios 18:21",
    resumo: "\"A morte e a vida estão no poder da língua; e aquele que a ama comerá do seu fruto.\"",
    arquivoMd: "o-poder-da-lingua-vida-ou-morte.md",
    referencias: ["Pv 18:21"]
  },

  {
    id: 'olhar-de-jesus',
    data: '2026-01-10',
    tema: 'Relacionamentos',
    titulo: '👁️  O olhar de Jesus',
    versoChave: 'Marcos 10:21',
    resumo: 'Jesus corrige com amor — e até o silêncio e o olhar podem restaurar.',
    arquivoMd: 'olhar-de-jesus.md',
    referencias: ['Mc 10:21', 'Lc 22:61']
  },
  {
    id: 'proposito-contra-ociosidade',
    data: '2026-01-13',
    tema: 'Disciplina',
    titulo: '🎯 Propósito contra a ociosidade',
    versoChave: '1 Timóteo 5:13–14',
    resumo: 'O propósito organiza a vida e protege o testemunho contra a ociosidade e a dispersão.',
    arquivoMd: 'proposito-contra-ociosidade.md',
    referencias: ['1Tm 5:13–14', 'Pv 10:4', 'Ef 5:16', 'Cl 2:8']
  },
  {
    id: 'ruins-suspeitas-devem-morrer',
    data: '2026-01-14',
    tema: 'Unidade',
    titulo: '🤝 Ruins suspeitas devem morrer',
    versoChave: '1 Timóteo 6:4',
    resumo: 'Discussões vazias alimentam suspeitas; Deus chama Seu povo à unidade e ao amor fraternal.',
    arquivoMd: 'ruins-suspeitas-devem-morrer.md',
    referencias: ['1Tm 6:3-6', '1Tm 6:9-10', '1Tm 6:20', 'Jo 15:8', 'Tg 5:16']
  },
  {
    id: "silencio-discernimento-jesus",
    data: "2026-01-17",
    tema: "Relacionamentos",
    titulo: "🛑 O silêncio que guarda o coração",
    versoChave: "Mateus 26:63",
    resumo: "Jesus ensina que o silêncio, em certos momentos, é um ato de fé e discernimento espiritual.",
    arquivoMd: "silencio-discernimento-jesus.md",
    referencias: ["Mt 26:63", "Mt 27:14", "Lc 23:9", "Pv 26:4-5", "Mc 4:34", "Jo 16:12", "Jo 2:24"]
  },
  {
    id: "disciplina-com-amor",
    data: "2026-01-23",
    tema: "Disciplina",
    titulo: "💪 Disciplina que sustenta a fé",
    versoChave: "1 Coríntios 9:27",
    resumo: "Disciplina é constância guiada por propósito e dependência de Deus, que fortalece a fé e organiza a vida.",
    arquivoMd: "disciplina-com-amor.md",
    referencias: ["1Co 9:27", "1Co 9:25", "Gl 6:9", "Pv 4:23"]
  },
  {
    id: "limites-e-paz-nos-relacionamentos",
    data: "2026-01-24",
    tema: "Relacionamentos",
    titulo: "🤝 Limites e paz nos relacionamentos",
    versoChave: "Romanos 12:18",
    resumo: "Buscar a paz inclui discernir limites quando a convivência contínua vira desgaste e contenda.",
    arquivoMd: "limites-e-paz-nos-relacionamentos.md",
    referencias: ["Rm 12:18", "Am 3:3", "Pv 22:3"]
  },
  {
    id: "a-morte-que-supreendeu-pilatos",
    data: "2026-01-28",
    tema: "Sacrifício e Redenção",
    titulo: "✝️ A morte que surpreendeu Pilatos",
    versoChave: "Marcos 15:44",
    resumo: "O espanto de Pilatos revela que a morte de Jesus na cruz não seguiu o padrão comum.",
    arquivoMd: "a-morte-que-supreendeu-pilatos.md",
    referencias: ["Mc 15:44", "Mc 15:37", "Jo 19:34"]
  },
  {
    id: "paz-e-verdade",
    data: "2026-01-30",
    tema: "Relacionamentos",
    titulo: "⚖️ Paz, verdade e responsabilidade cristã",
    versoChave: "Romanos 12:18",
    resumo: "Nem toda paz é virtude; às vezes, o amor à verdade exige posicionamento.",
    arquivoMd: "paz-e-verdade.md",
    referencias: ["Rm 12:18", "Mt 10:34", "Tg 4:17"]
  },
  {
    id: "submissao-e-testemunho-silencioso",
    data: "2026-02-11",
    tema: "Relacionamentos",
    titulo: "🤍 Submissão que Testemunha",
    versoChave: "1 Pedro 3:1",
    resumo: "Quando o diálogo não convence, o testemunho pode transformar.",
    arquivoMd: "submissao-e-testemunho-silencioso.md",
    referencias: ["1Pe 3:1-4", "Ef 5:25", "Rm 14:12"]
  },
  {
    id: "as-curas-o-monte-e-o-caminho-do-reino",
    data: "2026-02-12",
    tema: "Caminhada Cristã",
    titulo: "⛰️ As Curas, o Monte e o Caminho do Reino",
    versoChave: "Mateus 5:20",
    resumo: "Jesus cura a dor imediata e depois revela o caminho profundo do caráter do Reino.",
    arquivoMd: "as-curas-o-monte-o-caminho-do-reino.md",
    referencias: [
      "Mt 4:23-25",
      "Mt 5:3-12",
      "Mt 5:13-20",
      "Mt 5:21-28",
      "Mt 23:27",
      "Ap 3:17",
      "2Co 7:10",
      "Ez 9:4",
      "Sl 25:9",
      "Sl 149:4",
      "Jr 23:6",
      "1Co 1:30",
      "Jo 6:35",
      "1Tm 4:5"
    ]
  }
];
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
    id: 'olhar-de-jesus',
    data: '2026-01-10',
    tema: 'Comunicação',
    titulo: '🕊️ O olhar de Jesus',
    versoChave: 'Lucas 22:61',
    resumo: 'Jesus comunicava sem palavras — e o olhar dEle curava, não feriu.',
    arquivoMd: 'olhar-de-jesus.md',
    referencias: ['Lc 22:61']
  },
  {
    id: 'poder-da-lingua',
    data: '2026-01-03',
    tema: 'Comunicação',
    titulo: '🗣️ O poder da língua: vida ou morte',
    versoChave: 'Provérbios 18:21',
    resumo: '“A morte e a vida estão no poder da língua; e aquele que a ama comerá do seu fruto.”',
    arquivoMd: 'poder-da-lingua.md',
    referencias: ['Pv 18:21']
  },
  {
    id: 'da-escuridao-a-luz',
    data: '2025-12-27',
    tema: 'Crescimento Espiritual',
    titulo: '🌅 Da Escuridão à Luz — um caminho que se aprende a ver',
    versoChave: 'Provérbios 4:18',
    resumo: 'Deus revela Sua luz com misericórdia e justiça, de forma gradual, para nos conduzir à transformação completa.',
    arquivoMd: 'da-escuridao-a-luz.md',
    referencias: ['Pv 4:18']
  }
];
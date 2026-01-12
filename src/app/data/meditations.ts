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
    titulo: '👁️  O olhar de Jesus',
    versoChave: 'Marcos 10:21',
    resumo: 'Jesus corrige com amor — e até o silêncio e o olhar podem restaurar.',
    arquivoMd: 'olhar-de-jesus.md',
    referencias: ['Mc 10:21', 'Lc 22:61']
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
  }
];
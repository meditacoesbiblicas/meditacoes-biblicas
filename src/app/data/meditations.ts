export type Meditacao = {
  id: string;
  titulo: string;
  versoChave: string;
  resumo: string;
  corpo: string[];
  referencias: string[];
  fontes: { titulo: string; url: string }[];
};

export const MEDITACOES: Meditacao[] = [
  {
    id: 'pv-20-6',
    titulo: 'O fiel é raro',
    versoChave: 'Provérbios 20:6 (ARA)',
    resumo: 'Muitos falam de bondade; a fidelidade real é rara e comprovada no caráter.',
    corpo: [
      'Salomão contrasta autopromoção com constância verdadeira.',
      'A fidelidade se prova quando ninguém está vendo.'
    ],
    referencias: ['Pv 20:6'],
    fontes: [
      { titulo: 'Caminho a Cristo — “A Prova do Discipulado”', url: 'https://m.egwwritings.org/pt/book/129.277' },
      { titulo: 'Educação, p. 57', url: 'https://m.egwwritings.org/pt/book/143.326' }
    ]
  }
];
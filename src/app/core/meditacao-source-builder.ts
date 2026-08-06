export function slugify(titulo: string): string {
  return titulo
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\p{L}\p{N}]+/gu, '-')
    .toLowerCase()
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-');
}

// Mesmo regex de scripts/generate-build-data.mjs, aplicado ao conteúdo vindo da API
// (não ao bundle local, que pode estar desatualizado em relação ao main).
export function extractExistingIds(meditationsSrc: string): string[] {
  return [
    ...meditationsSrc.matchAll(/id:\s*["']([^"']+)["'][^}]*?arquivoMd:\s*["']([^"']+)["']/gs)
  ].map(([, id]) => id);
}

export interface NovaMeditacaoInput {
  id: string;
  data: string;
  tema: string;
  titulo: string;
  versoChave: string;
  resumo: string;
  arquivoMd: string;
  referencias: string[];
}

// JSON.stringify escapa aspas, barras invertidas, quebras de linha etc. de forma
// segura e produz uma string literal válida em TS.
export function buildMeditacaoLiteral(m: NovaMeditacaoInput): string {
  const refs = m.referencias.map(r => JSON.stringify(r)).join(', ');
  return `  {
    id: ${JSON.stringify(m.id)},
    data: ${JSON.stringify(m.data)},
    tema: ${JSON.stringify(m.tema)},
    titulo: ${JSON.stringify(m.titulo)},
    versoChave: ${JSON.stringify(m.versoChave)},
    resumo: ${JSON.stringify(m.resumo)},
    arquivoMd: ${JSON.stringify(m.arquivoMd)},
    referencias: [${refs}]
  },\n`;
}

// Insere logo após "MEDITACOES: Meditacao[] = [" — evita ter que localizar o "]" de
// fechamento do array (frágil por causa dos colchetes de `referencias`).
export function insertMeditacaoLiteral(meditationsSrc: string, literal: string): string {
  const marker = 'export const MEDITACOES: Meditacao[] = [';
  const idx = meditationsSrc.indexOf(marker);
  if (idx === -1) {
    throw new Error(
      'Não encontrei "export const MEDITACOES" em meditations.ts — abortando para não corromper o arquivo.'
    );
  }
  const insertAt = idx + marker.length;
  return meditationsSrc.slice(0, insertAt) + '\n' + literal + meditationsSrc.slice(insertAt);
}

const SECOES_ESPERADAS = [
  '## ✨ Meditação',
  '## 📖 Orientação',
  '## 🛠️ Aplicações práticas',
  '## 🙏 Oração final'
];

export function secoesFaltando(markdown: string): string[] {
  return SECOES_ESPERADAS.filter(s => !markdown.includes(s));
}

import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const meditationsFile = join(__dirname, '../src/app/data/meditations.ts');
const siteConfigFile = join(__dirname, '../src/app/core/site.config.ts');
const contentDir = join(__dirname, '../public/content');
const routesOutFile = join(__dirname, '../prerender-routes.txt');
const sitemapOutFile = join(__dirname, '../public/sitemap.xml');
const readingTimesOutFile = join(__dirname, '../src/app/data/reading-times.ts');

const meditationsSrc = readFileSync(meditationsFile, 'utf-8');

const meditacoes = [...meditationsSrc.matchAll(
  /id:\s*["']([^"']+)["'][^}]*?arquivoMd:\s*["']([^"']+)["']/gs
)].map(([, id, arquivoMd]) => ({ id, arquivoMd }));

if (meditacoes.length === 0) {
  throw new Error('Nenhuma meditação encontrada em meditations.ts — verifique o regex.');
}

// --- rotas para prerender + sitemap ---

const siteConfigSrc = readFileSync(siteConfigFile, 'utf-8');
const siteUrlMatch = siteConfigSrc.match(/SITE_URL\s*=\s*["']([^"']+)["']/);
if (!siteUrlMatch) {
  throw new Error('SITE_URL não encontrado em site.config.ts — verifique o regex.');
}
const siteUrl = siteUrlMatch[1];

const routes = ['/', '/sobre', '/quem-sou-eu', ...meditacoes.map(m => `/meditacao/${m.id}`)];

writeFileSync(routesOutFile, routes.join('\n') + '\n');
console.log(`prerender-routes.txt gerado com ${routes.length} rotas.`);

const urlEntries = routes
  .map(path => `  <url><loc>${siteUrl}${path === '/' ? '/' : path}</loc></url>`)
  .join('\n');

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urlEntries}\n</urlset>\n`;

writeFileSync(sitemapOutFile, sitemap);
console.log(`sitemap.xml gerado com ${routes.length} URLs.`);

// --- tempo de leitura (calculado a partir do markdown real) ---

const PALAVRAS_POR_MINUTO = 200;

function estimarMinutos(markdown) {
  const texto = markdown
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // links -> só o texto
    .replace(/^#{1,6}\s+/gm, '')             // headings
    .replace(/^>\s?/gm, '')                  // blockquote
    .replace(/[*_~`]/g, '')                  // ênfase/código
    .replace(/^[-•]\s+/gm, '')               // listas
    .replace(/^-{3,}\s*$/gm, '');            // hr

  const palavras = texto.split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(palavras / PALAVRAS_POR_MINUTO));
}

const tempos = {};
for (const { id, arquivoMd } of meditacoes) {
  const md = readFileSync(join(contentDir, arquivoMd), 'utf-8');
  tempos[id] = estimarMinutos(md);
}

const entradas = Object.entries(tempos)
  .map(([id, min]) => `  '${id}': ${min},`)
  .join('\n');

const readingTimesFile = `// Gerado automaticamente por scripts/generate-build-data.mjs — não editar manualmente.
export const TEMPOS_LEITURA: Record<string, number> = {
${entradas}
};
`;

writeFileSync(readingTimesOutFile, readingTimesFile);
console.log(`reading-times.ts gerado com ${meditacoes.length} entradas.`);

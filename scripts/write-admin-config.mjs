// Gera src/app/core/admin.config.ts a partir das variáveis de ambiente
// ADMIN_ROUTE_PATH e ADMIN_GATE_PASSWORD. Usado só no CI (o workflow de deploy
// injeta essas duas variáveis a partir de secrets do repositório) — localmente,
// cada dev mantém seu próprio admin.config.ts (fora do git, veja .gitignore).
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const outFile = join(__dirname, '../src/app/core/admin.config.ts');

const routePath = process.env.ADMIN_ROUTE_PATH;
const gatePassword = process.env.ADMIN_GATE_PASSWORD;

if (!routePath || !gatePassword) {
  throw new Error(
    'Secrets ADMIN_ROUTE_PATH e/ou ADMIN_GATE_PASSWORD não configurados no repositório ' +
      '(Settings → Secrets and variables → Actions).'
  );
}

const content = `// Gerado automaticamente em CI por scripts/write-admin-config.mjs — não editar manualmente.
export const ADMIN_ROUTE_PATH = ${JSON.stringify(routePath)};
export const ADMIN_GATE_PASSWORD = ${JSON.stringify(gatePassword)};

export const GITHUB_OWNER = 'meditacoesbiblicas';
export const GITHUB_REPO = 'meditacoes-biblicas';
export const GITHUB_BRANCH = 'main';

export const MEDITATIONS_TS_PATH = 'src/app/data/meditations.ts';
export const CONTENT_DIR = 'public/content';

export const LS_KEY_PAT = 'admin_gh_pat';
export const SS_KEY_GATE_OK = 'admin_gate_ok';
`;

writeFileSync(outFile, content);
console.log('admin.config.ts gerado a partir dos secrets do repositório.');

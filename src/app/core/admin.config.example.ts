// Template público — este arquivo VAI pro repositório (é seguro, não tem segredo real).
//
// Como usar:
// 1. Copie este arquivo para `admin.config.ts` (mesmo diretório) — esse nome está no
//    .gitignore e nunca será commitado, porque o repositório é público.
// 2. Preencha ADMIN_ROUTE_PATH e ADMIN_GATE_PASSWORD com valores só seus.
// 3. Configure os mesmos dois valores como secrets do repositório no GitHub
//    (Settings → Secrets and variables → Actions → New repository secret):
//    ADMIN_ROUTE_PATH e ADMIN_GATE_PASSWORD — o workflow de deploy usa esses
//    secrets para gerar este mesmo arquivo durante o build em produção.
//
// Lembrete de segurança: ADMIN_GATE_PASSWORD é só uma cortina de UX (fica visível
// em qualquer inspeção do bundle JS publicado). A segurança real da área de admin
// é o GitHub Personal Access Token, colado manualmente na tela e guardado só no
// localStorage do seu navegador — nunca em código.

export const ADMIN_ROUTE_PATH = 'troque-este-caminho';
export const ADMIN_GATE_PASSWORD = 'troque-esta-senha';

export const GITHUB_OWNER = 'meditacoesbiblicas';
export const GITHUB_REPO = 'meditacoes-biblicas';
export const GITHUB_BRANCH = 'main';

export const MEDITATIONS_TS_PATH = 'src/app/data/meditations.ts';
export const CONTENT_DIR = 'public/content';

export const LS_KEY_PAT = 'admin_gh_pat';
export const SS_KEY_GATE_OK = 'admin_gate_ok';

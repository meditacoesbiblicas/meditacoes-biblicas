import { RenderMode, ServerRoute } from '@angular/ssr';
import { MEDITACOES } from './data/meditations';

export const serverRoutes: ServerRoute[] = [
  {
    path: 'meditacao/:id',
    renderMode: RenderMode.Prerender,
    async getPrerenderParams() {
      return MEDITACOES.filter(m => !m.url).map(m => ({ id: m.id }));
    }
  },
  {
    path: '',
    renderMode: RenderMode.Prerender
  },
  {
    path: 'sobre',
    renderMode: RenderMode.Prerender
  },
  {
    path: 'quem-sou-eu',
    renderMode: RenderMode.Prerender
  },
  {
    // Rota curinga: qualquer caminho desconhecido cai no cliente
    // (o app redireciona para a home via app.routes.ts).
    path: '**',
    renderMode: RenderMode.Client
  }
];

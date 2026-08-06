import { Routes } from '@angular/router';
import { ADMIN_ROUTE_PATH } from './core/admin.config';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/home/home.page') },
  {
    path: 'meditacao/:id',
    loadComponent: () => import('./pages/meditacao/meditacao.page') },
  {
    path: 'sobre',
    loadComponent: () => import('./pages/sobre/sobre.page') },
  {
  path: 'quem-sou-eu',
  loadComponent: () => import('./pages/quem-sou-eu/quem-sou-eu.page')
  },
  {
    // Rota escondida (sem link em nenhum lugar do site) — NÃO adicionar em
    // app.routes.server.ts, para nunca ser prerenderizada/gerar HTML estático.
    path: ADMIN_ROUTE_PATH,
    loadComponent: () => import('./pages/admin/admin.page')
  },
  { path: '**', redirectTo: '' }

];
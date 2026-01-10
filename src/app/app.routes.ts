import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/home/home.page') },
  { path: 'meditacao/:id', loadComponent: () => import('./pages/meditacao/meditacao.page') },
  { path: '**', redirectTo: '' }
];
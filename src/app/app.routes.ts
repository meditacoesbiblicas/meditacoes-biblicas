import { Routes } from '@angular/router';

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
  { path: '**', redirectTo: '' }

];
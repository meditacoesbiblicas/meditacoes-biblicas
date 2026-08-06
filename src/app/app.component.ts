
import { Component, OnDestroy, inject, DOCUMENT } from '@angular/core';
import {
  NavigationStart,
  Router,
  RouterLink,
  RouterLinkActive,
  RouterOutlet,
} from '@angular/router';
import { filter, Subscription } from 'rxjs';
import { CookieConsentComponent } from './core/cookie-consent.component';
import { ADMIN_ROUTE_PATH } from './core/admin.config';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, CookieConsentComponent],
  templateUrl: './app.component.html',
})
export class AppComponent implements OnDestroy {
  private doc = inject(DOCUMENT);
  private baseHref = this.doc.querySelector('base')?.getAttribute('href') ?? '/';
  private routerSub: Subscription;

  menuAberto = false;

  private cliquesSegredo: number[] = [];
  private readonly JANELA_CLIQUES_MS = 1500;
  private readonly CLIQUES_NECESSARIOS = 3;

  constructor(private router: Router) {
    // Se navegar por routerLink (ou back/forward), fecha o menu mobile.
    this.routerSub = this.router.events
      .pipe(filter(e => e instanceof NavigationStart))
      .subscribe(() => this.fecharMenu());
  }

  ngOnDestroy() {
    this.routerSub.unsubscribe();
  }

  asset(path: string) {
    const base = this.baseHref.endsWith('/') ? this.baseHref : this.baseHref + '/';
    return base + path.replace(/^\//, '');
  }

  abrirMenu() {
    this.menuAberto = true;
    this.doc.body.style.overflow = 'hidden';
  }

  fecharMenu() {
    this.menuAberto = false;
    this.doc.body.style.overflow = '';
  }

  // 3 cliques seguidos na marca do site abrem a rota de admin — sem nenhum
  // link visível. Não substitui a segurança real (token do GitHub), é só
  // mais uma camada de obscuridade além de saber a URL direta.
  registrarCliqueSegredo(event: MouseEvent): void {
    const agora = Date.now();
    this.cliquesSegredo = this.cliquesSegredo.filter(
      t => agora - t < this.JANELA_CLIQUES_MS
    );
    this.cliquesSegredo.push(agora);

    if (this.cliquesSegredo.length >= this.CLIQUES_NECESSARIOS) {
      this.cliquesSegredo = [];
      event.preventDefault();
      event.stopPropagation();
      this.router.navigateByUrl('/' + ADMIN_ROUTE_PATH);
    }
  }
}
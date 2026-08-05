
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
}
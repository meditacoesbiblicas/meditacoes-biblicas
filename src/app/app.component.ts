import { AfterViewInit, Component, OnDestroy } from '@angular/core';
import {
  NavigationStart,
  Router,
  RouterLink,
  RouterLinkActive,
  RouterOutlet,
} from '@angular/router';
import { filter, Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.component.html',
})
export class AppComponent implements AfterViewInit, OnDestroy {
  private baseHref = document.querySelector('base')?.getAttribute('href') ?? '/';
  private routerSub?: Subscription;

  constructor(private router: Router) {}

  ngAfterViewInit() {
    // 1) Se navegar por routerLink, fecha o menu e limpa backdrop
    this.routerSub = this.router.events
      .pipe(filter(e => e instanceof NavigationStart))
      .subscribe(() => this.fecharMenuMobile());

    // 2) Defesa extra: quando o offcanvas fechar, garante que o backdrop some
    const menu = document.getElementById('menuMobile');
    menu?.addEventListener('hidden.bs.offcanvas', () => this.limparBackdropResidual());

    // Em alguns browsers o fade pode “prender” — esse timeout ajuda a garantir a remoção
    menu?.addEventListener('hide.bs.offcanvas', () => {
      setTimeout(() => this.limparBackdropResidual(), 0);
    });
  }

  ngOnDestroy() {
    this.routerSub?.unsubscribe();
  }

  asset(path: string) {
    const base = this.baseHref.endsWith('/') ? this.baseHref : this.baseHref + '/';
    return base + path.replace(/^\//, '');
  }

  private fecharMenuMobile() {
    const menu = document.getElementById('menuMobile');
    if (menu?.classList.contains('show')) {
      // fecha visualmente (Bootstrap também deve fechar, isso aqui é “cinto e suspensório”)
      menu.classList.remove('show');
      menu.setAttribute('aria-hidden', 'true');
    }
    this.limparBackdropResidual();
  }

  private limparBackdropResidual() {
    // remove apenas o backdrop do offcanvas (não mexe em modal)
    document.querySelectorAll('.offcanvas-backdrop').forEach(el => el.remove());

    // remove travas de scroll/padding que às vezes ficam presas
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
  }
}
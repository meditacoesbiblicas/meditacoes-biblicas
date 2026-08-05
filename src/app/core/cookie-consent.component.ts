import { DOCUMENT, isPlatformBrowser } from '@angular/common';
import { Component, PLATFORM_ID, inject } from '@angular/core';

const CHAVE_CONSENTIMENTO = 'consentimento-analytics';
const GA_ID = 'G-XSVCPQ5976';

@Component({
  selector: 'app-cookie-consent',
  standalone: true,
  template: `
    @if (mostrarBanner) {
      <div class="cookie-consent" role="dialog" aria-label="Consentimento de cookies">
        <p class="mb-2 mb-sm-0">
          Usamos cookies para estatísticas de uso (Google Analytics). Você aceita?
        </p>
        <div class="d-flex gap-2 flex-shrink-0">
          <button type="button" class="btn btn-sm btn-outline-secondary" (click)="recusar()">
            Recusar
          </button>
          <button type="button" class="btn btn-sm btn-primary" (click)="aceitar()">
            Aceitar
          </button>
        </div>
      </div>
    }
  `,
})
export class CookieConsentComponent {
  private isBrowser = isPlatformBrowser(inject(PLATFORM_ID));
  private doc = inject(DOCUMENT);

  mostrarBanner = false;

  constructor() {
    if (!this.isBrowser) {
      return;
    }

    const escolha = localStorage.getItem(CHAVE_CONSENTIMENTO);
    if (escolha === 'aceito') {
      this.carregarGoogleAnalytics();
    } else if (escolha !== 'recusado') {
      this.mostrarBanner = true;
    }
  }

  aceitar(): void {
    localStorage.setItem(CHAVE_CONSENTIMENTO, 'aceito');
    this.mostrarBanner = false;
    this.carregarGoogleAnalytics();
  }

  recusar(): void {
    localStorage.setItem(CHAVE_CONSENTIMENTO, 'recusado');
    this.mostrarBanner = false;
  }

  private carregarGoogleAnalytics(): void {
    if (this.doc.getElementById('ga-script')) {
      return;
    }

    const script = this.doc.createElement('script');
    script.id = 'ga-script';
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    this.doc.head.appendChild(script);

    const win = window as unknown as { dataLayer: unknown[]; gtag: (...args: unknown[]) => void };
    win.dataLayer = win.dataLayer || [];
    win.gtag = (...args: unknown[]) => win.dataLayer.push(args);
    win.gtag('js', new Date());
    win.gtag('config', GA_ID);
  }
}

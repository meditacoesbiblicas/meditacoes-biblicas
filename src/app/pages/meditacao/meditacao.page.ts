import { Component } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { HttpClient } from '@angular/common/http';

import { marked } from 'marked';
import { firstValueFrom } from 'rxjs';

import { MEDITACOES, Meditacao } from '../../data/meditations';

@Component({
  standalone: true,
  imports: [RouterLink],
  templateUrl: './meditacao.page.html'
})
export default class MeditacaoPage {
  id = '';
  m: Meditacao | null = null;
  html: SafeHtml = '';

  copiado = false;
  urlAtual = '';

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private sanitizer: DomSanitizer
  ) {
    this.route.paramMap.subscribe(pm => {
      this.id = pm.get('id') ?? '';
      this.m = MEDITACOES.find(x => x.id === this.id) ?? null;
      this.urlAtual = window.location.href;
      void this.loadMarkdown();
    });
  }

  private async loadMarkdown(): Promise<void> {
    const file = this.m?.arquivoMd ?? '';
    if (!file) {
      this.html = '';
      return;
    }

    const md = await firstValueFrom(
      this.http.get(`content/${file}`, { responseType: 'text' })
    );

    const parsed = await marked.parse(md ?? '');
    this.html = this.sanitizer.bypassSecurityTrustHtml(parsed);
  }

  async compartilhar(): Promise<void> {
    const url = this.urlAtual || window.location.href;
    const title = this.m?.titulo ?? 'Meditação';
    const text = this.m?.resumo ?? '';

    if (navigator.share) {
      try {
        await navigator.share({ title, text, url });
        return;
      } catch {
        // usuário pode cancelar; segue pro fallback
      }
    }

    await this.copiar(url);
    this.mostrarCopiado();
  }

  private async copiar(texto: string): Promise<void> {
    try {
      await navigator.clipboard.writeText(texto);
    } catch {
      const el = document.createElement('textarea');
      el.value = texto;
      el.style.position = 'fixed';
      el.style.opacity = '0';
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
    }
  }

  private mostrarCopiado(): void {
    this.copiado = true;
    window.setTimeout(() => (this.copiado = false), 2000);
  }
}
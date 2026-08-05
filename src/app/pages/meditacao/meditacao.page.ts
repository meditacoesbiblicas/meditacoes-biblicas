import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { HttpClient } from '@angular/common/http';

import { marked } from 'marked';
import { firstValueFrom } from 'rxjs';

import { MEDITACOES, Meditacao } from '../../data/meditations';
import { TEMPOS_LEITURA } from '../../data/reading-times';
import { SeoService } from '../../core/seo.service';
import { SITE_URL } from '../../core/site.config';

// mesma ordenação usada por padrão na home (mais recentes primeiro)
const MEDITACOES_POR_DATA = [...MEDITACOES].sort((a, b) => b.data.localeCompare(a.data));

@Component({
  standalone: true,
  imports: [RouterLink],
  templateUrl: './meditacao.page.html'
})
export default class MeditacaoPage {
  private seo = inject(SeoService);

  id = '';
  m: Meditacao | null = null;
  html: SafeHtml = '';
  carregando = true;
  tempoLeitura = 1;

  anterior: Meditacao | null = null;
  proxima: Meditacao | null = null;

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
      this.tempoLeitura = TEMPOS_LEITURA[this.id] ?? 1;
      this.urlAtual = `${SITE_URL}/meditacao/${this.id}`;

      const indice = MEDITACOES_POR_DATA.findIndex(x => x.id === this.id);
      // "anterior" = publicada mais recentemente; "próxima" = mais antiga
      this.anterior = indice > 0 ? MEDITACOES_POR_DATA[indice - 1] : null;
      this.proxima =
        indice >= 0 && indice < MEDITACOES_POR_DATA.length - 1
          ? MEDITACOES_POR_DATA[indice + 1]
          : null;

      if (this.m) {
        this.seo.set({
          title: this.m.titulo,
          description: this.m.resumo,
          path: `/meditacao/${this.m.id}`
        });
      } else {
        this.seo.set({
          title: 'Meditação não encontrada',
          description: 'Esta meditação não existe ou foi removida.',
          path: `/meditacao/${this.id}`
        });
      }

      void this.loadMarkdown();
    });
  }

  private async loadMarkdown(): Promise<void> {
    this.carregando = true;
    this.html = '';

    const file = this.m?.arquivoMd ?? '';
    if (!file) {
      this.carregando = false;
      return;
    }

    try {
      const md = await firstValueFrom(
        this.http.get(`content/${file}`, { responseType: 'text' })
      );

      const parsed = await marked.parse(md ?? '');
      this.html = this.sanitizer.bypassSecurityTrustHtml(parsed);
    } finally {
      this.carregando = false;
    }
  }

  formatarData(iso: string) {
    const [y, m, d] = iso.split('-');
    return `${d}/${m}/${y}`;
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
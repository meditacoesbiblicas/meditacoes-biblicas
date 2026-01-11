import { Component } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';

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

  constructor(private route: ActivatedRoute, private sanitizer: DomSanitizer) {
    this.route.paramMap.subscribe(pm => {
      this.id = pm.get('id') ?? '';
      this.m = MEDITACOES.find(x => x.id === this.id) ?? null;
      void this.renderMarkdown(); // chama async sem travar
    });
  }

  private async renderMarkdown(): Promise<void> {
    const md = this.m?.conteudoMd ?? '';

    // marked.parse pode retornar string OU Promise<string>
    const parsed = await marked.parse(md);

    this.html = this.sanitizer.bypassSecurityTrustHtml(parsed);
  }
}
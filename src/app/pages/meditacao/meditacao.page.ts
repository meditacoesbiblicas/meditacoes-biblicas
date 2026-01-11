import { Component } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';

import { MEDITACOES, Meditacao } from '../../data/meditations';
import { HttpClient } from '@angular/common/http';

import { firstValueFrom } from 'rxjs';


@Component({
  standalone: true,
  imports: [RouterLink],
  templateUrl: './meditacao.page.html'
})
export default class MeditacaoPage {
  id = '';
  m: Meditacao | null = null;
  html: SafeHtml = '';

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private sanitizer: DomSanitizer
  ) {
    this.route.paramMap.subscribe(pm => {
      this.id = pm.get('id') ?? '';
      this.m = MEDITACOES.find(x => x.id === this.id) ?? null;
      void this.loadMarkdown(); 
    });
  }

  private async loadMarkdown(): Promise<void> {
    const file = this.m?.arquivoMd ?? '';
    if (!file) { this.html = ''; return; }


    const md = await firstValueFrom(
      this.http.get(`content/${file}`, { responseType: 'text' })
    );

    const parsed = await marked.parse(md ?? '');
    this.html = this.sanitizer.bypassSecurityTrustHtml(parsed);
  }

}
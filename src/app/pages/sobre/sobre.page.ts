import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { SeoService } from '../../core/seo.service';

@Component({
  standalone: true,
  imports: [RouterLink],
  templateUrl: './sobre.page.html'
})
export default class SobrePage {
  private seo = inject(SeoService);

  constructor() {
    this.seo.set({
      title: 'Sobre',
      description: 'Um projeto simples para organizar e compartilhar meditações bíblicas curtas.',
      path: '/sobre'
    });
  }
}
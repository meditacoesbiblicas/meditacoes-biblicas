import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { SeoService } from '../../core/seo.service';

@Component({
  standalone: true,
  imports: [RouterLink],
  templateUrl: './quem-sou-eu.page.html'
})
export default class QuemSouEuPage {
  private seo = inject(SeoService);

  constructor() {
    this.seo.set({
      title: 'Quem sou eu',
      description: 'Um pouco sobre quem escreve estas meditações.',
      path: '/quem-sou-eu'
    });
  }
}
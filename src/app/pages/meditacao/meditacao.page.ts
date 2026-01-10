import { Component } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MEDITACOES } from '../../data/meditations';

@Component({
  standalone: true,
  imports: [RouterLink],
  templateUrl: './meditacao.page.html'
})
export default class MeditacaoPage {
  id = '';
  m = MEDITACOES[0];

  constructor(private route: ActivatedRoute) {
    this.id = this.route.snapshot.paramMap.get('id') ?? '';
    this.m = MEDITACOES.find(x => x.id === this.id) ?? MEDITACOES[0];
  }
}
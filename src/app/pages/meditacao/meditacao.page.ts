import { Component } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MEDITACOES } from '../../data/meditacoes';

@Component({
  standalone: true,
  imports: [RouterLink],
  templateUrl: './meditacao.page.html'
})
export default class MeditacaoPage {
  id = this.route.snapshot.paramMap.get('id') ?? '';
  m = MEDITACOES.find(x => x.id === this.id);

  constructor(private route: ActivatedRoute) {}
}
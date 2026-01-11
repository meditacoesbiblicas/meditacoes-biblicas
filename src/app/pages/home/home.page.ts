import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MEDITACOES } from '../../data/meditations';

@Component({
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './home.page.html'
})
export default class HomePage {
  meditacoes = [...MEDITACOES].sort((a, b) => b.data.localeCompare(a.data));

  temaSelecionado = 'Todos';

  get temas(): string[] {
    const lista = this.meditacoes.map(m => m.tema);
    return ['Todos', ...Array.from(new Set(lista)).sort()];
  }

  get meditacoesFiltradas() {
    if (this.temaSelecionado === 'Todos') return this.meditacoes;
    return this.meditacoes.filter(m => m.tema === this.temaSelecionado);
  }
}
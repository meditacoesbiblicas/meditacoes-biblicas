import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MEDITACOES } from '../../data/meditations';

type Ordem = 'recentes' | 'antigas' | 'tema';

@Component({
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './home.page.html'
})
export default class HomePage {
  // base (sempre ordenada por data desc)
  meditacoes = [...MEDITACOES].sort((a, b) => b.data.localeCompare(a.data));

  temaSelecionado = 'Todos';

  // NOVO: busca + ordenação
  termoBusca = '';
  ordem: Ordem = 'recentes';

  get temas(): string[] {
    const lista = this.meditacoes.map(m => m.tema);
    return ['Todos', ...Array.from(new Set(lista)).sort()];
  }

  // NOVO: contagem por tema (para chips)
  get contagemPorTema(): Partial<Record<string, number>> {
    const map: Record<string, number> = { Todos: this.meditacoes.length };
    for (const m of this.meditacoes) {
      map[m.tema] = (map[m.tema] ?? 0) + 1;
    }
    return map;
  }

  get meditacoesFiltradas() {
    const termo = this.normalizar(this.termoBusca);

    let lista = this.meditacoes;

    // filtro por tema
    if (this.temaSelecionado !== 'Todos') {
      lista = lista.filter(m => m.tema === this.temaSelecionado);
    }

    // filtro por busca (titulo, resumo, versoChave, tema, referencias)
    if (termo) {
      lista = lista.filter(m => {
        const hay = [
          m.titulo,
          m.resumo,
          m.versoChave,
          m.tema,
          ...(m.referencias ?? [])
        ]
          .join(' ')
          .toLowerCase();

        return this.normalizar(hay).includes(termo);
      });
    }

    // ordenação
    if (this.ordem === 'recentes') {
      lista = [...lista].sort((a, b) => b.data.localeCompare(a.data));
    } else if (this.ordem === 'antigas') {
      lista = [...lista].sort((a, b) => a.data.localeCompare(b.data));
    } else if (this.ordem === 'tema') {
      lista = [...lista].sort((a, b) => {
        const byTema = a.tema.localeCompare(b.tema);
        if (byTema !== 0) return byTema;
        return b.data.localeCompare(a.data);
      });
    }

    return lista;
  }

  formatarData(iso: string) {
    const [y, m, d] = iso.split('-');
    return `${d}/${m}/${y}`;
  }

  private normalizar(s: string): string {
    return (s ?? '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .trim();
  }

  filtrosAbertos = false;

  toggleFiltros() {
    this.filtrosAbertos = !this.filtrosAbertos;
  }
}
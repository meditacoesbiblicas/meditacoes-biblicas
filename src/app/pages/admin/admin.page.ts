import { Component, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { DomSanitizer, Meta, SafeHtml } from '@angular/platform-browser';
import { marked } from 'marked';

import {
  ADMIN_GATE_PASSWORD,
  CONTENT_DIR,
  GITHUB_OWNER,
  GITHUB_REPO,
  LS_KEY_GOATCOUNTER_TOKEN,
  LS_KEY_PAT,
  MEDITATIONS_TS_PATH,
  SS_KEY_GATE_OK
} from '../../core/admin.config';
import { GithubApiError, GithubContentApiService } from '../../core/github-content-api.service';
import {
  GoatCounterApiError,
  GoatCounterApiService,
  LocationStat,
  TotalStats
} from '../../core/goatcounter-api.service';
import {
  buildMeditacaoLiteral,
  extractExistingIds,
  insertMeditacaoLiteral,
  secoesFaltando,
  slugify
} from '../../core/meditacao-source-builder';
import { MEDITACOES } from '../../data/meditations';

type Estado = 'portao' | 'token' | 'form' | 'publicando' | 'sucesso' | 'erro';
type Secao = 'publicar' | 'estatisticas';
type EstadoEstatisticas = 'token' | 'carregando' | 'dados' | 'erro';

@Component({
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './admin.page.html'
})
export default class AdminPage {
  private isBrowser = isPlatformBrowser(inject(PLATFORM_ID));
  private github = inject(GithubContentApiService);
  private goatcounter = inject(GoatCounterApiService);
  private sanitizer = inject(DomSanitizer);
  private meta = inject(Meta);

  readonly githubActionsUrl = `https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}/actions`;
  readonly temasExistentes = Array.from(new Set(MEDITACOES.map(m => m.tema))).sort();

  estado: Estado = 'portao';
  secaoAtiva: Secao = 'publicar';

  gcEstado: EstadoEstatisticas = 'token';
  gcTokenInput = '';
  gcTotal: TotalStats | null = null;
  gcLocations: LocationStat[] = [];
  gcErro = '';
  readonly gcPeriodoDias = 30;

  senhaInput = '';
  senhaErro = '';

  patInput = '';

  titulo = '';
  versoChave = '';
  tema = '';
  data = new Date().toISOString().slice(0, 10);
  referenciasTexto = '';
  resumo = '';
  corpoMarkdown = '';
  slug = '';
  private slugEditadoManualmente = false;

  mostrarPreview = false;
  previewHtml: SafeHtml = '';
  avisoSecoes: string[] = [];

  errosValidacao: string[] = [];
  erroPublicacao = '';
  slugPublicado = '';

  constructor() {
    this.meta.addTag({ name: 'robots', content: 'noindex, nofollow' });

    if (this.isBrowser && sessionStorage.getItem(SS_KEY_GATE_OK) === '1') {
      this.avancarDoPortao();
    }
  }

  private avancarDoPortao(): void {
    this.estado = localStorage.getItem(LS_KEY_PAT) ? 'form' : 'token';
  }

  entrar(): void {
    if (this.senhaInput === ADMIN_GATE_PASSWORD) {
      sessionStorage.setItem(SS_KEY_GATE_OK, '1');
      this.senhaErro = '';
      this.avancarDoPortao();
    } else {
      this.senhaErro = 'Senha incorreta.';
    }
    this.senhaInput = '';
  }

  salvarToken(): void {
    const token = this.patInput.trim();
    if (!token) return;
    localStorage.setItem(LS_KEY_PAT, token);
    this.patInput = '';
    this.estado = 'form';
  }

  trocarToken(): void {
    localStorage.removeItem(LS_KEY_PAT);
    this.estado = 'token';
  }

  onTituloChange(): void {
    if (!this.slugEditadoManualmente) {
      this.slug = slugify(this.titulo);
    }
  }

  onSlugChange(): void {
    this.slugEditadoManualmente = true;
  }

  regenerarSlug(): void {
    this.slug = slugify(this.titulo);
    this.slugEditadoManualmente = false;
  }

  async atualizarPreview(): Promise<void> {
    const parsed = await marked.parse(this.corpoMarkdown || '');
    this.previewHtml = this.sanitizer.bypassSecurityTrustHtml(parsed);
    this.avisoSecoes = secoesFaltando(this.corpoMarkdown);
    this.mostrarPreview = true;
  }

  private referencias(): string[] {
    return this.referenciasTexto
      .split(',')
      .map(r => r.trim())
      .filter(Boolean);
  }

  private validar(): boolean {
    const erros: string[] = [];
    if (!this.titulo.trim()) erros.push('Título é obrigatório.');
    if (!this.versoChave.trim()) erros.push('Verso-chave é obrigatório.');
    if (!this.tema.trim()) erros.push('Tema é obrigatório.');
    if (!this.resumo.trim()) erros.push('Resumo é obrigatório.');
    if (!this.corpoMarkdown.trim()) erros.push('Corpo em markdown é obrigatório.');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(this.data)) erros.push('Data inválida.');
    if (!this.referencias().length) erros.push('Informe ao menos uma referência.');
    if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(this.slug)) {
      erros.push('Slug inválido (use letras minúsculas, números e hífen).');
    }
    this.errosValidacao = erros;
    return erros.length === 0;
  }

  async publicar(): Promise<void> {
    this.erroPublicacao = '';
    if (!this.validar()) return;

    this.estado = 'publicando';
    const arquivoMd = `${this.slug}.md`;
    const pathMd = `${CONTENT_DIR}/${arquivoMd}`;

    try {
      const existenteMd = await this.github.getFile(pathMd);
      await this.github.putFile(
        pathMd,
        this.corpoMarkdown,
        `conteúdo: adiciona meditação "${this.titulo}"`,
        existenteMd?.sha
      );
    } catch (e) {
      this.falhar(e, 'Falha ao criar o arquivo .md. Nada foi publicado. Tente novamente.');
      return;
    }

    try {
      const atual = await this.github.getFile(MEDITATIONS_TS_PATH);
      if (!atual) {
        throw new Error('meditations.ts não encontrado no repositório.');
      }

      const idsExistentes = extractExistingIds(atual.content);
      if (idsExistentes.includes(this.slug)) {
        this.erroPublicacao =
          `O arquivo "${arquivoMd}" foi criado/atualizado, mas o id "${this.slug}" já existe em meditations.ts. ` +
          'Troque o slug e clique em Publicar de novo — o .md já existente será apenas atualizado.';
        this.estado = 'erro';
        return;
      }

      const literal = buildMeditacaoLiteral({
        id: this.slug,
        data: this.data,
        tema: this.tema,
        titulo: this.titulo,
        versoChave: this.versoChave,
        resumo: this.resumo,
        arquivoMd,
        referencias: this.referencias()
      });
      const novoConteudo = insertMeditacaoLiteral(atual.content, literal);
      await this.github.putFile(
        MEDITATIONS_TS_PATH,
        novoConteudo,
        `feat: adiciona meditação "${this.titulo}" ao índice`,
        atual.sha
      );
    } catch (e) {
      this.falhar(
        e,
        `O arquivo "${arquivoMd}" foi criado, mas houve falha ao atualizar meditations.ts. ` +
          'O site ainda NÃO vai exibir essa meditação. Clique em Publicar de novo — ' +
          'o sistema vai detectar que o .md já existe e só tentará atualizar o índice desta vez.'
      );
      return;
    }

    this.slugPublicado = this.slug;
    this.estado = 'sucesso';
  }

  private falhar(e: unknown, mensagemBase: string): void {
    const detalhe = e instanceof GithubApiError ? ` (${e.status} — ${e.message})` : '';
    this.erroPublicacao = `${mensagemBase}${detalhe}`;
    this.estado = 'erro';
  }

  voltarParaForm(): void {
    this.estado = 'form';
  }

  publicarOutra(): void {
    this.titulo = '';
    this.versoChave = '';
    this.tema = '';
    this.data = new Date().toISOString().slice(0, 10);
    this.referenciasTexto = '';
    this.resumo = '';
    this.corpoMarkdown = '';
    this.slug = '';
    this.slugEditadoManualmente = false;
    this.mostrarPreview = false;
    this.errosValidacao = [];
    this.avisoSecoes = [];
    this.erroPublicacao = '';
    this.slugPublicado = '';
    this.estado = 'form';
  }

  selecionarSecao(secao: Secao): void {
    this.secaoAtiva = secao;
    if (secao === 'estatisticas') {
      if (this.isBrowser && localStorage.getItem(LS_KEY_GOATCOUNTER_TOKEN)) {
        void this.carregarEstatisticas();
      } else {
        this.gcEstado = 'token';
      }
    }
  }

  salvarTokenGoatCounter(): void {
    const token = this.gcTokenInput.trim();
    if (!token) return;
    localStorage.setItem(LS_KEY_GOATCOUNTER_TOKEN, token);
    this.gcTokenInput = '';
    void this.carregarEstatisticas();
  }

  trocarTokenGoatCounter(): void {
    localStorage.removeItem(LS_KEY_GOATCOUNTER_TOKEN);
    this.gcTotal = null;
    this.gcLocations = [];
    this.gcEstado = 'token';
  }

  async carregarEstatisticas(): Promise<void> {
    this.gcEstado = 'carregando';
    this.gcErro = '';

    const inicio = new Date(Date.now() - this.gcPeriodoDias * 24 * 60 * 60 * 1000)
      .toISOString()
      .slice(0, 10);

    try {
      const [total, locations] = await Promise.all([
        this.goatcounter.getTotal(inicio),
        this.goatcounter.getLocations(inicio)
      ]);
      this.gcTotal = total;
      this.gcLocations = locations;
      this.gcEstado = 'dados';
    } catch (e) {
      const detalhe = e instanceof GoatCounterApiError ? ` (${e.status} — ${e.message})` : '';
      this.gcErro = `Falha ao carregar estatísticas${detalhe}`;
      this.gcEstado = 'erro';
    }
  }
}

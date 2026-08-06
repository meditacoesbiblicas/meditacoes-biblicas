import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { GITHUB_BRANCH, GITHUB_OWNER, GITHUB_REPO, LS_KEY_PAT } from './admin.config';

export interface GithubFile {
  content: string;
  sha: string;
}

export class GithubApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

interface GithubContentsResponse {
  content: string;
  sha: string;
}

@Injectable({ providedIn: 'root' })
export class GithubContentApiService {
  private http = inject(HttpClient);
  private isBrowser = isPlatformBrowser(inject(PLATFORM_ID));

  private baseUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents`;

  private headers(): HttpHeaders {
    const token = this.isBrowser ? localStorage.getItem(LS_KEY_PAT) : null;
    if (!token) {
      throw new GithubApiError(0, 'Nenhum token do GitHub configurado.');
    }
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28'
    });
  }

  /** Retorna null se o arquivo não existir (404) — usado para decidir create vs update. */
  async getFile(path: string): Promise<GithubFile | null> {
    try {
      const res = await firstValueFrom(
        this.http.get<GithubContentsResponse>(`${this.baseUrl}/${path}?ref=${GITHUB_BRANCH}`, {
          headers: this.headers()
        })
      );
      return { content: base64ToUtf8(res.content), sha: res.sha };
    } catch (e) {
      if (e instanceof HttpErrorResponse) {
        if (e.status === 404) {
          return null;
        }
        throw new GithubApiError(e.status, e.error?.message ?? e.message);
      }
      throw e;
    }
  }

  async putFile(path: string, content: string, message: string, sha?: string): Promise<void> {
    try {
      await firstValueFrom(
        this.http.put(
          `${this.baseUrl}/${path}`,
          {
            message,
            content: utf8ToBase64(content),
            branch: GITHUB_BRANCH,
            ...(sha ? { sha } : {})
          },
          { headers: this.headers() }
        )
      );
    } catch (e) {
      if (e instanceof HttpErrorResponse) {
        throw new GithubApiError(e.status, e.error?.message ?? e.message);
      }
      throw e;
    }
  }
}

export function base64ToUtf8(b64: string): string {
  const binary = atob(b64.replace(/\n/g, ''));
  const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
  return new TextDecoder('utf-8').decode(bytes);
}

export function utf8ToBase64(str: string): string {
  const bytes = new TextEncoder().encode(str);
  let binary = '';
  bytes.forEach(b => (binary += String.fromCharCode(b)));
  return btoa(binary);
}

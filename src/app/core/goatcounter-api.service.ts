import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { GOATCOUNTER_SITE_CODE } from './site.config';
import { LS_KEY_GOATCOUNTER_TOKEN } from './admin.config';

export interface TotalStats {
  total: number;
  totalEvents: number;
}

export interface LocationStat {
  nome: string;
  contagem: number;
}

export class GoatCounterApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

interface ApiCountTotalResponse {
  total: number;
  total_events: number;
}

interface ApiStatsResponse {
  stats: { name: string; count: number }[];
  more: boolean;
}

@Injectable({ providedIn: 'root' })
export class GoatCounterApiService {
  private http = inject(HttpClient);
  private isBrowser = isPlatformBrowser(inject(PLATFORM_ID));

  private baseUrl = `https://${GOATCOUNTER_SITE_CODE}.goatcounter.com/api/v0`;

  private headers(): HttpHeaders {
    const token = this.isBrowser ? localStorage.getItem(LS_KEY_GOATCOUNTER_TOKEN) : null;
    if (!token) {
      throw new GoatCounterApiError(0, 'Nenhum token do GoatCounter configurado.');
    }
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  async getTotal(startIso: string): Promise<TotalStats> {
    try {
      const res = await firstValueFrom(
        this.http.get<ApiCountTotalResponse>(`${this.baseUrl}/stats/total`, {
          headers: this.headers(),
          params: { start: startIso }
        })
      );
      return { total: res.total, totalEvents: res.total_events };
    } catch (e) {
      throw this.normalizarErro(e);
    }
  }

  async getLocations(startIso: string): Promise<LocationStat[]> {
    try {
      const res = await firstValueFrom(
        this.http.get<ApiStatsResponse>(`${this.baseUrl}/stats/locations`, {
          headers: this.headers(),
          params: { start: startIso, limit: '20' }
        })
      );
      return res.stats.map(s => ({ nome: s.name, contagem: s.count }));
    } catch (e) {
      throw this.normalizarErro(e);
    }
  }

  private normalizarErro(e: unknown): GoatCounterApiError {
    if (e instanceof GoatCounterApiError) return e;
    if (e instanceof HttpErrorResponse) {
      return new GoatCounterApiError(e.status, e.error?.error ?? e.message);
    }
    return new GoatCounterApiError(0, String(e));
  }
}

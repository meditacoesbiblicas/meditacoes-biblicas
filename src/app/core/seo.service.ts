
import { Injectable, inject, DOCUMENT } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';
import { SITE_NAME, SITE_OG_IMAGE, SITE_URL } from './site.config';

export interface SeoData {
  /** Título da página, sem o sufixo do nome do site. */
  title: string;
  description: string;
  /** Caminho da rota, começando com "/" (ex.: "/", "/meditacao/olhar-de-jesus"). */
  path: string;
  image?: string;
}

@Injectable({ providedIn: 'root' })
export class SeoService {
  private meta = inject(Meta);
  private titleService = inject(Title);
  private doc = inject(DOCUMENT);

  set(data: SeoData): void {
    const fullTitle = data.title === SITE_NAME ? SITE_NAME : `${data.title} — ${SITE_NAME}`;
    const url = `${SITE_URL}${data.path}`;
    const image = data.image ?? SITE_OG_IMAGE;

    this.titleService.setTitle(fullTitle);

    this.setTag('description', data.description);
    this.setTag('og:type', 'website');
    this.setTag('og:site_name', SITE_NAME);
    this.setTag('og:title', fullTitle);
    this.setTag('og:description', data.description);
    this.setTag('og:url', url);
    this.setTag('og:image', image);
    this.setTag('twitter:card', 'summary_large_image');
    this.setTag('twitter:title', fullTitle);
    this.setTag('twitter:description', data.description);
    this.setTag('twitter:image', image);

    this.setCanonical(url);
  }

  private setTag(name: string, content: string): void {
    const attr: 'property' | 'name' = name.startsWith('og:') ? 'property' : 'name';
    const selector = `${attr}="${name}"`;

    if (this.meta.getTag(selector)) {
      this.meta.updateTag({ [attr]: name, content });
    } else {
      this.meta.addTag({ [attr]: name, content });
    }
  }

  private setCanonical(url: string): void {
    let link = this.doc.head.querySelector<HTMLLinkElement>('link[rel="canonical"]');
    if (!link) {
      link = this.doc.createElement('link');
      link.setAttribute('rel', 'canonical');
      this.doc.head.appendChild(link);
    }
    link.setAttribute('href', url);
  }
}

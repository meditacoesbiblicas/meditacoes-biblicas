// Gera o QR Code do estudo (matriz -> SVG) e prova que ele decodifica para a URL certa.
// O QR aponta para a ILUSTRAÇÃO ampliada (caminho-ampliado.html): quem escaneia já cai na imagem com as portas clicáveis.
// Uso (fora do repositório, numa pasta com as dependências):  npm i qrcode jsqr pngjs && node gerar_qr.mjs
// Saída: qr.svg ao lado do script; copie para public/bem-aventurancas/ (ou para a pasta do rascunho). Se a URL mudar, gere de novo.
// Gera o QR Code do estudo (matriz -> SVG) e prova que ele decodifica para a URL certa.
import QRCode from 'qrcode';
import jsQR from 'jsqr';
import { PNG } from 'pngjs';
import { writeFileSync } from 'node:fs';

const URL_ESTUDO = 'https://meditacoesbiblicas.github.io/meditacoes-biblicas/bem-aventurancas/caminho-ampliado.html';
const MARGEM = 4; // zona de silêncio exigida pelo padrão (em módulos)

const qr = QRCode.create(URL_ESTUDO, { errorCorrectionLevel: 'Q' });
const n = qr.modules.size;
const dados = qr.modules.data; // 1 = módulo escuro
const escuro = (x, y) => dados[y * n + x] === 1;

// ---- SVG: um segmento por sequência horizontal de módulos escuros ----
let caminho = '';
for (let y = 0; y < n; y++) {
  let x = 0;
  while (x < n) {
    if (!escuro(x, y)) { x++; continue; }
    let len = 0;
    while (x + len < n && escuro(x + len, y)) len++;
    caminho += `M${x + MARGEM} ${y + MARGEM}h${len}v1h-${len}z`;
    x += len;
  }
}
const lado = n + MARGEM * 2;
const svg = `<svg class="qr-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${lado} ${lado}" role="img" aria-label="QR Code que abre o estudo Bem-aventuranças · Mateus 5" shape-rendering="crispEdges"><rect width="${lado}" height="${lado}" fill="#fff"/><path fill="#000" d="${caminho}"/></svg>`;
writeFileSync(new URL('./qr.svg', import.meta.url), svg);

// ---- Prova: desenha a MESMA matriz num PNG e decodifica ----
const escala = 10;
const px = lado * escala;
const png = new PNG({ width: px, height: px });
for (let py = 0; py < px; py++) {
  for (let pxx = 0; pxx < px; pxx++) {
    const mx = Math.floor(pxx / escala) - MARGEM;
    const my = Math.floor(py / escala) - MARGEM;
    const preto = mx >= 0 && my >= 0 && mx < n && my < n && escuro(mx, my);
    const i = (py * px + pxx) * 4;
    png.data[i] = png.data[i + 1] = png.data[i + 2] = preto ? 0 : 255;
    png.data[i + 3] = 255;
  }
}
const lido = jsQR(new Uint8ClampedArray(png.data), px, px);
console.log('versão do QR:', qr.version, '| módulos:', n, '| lado c/ margem:', lado);
console.log('decodificado :', lido ? lido.data : '(FALHOU)');
console.log('confere      :', lido?.data === URL_ESTUDO ? 'SIM' : 'NÃO');

// Gera um QR Code (matriz -> SVG) e prova que ele decodifica para a URL certa.
// Uso (numa pasta com as dependências: npm i qrcode jsqr pngjs):
//   node gerar_qr.mjs <url> <saida.svg> "<texto alternativo>"
// Gerados para o estudo "Quanto custa?": qr-desenvolvimento.svg (abre o desenvolvimento, para testar no celular) e
// qr-producao.svg (abre o endereço definitivo, que só passa a existir depois da publicação). O build.py copia o certo como qr.svg.
import QRCode from 'qrcode';
import jsQR from 'jsqr';
import { PNG } from 'pngjs';
import { writeFileSync } from 'node:fs';

const [url, saida, alt] = process.argv.slice(2);
if (!url || !saida) { console.error('uso: node gerar_qr.mjs <url> <saida.svg> "<alt>"'); process.exit(1); }
const MARGEM = 4; // zona de silêncio exigida pelo padrão (em módulos)

const qr = QRCode.create(url, { errorCorrectionLevel: 'Q' });
const n = qr.modules.size;
const dados = qr.modules.data; // 1 = módulo escuro
const escuro = (x, y) => dados[y * n + x] === 1;

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
const svg = `<svg class="qr-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${lado} ${lado}" role="img" aria-label="${alt || 'QR Code'}" shape-rendering="crispEdges"><rect width="${lado}" height="${lado}" fill="#fff"/><path d="${caminho}" fill="#000"/></svg>\n`;
writeFileSync(saida, svg);

// Prova: desenha a MESMA matriz num PNG e decodifica
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
console.log('versão do QR:', qr.version, '| módulos:', n, '| arquivo:', saida);
console.log('decodificado :', lido ? lido.data : '(FALHOU)');
console.log('confere      :', lido?.data === url ? 'SIM' : 'NÃO');
if (lido?.data !== url) process.exit(2);

import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const leadHandler = require('../api/lead.js');

const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const port = Number(process.env.PORT || 4173);

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
  '.mp4': 'video/mp4',
  '.ico': 'image/x-icon'
};

function loadEnvFile(filePath) {
  return readFile(filePath, 'utf8')
    .then((text) => {
      text.split(/\r?\n/).forEach((line) => {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) return;
        const eq = trimmed.indexOf('=');
        if (eq < 1) return;
        const key = trimmed.slice(0, eq).trim();
        const value = trimmed.slice(eq + 1).trim();
        if (!process.env[key]) process.env[key] = value;
      });
    })
    .catch(() => {});
}

await loadEnvFile(join(root, '.env.local'));
await loadEnvFile(join(root, '.env'));

const server = createServer(async (req, res) => {
  const url = new URL(req.url || '/', `http://127.0.0.1:${port}`);

  if (url.pathname === '/api/lead') {
    await leadHandler(req, res);
    return;
  }

  let relative = decodeURIComponent(url.pathname);
  if (relative.endsWith('/')) relative += 'index.html';
  if (relative === '/') relative = '/index.html';

  const filePath = normalize(join(root, relative));
  if (!filePath.startsWith(root)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }

  try {
    const info = await stat(filePath);
    if (!info.isFile()) throw new Error('not a file');
    const body = await readFile(filePath);
    res.writeHead(200, { 'Content-Type': TYPES[extname(filePath)] || 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Not found');
  }
});

server.listen(port, () => {
  console.log(`CDF eval server: http://127.0.0.1:${port}/evaluation.html`);
});

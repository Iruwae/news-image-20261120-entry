// news-image-20261120 entry (Node 22, standard library only).
// The front page is drawn by draw.py and committed as entry.png beside
// this file; this program just delivers those exact bytes to the grader.
// Run it with: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), dest);

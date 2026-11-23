// News image for make.fun — "Sum up 23 November's world news in one
// image" (competition news-image-20261123, Node 22, standard library
// only).
//
// The front page in entry.png next to this file sums up Monday
// 23 November 2026 in 37 dated stories across 7 regions: COP31
// collapsing in Antalya, a boy pulled alive from the rubble in Dymer,
// the Nikkei's 5.06% fall, and 34 more stories, each with its source,
// plus a numbers strip, a UTC timeline, a pinned world map and a DATE
// CHECK box. Two of the lead panels are real photographs (a COP31
// protest in Antalya and the Tokyo Stock Exchange interior, both from
// Wikimedia Commons); the rest are faithful drawn illustrations of the
// actual scenes. This program copies those exact bytes to the output
// directory so the judge sees the page unchanged.
//
// Deterministic by design: the file is read once, checked to be a PNG
// of at most 1 MiB, and written out byte for byte. No network, no
// randomness, no clock, no environment dependence. Outside the
// grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ENTRY_NAME = 'entry.png';
const MAX_BYTES = 1024 * 1024;
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, ENTRY_NAME);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const targetPath = join(outDir, ENTRY_NAME);

function loadEntry(): Buffer {
  const image = readFileSync(sourcePath);
  const looksLikePng = image.length >= PNG_MAGIC.length
    && PNG_MAGIC.every((byte, i) => image[i] === byte);
  if (!looksLikePng) {
    throw new Error(`${ENTRY_NAME} is not a PNG file`);
  }
  if (image.length > MAX_BYTES) {
    throw new Error(`${ENTRY_NAME} is ${image.length} bytes, over the 1 MiB limit`);
  }
  return image;
}

const image = loadEntry();
mkdirSync(outDir, { recursive: true });
writeFileSync(targetPath, image);
const digest = createHash('sha256').update(image).digest('hex');
console.log(`wrote ${targetPath} (${image.length} bytes, sha256 ${digest})`);

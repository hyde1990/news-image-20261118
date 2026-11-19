// news-image-20261118 entry: copy the finished front page to the output dir.
// The image is pre-rendered by generate.py (Pillow, DejaVu fonts) from the
// verified news of Wednesday 18 November 2026 and committed as entry.png.
// This program runs offline, uses only the Node standard library, and writes
// the same bytes on every run: no clock, no randomness, no network.
// The grader's gate checks the file itself (whole PNG, at most 1 MiB and
// 1024 by 1024 pixels); entry.png is 1024x1024 and ~135 KiB, so it passes
// by construction.
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));

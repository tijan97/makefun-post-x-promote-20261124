// Post-x-promote entry (Node 22, standard library only).
//
// The entry is the X post itself: one post of the entrant's own on X that
// quotes make.fun's make-your-own-bounty post
// (https://x.com/makefunai/status/2124915864336236646) or links to it, with
// a photo of its own attached, make.fun or the @makefunai tag and the
// entrant's play code in its text. POST.json at the repository root names
// that post. This program copies POST.json to the output directory, where
// the gate reads it; nothing this program writes about the post is scored.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR: string = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR: string = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const sourcePath: string = join(BOT_DIR, "POST.json");
const raw: string = readFileSync(sourcePath, "utf8");
const post: unknown = JSON.parse(raw);

if (typeof post !== "object" || post === null || Array.isArray(post)) {
  throw new Error("POST.json must hold a JSON object naming the post");
}
const url: unknown = (post as { url?: unknown }).url;
if (typeof url !== "string" || url.length === 0) {
  throw new Error("POST.json must hold a non-empty string url");
}
try {
  new URL(url);
} catch {
  throw new Error("POST.json url must be a valid address");
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(join(OUTPUT_DIR, "POST.json"), raw, "utf8");
console.log(`POST.json copied to ${OUTPUT_DIR} (${url})`);

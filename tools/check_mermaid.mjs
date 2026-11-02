#!/usr/bin/env node
/**
 * Optional Mermaid validation: parses every ```mermaid block with the real
 * Mermaid parser (headless, via jsdom). Catches syntax errors that a structural
 * check cannot.
 *
 * Setup (in a scratch directory, outside the repository):
 *
 *   mkdir -p "$TMPDIR/mmcheck" && cd "$TMPDIR/mmcheck"
 *   npm init -y
 *   npm i mermaid@11 jsdom
 *
 * Usage:
 *
 *   node tools/check_mermaid.mjs . "$TMPDIR/mmcheck/node_modules"
 *
 * Exit code 1 when any diagram fails to parse.
 *
 * Why jsdom: Mermaid needs a DOM. A full browser render (mermaid-cli) is the
 * strongest check; this is the fastest reliable one and needs no browser binary.
 */
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const root = process.argv[2] ?? ".";
const modulesRoot = process.argv[3];

if (!modulesRoot) {
  console.error("usage: check_mermaid.mjs <docs-root> <node_modules-path>");
  process.exit(2);
}

const { JSDOM } = await import(pathToFileURL(path.join(modulesRoot, "jsdom", "lib", "api.js")).href);
const dom = new JSDOM("<!doctype html><html><body></body></html>", {
  pretendToBeVisual: true,
  url: "http://localhost/",
});

globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.DOMParser = dom.window.DOMParser;
globalThis.Element = dom.window.Element;
globalThis.HTMLElement = dom.window.HTMLElement;
globalThis.SVGElement = dom.window.SVGElement;
globalThis.Node = dom.window.Node;
globalThis.getComputedStyle = dom.window.getComputedStyle.bind(dom.window);

const mermaid = (
  await import(pathToFileURL(path.join(modulesRoot, "mermaid", "dist", "mermaid.core.mjs")).href)
).default;

mermaid.initialize({ startOnLoad: false, securityLevel: "loose" });

const EXCLUDED = new Set([
  ".git",
  ".github",
  "node_modules",
  "dist",
  "build",
  "target",
  "coverage",
  "__pycache__",
  ".venv",
  "venv",
]);

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (EXCLUDED.has(entry.name)) continue;
      walk(full, out);
    } else if (entry.name.endsWith(".md")) {
      out.push(full);
    }
  }
  return out;
}

function extractBlocks(file) {
  const lines = fs.readFileSync(file, "utf8").split("\n");
  const blocks = [];
  let inFence = false;
  let fence = "";
  let info = "";
  let buffer = [];
  let start = 0;

  for (let i = 0; i < lines.length; i += 1) {
    const match = lines[i].match(/^(`{3,}|~{3,})(.*)$/);
    if (match) {
      const token = match[1];
      if (!inFence) {
        inFence = true;
        fence = token;
        info = (match[2].trim().split(/\s+/)[0] || "").toLowerCase();
        buffer = [];
        start = i + 2;
      } else if (token[0] === fence[0] && token.length >= fence.length) {
        if (info === "mermaid") {
          blocks.push({ file, line: start, code: buffer.join("\n") });
        }
        inFence = false;
      }
      continue;
    }
    if (inFence) buffer.push(lines[i]);
  }
  return blocks;
}

const files = walk(root).sort();
const blocks = files.flatMap(extractBlocks);

let ok = 0;
const failures = [];

for (const block of blocks) {
  try {
    await mermaid.parse(block.code);
    ok += 1;
  } catch (error) {
    const message = error?.str ?? error?.message ?? String(error);
    failures.push({
      file: path.relative(root, block.file),
      line: block.line,
      error: String(message).replace(/\s+/g, " ").slice(0, 300),
    });
  }
}

for (const failure of failures) {
  console.error(`${failure.file}:${failure.line}: mermaid: ${failure.error}`);
}

console.log(
  `mermaid blocks=${blocks.length} parsed=${ok} failed=${failures.length} files=${files.length}`,
);

process.exit(failures.length ? 1 : 0);

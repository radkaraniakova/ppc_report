// Render SVG → PNG náhľady (Chromium cez Playwright).  node render.mjs [scale]
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "playwright");
import { readdirSync, readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const svgDir = resolve(here, "../svg");
const pngDir = resolve(here, "../png");
const scale = Number(process.argv[2] || 1.2);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1000, height: 1414 }, deviceScaleFactor: scale });
for (const f of readdirSync(svgDir).filter((f) => f.endsWith(".svg")).sort()) {
  const svg = readFileSync(resolve(svgDir, f), "utf8").replace(/width="297mm" height="420mm"/, 'width="1000" height="1414"');
  await page.setContent(`<html><body style="margin:0">${svg}</body></html>`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: resolve(pngDir, f.replace(".svg", ".png")), clip: { x: 0, y: 0, width: 1000, height: 1414 } });
  console.log("✓", f);
}
await browser.close();

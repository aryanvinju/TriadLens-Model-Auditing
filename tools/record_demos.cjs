// Record current working software; these are retrospective scope demonstrations.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const out = path.join(root, 'output', 'demo');
fs.mkdirSync(out, { recursive: true });
const base = process.env.DEMO_URL || 'http://127.0.0.1:5004';
async function record(browser, name, seconds, steps) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 }, recordVideo: { dir: out, size: { width: 1280, height: 720 } } });
  const page = await context.newPage();
  const started = Date.now();
  await page.goto(base);
  await page.locator('#health').filter({ hasText: 'Models ready' }).waitFor();
  await steps(page);
  await page.waitForTimeout(Math.max(0, seconds * 1000 - (Date.now() - started)));
  const video = page.video();
  await context.close();
  const source = await video.path();
  const target = path.join(out, name + '.webm');
  const ffmpeg = process.env.FFMPEG_PATH;
  if (!ffmpeg) throw new Error('Set FFMPEG_PATH to an installed ffmpeg executable.');
  const result = spawnSync(ffmpeg, ['-y','-i',source,'-t',String(seconds),'-c:v','copy',target], { encoding:'utf8' });
  if (result.status !== 0) throw new Error(result.stderr);
  console.log(target);
}
(async () => {
  const browser = await chromium.launch({ channel:'msedge' });
  try {
    if (!process.env.SKIP_SPRINT1) await record(browser, 'sprint1-scope-20261113', 60, async page => {
      await page.waitForTimeout(8000);
      await page.locator('#record-title').scrollIntoViewIfNeeded();
      await page.locator('#example').click();
      await page.locator('#flow-output').filter({ hasText:'Saved dataset label:' }).waitFor();
      await page.waitForTimeout(12000);
      await page.locator('select[name="model"]').selectOption('ML');
      await page.locator('#submit').click();
      await page.locator('#results').scrollIntoViewIfNeeded();
      await page.waitForTimeout(14000);
      await page.locator('#metrics-body').scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(out,'sprint1.png')});
    });
    await record(browser, 'sprint2-scope-20261113', 120, async page => {
      await page.waitForTimeout(12000);
      await page.locator('#slice-body').scrollIntoViewIfNeeded();
      await page.waitForTimeout(12000);
      await page.locator('#record-title').scrollIntoViewIfNeeded();
      await page.locator('#sample-kind').selectOption('disagreement');
      await page.locator('#example').click();
      await page.locator('#audit').filter({hasText:'Model labels disagree'}).waitFor();
      await page.locator('#results').scrollIntoViewIfNeeded();
      await page.waitForTimeout(20000);
      await page.locator('#sample-kind').selectOption('all_wrong');
      await page.locator('#example').click();
      await page.locator('#reference-check').waitFor({state:'visible'});
      await page.waitForTimeout(15000);
      await page.locator('#sensitivity').click();
      await page.locator('#sensitivity-summary').filter({hasText:'16 one-field changes tested'}).waitFor();
      await page.locator('#sensitivity-panel').scrollIntoViewIfNeeded();
      await page.waitForTimeout(15000);
      await page.locator('#session-body').scrollIntoViewIfNeeded();
      await page.waitForTimeout(15000);
      await page.locator('#metrics-body').scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(out,'sprint2.png')});
    });
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exit(1);});

const { test, expect } = require('playwright/test');

test('@full input, processing and output are visible for a held-out audit', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('#health')).toHaveText('Models ready');
  await expect(page.locator('#summary-disagreements')).toContainText('6 / 55');
  await expect(page.locator('#slice-body tr')).toHaveCount(4);

  await page.locator('#sample-kind').selectOption('disagreement');
  await page.getByRole('button', { name: 'Load random record' }).click();

  await expect(page.locator('#flow-input')).toContainText('15 survey fields');
  await expect(page.locator('#flow-processing')).toContainText('ran ML, DL, QML');
  await expect(page.locator('#flow-output')).toContainText('Saved dataset label:');
  await expect(page.locator('#audit')).toContainText('Model labels disagree');
  await expect(page.locator('#session-body tr')).toHaveCount(1);
  await page.getByRole('button', { name: 'Check one-field changes' }).click();
  await expect(page.locator('#sensitivity-summary')).toContainText('16 one-field changes tested');
  await page.screenshot({ path: 'test-results/input-processing-output.png', fullPage: true });
});

test('@full a missing required input blocks an audit before a request', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Run audit' }).click();
  await expect(page.locator('select[name="GENDER"]')).toBeFocused();
  await expect(page.locator('#flow-output')).toHaveText('No prediction yet.');
});

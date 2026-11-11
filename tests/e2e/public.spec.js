const { test, expect } = require('playwright/test');

const features = {
  GENDER: 'F', AGE: 52, SMOKING: 1, YELLOW_FINGERS: 1,
  ANXIETY: 1, PEER_PRESSURE: 1, 'CHRONIC DISEASE': 1,
  FATIGUE: 1, ALLERGY: 1, WHEEZING: 1, 'ALCOHOL CONSUMING': 1,
  COUGHING: 1, 'SHORTNESS OF BREATH': 1, 'SWALLOWING DIFFICULTY': 1,
  'CHEST PAIN': 1,
};

test('@public browser renders input to output using an explicit UI fixture', async ({ page }) => {
  await page.route('**/api/example?*', route => route.fulfill({
    json: { model: 'ALL', features, reference: { row_id: 101, actual_label: 'NO' }, sample_kind: 'any', source: 'test fixture' },
  }));
  await page.route('**/api/predict', route => {
    const request = route.request().postDataJSON();
    expect(request.model).toBe('ALL');
    expect(Object.keys(request.features)).toHaveLength(15);
    return route.fulfill({ json: {
      results: [
        { model: 'ML', label: 'NO', score: 0.2, score_type: 'class YES model score' },
        { model: 'DL', label: 'NO', score: 0.3, score_type: 'class YES model score' },
        { model: 'QML', label: 'YES', score: 0.4, score_type: 'SVM decision margin (not a probability)' },
      ],
      comparison: { unanimous: false, agreement_count: 2, majority_dataset_label: 'NO', review_flag: true, review_reasons: ['Model labels disagree'] },
      warnings: [],
    } });
  });

  await page.goto('/');
  await page.getByRole('button', { name: 'Load random record' }).click();
  await expect(page.locator('#flow-input')).toContainText('15 survey fields');
  await expect(page.locator('#flow-processing')).toContainText('ran ML, DL, QML');
  await expect(page.locator('#flow-output')).toContainText('ML: NO; DL: NO; QML: YES');
  await expect(page.locator('#reference-check')).toContainText('Saved label: NO');
  await page.screenshot({ path: 'test-results/input-processing-output-ci.png', fullPage: true });
});

const { defineConfig } = require('playwright/test');

const port = Number(process.env.TRIADLENS_TEST_PORT || 5010);

module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  use: {
    baseURL: `http://127.0.0.1:${port}`,
    browserName: 'chromium',
    ...(process.env.PLAYWRIGHT_USE_EDGE === '1' ? { channel: 'msedge' } : {}),
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  reporter: [['list'], ['html', { open: 'never' }]],
  webServer: {
    command: 'python app.py',
    url: `http://127.0.0.1:${port}/health/live`,
    env: { ...process.env, PORT: String(port), HOST: '127.0.0.1' },
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});

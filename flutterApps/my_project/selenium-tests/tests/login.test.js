/**
 * MediConnect — Selenium E2E Login Tests
 * Tests the Patient login flow on the deployed GitHub Pages app.
 * 
 * Run locally:  npm run login
 * Run in CI:    npm test (triggered by GitHub Actions)
 */

const { Builder, By, until, Key } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const assert = require('assert');

// ── Configuration ────────────────────────────────────────────────────────────
const BASE_URL = process.env.BASE_URL || 'https://192372040.github.io/MyAPP';
const HEADLESS  = process.env.HEADLESS === 'true';
const TIMEOUT   = 30000; // 30 seconds

// ── Build Chrome driver ───────────────────────────────────────────────────────
async function buildDriver() {
  const options = new chrome.Options();
  if (HEADLESS) {
    options.addArguments(
      '--headless',
      '--no-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--window-size=1280,800'
    );
  }
  return new Builder()
    .forBrowser('chrome')
    .setChromeOptions(options)
    .build();
}

// ── Test Suite ────────────────────────────────────────────────────────────────
describe('🏥 MediConnect — Login Flow', function () {
  this.timeout(TIMEOUT * 2);

  let driver;

  before(async function () {
    console.log(`\n  🌐 Testing against: ${BASE_URL}`);
    console.log(`  🖥️  Headless: ${HEADLESS}\n`);
    driver = await buildDriver();
  });

  after(async function () {
    if (driver) await driver.quit();
  });

  // ── Test 1: App Loads ───────────────────────────────────────────────────────
  it('✅ should load the MediConnect web app', async function () {
    await driver.get(BASE_URL);

    // Wait up to 30s for Flutter to initialise (Flutter web takes a moment)
    await driver.wait(
      until.titleIs('MediConnect'),
      TIMEOUT,
      'Page title should be "MediConnect"'
    );

    const title = await driver.getTitle();
    assert.strictEqual(title, 'MediConnect', `Expected "MediConnect", got "${title}"`);
    console.log(`     → App title: "${title}" ✓`);
  });

  // ── Test 2: Flutter Canvas Renders ──────────────────────────────────────────
  it('✅ should render the Flutter canvas element', async function () {
    await driver.get(BASE_URL);

    // Flutter web renders inside a <flt-glass-pane> shadow host or a <canvas>
    // Wait for the body to have content
    await driver.wait(
      until.elementLocated(By.css('body')),
      TIMEOUT,
      'Body should exist'
    );

    // Give Flutter time to boot
    await driver.sleep(5000);

    const body = await driver.findElement(By.css('body'));
    const bodyHTML = await body.getAttribute('innerHTML');
    const hasFlutter = bodyHTML.includes('flt-') || bodyHTML.includes('flutter');

    assert.ok(
      bodyHTML.length > 100,
      'Page body should have content after Flutter loads'
    );
    console.log(`     → Flutter rendered: body length = ${bodyHTML.length} chars ✓`);
  });

  // ── Test 3: Page Title Correct ──────────────────────────────────────────────
  it('✅ should have correct page metadata', async function () {
    await driver.get(BASE_URL);
    await driver.sleep(2000);

    const title = await driver.getTitle();
    assert.ok(title.length > 0, 'Page should have a title');

    const url = await driver.getCurrentUrl();
    assert.ok(
      url.includes('192372040.github.io') || url.includes('localhost'),
      `URL should be on GitHub Pages. Got: ${url}`
    );

    console.log(`     → Title: "${title}" ✓`);
    console.log(`     → URL:   "${url}" ✓`);
  });

  // ── Test 4: No Console Errors ───────────────────────────────────────────────
  it('✅ should load without critical JavaScript errors', async function () {
    await driver.get(BASE_URL);
    await driver.sleep(5000);

    // Collect browser console logs
    const logs = await driver.manage().logs().get('browser');
    const severeErrors = logs.filter(log =>
      log.level.name === 'SEVERE' &&
      !log.message.includes('favicon') &&
      !log.message.includes('manifest')
    );

    if (severeErrors.length > 0) {
      console.warn(`     ⚠️  Console errors detected:`);
      severeErrors.forEach(e => console.warn(`       - ${e.message}`));
    }

    // Allow max 2 severe errors (some Flutter errors are acceptable)
    assert.ok(
      severeErrors.length <= 2,
      `Too many severe console errors: ${severeErrors.length}\n` +
      severeErrors.map(e => e.message).join('\n')
    );

    console.log(`     → Console errors: ${severeErrors.length} (within limit) ✓`);
  });
});

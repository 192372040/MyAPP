/**
 * MediConnect — Selenium E2E Tests
 * Tests the live MediConnect web app on GitHub Pages.
 */

const { Builder, By, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const assert = require('assert');

const BASE_URL = process.env.BASE_URL || 'https://192372040.github.io/MyAPP';
const HEADLESS  = process.env.HEADLESS === 'true';
const TIMEOUT   = 25000;

async function buildDriver() {
  const options = new chrome.Options();
  if (HEADLESS) {
    options.addArguments(
      '--headless', '--no-sandbox',
      '--disable-dev-shm-usage', '--disable-gpu',
      '--window-size=1280,800'
    );
  }
  return new Builder().forBrowser('chrome').setChromeOptions(options).build();
}

describe('🏥 MediConnect — Website Tests', function () {
  this.timeout(60000);
  let driver;

  before(async function () {
    console.log(`\n  🌐 URL: ${BASE_URL}`);
    driver = await buildDriver();
  });

  after(async function () {
    if (driver) await driver.quit();
  });

  // ── Test 1: Page loads with correct title ─────────────────────
  it('✅ should load with title "MediConnect"', async function () {
    await driver.get(BASE_URL);
    await driver.wait(until.titleIs('MediConnect'), TIMEOUT,
      'Title should be "MediConnect"');
    const title = await driver.getTitle();
    assert.strictEqual(title, 'MediConnect');
    console.log(`     → Title: "${title}" ✓`);
  });

  // ── Test 2: Page has content ──────────────────────────────────
  it('✅ should render page content', async function () {
    await driver.get(BASE_URL);
    await driver.wait(until.elementLocated(By.css('body')), TIMEOUT);
    await driver.sleep(2000);
    const body = await driver.findElement(By.css('body'));
    const text = await body.getText();
    assert.ok(text.length > 50, 'Page should have visible text content');
    console.log(`     → Content length: ${text.length} chars ✓`);
  });

  // ── Test 3: Email input exists ────────────────────────────────
  it('✅ should have an email input field', async function () {
    await driver.get(BASE_URL);
    await driver.sleep(2000);
    const emailField = await driver.wait(
      until.elementLocated(By.id('email')), TIMEOUT,
      'Email input should exist'
    );
    const isDisplayed = await emailField.isDisplayed();
    assert.ok(isDisplayed, 'Email input should be visible');
    console.log(`     → Email field found and visible ✓`);
  });

  // ── Test 4: Login button exists ───────────────────────────────
  it('✅ should have a login button', async function () {
    await driver.get(BASE_URL);
    await driver.sleep(2000);
    const loginBtn = await driver.wait(
      until.elementLocated(By.id('login-button')), TIMEOUT,
      'Login button should exist'
    );
    const text = await loginBtn.getText();
    assert.ok(text.length > 0, 'Login button should have text');
    console.log(`     → Login button: "${text}" ✓`);
  });
});

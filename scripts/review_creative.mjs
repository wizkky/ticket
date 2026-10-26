/** Browser review of the creative ecosystem against the local production build.
 * Run from the repository root: node scripts/review_creative.mjs
 * Uses existing demo accounts; does not publish events or reset data.
 */
import { chromium } from "../apps/web/node_modules/@playwright/test/index.mjs";
import AxeBuilder from "../apps/web/node_modules/@axe-core/playwright/dist/index.mjs";
import fs from "node:fs/promises";
import assert from "node:assert/strict";

const base = "http://localhost:5173";
const credentials = JSON.parse(
  await fs.readFile(".local/demo-credentials.json", "utf8"),
);
const messages = JSON.parse(
  await fs.readFile("apps/web/messages/es.json", "utf8"),
);
const msg = (key) =>
  key.split(".").reduce((object, part) => object[part], messages);
const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_EXECUTABLE_PATH || "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
const checks = [],
  errors = [];
await fs.mkdir("docs/screenshots", { recursive: true });

function passed(name, extra = {}) {
  checks.push({ name, ...extra });
  console.log(name);
}
async function context(role) {
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    locale: "es-CL",
    timezoneId: "America/Santiago",
  });
  await ctx.addCookies([{ name: "PARAGLIDE_LOCALE", value: "es", url: base }]);
  const page = await ctx.newPage();
  page.on("pageerror", (error) =>
    errors.push({ role: role || "public", message: error.message }),
  );
  if (role) {
    await page.goto(base + "/login");
    await page.locator("[name=email]").fill(credentials[role].email);
    await page.locator("[name=password]").fill(credentials[role].password);
    await page.locator("button[type=submit]").click();
    await page.waitForURL("**/dashboard");
    await page
      .locator("header")
      .getByRole("link", { name: msg("creative.myCaudal"), exact: true })
      .waitFor();
  }
  return { ctx, page };
}
let lastVisit = 0;
async function visit(page, path) {
  // Public SSR loads fan out to several API calls. Respect the live 60/min limit.
  const pause = Math.max(0, 7000 - (Date.now() - lastVisit));
  if (pause) await page.waitForTimeout(pause);
  lastVisit = Date.now();
  const response = await page.goto(base + path);
  assert.equal(response.status(), 200, path);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(350);
  assert.equal(
    /emergia/i.test(await page.locator("body").innerText()),
    false,
    "Retired brand in visible text",
  );
  assert.equal(
    await page.locator('img[src*="emergia"],img[alt*="Emergia"]').count(),
    0,
  );
  assert.equal(await page.locator('a[href=""],a[href="#"]').count(), 0);
}
async function capture(
  page,
  name,
  path,
  sizes = [
    ["desktop", 1440, 1000],
    ["mobile", 390, 844],
  ],
) {
  await visit(page, path);
  for (const [size, width, height] of sizes) {
    await page.setViewportSize({ width, height });
    await page.waitForTimeout(200);
    assert.equal(
      await page.evaluate(
        () => document.documentElement.scrollWidth > innerWidth + 1,
      ),
      false,
      `${name}/${size}: horizontal overflow`,
    );
    await page.screenshot({
      path: `docs/screenshots/caudal-v4-${name}-${size}.png`,
      fullPage: true,
    });
    passed(`${name} ${size}: HTTP 200, no overflow or retired branding`);
  }
  await page.setViewportSize({ width: 1440, height: 1000 });
}
async function accessibility(page, name) {
  const result = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  const violations = result.violations.map((entry) => ({
    id: entry.id,
    impact: entry.impact,
    targets: entry.nodes.map((node) => node.target),
  }));
  checks.push({ name: "axe " + name, violations });
  assert.deepEqual(violations, [], `Accessibility violations: ${name}`);
}

try {
  const pub = await context();
  for (const [name, path] of [
    ["home", "/"],
    ["agenda", "/agenda"],
    ["comunidad", "/comunidad"],
    ["ecosistema", "/ecosistema"],
    ["catalogo", "/events"],
    ["tickets", "/tickets"],
  ]) {
    await capture(pub.page, name, path);
    await accessibility(pub.page, name + " desktop");
  }
  await visit(pub.page, "/");
  assert.match(await pub.page.title(), /Caudal Creativo/);
  assert.equal(
    await pub.page.locator('header img[alt="Caudal Creativo"]').count(),
    1,
  );
  await pub.page
    .locator("#activity-search")
    .fill("sin-resultados-creative-review");
  await pub.page.locator("form[role=search] button").click();
  await pub.page.waitForURL(/search=sin-resultados/);
  assert.equal(await pub.page.locator("main article").count(), 0);
  passed("Home search uses real discovery and its empty state");

  await visit(pub.page, "/events?category=oficios");
  await pub.page.locator(".categories a[aria-current=page]").waitFor();
  assert.match(
    await pub.page.locator("main").innerText(),
    /Aún no hay actividades publicadas en esta categoría/,
  );
  const calendarPending = pub.page.waitForResponse((response) =>
    response.url().includes("/api/events/calendar"),
  );
  await pub.page
    .getByRole("button", { name: msg("calendar.calendar_view"), exact: true })
    .click();
  const calendarResponse = await calendarPending;
  assert.equal(calendarResponse.status(), 200);
  assert.ok(
    new URL(calendarResponse.url()).searchParams
      .getAll("tags")
      .includes("taller"),
  );
  await pub.page.waitForURL(/viewMode=calendar/);
  assert.equal(new URL(pub.page.url()).searchParams.get("category"), "oficios");
  await pub.page.locator(".calendar-controls").waitFor();
  const beforeMonth = new URL(pub.page.url()).searchParams.get("month");
  await pub.page
    .locator(".calendar-controls")
    .getByRole("button", { name: msg("calendar.next"), exact: true })
    .click();
  await pub.page.waitForURL(
    (url) => url.searchParams.get("month") !== beforeMonth,
  );
  assert.equal(new URL(pub.page.url()).searchParams.get("category"), "oficios");
  passed(
    "Categories apply to real listing/calendar, remain in the URL and show honest empty states",
  );
  await pub.page.locator(".categories a").first().click();
  await pub.page.waitForURL((url) => !url.searchParams.has("category"));
  assert.equal(
    new URL(pub.page.url()).searchParams.get("viewMode"),
    "calendar",
  );
  passed("Clearing the category preserves calendar mode");

  await visit(pub.page, "/");
  await pub.page
    .locator("footer")
    .getByRole("button", { name: msg("caudal.pause"), exact: true })
    .click();
  await pub.page.reload();
  assert.equal(
    await pub.page.locator("html").getAttribute("data-caudal-motion"),
    "paused",
  );
  assert.equal(
    await pub.page
      .locator(".original-symbol")
      .evaluate((node) => getComputedStyle(node).animationPlayState),
    "paused",
  );
  passed("Motion preference persists and pauses the supplied symbol");

  await pub.page.setViewportSize({ width: 390, height: 844 });
  const toggle = pub.page.getByRole("button", {
    name: msg("nav.toggleMenu"),
    exact: true,
  });
  await toggle.click();
  const drawer = pub.page.getByRole("dialog", {
    name: msg("nav.mobileNavigation"),
    exact: true,
  });
  await drawer.waitFor();
  for (let i = 0; i < 14; i++) {
    await pub.page.keyboard.press("Tab");
    assert.equal(
      await drawer.evaluate((node) => node.contains(document.activeElement)),
      true,
    );
  }
  await pub.page.keyboard.press("Escape");
  assert.equal(
    await toggle.evaluate((node) => node === document.activeElement),
    true,
  );
  passed("Mobile menu: trapped focus, Escape and focus return");
  const theme = pub.page.getByRole("button", {
    name: msg("theme.toggleTheme"),
    exact: true,
  });
  await theme.click();
  await pub.page
    .getByRole("menuitemradio", { name: msg("theme.light"), exact: true })
    .click();
  await pub.page.reload();
  assert.equal(
    await pub.page
      .locator("html")
      .evaluate((node) => node.classList.contains("dark")),
    false,
  );
  await accessibility(pub.page, "home light mobile");
  await pub.page.screenshot({
    path: "docs/screenshots/caudal-v4-home-light-mobile.png",
    fullPage: true,
  });
  await pub.page.emulateMedia({ reducedMotion: "reduce" });
  await pub.page.reload();
  assert.equal(
    await pub.page
      .getByRole("button", { name: msg("caudal.reducedMotion"), exact: true })
      .first()
      .isDisabled(),
    true,
  );
  assert.equal(
    await pub.page
      .locator(".original-symbol")
      .evaluate((node) => getComputedStyle(node).animationName),
    "none",
  );
  passed("Light theme persists; reduced motion disables animation");

  for (const locale of ["es", "en", "de", "fr", "it", "pt"]) {
    await pub.ctx.addCookies([
      { name: "PARAGLIDE_LOCALE", value: locale, url: base },
    ]);
    await visit(pub.page, "/");
    for (const width of [320, 390, 768, 1024, 1280, 1440]) {
      await pub.page.setViewportSize({ width, height: 900 });
      await pub.page.waitForTimeout(150);
      assert.equal(
        await pub.page.evaluate(
          () => document.documentElement.scrollWidth > innerWidth + 1,
        ),
        false,
        `${locale}/${width}`,
      );
    }
  }
  passed(
    "Six languages, six viewport widths (320–1440 px): no horizontal overflow",
  );

  const buyer = await context("buyer");
  await capture(buyer.page, "mi-caudal", "/dashboard");
  await accessibility(buyer.page, "Mi Caudal");
  await visit(buyer.page, "/dashboard/tickets");
  assert.equal((await buyer.page.goto(base + "/administration")).status(), 403);
  passed("Buyer: existing login, account, tickets and administration denied");
  const producer = await context("producer_a");
  await capture(producer.page, "productor", "/org/caudal-demo-a/admin", [
    ["desktop", 1440, 1000],
    ["mobile", 390, 844],
  ]);
  await visit(
    producer.page,
    "/org/caudal-demo-a/admin/events/cafd0000-0000-4000-8000-000000000001/edit",
  );
  await visit(
    producer.page,
    "/org/caudal-demo-a/admin/events/cafd0000-0000-4000-8000-000000000001/door",
  );
  assert.equal(
    (await producer.page.goto(base + "/administration")).status(),
    403,
  );
  const other = await context("producer_b");
  assert.ok(
    [403, 404].includes(
      (await other.page.goto(base + "/org/caudal-demo-a/admin")).status(),
    ),
  );
  passed("Producer: management, editor, door and organization isolation");
  const admin = await context("admin");
  await visit(admin.page, "/administration");
  passed("Platform administrator retains protected workspace");
  assert.deepEqual(errors, [], "Browser JavaScript errors");
  console.log(JSON.stringify({ checks: checks.length, errors: errors.length }));
} finally {
  await fs.writeFile(
    ".local/creative-review.json",
    JSON.stringify({ checks, errors }, null, 2),
  );
  await browser.close();
}

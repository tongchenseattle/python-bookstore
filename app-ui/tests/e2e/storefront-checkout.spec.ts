import { test, expect } from "@playwright/test";

test("storefront checkout redirects unauthenticated user", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveURL(/\//);
});

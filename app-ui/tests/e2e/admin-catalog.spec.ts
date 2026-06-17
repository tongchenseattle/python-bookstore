import { test, expect } from "@playwright/test";

test("admin catalog auth flow", async ({ page }) => {
  await page.goto("/admin/sign-in");
  await expect(page).toHaveURL(/admin\/sign-in/);
});

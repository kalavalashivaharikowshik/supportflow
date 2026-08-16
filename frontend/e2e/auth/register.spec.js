import {
  expect,
  test,
} from "@playwright/test";


test(
  "new requester can register",
  async ({ page }) => {
    const uniqueEmail =

      `requester-${Date.now()}@example.com`;

    await page.goto(
      "/register"
    );

    await page
      .getByLabel("Full name")
      .fill(
        "Playwright Requester"
      );

    await page
      .getByLabel("Email")
      .fill(
        uniqueEmail
      );

    await page
      .getByLabel(
        "Password",
        {
          exact: true,
        }
      )
      .fill(
        "Requester@123"
      );

    await page
      .getByLabel(
        "Confirm password"
      )
      .fill(
        "Requester@123"
      );

    await page
      .getByRole(
        "button",
        {
          name:
            "Create account",
        }
      )
      .click();

    await expect(
      page
    ).toHaveURL(
      /\/login$/
    );

    await expect(
      page.getByRole(
        "heading",
        {
          name:
            "Welcome back",
        }
      )
    ).toBeVisible();
  }
);
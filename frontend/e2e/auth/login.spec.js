import {
  expect,
  test,
} from "@playwright/test";

import {
  E2E_USERS,
} from "../utils/testUsers";

import {
  loginAs,
} from "../utils/auth";


test(
  "requester can log in",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.requester
    );

    await expect(
      page
    ).toHaveURL(
      /\/requester$/
    );

    await expect(
      page.getByRole(
        "heading",
        {
          name:
            "Requester Dashboard",
        }
      )
    ).toBeVisible();
  }
);

test(
  "invalid password shows login error",
  async ({ page }) => {
    await page.goto(
      "/login"
    );

    await page
      .getByLabel("Email")
      .fill(
        E2E_USERS
          .requester
          .email
      );

    await page
      .getByLabel("Password")
      .fill(
        "WrongPassword123"
      );

    await page
      .getByRole(
        "button",
        {
          name: "Sign in",
        }
      )
      .click();

    await expect(
      page
    ).toHaveURL(
      /\/login$/
    );

    await expect(
      page.getByText(
        /invalid|incorrect|unauthorized|credentials/i
      )
    ).toBeVisible();
  }
);
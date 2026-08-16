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
  "requester can create a critical ticket",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.requester
    );

    await page.goto(
      "/requester/tickets/create"
    );

    await page
      .getByLabel("Title")
      .fill(
        "Production API unavailable"
      );

    await page
      .getByLabel(
        "Description"
      )
      .fill(
        "Production API requests are failing for all customers."
      );

    await page
      .getByLabel(
        "Category"
      )
      .selectOption(
        "TECHNICAL"
      );

    await page
      .getByLabel(
        "Priority"
      )
      .selectOption(
        "CRITICAL"
      );

    await page
      .getByRole(
        "button",
        {
          name:
            "Create ticket",
        }
      )
      .click();

    await expect(
      page
    ).toHaveURL(
      /\/tickets\/\d+$/
    );

    await expect(
      page.getByRole(
        "heading",
        {
          name:
            "Production API unavailable",
        }
      )
    ).toBeVisible();

    await expect(
      page.getByText(
        "Critical",
        {
          exact: true,
        }
      )
    ).toBeVisible();

    await expect(
      page.getByText(
        "Open",
        {
          exact: true,
        }
      )
    ).toBeVisible();
  }
);
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
  "requester can search and filter own tickets",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.requester
    );

    await page.goto(
      "/requester/tickets"
    );

    await expect(
      page.getByRole(
        "heading",
        {
          name: "My Tickets",
        }
      )
    ).toBeVisible();

    const searchBox =
      page.getByRole(
        "searchbox"
      );

    await searchBox.fill(
      "Production API unavailable"
    );

    await expect(
      page.getByText(
        "Production API unavailable",
        {
          exact: true,
        }
      ).first()
    ).toBeVisible();

    const selects =
      page.locator("select");

    const prioritySelect =
      selects.nth(0);

    await prioritySelect
      .selectOption(
        "CRITICAL"
      );

    await expect(
      prioritySelect
    ).toHaveValue(
      "CRITICAL"
    );

    await expect(
      page.getByText(
        "Production API unavailable",
        {
          exact: true,
        }
      ).first()
    ).toBeVisible();
  }
);
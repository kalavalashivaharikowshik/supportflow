import {
  expect,
  test,
} from "@playwright/test";

import {
  E2E_USERS,
} from "../utils/testUsers";

import {
  loginAs,
  logout,
} from "../utils/auth";


test(
  "admin can assign requester ticket to agent",
  async ({ page }) => {
    const ticketTitle =
      `Assignment E2E ${Date.now()}`;

    await loginAs(
      page,
      E2E_USERS.requester
    );

    await page.goto(
      "/requester/tickets/create"
    );

    await page
      .getByLabel("Title")
      .fill(ticketTitle);

    await page
      .getByLabel("Description")
      .fill(
        "This ticket is created to verify Admin assignment through Playwright."
      );

    await page
      .getByLabel("Category")
      .selectOption(
        "TECHNICAL"
      );

    await page
      .getByLabel("Priority")
      .selectOption(
        "HIGH"
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

    const ticketUrl =
      page.url();

    await expect(
      page.getByRole(
        "heading",
        {
          name:
            ticketTitle,
        }
      )
    ).toBeVisible();

    await logout(page);

    await loginAs(
      page,
      E2E_USERS.admin
    );

    await page.goto(
    ticketUrl
    );

    await page.goto(
      ticketUrl
    );

    await expect(
      page.getByRole(
        "heading",
        {
          name:
            ticketTitle,
        }
      )
    ).toBeVisible();

    const adminActions =
    page
        .getByRole(
        "heading",
        {
            name: "Admin Actions",
        }
        )
        .locator("..");

    const agentSelect =
    adminActions
        .getByRole(
        "combobox"
        )
        .first();

    await expect(
    agentSelect
    ).toBeVisible();

    const agentOption =
    agentSelect
        .locator("option")
        .filter({
        hasText:
            E2E_USERS.agent.email,
        });

    await expect(
    agentOption
    ).toHaveCount(1);

    const agentValue =
    await agentOption
        .getAttribute("value");

    expect(
    agentValue
    ).toBeTruthy();

    await agentSelect
    .selectOption(
        agentValue
    );

    await page
      .getByRole(
        "button",
        {
          name:
            "Assign Ticket",
        }
      )
      .click();

    await expect(
      page.getByText(
        "Assigned",
        {
          exact: true,
        }
      )
    ).toBeVisible();
  }
);
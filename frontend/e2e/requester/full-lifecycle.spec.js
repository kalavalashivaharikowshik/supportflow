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
  "complete support ticket lifecycle works end to end",
  async ({ page }) => {
    const ticketTitle =
      `Full Lifecycle E2E ${Date.now()}`;

    const agentResponse =
      `Agent public response ${Date.now()}`;

    const resolutionSummary =
      `Issue resolved successfully ${Date.now()}`;


    // 1. REQUESTER creates ticket
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
        "This ticket verifies the complete SupportFlow lifecycle."
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
          name: "Create ticket",
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
          name: ticketTitle,
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


    // 2. ADMIN assigns ticket
    await logout(page);

    await loginAs(
      page,
      E2E_USERS.admin
    );

    await page.goto(
      ticketUrl
    );

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
          name: "Assign Ticket",
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


    // 3. AGENT starts work
    await logout(page);

    await loginAs(
      page,
      E2E_USERS.agent
    );

    await page.goto(
      ticketUrl
    );

    await page
      .getByRole(
        "button",
        {
          name: "Start Work",
        }
      )
      .click();

    await expect(
      page.getByText(
        "In Progress",
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // 4. AGENT sends public response
    await page
      .getByPlaceholder(
        "Write a response..."
      )
      .fill(
        agentResponse
      );

    await page
      .getByRole(
        "button",
        {
          name: "Send response",
        }
      )
      .click();

    await expect(
      page.getByText(
        agentResponse,
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // 5. AGENT resolves ticket
    await page
      .getByPlaceholder(
        "Describe the fix or resolution..."
      )
      .fill(
        resolutionSummary
      );

    await page
      .getByRole(
        "button",
        {
          name: "Resolve Ticket",
        }
      )
      .click();

    const resolveDialog =
      page.getByRole(
        "dialog"
      );

    await expect(
      resolveDialog
    ).toBeVisible();

    await resolveDialog
      .getByRole(
        "button",
        {
          name: "Resolve Ticket",
        }
      )
      .click();

    await expect(
      page.getByText(
        "Resolved",
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // 6. REQUESTER verifies resolution
    await logout(page);

    await loginAs(
      page,
      E2E_USERS.requester
    );

    await page.goto(
      ticketUrl
    );

    await expect(
      page.getByText(
        "Resolved",
        {
          exact: true,
        }
      ).first()
    ).toBeVisible();

    await expect(
      page.getByText(
        agentResponse,
        {
          exact: true,
        }
      )
    ).toBeVisible();

    await expect(
      page.getByText(
        resolutionSummary,
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // 7. REQUESTER closes ticket
    await page
      .getByRole(
        "button",
        {
          name: "Close Ticket",
        }
      )
      .click();

    const closeDialog =
      page.getByRole(
        "dialog"
      );

    await expect(
      closeDialog
    ).toBeVisible();

    await closeDialog
      .getByRole(
        "button",
        {
          name: "Close Ticket",
        }
      )
      .click();


    // 8. Verify final CLOSED state
    await expect(
      page.getByText(
        "Closed",
        {
          exact: true,
        }
      )
    ).toBeVisible();

    await expect(
      page.getByPlaceholder(
        "Write a response..."
      )
    ).toHaveCount(0);
  }
);
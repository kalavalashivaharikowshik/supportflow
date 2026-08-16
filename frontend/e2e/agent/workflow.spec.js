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
  "assigned agent can start work on a ticket",
  async ({ page }) => {
    const ticketTitle =
      `Agent Workflow E2E ${Date.now()}`;

    /*
     * STEP 1
     * Requester creates ticket
     */
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
        "This ticket verifies the assigned Agent can start work through the UI."
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


    /*
     * STEP 2
     * Admin assigns ticket
     */
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
        .getAttribute(
        "value"
        );

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


    /*
     * STEP 3
     * Assigned Agent logs in
     */
    await logout(page);

    await loginAs(
      page,
      E2E_USERS.agent
    );
    
    /*
     * STEP 4
     * Agent opens same ticket
     */
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

    await expect(
      page.getByText(
        "Assigned",
        {
          exact: true,
        }
      )
    ).toBeVisible();


    /*
     * STEP 5
     * Agent starts work
     */
    await page
      .getByRole(
        "button",
        {
          name:
            "Start Work",
        }
      )
      .click();


    /*
     * STEP 6
     * Verify status changed
     */
    await expect(
      page.getByText(
        "In Progress",
        {
          exact: true,
        }
      )
    ).toBeVisible();

    await expect(
      page.getByRole(
        "button",
        {
          name:
            "Start Work",
        }
      )
    ).toHaveCount(0);

    const publicResponse =
    `Public response E2E ${Date.now()}`;

    await page
    .getByPlaceholder(
        "Write a response..."
    )
    .fill(
        publicResponse
    );

    await page
    .getByRole(
        "button",
        {
        name:
            "Send response",
        }
    )
    .click();

    await expect(
    page.getByText(
        publicResponse,
        {
        exact: true,
        }
    )
    ).toBeVisible();
    }
);
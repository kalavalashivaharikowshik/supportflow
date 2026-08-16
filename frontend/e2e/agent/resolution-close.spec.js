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
  "requester can close a resolved ticket",
  async ({ page }) => {
    const ticketTitle =
      `Requester Close E2E ${Date.now()}`;

    const publicResponse =
      `Agent response E2E ${Date.now()}`;

    const resolutionSummary =
      `Resolution summary E2E ${Date.now()}`;


    // STEP 1:
    // Requester creates the ticket
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
        "This ticket verifies that a requester can close a resolved ticket."
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


    // STEP 2:
    // Admin assigns the ticket
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


    // STEP 3:
    // Agent starts working
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
          name:
            "Start Work",
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


    // STEP 4:
    // Agent sends public response
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


    // STEP 5:
    // Agent enters resolution summary
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
          name:
            "Resolve Ticket",
        }
      )
      .click();


    // STEP 6:
    // Confirm Agent resolution
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
          name:
            "Resolve Ticket",
        }
      )
      .click();

    await expect(
      page.getByText(
        "Resolved",
        {
          exact: true,
        }
      ).first()
    ).toBeVisible();


    // STEP 7:
    // Requester logs back in
    await logout(page);

    await loginAs(
      page,
      E2E_USERS.requester
    );

    await page.goto(
      ticketUrl
    );


    // STEP 8:
    // Requester sees resolved ticket
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
        "Resolved",
        {
          exact: true,
        }
      ).first()
    ).toBeVisible();


    // STEP 9:
    // Requester sees Agent response
    await expect(
      page.getByText(
        publicResponse,
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // STEP 10:
    // Requester sees resolution summary
    await expect(
      page.getByText(
        "Resolution Summary",
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


    // STEP 11:
    // Requester should have lifecycle actions
    await expect(
      page.getByRole(
        "button",
        {
          name: "Reopen",
        }
      )
    ).toBeVisible();

    await expect(
      page.getByRole(
        "button",
        {
          name:
            "Close Ticket",
        }
      )
    ).toBeVisible();


    // STEP 12:
    // Requester starts close action
    await page
      .getByRole(
        "button",
        {
          name:
            "Close Ticket",
        }
      )
      .click();


    // STEP 13:
    // Custom confirmation dialog
    const closeDialog =
      page.getByRole(
        "dialog"
      );

    await expect(
      closeDialog
    ).toBeVisible();

    await expect(
      closeDialog.getByRole(
        "heading",
        {
          name:
            "Close ticket?",
        }
      )
    ).toBeVisible();


    // STEP 14:
    // Confirm closure
    await closeDialog
      .getByRole(
        "button",
        {
          name:
            "Close Ticket",
        }
      )
      .click();


    // STEP 15:
    // Verify final status
    await expect(
      page.getByText(
        "Closed",
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // STEP 16:
    // Closed tickets cannot receive replies
    await expect(
      page.getByPlaceholder(
        "Write a response..."
      )
    ).toHaveCount(0);


    // STEP 17:
    // Close/Reopen actions should disappear
    await expect(
      page.getByRole(
        "button",
        {
          name:
            "Close Ticket",
        }
      )
    ).toHaveCount(0);

    await expect(
      page.getByRole(
        "button",
        {
          name: "Reopen",
        }
      )
    ).toHaveCount(0);
  }
);
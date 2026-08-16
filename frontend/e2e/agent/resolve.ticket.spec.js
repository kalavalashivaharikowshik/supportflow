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
  "assigned agent can resolve an in-progress ticket",
  async ({ page }) => {
    const ticketTitle =
      `Resolve E2E ${Date.now()}`;

    const resolutionSummary =
      `Resolution completed successfully ${Date.now()}`;


    // STEP 1:
    // Requester creates ticket
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
        "This ticket verifies the complete Agent resolution workflow."
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
    // Admin assigns ticket to Agent
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
    // Agent logs in
    await logout(page);

    await loginAs(
      page,
      E2E_USERS.agent
    );

    await page.goto(
      ticketUrl
    );


    // STEP 4:
    // Agent starts work
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


    // STEP 5:
    // Agent enters resolution summary
    await page
      .getByPlaceholder(
        "Describe the fix or resolution..."
      )
      .fill(
        resolutionSummary
      );


    // STEP 6:
    // Open confirmation dialog
    await page
      .getByRole(
        "button",
        {
          name:
            "Resolve Ticket",
        }
      )
      .click();


    // STEP 7:
    // Verify custom modal opened
    const dialog =
      page.getByRole(
        "dialog"
      );

    await expect(
      dialog
    ).toBeVisible();

    await expect(
      dialog.getByRole(
        "heading",
        {
          name:
            "Resolve ticket?",
        }
      )
    ).toBeVisible();


    // STEP 8:
    // Confirm resolution
    await dialog
      .getByRole(
        "button",
        {
          name:
            "Resolve Ticket",
        }
      )
      .click();


    // STEP 9:
    // Verify ticket status
    await expect(
      page.getByText(
        "Resolved",
        {
          exact: true,
        }
      ).first()
    ).toBeVisible();


    // STEP 10:
    // Verify summary is visible
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
    // Resolve form should disappear
    await expect(
      page.getByPlaceholder(
        "Describe the fix or resolution..."
      )
    ).toHaveCount(0);
  }
);
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
  "internal note is hidden from requester",
  async ({ page }) => {
    const ticketTitle =
      `Internal Note E2E ${Date.now()}`;

    const internalNote =
      `PRIVATE-E2E-${Date.now()}`;


    // 1. Requester creates ticket
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
        "This ticket verifies that internal notes stay private."
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


    // 2. Admin assigns ticket
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


    // 3. Agent opens ticket
    await logout(page);

    await loginAs(
      page,
      E2E_USERS.agent
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


    // 4. Agent enables Internal Note
    await page
      .getByRole(
        "checkbox",
        {
          name:
            /internal note/i,
        }
      )
      .check();


    // 5. Agent writes private note
    await page
      .getByPlaceholder(
        "Write a response..."
      )
      .fill(
        internalNote
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


    // 6. Agent should see the note
    await expect(
      page.getByText(
        internalNote,
        {
          exact: true,
        }
      )
    ).toBeVisible();

    await expect(
      page.getByText(
        "Internal Note",
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // 7. Requester logs back in
    await logout(page);

    await loginAs(
      page,
      E2E_USERS.requester
    );

    await page.goto(
      ticketUrl
    );


    // 8. Requester still sees ticket
    await expect(
      page.getByRole(
        "heading",
        {
          name:
            ticketTitle,
        }
      )
    ).toBeVisible();


    // 9. PRIVATE NOTE MUST NOT APPEAR
    await expect(
      page.getByText(
        internalNote,
        {
          exact: true,
        }
      )
    ).toHaveCount(0);


    // 10. Internal-note marker also must not appear
    await expect(
      page.getByText(
        "Internal Note",
        {
          exact: true,
        }
      )
    ).toHaveCount(0);
  }
);
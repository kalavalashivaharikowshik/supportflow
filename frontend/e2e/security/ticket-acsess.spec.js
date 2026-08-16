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
  "requester cannot access another requester's ticket",
  async ({ page }) => {
    const ticketTitle =
      `Private Ticket E2E ${Date.now()}`;

    const secondRequesterEmail =
      `second-requester-${Date.now()}@example.com`;

    const secondRequesterPassword =
      "Requester@123";


    // STEP 1:
    // Seeded requester creates a private ticket
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
        "This ticket must only be visible to the requester who created it."
      );

    await page
      .getByLabel("Category")
      .selectOption(
        "TECHNICAL"
      );

    await page
      .getByLabel("Priority")
      .selectOption(
        "MEDIUM"
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


    // STEP 2:
    // Logout original requester
    await logout(page);


    // STEP 3:
    // Register a completely different requester
    await page.goto(
      "/register"
    );

    await page
      .getByLabel("Full name")
      .fill(
        "Second E2E Requester"
      );

    await page
      .getByLabel("Email")
      .fill(
        secondRequesterEmail
      );

    await page
      .getByLabel(
        "Password",
        {
          exact: true,
        }
      )
      .fill(
        secondRequesterPassword
      );

    await page
      .getByLabel(
        "Confirm password"
      )
      .fill(
        secondRequesterPassword
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


    // STEP 4:
    // Login as second requester
    await page
      .getByLabel("Email")
      .fill(
        secondRequesterEmail
      );

    await page
      .getByLabel("Password")
      .fill(
        secondRequesterPassword
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
      /\/requester$/
    );


    // STEP 5:
    // Manually attempt to open first requester's ticket
    await page.goto(
      ticketUrl
    );


    // STEP 6:
    // Sensitive ticket content must NOT render
    await expect(
      page.getByText(
        ticketTitle,
        {
          exact: true,
        }
      )
    ).toHaveCount(0);


    // STEP 7:
    // Frontend should show its error state
    await expect(
      page.getByText(
        /permission|access|forbidden|not allowed/i
      )
    ).toBeVisible();
  }
);
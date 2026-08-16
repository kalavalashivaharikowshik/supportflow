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
  "agent receives live assignment notification without refresh",
  async ({ browser }) => {
    const ticketTitle =
      `Live Assignment E2E ${Date.now()}`;


    // STEP 1:
    // Create separate browser sessions
    const requesterContext =
      await browser.newContext();

    const adminContext =
      await browser.newContext();

    const agentContext =
      await browser.newContext();


    const requesterPage =
      await requesterContext.newPage();

    const adminPage =
      await adminContext.newPage();

    const agentPage =
      await agentContext.newPage();


    try {
      // STEP 2:
      // Requester creates a fresh ticket
      await loginAs(
        requesterPage,
        E2E_USERS.requester
      );

      await requesterPage.goto(
        "/requester/tickets/create"
      );

      await requesterPage
        .getByLabel("Title")
        .fill(ticketTitle);

      await requesterPage
        .getByLabel("Description")
        .fill(
          "This ticket verifies live WebSocket assignment notifications."
        );

      await requesterPage
        .getByLabel("Category")
        .selectOption(
          "TECHNICAL"
        );

      await requesterPage
        .getByLabel("Priority")
        .selectOption(
          "HIGH"
        );

      await requesterPage
        .getByRole(
          "button",
          {
            name:
              "Create ticket",
          }
        )
        .click();

      await expect(
        requesterPage
      ).toHaveURL(
        /\/tickets\/\d+$/
      );

      const ticketUrl =
        requesterPage.url();


      // STEP 3:
      // Admin logs in
      await loginAs(
        adminPage,
        E2E_USERS.admin
      );

      await adminPage.goto(
        ticketUrl
      );


      // STEP 4:
      // Agent logs in and stays on dashboard
      await loginAs(
        agentPage,
        E2E_USERS.agent
      );

      await expect(
        agentPage
      ).toHaveURL(
        /\/agent$/
      );


      // STEP 5:
      // Verify notification bell exists
      const notificationBell =
        agentPage.getByRole(
          "button",
          {
            name:
              "Notifications",
          }
        );

      await expect(
        notificationBell
      ).toBeVisible();


      // STEP 6:
      // Read unread count before assignment
      const badgeBefore =
        notificationBell.locator(
          "span"
        ).first();

      let unreadBefore = 0;

      if (
        await badgeBefore.count()
      ) {
        const text =
          await badgeBefore.textContent();

        const parsed =
          Number(text);

        if (
          Number.isFinite(
            parsed
          )
        ) {
          unreadBefore =
            parsed;
        }
      }


      // STEP 7:
      // Admin assigns ticket to Agent
      const adminActions =
    adminPage
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

      await adminPage
        .getByRole(
          "button",
          {
            name:
              "Assign Ticket",
          }
        )
        .click();

      await expect(
        adminPage.getByText(
          "Assigned",
          {
            exact: true,
          }
        )
      ).toBeVisible();


      // STEP 8:
      // IMPORTANT:
      // Do NOT reload the Agent page.
      // Wait for live notification.

      await expect
        .poll(
          async () => {
            const badge =
              notificationBell.locator(
                "span"
              ).first();

            if (
              !await badge.count()
            ) {
              return 0;
            }

            const text =
              await badge.textContent();

            const parsed =
              Number(text);

            return Number.isFinite(
              parsed
            )
              ? parsed
              : 0;
          },
          {
            timeout:
              10_000,
          }
        )
        .toBeGreaterThan(
          unreadBefore
        );


      // STEP 9:
      // Open notification dropdown
      await notificationBell.click();


      // STEP 10:
      // Verify assignment notification appears
      await expect(
        agentPage.getByText(
          /assigned/i
        ).first()
      ).toBeVisible();
    } finally {
      await requesterContext.close();
      await adminContext.close();
      await agentContext.close();
    }
  }
);
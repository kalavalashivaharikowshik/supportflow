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
  "admin can deactivate and reactivate a secondary agent",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.admin
    );

    await page.goto(
      "/admin/users"
    );

    await expect(
      page.getByRole(
        "heading",
        {
          name:
            "User Management",
        }
      )
    ).toBeVisible();


    // STEP 1:
    // Search for secondary Agent
    const searchBox =
      page.getByRole(
        "searchbox"
      );

    await searchBox.fill(
      E2E_USERS
        .agentTwo
        .email
    );


    // STEP 2:
    // Find row containing agent2
    const agentRow =
      page.getByRole(
        "row"
      ).filter({
        hasText:
          E2E_USERS
            .agentTwo
            .email,
      });

    await expect(
      agentRow
    ).toBeVisible();


    // STEP 3:
    // Make sure account begins Active
    await expect(
      agentRow.getByText(
        "Active",
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // STEP 4:
    // Click Deactivate
    await agentRow
      .getByRole(
        "button",
        {
          name:
            "Deactivate",
        }
      )
      .click();


    // STEP 5:
    // Confirm dialog opens
    const deactivateDialog =
      page.getByRole(
        "dialog"
      );

    await expect(
      deactivateDialog
    ).toBeVisible();

    await expect(
      deactivateDialog
        .getByRole(
          "heading",
          {
            name:
              "Deactivate user?",
          }
        )
    ).toBeVisible();


    // STEP 6:
    // Confirm deactivation
    await deactivateDialog
      .getByRole(
        "button",
        {
          name:
            "Deactivate",
        }
      )
      .click();


    // STEP 7:
    // Wait for table refresh
    const inactiveRow =
      page.getByRole(
        "row"
      ).filter({
        hasText:
          E2E_USERS
            .agentTwo
            .email,
      });

    await expect(
      inactiveRow.getByText(
        "Inactive",
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // STEP 8:
    // Reactivate same Agent
    await inactiveRow
      .getByRole(
        "button",
        {
          name:
            "Activate",
        }
      )
      .click();


    // STEP 9:
    // Confirm activation
    const activateDialog =
      page.getByRole(
        "dialog"
      );

    await expect(
      activateDialog
    ).toBeVisible();

    await expect(
      activateDialog
        .getByRole(
          "heading",
          {
            name:
              "Activate user?",
          }
        )
    ).toBeVisible();

    await activateDialog
      .getByRole(
        "button",
        {
          name:
            "Activate",
        }
      )
      .click();


    // STEP 10:
    // Final state MUST be Active
    const activeRow =
      page.getByRole(
        "row"
      ).filter({
        hasText:
          E2E_USERS
            .agentTwo
            .email,
      });

    await expect(
      activeRow.getByText(
        "Active",
        {
          exact: true,
        }
      )
    ).toBeVisible();
  }
);
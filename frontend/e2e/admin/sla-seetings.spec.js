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
  "admin can update and restore SLA configuration",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.admin
    );

    await page.goto(
      "/admin/sla"
    );

    await expect(
      page.getByRole(
        "heading",
        {
          name:
            "SLA Settings",
        }
      )
    ).toBeVisible();


    // STEP 1:
    // Verify all SLA priorities exist
    await expect(
      page.getByText(
        "LOW",
        {
          exact: true,
        }
      )
    ).toBeVisible();

    await expect(
      page.getByText(
        "MEDIUM",
        {
          exact: true,
        }
      )
    ).toBeVisible();

    await expect(
      page.getByText(
        "HIGH",
        {
          exact: true,
        }
      )
    ).toBeVisible();

    await expect(
      page.getByText(
        "CRITICAL",
        {
          exact: true,
        }
      )
    ).toBeVisible();


    // STEP 2:
    // Find the HIGH SLA card
    const highCard =
      page.getByText(
        "HIGH",
        {
          exact: true,
        }
      )
      .locator("..");


    const highInput =
      highCard.getByRole(
        "spinbutton"
      );


    // STEP 3:
    // Read current HIGH SLA value
    const originalValue =
      await highInput
        .inputValue();

    const originalNumber =
      Number(
        originalValue
      );


    // STEP 4:
    // Choose another valid value
    const newValue =
      String(
        originalNumber + 1
      );


    // STEP 5:
    // Update HIGH SLA
    await highInput.fill(
      newValue
    );

    await highCard
      .getByRole(
        "button",
        {
          name: "Save",
        }
      )
      .click();


    // STEP 6:
    // Verify value remains
    await expect(
      highInput
    ).toHaveValue(
      newValue
    );


    // STEP 7:
    // Refresh page to prove backend persistence
    await page.reload();

    const refreshedHighCard =
      page.getByText(
        "HIGH",
        {
          exact: true,
        }
      )
      .locator("..");

    const refreshedHighInput =
      refreshedHighCard
        .getByRole(
          "spinbutton"
        );

    await expect(
      refreshedHighInput
    ).toHaveValue(
      newValue
    );


    // STEP 8:
    // Restore original value
    await refreshedHighInput
      .fill(
        originalValue
      );

    await refreshedHighCard
      .getByRole(
        "button",
        {
          name: "Save",
        }
      )
      .click();


    // STEP 9:
    // Verify restoration
    await expect(
      refreshedHighInput
    ).toHaveValue(
      originalValue
    );


    // STEP 10:
    // Refresh once more
    await page.reload();

    const finalHighCard =
      page.getByText(
        "HIGH",
        {
          exact: true,
        }
      )
      .locator("..");

    await expect(
      finalHighCard
        .getByRole(
          "spinbutton"
        )
    ).toHaveValue(
      originalValue
    );
  }
);
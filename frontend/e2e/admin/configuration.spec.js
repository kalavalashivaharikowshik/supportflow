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
  "admin can update and restore application configuration",
  async ({ page }) => {
    // STEP 1:
    // Login as Admin
    await loginAs(
      page,
      E2E_USERS.admin
    );


    // STEP 2:
    // Open Admin Configuration page
    await page.goto(
      "/admin/config"
    );

    await expect(
      page.getByRole(
        "heading",
        {
          name:
            "Admin Configuration",
        }
      )
    ).toBeVisible();


    // STEP 3:
    // Locate SLA warning threshold input
    const thresholdInput =
      page
        .getByRole(
          "spinbutton"
        )
        .first();

    await expect(
      thresholdInput
    ).toBeVisible();


    // STEP 4:
    // Read current configuration value
    const originalValue =
      await thresholdInput
        .inputValue();


    // STEP 5:
    // Choose a different valid value
    const newValue =
      originalValue === "85"
        ? "80"
        : "85";


    // STEP 6:
    // Update threshold
    await thresholdInput
      .fill(
        newValue
      );


    // STEP 7:
    // Save configuration
    await page
      .getByRole(
        "button",
        {
          name:
            "Save Configuration",
        }
      )
      .click();


    // STEP 8:
    // Verify changed value remains
    await expect(
      thresholdInput
    ).toHaveValue(
      newValue
    );


    // STEP 9:
    // Reload page
    await page.reload();


    // STEP 10:
    // Locate input again after reload
    const refreshedThresholdInput =
      page
        .getByRole(
          "spinbutton"
        )
        .first();

    await expect(
      refreshedThresholdInput
    ).toBeVisible();


    // STEP 11:
    // Verify new value persisted
    await expect(
      refreshedThresholdInput
    ).toHaveValue(
      newValue
    );


    // STEP 12:
    // Restore original value
    await refreshedThresholdInput
      .fill(
        originalValue
      );


    // STEP 13:
    // Save restored configuration
    await page
      .getByRole(
        "button",
        {
          name:
            "Save Configuration",
        }
      )
      .click();


    // STEP 14:
    // Verify restored value
    await expect(
      refreshedThresholdInput
    ).toHaveValue(
      originalValue
    );


    // STEP 15:
    // Reload again
    await page.reload();


    // STEP 16:
    // Locate input after second reload
    const finalThresholdInput =
      page
        .getByRole(
          "spinbutton"
        )
        .first();

    await expect(
      finalThresholdInput
    ).toBeVisible();


    // STEP 17:
    // Prove restored value persisted
    await expect(
      finalThresholdInput
    ).toHaveValue(
      originalValue
    );
  }
);
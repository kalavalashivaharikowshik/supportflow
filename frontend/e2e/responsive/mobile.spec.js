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


test.use({
  viewport: {
    width: 375,
    height: 812,
  },
});


test(
  "requester mobile navigation works",
  async ({ page }) => {
    // STEP 1:
    // Login as requester
    await loginAs(
      page,
      E2E_USERS.requester
    );

    await expect(
      page
    ).toHaveURL(
      /\/requester$/
    );


    // STEP 2:
    // Verify requester dashboard
    await expect(
      page.getByRole(
        "heading",
        {
          name:
            "Requester Dashboard",
        }
      )
    ).toBeVisible();


    // STEP 3:
    // Mobile menu button should be visible
    const menuButton =
      page.getByRole(
        "button",
        {
          name:
            "Open navigation",
        }
      );

    await expect(
      menuButton
    ).toBeVisible();


    // STEP 4:
    // Open mobile drawer
    await menuButton.click();


    // STEP 5:
    // Verify mobile navigation is visible
    const navigation =
      page.getByRole(
        "navigation",
        {
          name:
            "Primary navigation",
        }
      );

    await expect(
      navigation
    ).toBeVisible();


    // STEP 6:
    // Verify Requester menu items
    await expect(
      navigation.getByRole(
        "link",
        {
          name:
            "Dashboard",
        }
      )
    ).toBeVisible();

    await expect(
      navigation.getByRole(
        "link",
        {
          name:
            "My Tickets",
        }
      )
    ).toBeVisible();

    await expect(
      navigation.getByRole(
        "link",
        {
          name:
            "Create Ticket",
        }
      )
    ).toBeVisible();


    // STEP 7:
    // Navigate using mobile drawer
    await navigation
      .getByRole(
        "link",
        {
          name:
            "My Tickets",
        }
      )
      .click();


    // STEP 8:
    // Verify correct route
    await expect(
      page
    ).toHaveURL(
      /\/requester\/tickets$/
    );


    // STEP 9:
    // Verify destination page
    await expect(
      page.getByRole(
        "heading",
        {
          name:
            "My Tickets",
        }
      )
    ).toBeVisible();


    // STEP 10:
    // Drawer should close automatically
    await expect(
      page.getByRole(
        "button",
        {
          name:
            "Close navigation",
        }
      )
    ).toHaveCount(0);


    // STEP 11:
    // Mobile menu button should be available again
    await expect(
      page.getByRole(
        "button",
        {
          name:
            "Open navigation",
        }
      )
    ).toBeVisible();
  }
);
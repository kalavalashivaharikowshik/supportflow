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
  "requester cannot open admin page",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.requester
    );

    await page.goto(
      "/admin"
    );

    await expect(
      page
    ).toHaveURL(
      /\/unauthorized$/
    );

    await expect(
      page.getByRole(
        "heading",
        {
          name: "Access denied",
        }
      )
    ).toBeVisible();
  }
);


test(
  "requester cannot open agent page",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.requester
    );

    await page.goto(
      "/agent"
    );

    await expect(
      page
    ).toHaveURL(
      /\/unauthorized$/
    );
  }
);


test(
  "agent cannot open admin page",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.agent
    );

    await page.goto(
      "/admin"
    );

    await expect(
      page
    ).toHaveURL(
      /\/unauthorized$/
    );
  }
);


test(
  "agent cannot open requester page",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.agent
    );

    await page.goto(
      "/requester"
    );

    await expect(
      page
    ).toHaveURL(
      /\/unauthorized$/
    );
  }
);


test(
  "admin cannot open requester page",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.admin
    );

    await page.goto(
      "/requester"
    );

    await expect(
      page
    ).toHaveURL(
      /\/unauthorized$/
    );
  }
);


test(
  "admin cannot open agent page",
  async ({ page }) => {
    await loginAs(
      page,
      E2E_USERS.admin
    );

    await page.goto(
      "/agent"
    );

    await expect(
      page
    ).toHaveURL(
      /\/unauthorized$/
    );
  }
);
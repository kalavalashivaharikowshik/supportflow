import {
  expect,
} from "@playwright/test";


export async function loginAs(
  page,
  user
) {
  await page.goto(
    "/login"
  );

  await page
    .getByLabel("Email")
    .fill(user.email);

  await page
    .getByLabel("Password")
    .fill(user.password);

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
  ).not.toHaveURL(
    /\/login$/
  );
}

export async function logout(
  page
) {
  const toasts =
    page.locator(
      '[data-rht-toaster] [role="status"]'
    );

  await expect(
    toasts
  ).toHaveCount(
    0,
    {
      timeout: 10_000,
    }
  );

  await page
    .getByRole(
      "button",
      {
        name: "Logout",
      }
    )
    .click();

  await expect(
    page
  ).toHaveURL(
    /\/login$/
  );
}
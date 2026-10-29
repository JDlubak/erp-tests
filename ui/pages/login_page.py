from playwright.sync_api import expect, Locator

from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    @property
    def sign_in_button(self) -> Locator:
        return self.page.get_by_role("button", name="Sign in",
                                     exact=True)

    def expect_visible(self) -> None:
        expect(self.page.get_by_role("heading",
                                     name="Manufacturing "
                                          "ERP")).to_be_visible()
        expect(self.sign_in_button).to_be_visible()

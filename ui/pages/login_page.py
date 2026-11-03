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

    # wypełnienie formularza i wysłanie go przyciskiem "Sign in"
    def sign_in(self, username: str, password: str) -> None:
        self.page.get_by_role("textbox").first.fill(username)
        self.page.locator("input[type='password']").fill(password)
        self.sign_in_button.click()

    # komunikat o błędnych danych logowania
    def expect_invalid_credentials_error(self) -> None:
        expect(self.page.get_by_text(
            "Invalid username or password")).to_be_visible()
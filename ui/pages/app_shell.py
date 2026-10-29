import re

from playwright.sync_api import expect, Locator

from ui.pages.base_page import BasePage


# Szkielet aplikacji po zalogowaniu, dziedziczący po BasePage
class AppShell(BasePage):
    path = "/"

    # znalezienie lokatora zawierającego awatar i nazwę użytkownika
    def user_menu_button(self, username: str) -> Locator:
        return self.page.locator(
            ".mantine-AppShell-header").get_by_role(
            "button",
            name=re.compile(rf"\b{re.escape(username)}$", re.I))

    # Szukanie odnośnika nawigacyjnego o konkretnej nazwie
    def nav_link(self, label: str) -> Locator:
        return self.navbar.get_by_role("link", name=label, exact=True)

    # Asercja potwierdzająca wystąpienie nagłówek "Dashboard"
    # (np. poprawne zalogowanie/wylogowanie)
    def expect_dashboard_for(self, username: str) -> None:
        expect(self.page.get_by_role("heading", name="Dashboard",
                                     exact=True)).to_be_visible()
        expect(self.user_menu_button(username)).to_be_visible()

    # realizacja procesu wylogowania się z systemu
    def sign_out(self, username: str) -> None:
        self.user_menu_button(username).click()
        self.page.get_by_role("menuitem", name="Sign out").click()

    # Sprawdzenie wystąpienia standardowego ekranu blokady dla
    # niepoprawnej roli użytkownika
    def expect_forbidden(self) -> None:
        expect(self.page.get_by_role("heading", name="403",
                                     exact=True)).to_be_visible()
        expect(self.page.get_by_text(
            "You don't have the role required for this "
            "action.")).to_be_visible()

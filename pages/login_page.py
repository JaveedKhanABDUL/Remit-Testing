from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Keycloak login page (realm auct-ppt)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator("#kc-page-title")
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.show_password_button = page.locator("#password-show-password")
        self.sign_in_button = page.locator("#kc-login")
        self.entra_id_button = page.locator("#social-epex-idp")
        self.alert_error = page.locator(
            "#input-error, .pf-v5-c-alert.pf-m-danger, .kc-feedback-text"
        )

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.sign_in_button.click()

    def toggle_password_visibility(self) -> None:
        self.show_password_button.click()

    def login_with_entra_id(self) -> None:
        self.entra_id_button.click()

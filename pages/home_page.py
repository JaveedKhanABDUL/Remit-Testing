import re

from playwright.sync_api import Page, expect

from config import settings
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page shown after a successful login; used to validate the login."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.indicator = (
            page.locator(settings.POST_LOGIN_SELECTOR)
            if settings.POST_LOGIN_SELECTOR
            else None
        )

    def expect_logged_in(self, timeout: int = 15000) -> None:
        # Left the Keycloak realm, and (optionally) the app element is visible.
        expect(self.page).not_to_have_url(re.compile(r"/realms/.+/login-actions/"), timeout=timeout)
        expect(self.page.locator("#kc-login")).to_have_count(0)
        if self.indicator is not None:
            expect(self.indicator).to_be_visible(timeout=timeout)

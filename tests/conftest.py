import pytest
from playwright.sync_api import Page

from config import settings
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    if not settings.BASE_URL:
        pytest.skip("BASE_URL is not set (see .env.example)")
    lp = LoginPage(page)
    lp.open(settings.BASE_URL)
    return lp

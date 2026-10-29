import pytest
from playwright.sync_api import expect

from config import settings
from pages.home_page import HomePage


def _expect_login_rejected(login_page):
    expect(login_page.alert_error.first).to_be_visible()
    expect(login_page.sign_in_button).to_be_visible()
    expect(login_page.username_input).to_be_visible()


def test_empty_credentials_rejected(login_page):
    login_page.login("", "")
    _expect_login_rejected(login_page)


def test_empty_password_rejected(login_page):
    login_page.login("some_user", "")
    _expect_login_rejected(login_page)


def test_empty_username_rejected(login_page):
    login_page.login("", "some_password")
    _expect_login_rejected(login_page)


def test_wrong_password_shows_message(login_page):
    login_page.login("invalid_user", "wrong_password")
    _expect_login_rejected(login_page)
    assert "invalid" in login_page.error_text().lower()


@pytest.mark.skipif(
    not (settings.USERNAME and settings.PASSWORD),
    reason="APP_USERNAME/APP_PASSWORD not set",
)
def test_valid_login_lands_on_app(login_page):
    login_page.login(settings.USERNAME, settings.PASSWORD)
    HomePage(login_page.page).expect_logged_in()


@pytest.mark.skipif(
    not settings.USERNAME, reason="APP_USERNAME not set"
)
def test_valid_user_wrong_password_rejected(login_page):
    login_page.login(settings.USERNAME, settings.PASSWORD + "_wrong")
    _expect_login_rejected(login_page)

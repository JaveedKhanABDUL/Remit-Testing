import pytest
from playwright.sync_api import expect

from config import settings
from pages.home_page import HomePage


def test_login_page_elements(login_page):
    expect(login_page.title).to_have_text("Sign in to your account")
    expect(login_page.username_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.sign_in_button).to_be_enabled()
    expect(login_page.entra_id_button).to_be_visible()


def test_password_visibility_toggle(login_page):
    expect(login_page.password_input).to_have_attribute("type", "password")
    login_page.toggle_password_visibility()
    expect(login_page.password_input).to_have_attribute("type", "text")


def test_invalid_login_shows_error(login_page):
    login_page.login("invalid_user", "invalid_password")
    expect(login_page.alert_error.first).to_be_visible()


@pytest.mark.skipif(
    not (settings.USERNAME and settings.PASSWORD),
    reason="APP_USERNAME/APP_PASSWORD not set",
)
def test_valid_login(login_page):
    login_page.login(settings.USERNAME, settings.PASSWORD)
    HomePage(login_page.page).expect_logged_in()

import os

from dotenv import load_dotenv

load_dotenv()

# The Keycloak login URL carries one-time session params, so start from the app URL;
# it redirects to the login page.
BASE_URL = os.getenv("BASE_URL", "")
USERNAME = os.getenv("APP_USERNAME", "")
PASSWORD = os.getenv("APP_PASSWORD", "")

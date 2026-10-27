# Remit-Testing
Remit Manual Testing

## Login automation (Playwright + pytest)

```
config/settings.py     env-based settings
pages/                 page objects (LoginPage)
tests/                 pytest tests and fixtures
```

Setup:
```
pip install -r requirements.txt
playwright install chromium
cp .env.example .env   # set BASE_URL, APP_USERNAME, APP_PASSWORD
pytest                 # add --headed to watch; report in reports/report.html
```

## Login automation (Playwright + pytest)

```
config/settings.py     env-based settings
pages/                 page objects (LoginPage)
tests/                 pytest tests and fixtures
```

Setup:
```
pip install -r requirements.txt
playwright install chromium
cp .env.example .env   # set BASE_URL, APP_USERNAME, APP_PASSWORD
pytest                 # add --headed to watch; report in reports/report.html
```

Run via entry point: `python run.py [--headed] [--browser firefox] [-k test_name]`

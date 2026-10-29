"""Entry point: python run.py [--headed] [--browser chromium|firefox|webkit] [pytest args...]"""
import argparse
import sys

import pytest


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the login automation tests")
    parser.add_argument("--headed", action="store_true", help="show the browser")
    parser.add_argument("--browser", default="chromium",
                        choices=["chromium", "firefox", "webkit"])
    parser.add_argument("--channel", default="chrome",
                        help="installed browser to use (chrome, msedge); 'bundled' uses Playwright's own")
    args, extra = parser.parse_known_args()

    pytest_args = ["--browser", args.browser, *extra]
    channel = "chromium" if args.channel == "bundled" else args.channel
    pytest_args += ["--browser-channel", channel]
    if args.headed:
        pytest_args.append("--headed")
    return pytest.main(pytest_args)


if __name__ == "__main__":
    sys.exit(main())

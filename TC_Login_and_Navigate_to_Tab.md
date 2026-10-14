# Test Case: Login and open the respective tab

Replace the `<placeholders>` with your application's real values.

| Field | Value |
|---|---|
| Test Case ID | TC-LOGIN-001 |
| Title | Valid user can log in and open the `<Tab Name>` tab |
| Priority | High |
| Type | Functional / Smoke |
| Preconditions | 1. Website `<URL>` is reachable.<br>2. A valid user account exists (`<username>` / `<password>`) with access to the `<Tab Name>` tab.<br>3. Supported browser is installed. |
| Test Data | URL: `<URL>`; Username: `<username>`; Password: `<password>`; Tab: `<Tab Name>` |

## Steps and expected results

| # | Step | Expected result |
|---|---|---|
| 1 | Open the browser and navigate to `<URL>`. | Login page loads with username, password fields and a Login button. |
| 2 | Enter the valid username. | Username is accepted in the field. |
| 3 | Enter the valid password. | Password is masked. |
| 4 | Click **Login**. | User is authenticated and the home/dashboard page is displayed, showing the tab menu. |
| 5 | Click the `<Tab Name>` tab. | The tab is highlighted as active and its page/content loads without errors. |
| 6 | Verify the page title/URL and key content of the tab. | Title/URL match `<Tab Name>`; expected content is displayed. |

**Postcondition:** User remains logged in on the `<Tab Name>` tab; log out to clean up.

## Related scenarios

| ID | Scenario | Expected result |
|---|---|---|
| TC-LOGIN-002 | Invalid password | Error message shown; user stays on login page. |
| TC-LOGIN-003 | Empty username/password | Validation message for required fields. |
| TC-LOGIN-004 | User without permission for the tab | Tab hidden/disabled or access-denied message. |
| TC-LOGIN-005 | Open tab URL directly while logged out | Redirected to login page. |

| Actual result | Status (Pass/Fail) | Comments |
|---|---|---|
| | Not Run | |

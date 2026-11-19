TOPIC = {
    "slug": "playwright",
    "title": "Automation with Playwright",
    "icon": "🎭",
    "summary": "Setup, locators, actions, assertions, pytest, Page Object Model",
    "lesson": r"""
## What is test automation?
Writing code that **does your manual test steps for you** – open browser, click, type, check result. Great for **regression** tests you repeat every release.

**Playwright** (by Microsoft) is a modern tool that works with Chrome, Firefox and Safari (WebKit), and waits for elements automatically.

---

## 1. Setup (on your laptop)
```text
pip install pytest-playwright
playwright install
```

## 2. Your first test
Create `test_example.py`:
```python
import re
from playwright.sync_api import Page, expect

def test_title(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))
```
Run:
```text
pytest                      # headless (no browser window)
pytest --headed             # see the browser
pytest --browser firefox
```
`page` is a **fixture** – pytest-playwright opens the browser for you.

---

## 3. Locators – finding elements ⭐
Prefer locators the **user** sees:
```python
page.get_by_role("button", name="Login")
page.get_by_label("Email")
page.get_by_placeholder("Enter password")
page.get_by_text("Welcome, Ravi")
page.get_by_test_id("submit-btn")       # data-testid="submit-btn"
```
CSS / XPath when needed:
```python
page.locator("#username")              # id
page.locator(".error-msg")             # class
page.locator("input[name='email']")    # attribute
page.locator("//button[text()='Login']")  # XPath
```

## 4. Actions
```python
page.goto("https://example.com/login")
page.get_by_label("Email").fill("test@mail.com")
page.get_by_label("Password").fill("Pass@123")
page.get_by_role("button", name="Login").click()
page.get_by_role("checkbox").check()
page.select_option("#city", "Pune")
page.keyboard.press("Enter")
```

## 5. Assertions with `expect` ⭐
```python
expect(page).to_have_url("https://example.com/dashboard")
expect(page.get_by_text("Welcome")).to_be_visible()
expect(page.locator(".error")).to_have_text("Invalid password")
expect(page.locator(".cart-count")).to_have_text("2")
expect(page.get_by_role("button", name="Pay")).to_be_enabled()
```
`expect` **waits and retries** (default 5 seconds) – no `time.sleep()` needed.

---

## 6. Full example: login test (positive + negative)
```python
from playwright.sync_api import Page, expect

URL = "https://the-internet.herokuapp.com/login"

def test_valid_login(page: Page):
    page.goto(URL)
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")

def test_invalid_login(page: Page):
    page.goto(URL)
    page.locator("#username").fill("wrong")
    page.locator("#password").fill("wrong")
    page.get_by_role("button", name="Login").click()
    expect(page.locator("#flash")).to_contain_text("Your username is invalid!")
```



<div class="viz" data-viz="playwright"></div>

## 7. Page Object Model (POM)
Keep locators in one class per page so tests stay clean:
```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_btn = page.get_by_role("button", name="Login")

    def login(self, user, pwd):
        self.username.fill(user)
        self.password.fill(pwd)
        self.login_btn.click()

def test_login(page):
    page.goto("https://the-internet.herokuapp.com/login")
    LoginPage(page).login("tomsmith", "SuperSecretPassword!")
```
If the UI changes, you fix **one** place.

## 8. Useful extras
- **Codegen** – records your clicks into code: `playwright codegen https://example.com`
- **Screenshots**: `page.screenshot(path="home.png")`
- **Trace viewer**: `pytest --tracing on` → see every step after a failure.
- **Parametrize** (data-driven):
```python
import pytest
@pytest.mark.parametrize("user,pwd", [("a","1"), ("b","2")])
def test_bad_logins(page, user, pwd): ...
```
""",
    "resources": [
        {"kind": "link", "title": "Playwright for Python – official docs", "url": "https://playwright.dev/python/docs/intro"},
        {"kind": "link", "title": "Playwright locators guide", "url": "https://playwright.dev/python/docs/locators"},
        {"kind": "link", "title": "The Internet – practice site for automation", "url": "https://the-internet.herokuapp.com/"},
        {"kind": "link", "title": "SauceDemo – practice shopping site", "url": "https://www.saucedemo.com/"},
        {"kind": "youtube", "title": "Playwright Python tutorial (search)", "url": "https://www.youtube.com/results?search_query=playwright+python+tutorial+for+beginners"},
    ],
    "theory": {
        "easy": [
            {"q": "Which command installs Playwright browsers?", "options": ["pip install browsers", "playwright install", "pytest --install", "npm start"], "answer": 1, "explain": "After pip install pytest-playwright, run playwright install."},
            {"q": "Which method types text into an input?", "options": ["click()", "fill()", "goto()", "expect()"], "answer": 1, "explain": "locator.fill('text')"},
            {"q": "Which method opens a URL?", "options": ["page.open()", "page.goto()", "page.visit()", "page.url()"], "answer": 1, "explain": "page.goto(url)"},
            {"q": "Which test type benefits MOST from automation?", "options": ["One-time exploratory test", "Regression tests repeated every release", "Usability testing", "Ad-hoc testing"], "answer": 1, "explain": "Repeated tests give the best return on automation."},
        ],
        "medium": [
            {"q": "Which locator is recommended (user-facing)?", "options": ["Long XPath", "get_by_role('button', name='Login')", "nth-child CSS", "Absolute XPath /html/body/div[3]"], "answer": 1, "explain": "Role/label/text locators are stable and readable."},
            {"q": "Why avoid time.sleep() in Playwright?", "options": ["It's not allowed", "Playwright auto-waits; sleep makes tests slow and still flaky", "It crashes the browser", "It only works in Firefox"], "answer": 1, "explain": "Auto-waiting + expect retries replace fixed sleeps."},
            {"q": "pytest --headed does what?", "options": ["Runs faster", "Shows the browser window", "Runs only header tests", "Generates a report"], "answer": 1, "explain": "Default is headless; --headed shows the browser."},
            {"q": "expect(locator).to_be_visible() will…", "options": ["Fail immediately if not visible", "Retry until visible or timeout", "Click the element", "Hide the element"], "answer": 1, "explain": "Web-first assertions retry up to the timeout."},
        ],
        "advanced": [
            {"q": "Main benefit of Page Object Model?", "options": ["Faster browsers", "Locators and actions in one place → easier maintenance", "No need for assertions", "Runs tests in parallel"], "answer": 1, "explain": "UI change → update one page class, not every test."},
            {"q": "What is 'page' in def test_x(page: Page)?", "options": ["A global variable", "A pytest fixture provided by pytest-playwright", "A Python keyword", "A class you must create"], "answer": 1, "explain": "Fixtures are injected by name."},
            {"q": "Which tool records your actions into code?", "options": ["playwright trace", "playwright codegen", "pytest record", "newman"], "answer": 1, "explain": "playwright codegen <url>"},
            {"q": "A 'flaky' test is one that…", "options": ["Always fails", "Passes and fails randomly without code changes", "Is very slow", "Has no assertions"], "answer": 1, "explain": "Often caused by timing issues or shared test data."},
        ],
        "expert": [
            {"q": "Best way to skip the login UI in 50 tests?", "options": ["Log in via UI each time", "Log in once and reuse storage_state (saved cookies)", "Disable auth on the server", "Use sleep"], "answer": 1, "explain": "storage_state saves auth state so tests start logged in."},
            {"q": "page.route('**/api/users', handler) is used for…", "options": ["Navigation", "Intercepting/mocking network requests", "Taking screenshots", "Counting elements"], "answer": 1, "explain": "Network interception lets you mock or block API calls."},
            {"q": "How to debug a CI failure you can't reproduce locally?", "options": ["Rerun forever", "Enable tracing and open the trace in Trace Viewer", "Add more sleeps", "Delete the test"], "answer": 1, "explain": "Traces include DOM snapshots, network and console for each step."},
            {"q": "Running tests in parallel with pytest uses…", "options": ["pytest -n auto (pytest-xdist)", "pytest --fast", "playwright parallel", "It's not possible"], "answer": 0, "explain": "pytest-xdist distributes tests across workers."},
        ],
    },
    "practical": {
        "easy": [
            {"type": "scenario", "q": "Which line clicks a button labelled 'Submit'?", "options": ["page.get_by_role('button', name='Submit').click()", "page.click.button('Submit')", "page.goto('Submit')", "expect('Submit').click()"], "answer": 0, "explain": "Locator first, then the action."},
            {"type": "scenario", "q": "Which line checks the page shows 'Welcome'?", "options": ["print('Welcome')", "expect(page.get_by_text('Welcome')).to_be_visible()", "page.fill('Welcome')", "assert page == 'Welcome'"], "answer": 1, "explain": "expect(...).to_be_visible() is a web-first assertion."},
        ],
        "medium": [
            {"type": "scenario", "q": "The email input has <label>Email</label>. Best locator?", "options": ["page.locator('/html/body/form/input[1]')", "page.get_by_label('Email')", "page.locator('input')", "page.get_by_text('input')"], "answer": 1, "explain": "get_by_label is readable and stable."},
            {"type": "scenario", "q": "After login, URL should be /dashboard. Which assertion?", "options": ["expect(page).to_have_url(re.compile('.*/dashboard'))", "page.url = '/dashboard'", "expect(page).to_be_visible()", "page.goto('/dashboard')"], "answer": 0, "explain": "to_have_url accepts a string or regex."},
        ],
        "advanced": [
            {"type": "scenario", "q": "Test fails: 'strict mode violation: locator resolved to 3 elements'. Fix?", "options": ["Add sleep", "Make the locator more specific (role + name, test id, or .first if intended)", "Run headed", "Ignore it"], "answer": 1, "explain": "Playwright locators are strict – they must match exactly one element for actions."},
            {"type": "scenario", "q": "You test login with 10 username/password combinations. Best approach?", "options": ["Write 10 copies of the test", "@pytest.mark.parametrize with the 10 data sets", "One test with a for loop and no assertions", "Manual testing"], "answer": 1, "explain": "Parametrize = data-driven, each case reported separately."},
        ],
        "expert": [
            {"type": "scenario", "q": "UI test for 'order history' is slow because it first creates orders through the UI. Better approach?", "options": ["Keep it", "Create orders via API in setup, then verify in the UI", "Remove the test", "Add retries"], "answer": 1, "explain": "Use APIs for setup; keep the UI only for what you're actually testing."},
            {"type": "scenario", "q": "A third-party payment widget makes tests flaky. Best option?", "options": ["Skip all checkout tests", "Mock the payment API with page.route for most tests, and keep one real end-to-end test", "Add sleep(10)", "Test only in production"], "answer": 1, "explain": "Mock for stability, plus a small real E2E check."},
        ],
    },
}

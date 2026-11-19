TOPIC = {
    "slug": "testing",
    "title": "Testing Basics",
    "icon": "🧪",
    "summary": "SDLC, STLC, types of testing, bug life cycle, test cases",
    "lesson": r"""
## 1. What is software testing?
Testing means **checking that the software does what it should, and finding problems before users do.**

> Example: On a shopping site, you check that adding 2 items to the cart shows the correct total.

---

## 2. SDLC – Software Development Life Cycle
How software is built, step by step:

| Step | What happens | Example |
|---|---|---|
| 1. Requirements | Client says what they want | "Users must log in with email + OTP" |
| 2. Design | Team plans how to build it | Screens, database tables |
| 3. Development | Developers write code | Login page is coded |
| 4. **Testing** | Testers check it | You test login with right/wrong OTP |
| 5. Deployment | It goes live | Users can use it |
| 6. Maintenance | Fix bugs, add features | OTP resend button added |

<div class="viz" data-viz="sdlc"></div>

**Models**
- **Waterfall** – one step after another, testing only at the end. Slow to change.
- **Agile** – small 2-week cycles called **sprints**. Build a little, test a little, every sprint. Most companies use this.
- **V-Model** – every development step has a matching testing step (requirements ↔ acceptance testing, design ↔ system testing).

---

## 3. STLC – Software Testing Life Cycle
The tester's own process:

1. **Requirement analysis** – read requirements, ask questions, find what is testable.
2. **Test planning** – decide scope, tools, people, timeline. Output: *Test Plan*.
3. **Test case design** – write test cases + prepare test data.
4. **Environment setup** – test server, logins, data ready.
5. **Test execution** – run test cases, mark Pass/Fail, log bugs.
6. **Test closure** – summary report: what passed, failed, open bugs, lessons learned.

<div class="viz" data-viz="stlc"></div>

> 💡 In interviews say: "In my current role I do test case design, execution and bug reporting."

---

## 4. Types of testing

### Functional (WHAT the system does)
- **Unit testing** – developers test one small function.
- **Integration testing** – modules working together. *Login → Dashboard loads user name.*
- **System testing** – the full application end-to-end.
- **UAT (User Acceptance Testing)** – client/business users check before go-live.

### Quick checks on a new build
- **Smoke testing** – "Does the build even work?" Open app, log in, main pages load. If smoke fails, testing stops.
- **Sanity testing** – a quick check of **one specific fix or feature**.
- **Regression testing** – re-test **old features** to make sure a new change didn't break them.

> Example: Developer fixes "Forgot password".
> - Checking the fix works → **Sanity**
> - Checking login, signup, profile still work → **Regression**

### Non-functional (HOW WELL it works)
- **Performance** – speed under load (1,000 users at once).
- **Security** – can someone hack it? (SQL injection, weak passwords)
- **Usability** – is it easy to use?
- **Compatibility** – works on Chrome, Firefox, Android, iPhone?

### Box testing
- **Black box** – test without seeing code (inputs → outputs). *What you do now.*
- **White box** – test with knowledge of code (developers, unit tests).
- **Grey box** – a bit of both (e.g. you check the database after a UI action).

---

## 5. Test case – how to write one
| Field | Example |
|---|---|
| ID | TC_LOGIN_01 |
| Title | Login with valid email and password |
| Pre-condition | User is registered |
| Steps | 1. Open login page 2. Enter email 3. Enter password 4. Click Login |
| Test data | test@mail.com / Pass@123 |
| Expected result | Dashboard opens with user name |
| Actual result | (filled during execution) |
| Status | Pass / Fail |

**Positive test** = valid input (correct password). **Negative test** = invalid input (wrong password, empty field).

### Test design techniques
- **Equivalence Partitioning** – split inputs into groups; test one from each. Age field 18–60 → test 10 (invalid), 30 (valid), 70 (invalid).
- **Boundary Value Analysis (BVA)** – test edges: 17, 18, 19 and 59, 60, 61. Most bugs hide at boundaries!
- **Decision table** – for combinations of conditions (e.g. discount = member AND order > ₹1000).
- **Error guessing** – use experience: special characters, very long text, blank spaces.

---

## 6. Bug life cycle
`New → Assigned → Open → Fixed → Retest → Closed`

Other states: **Reopened** (fix didn't work), **Rejected** (not a bug), **Deferred** (fix later), **Duplicate**.

<div class="viz" data-viz="buglife"></div>

### Severity vs Priority
- **Severity** = how badly it breaks the system (tester decides).
- **Priority** = how soon it must be fixed (business/manager decides).

| Example | Severity | Priority |
|---|---|---|
| Payment page crashes | High | High |
| Company logo misspelled on home page | Low | **High** |
| App crashes on a rarely used old report | High | Low |
| Typo in Help page | Low | Low |

### A good bug report
Title, steps to reproduce, expected vs actual result, environment (browser, version), severity, priority, screenshot/video.

---

## ✍️ Practice
Pick one module you tested at work. Write: which STLC steps you did, which testing types you did, and one bug with severity + priority.
""",
    "resources": [
        {"kind": "youtube", "title": "STLC explained (search)", "url": "https://www.youtube.com/results?search_query=STLC+software+testing+life+cycle"},
        {"kind": "youtube", "title": "Smoke vs Sanity vs Regression (search)", "url": "https://www.youtube.com/results?search_query=smoke+vs+sanity+vs+regression+testing"},
        {"kind": "youtube", "title": "Boundary Value Analysis (search)", "url": "https://www.youtube.com/results?search_query=boundary+value+analysis+equivalence+partitioning"},
        {"kind": "link", "title": "ISTQB – Foundation Level syllabus (official site)", "url": "https://www.istqb.org/"},
        {"kind": "link", "title": "Guru99 – Software Testing tutorial", "url": "https://www.guru99.com/software-testing.html"},
    ],
    "theory": {
        "easy": [
            {"q": "What does STLC stand for?", "options": ["Software Testing Life Cycle", "System Test Logic Check", "Software Tool Life Cycle", "Standard Test Level Chart"], "answer": 0, "explain": "STLC is the tester's process: analysis → planning → design → setup → execution → closure."},
            {"q": "Which testing checks that a new build's main features work at all?", "options": ["Regression", "Smoke", "Performance", "UAT"], "answer": 1, "explain": "Smoke testing is a quick 'does it even work?' check on a new build."},
            {"q": "Testing without looking at the code is called…", "options": ["White box", "Unit testing", "Black box", "Code review"], "answer": 2, "explain": "Black box = inputs and outputs only, no code knowledge."},
            {"q": "Who usually performs UAT?", "options": ["Developers", "Testers only", "Client / business users", "Database admin"], "answer": 2, "explain": "User Acceptance Testing is done by the client or business users before go-live."},
        ],
        "medium": [
            {"q": "A developer fixed a bug. You re-test old features to ensure nothing else broke. This is…", "options": ["Sanity testing", "Regression testing", "Smoke testing", "Unit testing"], "answer": 1, "explain": "Regression = re-testing existing features after a change."},
            {"q": "Severity is decided mainly by…", "options": ["The client", "The tester, based on impact", "The developer", "The HR team"], "answer": 1, "explain": "Severity = technical impact, set by the tester. Priority = urgency, set by business/manager."},
            {"q": "Which is the correct order in STLC?", "options": ["Planning → Analysis → Execution → Design", "Analysis → Planning → Design → Execution", "Design → Planning → Execution → Closure", "Execution → Design → Planning → Analysis"], "answer": 1, "explain": "Requirement analysis → Test planning → Test case design → Env setup → Execution → Closure."},
            {"q": "A bug fix didn't work when retested. The bug status becomes…", "options": ["Closed", "Deferred", "Reopened", "Rejected"], "answer": 2, "explain": "If the fix fails retest, the bug is Reopened."},
        ],
        "advanced": [
            {"q": "Age field accepts 18 to 60. Which set is the best Boundary Value Analysis?", "options": ["18, 30, 60", "17, 18, 19, 59, 60, 61", "0, 100", "20, 40, 50"], "answer": 1, "explain": "BVA tests just below, on, and just above each boundary."},
            {"q": "Company name misspelled on the home page. Best classification?", "options": ["High severity, High priority", "Low severity, High priority", "High severity, Low priority", "Low severity, Low priority"], "answer": 1, "explain": "It doesn't break functionality (low severity) but is very visible to customers (high priority)."},
            {"q": "In the V-Model, acceptance testing corresponds to which development phase?", "options": ["Coding", "Module design", "Requirements analysis", "Architecture design"], "answer": 2, "explain": "V-Model pairs requirements ↔ acceptance testing, system design ↔ system testing, etc."},
            {"q": "Checking the database after submitting a form in the UI is an example of…", "options": ["Black box", "White box", "Grey box", "Unit testing"], "answer": 2, "explain": "Grey box: you test via UI but use some internal knowledge (DB) to verify."},
        ],
        "expert": [
            {"q": "Which statement about exhaustive testing is correct?", "options": ["It is always required before release", "It is impossible except for trivial cases, so we use risk-based testing", "Automation makes it easy", "It means running regression daily"], "answer": 1, "explain": "A core ISTQB principle: exhaustive testing is impossible, so prioritise by risk."},
            {"q": "'Pesticide paradox' means…", "options": ["Tests damage the system", "Repeating the same tests stops finding new bugs", "Too many bugs slow developers", "Automation replaces manual testing"], "answer": 1, "explain": "Tests must be reviewed and updated, or they stop finding new defects."},
            {"q": "Discount applies only if user is a member AND cart > ₹1000. Which technique fits best?", "options": ["BVA only", "Decision table testing", "Error guessing", "Smoke testing"], "answer": 1, "explain": "Decision tables cover combinations of conditions (member Y/N × cart >1000 Y/N)."},
            {"q": "Entry criteria for test execution typically include…", "options": ["All bugs closed", "Test environment ready, build deployed, test cases reviewed", "Client sign-off", "Production release done"], "answer": 1, "explain": "Entry criteria define when testing can start; exit criteria define when it can stop."},
        ],
    },
    "practical": {
        "easy": [
            {"type": "scenario", "q": "Login page: which is a NEGATIVE test case?", "options": ["Valid email + valid password", "Valid email + wrong password", "Click 'Remember me' with valid login", "Login and check dashboard name"], "answer": 1, "explain": "Negative tests use invalid input and expect an error."},
            {"type": "scenario", "q": "New build arrives at 10 AM. What do you run FIRST?", "options": ["Full regression", "Performance test", "Smoke test", "UAT"], "answer": 2, "explain": "Smoke first: if the build is broken, no point running anything else."},
        ],
        "medium": [
            {"type": "scenario", "q": "A password field must be 8–16 characters. Which lengths should you test with BVA?", "options": ["8 and 16 only", "7, 8, 9, 15, 16, 17", "1, 10, 20", "0 and 100"], "answer": 1, "explain": "Test just below, on and just above each boundary."},
            {"type": "scenario", "q": "Your bug report says 'Login not working'. What's MOST missing?", "options": ["Your name", "Steps to reproduce + expected vs actual result", "Developer's name", "Release date"], "answer": 1, "explain": "A developer must be able to reproduce it: steps, data, expected vs actual, environment."},
        ],
        "advanced": [
            {"type": "scenario", "q": "Release is tomorrow; you have 2 hours and 300 regression cases. Best approach?", "options": ["Run cases in ID order", "Risk-based: run high-priority cases for changed & critical modules", "Skip testing", "Only run newest cases"], "answer": 1, "explain": "With limited time, prioritise by risk and business criticality."},
            {"type": "scenario", "q": "A bug only happens on Safari on iPhone. Which testing type found it?", "options": ["Compatibility testing", "Unit testing", "Load testing", "Smoke testing"], "answer": 0, "explain": "Compatibility testing covers browsers, devices and OS versions."},
        ],
        "expert": [
            {"type": "scenario", "q": "Developer says 'Works on my machine' and rejects your bug. Best next step?", "options": ["Close the bug", "Argue in the team chat", "Share exact environment, data, video/logs and reproduce together", "Raise it to the client"], "answer": 2, "explain": "Give evidence and reproduce together; environment differences are a common cause."},
            {"type": "scenario", "q": "Same critical bug keeps coming back in each release. What should QA propose?", "options": ["Test it manually every time", "Add an automated regression test for it and do root cause analysis", "Mark it Deferred", "Lower its severity"], "answer": 1, "explain": "Automate the regression check and find the root cause so it stops recurring."},
        ],
    },
}

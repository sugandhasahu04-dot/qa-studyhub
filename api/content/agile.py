TOPIC = {
    "slug": "agile",
    "title": "Agile, Scrum & JIRA",
    "icon": "🏃",
    "summary": "Sprints, ceremonies, user stories, JIRA bug tickets, tester's role",
    "lesson": r"""
## Agile in one line
Build software in **small pieces**, get feedback often, and improve every cycle – instead of one big release at the end.

## Scrum – the most common Agile method
Work happens in **sprints** (usually 2 weeks).

### Roles
| Role | Job |
|---|---|
| **Product Owner** | Decides *what* to build, owns the backlog, sets priority |
| **Scrum Master** | Removes blockers, runs the process |
| **Dev Team** | Developers + **testers** who build and test |

### Ceremonies (meetings)
| Meeting | When | What testers do |
|---|---|---|
| **Sprint Planning** | Start of sprint | Estimate testing effort, ask questions on stories |
| **Daily Stand-up** (15 min) | Every day | Yesterday / today / blockers |
| **Sprint Review / Demo** | End of sprint | Show tested features |
| **Retrospective** | After review | What went well, what to improve |
| **Backlog Refinement** | Mid-sprint | Clarify upcoming stories, acceptance criteria |



<div class="viz" data-viz="sprint"></div>

### Artifacts
- **Product Backlog** – full to-do list for the product.
- **Sprint Backlog** – items chosen for this sprint.
- **Increment** – working software at sprint end.

---

## User story
Format: **As a** *type of user*, **I want** *something*, **so that** *benefit*.
> As a **customer**, I want to **reset my password**, so that I can **log in if I forget it**.

**Acceptance criteria** (what must be true – you test these!):
- Reset link sent to the registered email
- Link expires after 30 minutes
- Error shown for unregistered email

Often written as **Given / When / Then**:
> **Given** I am on the login page, **When** I click "Forgot password" and enter a registered email, **Then** I receive a reset link.

**Story points** – rough size of work (1, 2, 3, 5, 8…), not hours.
**Definition of Done (DoD)** – checklist for "finished": coded, reviewed, **tested**, no open critical bugs.

---

## JIRA basics
JIRA is the tool where stories, tasks and bugs live.

- **Issue types**: Epic (big feature) → Story → Task / Sub-task, and **Bug**.
- **Board**: columns like *To Do → In Progress → In Review → QA → Done*.
- **Good bug ticket in JIRA**:
  - Summary: *"Cart total ignores discount code on checkout page"*
  - Steps to reproduce, Expected, Actual
  - Environment (QA server, Chrome 120)
  - Severity / Priority, Attachments (screenshot/video)
  - Link to the related story

## Tester's role in Agile
- Join early: review stories and acceptance criteria in refinement.
- Test **during** the sprint, not after.
- Automate regression so each sprint stays fast.
- "Shift-left" = test earlier in the cycle to find bugs cheaper.
""",
    "resources": [
        {"kind": "pdf", "title": "The Scrum Guide (official, free)", "url": "https://scrumguides.org/scrum-guide.html"},
        {"kind": "link", "title": "Atlassian – Agile coach", "url": "https://www.atlassian.com/agile"},
        {"kind": "link", "title": "Atlassian – JIRA tutorial", "url": "https://www.atlassian.com/software/jira/guides"},
        {"kind": "youtube", "title": "Agile Scrum for testers (search)", "url": "https://www.youtube.com/results?search_query=agile+scrum+for+testers"},
    ],
    "theory": {
        "easy": [
            {"q": "A sprint usually lasts…", "options": ["1 day", "1–4 weeks (often 2)", "6 months", "1 year"], "answer": 1, "explain": "Most teams use 2-week sprints."},
            {"q": "Who decides the priority of backlog items?", "options": ["Scrum Master", "Product Owner", "Tester", "HR"], "answer": 1, "explain": "The Product Owner owns and orders the backlog."},
            {"q": "Daily stand-up is about…", "options": ["1 hour", "15 minutes", "Half a day", "No fixed time"], "answer": 1, "explain": "A short daily sync: yesterday, today, blockers."},
            {"q": "In JIRA, a defect is logged as issue type…", "options": ["Epic", "Bug", "Story", "Theme"], "answer": 1, "explain": "Bug."},
        ],
        "medium": [
            {"q": "User story format?", "options": ["Given/When/Then only", "As a <user>, I want <goal>, so that <benefit>", "Steps/Expected/Actual", "Title/Priority"], "answer": 1, "explain": "Acceptance criteria are often Given/When/Then."},
            {"q": "Which meeting discusses what to improve in the process?", "options": ["Sprint Planning", "Retrospective", "Sprint Review", "Stand-up"], "answer": 1, "explain": "Retro = inspect and adapt the way the team works."},
            {"q": "Story points measure…", "options": ["Exact hours", "Relative size/effort of work", "Number of bugs", "Salary"], "answer": 1, "explain": "Relative estimation, often Fibonacci numbers."},
            {"q": "The Scrum Master mainly…", "options": ["Writes code", "Removes blockers and coaches the team on Scrum", "Decides priorities", "Approves salaries"], "answer": 1, "explain": "A servant-leader for the team."},
        ],
        "advanced": [
            {"q": "Definition of Done is…", "options": ["The PO's wish list", "A shared checklist every item must meet to be 'done' (incl. testing)", "A JIRA status", "The release date"], "answer": 1, "explain": "Typically: coded, reviewed, tested, documented."},
            {"q": "'Shift-left testing' means…", "options": ["Testing only at the end", "Testing earlier in the lifecycle", "Moving testers to another team", "Testing on the left monitor"], "answer": 1, "explain": "Earlier testing = cheaper bug fixes."},
            {"q": "An Epic is…", "options": ["A small bug", "A large body of work split into stories", "A sprint", "A test case"], "answer": 1, "explain": "Epic → Stories → Tasks."},
            {"q": "Acceptance criteria are written mainly to…", "options": ["Estimate cost", "Define conditions a story must satisfy to be accepted", "Assign developers", "Plan holidays"], "answer": 1, "explain": "Testers derive test cases from them."},
        ],
        "expert": [
            {"q": "Velocity is…", "options": ["Speed of the server", "Story points completed per sprint, used for planning", "Number of testers", "Bugs per day"], "answer": 1, "explain": "Used to forecast how much fits in future sprints."},
            {"q": "BDD (Behaviour Driven Development) uses…", "options": ["Given/When/Then scenarios shared by business, dev and QA", "Only unit tests", "No tests", "Waterfall phases"], "answer": 0, "explain": "Tools like Cucumber/behave turn these into automated tests."},
            {"q": "Story is 'done' in dev but QA finds a critical bug on the last sprint day. Correct handling?", "options": ["Mark it done anyway", "It doesn't meet DoD – it goes back, isn't counted as done this sprint", "Delete the bug", "Lower severity"], "answer": 1, "explain": "Only items meeting DoD count toward the increment."},
            {"q": "Kanban differs from Scrum mainly by…", "options": ["No board", "Continuous flow with WIP limits instead of fixed sprints", "No testers", "Longer meetings"], "answer": 1, "explain": "Kanban limits work-in-progress and has no fixed-length sprints."},
        ],
    },
    "practical": {
        "easy": [
            {"type": "scenario", "q": "In stand-up you say you're blocked because the QA server is down. Who should help remove it?", "options": ["Product Owner", "Scrum Master (with the team)", "Client", "Nobody"], "answer": 1, "explain": "Removing blockers is a key Scrum Master duty."},
            {"type": "scenario", "q": "Best JIRA bug summary?", "options": ["Not working", "Cart total ignores discount code on checkout page", "URGENT!!!", "Bug in app"], "answer": 1, "explain": "Specific: what, where, what's wrong."},
        ],
        "medium": [
            {"type": "scenario", "q": "A story has no acceptance criteria. As a tester you…", "options": ["Guess and test", "Ask the PO in refinement to add clear acceptance criteria", "Skip testing", "Reject the sprint"], "answer": 1, "explain": "Clarify early – shift-left."},
            {"type": "scenario", "q": "Write a test from: 'Reset link expires after 30 minutes'. Which is right?", "options": ["Click link after 31 minutes → expect 'link expired' message", "Click link immediately only", "Check email subject", "Test login"], "answer": 0, "explain": "Test the boundary: after expiry the link must not work (and also check at 29 minutes)."},
        ],
        "advanced": [
            {"type": "scenario", "q": "Sprint ends tomorrow; 3 stories untested. Best action?", "options": ["Mark them done", "Tell the team in stand-up, prioritise by risk, and don't count untested stories as done", "Work all night silently", "Blame developers"], "answer": 1, "explain": "Be transparent; DoD protects quality."},
            {"type": "scenario", "q": "Same type of bug appears every sprint. What do you raise in the retro?", "options": ["Nothing", "Root cause + a fix like adding a unit/automated test or a checklist item", "Ask for a new tester", "Lower severity"], "answer": 1, "explain": "Retros exist to improve the process."},
        ],
        "expert": [
            {"type": "scenario", "q": "Regression takes 3 days and the sprint is 2 weeks. Best long-term fix?", "options": ["Skip regression", "Automate stable high-value regression cases and run them in CI", "Hire more manual testers only", "Longer sprints"], "answer": 1, "explain": "Automation keeps regression fast every sprint."},
            {"type": "scenario", "q": "Write a Given/When/Then for: 'show an error for an unregistered email'.", "options": ["Given I'm on Forgot Password, When I enter an unregistered email and submit, Then I see 'Email not found'", "When login, Then dashboard", "Given email, Then error", "Click submit"], "answer": 0, "explain": "Clear precondition, action and expected result."},
        ],
    },
}

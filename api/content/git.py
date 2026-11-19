TOPIC = {
    "slug": "git",
    "title": "Git & GitHub",
    "icon": "🌿",
    "summary": "init, add, commit, push, branches, pull requests, README",
    "lesson": r"""
## What is Git?
**Git** saves versions of your code (like "Save As" with history). **GitHub** is a website that stores your Git projects online – recruiters can see your work there.

---

## 1. One-time setup
```text
git config --global user.name "Sugandha"
git config --global user.email "you@mail.com"
```

## 2. The basic flow ⭐
```text
git init                     # start tracking this folder
git status                   # what changed?
git add .                    # stage all changes
git commit -m "Add login tests"   # save a version
git log --oneline            # see history
```
Think of it as: **edit → add (put in box) → commit (seal the box with a label)**.

<div class="viz" data-viz="git"></div>



## 3. Put it on GitHub
1. On github.com → **New repository** → name it `qa-automation-portfolio`.
2. Then:
```text
git remote add origin https://github.com/<you>/qa-automation-portfolio.git
git branch -M main
git push -u origin main
```
Next time just: `git add .` → `git commit -m "..."` → `git push`.

## 4. Get changes
```text
git clone <url>     # copy a repo to your laptop (first time)
git pull            # get latest changes
```

---

## 5. Branches
Work on a feature without touching `main`:
```text
git checkout -b add-cart-tests    # create + switch
# ...edit, add, commit...
git push -u origin add-cart-tests
```
Then open a **Pull Request (PR)** on GitHub → teammate reviews → **Merge** into main.

## 6. Merge conflict
Happens when two people change the same line. Git marks it:
```text
<<<<<<< HEAD
timeout = 5
=======
timeout = 10
>>>>>>> add-cart-tests
```
Keep the right line, delete the markers, then `git add` + `git commit`.

## 7. .gitignore
A file listing what NOT to upload:
```text
__pycache__/
.venv/
*.log
.env
```
Never commit passwords or tokens!

## 8. A good README for your portfolio
- What the project tests (e.g. "Login and cart tests for SauceDemo")
- Tools: Python, Playwright, pytest
- How to run: `pip install -r requirements.txt` → `pytest`
- Screenshot of a test report
""",
    "resources": [
        {"kind": "pdf", "title": "Pro Git book (free online + PDF download)", "url": "https://git-scm.com/book/en/v2"},
        {"kind": "link", "title": "GitHub Skills – free interactive courses", "url": "https://skills.github.com/"},
        {"kind": "link", "title": "Learn Git Branching (visual game)", "url": "https://learngitbranching.js.org/"},
        {"kind": "youtube", "title": "Git and GitHub for beginners (search)", "url": "https://www.youtube.com/results?search_query=git+and+github+for+beginners"},
    ],
    "theory": {
        "easy": [
            {"q": "Which command saves a version with a message?", "options": ["git push", "git commit -m \"msg\"", "git save", "git add"], "answer": 1, "explain": "commit records a snapshot locally."},
            {"q": "Which command uploads commits to GitHub?", "options": ["git pull", "git push", "git clone", "git init"], "answer": 1, "explain": "push sends local commits to the remote."},
            {"q": "git status shows…", "options": ["Your GitHub followers", "Changed, staged and untracked files", "The commit history graph", "Network status"], "answer": 1, "explain": "Use it often to see what's going on."},
            {"q": "git clone is used to…", "options": ["Delete a repo", "Copy a remote repo to your machine", "Create a branch", "Merge code"], "answer": 1, "explain": "First-time download of a repository."},
        ],
        "medium": [
            {"q": "What does git add . do?", "options": ["Commits everything", "Stages all changes for the next commit", "Pushes to GitHub", "Creates a branch"], "answer": 1, "explain": "add = stage; commit = save."},
            {"q": "Purpose of a branch?", "options": ["Backup to cloud", "Work on changes separately without affecting main", "Delete history", "Speed up git"], "answer": 1, "explain": "Branches isolate work until it's reviewed and merged."},
            {"q": "What is a Pull Request?", "options": ["Downloading code", "A request to review and merge your branch into another", "A git command", "A bug report"], "answer": 1, "explain": "PRs are where code review happens."},
            {"q": ".gitignore is for…", "options": ["Ignoring bugs", "Listing files Git should not track", "Hiding commits", "Blocking users"], "answer": 1, "explain": "e.g. __pycache__/, .env, logs."},
        ],
        "advanced": [
            {"q": "git pull is roughly equal to…", "options": ["git fetch + git merge", "git push + git commit", "git clone", "git add + commit"], "answer": 0, "explain": "pull = fetch remote changes then merge them."},
            {"q": "When does a merge conflict happen?", "options": ["Every merge", "When the same lines changed differently in two branches", "When the repo is private", "When you push twice"], "answer": 1, "explain": "Git can't decide which change to keep."},
            {"q": "git checkout -b feature does what?", "options": ["Deletes feature", "Creates branch 'feature' and switches to it", "Merges feature", "Pushes feature"], "answer": 1, "explain": "Also: git switch -c feature."},
            {"q": "Safest way to undo a pushed commit on a shared branch?", "options": ["git reset --hard + force push", "git revert <commit>", "Delete the repo", "Edit history on GitHub"], "answer": 1, "explain": "revert creates a new commit that undoes the change – history stays safe."},
        ],
        "expert": [
            {"q": "git stash is used to…", "options": ["Delete changes", "Temporarily shelve uncommitted changes", "Merge branches", "Create tags"], "answer": 1, "explain": "git stash, then git stash pop to bring them back."},
            {"q": "Rebase vs merge?", "options": ["Identical", "Rebase rewrites your commits on top of another branch for a linear history; merge creates a merge commit", "Merge deletes history", "Rebase is only for GitHub"], "answer": 1, "explain": "Don't rebase shared/pushed branches."},
            {"q": "How do automated tests usually run on every push?", "options": ["Manually", "CI pipeline (e.g. GitHub Actions/Jenkins) triggered by push/PR", "git test", "Cron on your laptop"], "answer": 1, "explain": "CI runs pytest on each push or PR."},
            {"q": "You accidentally committed a password. Best action?", "options": ["Delete the line in a new commit only", "Rotate (change) the password immediately, then remove it from history", "Make repo private and forget it", "Ignore it"], "answer": 1, "explain": "Once pushed, assume it's leaked – rotate first."},
        ],
    },
    "practical": {
        "easy": [
            {"type": "scenario", "q": "You edited test_login.py. Correct order to save it to GitHub?", "options": ["push → commit → add", "add → commit → push", "commit → add → push", "clone → push"], "answer": 1, "explain": "Stage, commit, push."},
            {"type": "scenario", "q": "You want to see which files you changed. Command?", "options": ["git status", "git push", "git init", "git clone"], "answer": 0, "explain": "git status."},
        ],
        "medium": [
            {"type": "scenario", "q": "Push is rejected: 'remote contains work you do not have'. What first?", "options": ["git push --force", "git pull, resolve conflicts if any, then push", "Delete the repo", "git init again"], "answer": 1, "explain": "Get remote changes first; never force-push shared branches."},
            {"type": "scenario", "q": "You want to add cart tests without affecting main. Command?", "options": ["git checkout -b add-cart-tests", "git commit main", "git merge main", "git push main"], "answer": 0, "explain": "Create a feature branch."},
        ],
        "advanced": [
            {"type": "scenario", "q": "You see <<<<<<< HEAD in a file after pulling. What now?", "options": ["Push as is", "Edit to keep the correct code, remove markers, git add, git commit", "Delete the file", "git init"], "answer": 1, "explain": "That's a merge conflict to resolve manually."},
            {"type": "scenario", "q": "Your .venv folder got uploaded. Fix?", "options": ["Leave it", "Add .venv/ to .gitignore and git rm -r --cached .venv, then commit", "Delete GitHub account", "git revert everything"], "answer": 1, "explain": "Untrack it and ignore it in future."},
        ],
        "expert": [
            {"type": "scenario", "q": "Team wants tests to run on every PR automatically. You propose…", "options": ["Daily manual run", "A GitHub Actions workflow that installs deps and runs pytest on pull_request", "Emailing results", "Running only before release"], "answer": 1, "explain": "CI gives fast feedback before merge."},
            {"type": "scenario", "q": "A bug appeared somewhere in the last 40 commits. Fastest way to find which commit?", "options": ["Read every commit", "git bisect", "git stash", "git clone again"], "answer": 1, "explain": "bisect does a binary search through history."},
        ],
    },
}

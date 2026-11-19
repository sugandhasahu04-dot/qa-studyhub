# 📚 QA StudyHub

A personal study website for switching to a QA / Test Engineer role. It's built with Python (Flask), stores data in a Postgres database and is hosted on Vercel.

## How it helps you remember (learning science)
- **Guided lessons** (`/learn/<topic>`) take you through a warm-up guess (pretesting), then small parts. After each part the text hides and you recall it from memory (retrieval practice). You finish by explaining the topic simply (the Feynman technique). A 🍅 Pomodoro timer is built in.
- **Daily Review** uses spaced-repetition flashcards on the SM-2 algorithm. Cards are mixed across topics (interleaving). Wrong quiz answers automatically become cards.
- **Mixed practice** gives you shuffled questions from all the topics you've learned.
- **Animated diagrams** (dual coding) cover SDLC, STLC, the bug life cycle, GROUP BY/HAVING, JOINs, Python loops, HTTP requests, Playwright, Git and Scrum.
- **Today page** shows your plan for the day, a streak, the cards due, and how strongly you remember each topic.
- **How to learn page** explains each method and the books it comes from (Make It Stick, Oakley, Dunlosky 2013, The Learning Scientists).

## What's inside
- **7 topics**, each with a simple lesson and easy examples: Testing Basics, SQL, Python, API Testing & Postman, Playwright, Git & GitHub, Agile/Scrum/JIRA
- **Books & videos**: recommended PDFs, YouTube and websites for each topic, and you can add your own links (for example a Google Drive PDF)
- **Quizzes** at 4 levels (Easy → Medium → Advanced → Expert), in 2 types:
  - **Theory**: concept and interview questions
  - **Practical**: you write real SQL or Python that runs and is checked automatically; other topics use real-work scenarios
- **Notes**: write, edit, search and delete notes, grouped by topic
- **Console**: run Python and SQL in the browser; SQL comes with practice tables
- **Progress**: lessons done, quiz scores, and which quizzes you passed (70% or more)

## Deploy to Vercel (one time, about 15 minutes, on a laptop)

1. **Put the code on GitHub**
   - Go to github.com, click **New repository**, name it `qa-studyhub`, keep it **Private**, and create it.
   - Click **"uploading an existing file"** and drag in everything from the unzipped `studyhub` folder: `api/`, `requirements.txt`, `vercel.json`, `README.md`, `.gitignore`. Then click **Commit**.
2. **Import it into Vercel**
   - Go to vercel.com and sign up with GitHub.
   - Click **Add New → Project**, choose `qa-studyhub`, then **Deploy**.
3. **Add the database**
   - In the Vercel project, open **Storage → Create Database → Neon (Postgres)**. It has a free plan.
   - Connect it to the project. Vercel then adds `DATABASE_URL` for you.
4. **Lock it with a password** (recommended)
   - Go to **Settings → Environment Variables** and add:
     - `APP_PASSWORD` = a password you choose
     - `SECRET_KEY` = any long random text
5. **Redeploy**: go to **Deployments**, click **⋯** on the latest deployment, then **Redeploy**.

Open your `https://qa-studyhub-xxxx.vercel.app` link and add it to your phone's home screen.

## Run it on your laptop (optional)
```
pip install -r requirements.txt
python api/index.py
```
Then open http://localhost:5000. When run locally without `DATABASE_URL`, it uses a SQLite file.

## Add or change study material
Each topic is one file in `api/content/` (for example `sql.py`):
- `lesson`: Markdown text
- `resources`: links
- `theory` / `practical`: questions for each level

Edit a file on GitHub and Vercel redeploys automatically.

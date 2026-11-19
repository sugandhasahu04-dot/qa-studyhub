TOPIC = {
    "slug": "sql",
    "title": "SQL",
    "icon": "🗄️",
    "summary": "SELECT, WHERE, GROUP BY, HAVING, JOINs, interview queries",
    "lesson": r"""
## Why testers need SQL
After you do something in the app (place an order, sign up), you check the **database** to confirm the data was saved correctly. That is called **backend / database testing**.

> 💡 Try every example in the **Console → SQL** tab. It has practice tables: `employees`, `departments`, `users`, `orders`, `bugs`.

---

## 1. SELECT – get data
```sql
SELECT * FROM employees;              -- all columns
SELECT name, salary FROM employees;   -- only some columns
```

## 2. WHERE – filter rows
```sql
SELECT * FROM employees WHERE salary > 50000;
SELECT * FROM employees WHERE city = 'Pune' AND salary > 50000;
SELECT * FROM employees WHERE city IN ('Pune', 'Delhi');
SELECT * FROM employees WHERE salary BETWEEN 40000 AND 60000;
SELECT * FROM users WHERE name LIKE 'A%';     -- starts with A
SELECT * FROM users WHERE city IS NULL;       -- empty city (never use = NULL)
```

## 3. ORDER BY and LIMIT
```sql
SELECT name, salary FROM employees ORDER BY salary DESC;   -- highest first
SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3;  -- top 3
```

---

## 4. Aggregate functions
| Function | Meaning | Example |
|---|---|---|
| `COUNT(*)` | how many rows | `SELECT COUNT(*) FROM bugs;` |
| `SUM(col)` | total | `SELECT SUM(amount) FROM orders;` |
| `AVG(col)` | average | `SELECT AVG(salary) FROM employees;` |
| `MAX` / `MIN` | biggest / smallest | `SELECT MAX(salary) FROM employees;` |

## 5. GROUP BY – one result per group ⭐
Think of it as **"for each ___"**.

"How many bugs **for each** status?"
```sql
SELECT status, COUNT(*) AS total
FROM bugs
GROUP BY status;
```
| status | total |
|---|---|
| Open | 4 |
| Closed | 2 |
| ... | ... |

## 6. HAVING – filter groups ⭐
- `WHERE` filters **rows before** grouping.
- `HAVING` filters **groups after** grouping.

"Which modules have **more than 1** bug?"
```sql
SELECT module, COUNT(*) AS total
FROM bugs
GROUP BY module
HAVING COUNT(*) > 1;
```

Both together: "Among **open** bugs, which modules have more than 1?"
```sql
SELECT module, COUNT(*)
FROM bugs
WHERE status = 'Open'        -- rows first
GROUP BY module
HAVING COUNT(*) > 1;         -- then groups
```

<div class="viz" data-viz="groupby"></div>

> **Order to remember:** `SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT`

---

## 7. JOINs – combine tables ⭐
`employees.department_id` links to `departments.id`.

**INNER JOIN** – only rows that match in both tables.
```sql
SELECT e.name, d.name AS department
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;
```
Rahul has no department → he is **not** shown.

**LEFT JOIN** – all rows from the left table, matched rows from the right, **NULL** where no match.
```sql
SELECT e.name, d.name AS department
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;
```
Rahul **is** shown with department = NULL.

<div class="viz" data-viz="joins"></div>

**Find rows with no match** (very common in testing!):
```sql
-- users who never placed an order
SELECT u.name
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.id IS NULL;
```

**SELF JOIN** – a table joined to itself (employee → manager):
```sql
SELECT e.name, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

---

## 8. Classic interview queries
**Find duplicate emails**
```sql
SELECT email, COUNT(*) FROM users
GROUP BY email HAVING COUNT(*) > 1;
```
**Second highest salary**
```sql
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```
**Employees earning more than the average** (subquery)
```sql
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

## 9. Changing data (know the basics)
```sql
INSERT INTO users (name, email, city) VALUES ('Test', 't@mail.com', 'Pune');
UPDATE bugs SET status = 'Closed' WHERE id = 3;
DELETE FROM users WHERE id = 7;   -- always use WHERE!
```
- **DELETE** removes rows (can use WHERE). **TRUNCATE** removes all rows fast. **DROP** removes the whole table.
- **Primary key** = unique id of a row. **Foreign key** = column pointing to another table's primary key.
""",
    "resources": [
        {"kind": "link", "title": "SQLBolt – interactive lessons", "url": "https://sqlbolt.com/"},
        {"kind": "link", "title": "W3Schools SQL tutorial", "url": "https://www.w3schools.com/sql/"},
        {"kind": "link", "title": "HackerRank SQL practice", "url": "https://www.hackerrank.com/domains/sql"},
        {"kind": "youtube", "title": "SQL GROUP BY and HAVING (search)", "url": "https://www.youtube.com/results?search_query=sql+group+by+having+explained"},
        {"kind": "youtube", "title": "SQL Joins explained (search)", "url": "https://www.youtube.com/results?search_query=sql+joins+explained+inner+left"},
        {"kind": "youtube", "title": "SQL interview questions for testers (search)", "url": "https://www.youtube.com/results?search_query=sql+interview+questions+for+testers"},
    ],
    "theory": {
        "easy": [
            {"q": "Which keyword filters rows?", "options": ["ORDER BY", "WHERE", "GROUP BY", "SELECT"], "answer": 1, "explain": "WHERE filters individual rows."},
            {"q": "How do you check for an empty (NULL) city?", "options": ["city = NULL", "city == NULL", "city IS NULL", "city EMPTY"], "answer": 2, "explain": "NULL is compared with IS NULL / IS NOT NULL, never with =."},
            {"q": "Which sorts results highest to lowest?", "options": ["ORDER BY salary ASC", "ORDER BY salary DESC", "SORT salary DOWN", "GROUP BY salary"], "answer": 1, "explain": "DESC = descending (high → low). ASC is the default."},
            {"q": "LIKE 'A%' matches names that…", "options": ["end with A", "contain A anywhere", "start with A", "are exactly A"], "answer": 2, "explain": "% means 'any characters'. 'A%' = starts with A."},
        ],
        "medium": [
            {"q": "Difference between WHERE and HAVING?", "options": ["No difference", "WHERE filters rows before grouping; HAVING filters groups after GROUP BY", "HAVING assigns values", "WHERE works only with numbers"], "answer": 1, "explain": "WHERE → rows, HAVING → groups (works with COUNT, SUM etc.)."},
            {"q": "Which returns ALL employees, even those without a department?", "options": ["INNER JOIN departments", "LEFT JOIN departments", "WHERE department_id = id", "GROUP BY department"], "answer": 1, "explain": "LEFT JOIN keeps every row of the left table; unmatched right columns are NULL."},
            {"q": "COUNT(*) vs COUNT(city)?", "options": ["Same thing", "COUNT(*) counts all rows; COUNT(city) skips NULL cities", "COUNT(city) counts distinct cities", "COUNT(*) skips NULLs"], "answer": 1, "explain": "COUNT(column) ignores NULL values."},
            {"q": "Correct clause order?", "options": ["SELECT, WHERE, FROM, GROUP BY", "SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY", "SELECT, FROM, HAVING, WHERE", "FROM, SELECT, ORDER BY, WHERE"], "answer": 1, "explain": "SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT."},
        ],
        "advanced": [
            {"q": "Which removes the whole table structure?", "options": ["DELETE", "TRUNCATE", "DROP", "REMOVE"], "answer": 2, "explain": "DROP deletes the table itself; TRUNCATE empties it; DELETE removes chosen rows."},
            {"q": "A foreign key is…", "options": ["A unique row id", "A column that refers to the primary key of another table", "An encrypted column", "An index"], "answer": 1, "explain": "e.g. orders.user_id → users.id."},
            {"q": "To find users with NO orders you would use…", "options": ["INNER JOIN orders", "LEFT JOIN orders … WHERE orders.id IS NULL", "GROUP BY user_id", "RIGHT JOIN users"], "answer": 1, "explain": "LEFT JOIN + IS NULL finds left rows without a match."},
            {"q": "SELECT DISTINCT city FROM users returns…", "options": ["All cities with duplicates", "Each city only once", "Count of cities", "Only NULL cities"], "answer": 1, "explain": "DISTINCT removes duplicate values."},
        ],
        "expert": [
            {"q": "What is a correlated subquery?", "options": ["A subquery in FROM", "A subquery that uses a column from the outer query and runs per outer row", "Any query with JOIN", "A query with UNION"], "answer": 1, "explain": "e.g. employees earning more than their own department's average."},
            {"q": "UNION vs UNION ALL?", "options": ["Same", "UNION removes duplicates; UNION ALL keeps them (faster)", "UNION ALL removes duplicates", "UNION only works on 2 columns"], "answer": 1, "explain": "UNION does a DISTINCT; UNION ALL simply appends."},
            {"q": "Which window function gives ranks with no gaps for ties (1,2,2,3)?", "options": ["RANK()", "ROW_NUMBER()", "DENSE_RANK()", "NTILE()"], "answer": 2, "explain": "RANK gives 1,2,2,4; DENSE_RANK gives 1,2,2,3; ROW_NUMBER gives 1,2,3,4."},
            {"q": "An index mainly helps to…", "options": ["Store more data", "Speed up searching/filtering, at some cost to inserts", "Encrypt data", "Prevent NULLs"], "answer": 1, "explain": "Indexes speed reads; they slow writes slightly and use space."},
        ],
    },
    "practical": {
        "easy": [
            {"type": "sql", "q": "Show the name and salary of all employees who earn more than 50000.", "solution": "SELECT name, salary FROM employees WHERE salary > 50000;", "hint": "SELECT … FROM employees WHERE …"},
            {"type": "sql", "q": "List all bugs whose status is 'Open'. Show all columns.", "solution": "SELECT * FROM bugs WHERE status = 'Open';", "hint": "Text values go in single quotes."},
            {"type": "sql", "q": "Show employee names and salaries, highest salary first. If two salaries are equal, sort those names A–Z.", "solution": "SELECT name, salary FROM employees ORDER BY salary DESC, name ASC;", "ordered": True, "hint": "ORDER BY salary DESC, name ASC"},
        ],
        "medium": [
            {"type": "sql", "q": "Count how many employees are in each department_id. Show department_id and the count.", "solution": "SELECT department_id, COUNT(*) FROM employees GROUP BY department_id;", "hint": "GROUP BY department_id"},
            {"type": "sql", "q": "Find duplicate emails in users: show each email that appears more than once, with its count.", "solution": "SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;", "hint": "GROUP BY email HAVING COUNT(*) > 1"},
            {"type": "sql", "q": "Show each employee's name with their department name (only employees that have a department).", "solution": "SELECT e.name, d.name FROM employees e JOIN departments d ON e.department_id = d.id;", "hint": "INNER JOIN departments ON employees.department_id = departments.id"},
        ],
        "advanced": [
            {"type": "sql", "q": "Find the second highest salary in employees (one value).", "solution": "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);", "hint": "MAX of salaries lower than the MAX."},
            {"type": "sql", "q": "List names of users who have never placed an order.", "solution": "SELECT u.name FROM users u LEFT JOIN orders o ON o.user_id = u.id WHERE o.id IS NULL;", "hint": "LEFT JOIN orders … WHERE o.id IS NULL"},
            {"type": "sql", "q": "For each module, count only the bugs with severity 'Critical' or 'Major'. Show module and count.", "solution": "SELECT module, COUNT(*) FROM bugs WHERE severity IN ('Critical','Major') GROUP BY module;", "hint": "WHERE first, then GROUP BY."},
        ],
        "expert": [
            {"type": "sql", "q": "Show the name and salary of employees who earn more than the average salary of THEIR OWN department.", "solution": "SELECT e.name, e.salary FROM employees e WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.department_id = e.department_id);", "hint": "Correlated subquery: compare with AVG where department_id matches the outer row."},
            {"type": "sql", "q": "Total delivered order amount per user name, highest first. Show name and total. Only include delivered orders.", "solution": "SELECT u.name, SUM(o.amount) AS total FROM users u JOIN orders o ON o.user_id = u.id WHERE o.status = 'delivered' GROUP BY u.id, u.name ORDER BY total DESC;", "ordered": True, "hint": "JOIN, WHERE status, GROUP BY user, ORDER BY SUM DESC"},
            {"type": "sql", "q": "Show each employee's name and their manager's name (NULL if no manager).", "solution": "SELECT e.name, m.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;", "hint": "Self join with LEFT JOIN on manager_id."},
        ],
    },
}

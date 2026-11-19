TOPIC = {
    "slug": "python",
    "title": "Python",
    "icon": "🐍",
    "summary": "Syntax, loops, functions, lists, dicts, files, errors, classes",
    "lesson": r"""
## Why Python for testers?
Python is used to write **automation tests** (Playwright, Selenium, pytest, API tests). It reads almost like English.

> 💡 Run every example in **Console → Python**. Change values and see what happens.

---

## 1. Variables and printing
```python
name = "Sugandha"      # text (string)
age = 25               # whole number (int)
salary = 45000.50      # decimal (float)
is_tester = True       # True / False (bool)

print(name)
print("Hello", name)
print(f"{name} is {age} years old")   # f-string: easiest way to mix text + values
```
No `int x;` like Java/C – Python figures out the type itself.

## 2. `=` vs `==` ⭐
- `x = 5` → **store** 5 in x (assignment)
- `x == 5` → **check** if x equals 5 → gives `True` or `False`

```python
x = 5
print(x == 5)   # True
print(x == 7)   # False
```

## 3. if / elif / else
```python
marks = 72
if marks >= 80:
    print("Distinction")
elif marks >= 40:
    print("Pass")
else:
    print("Fail")
```
- Colon `:` at the end of the line.
- **Indentation (4 spaces)** decides what is inside the block – no `{ }` in Python.
- Other comparisons: `!=` (not equal), `>`, `<`, `>=`, `<=`, and `and`, `or`, `not`.

---

## 4. Loops ⭐
**Java/C style (does NOT work in Python):**
```text
for (i = 1; i <= 5; i++) { print(i) }
```
**Python style:**
```python
for i in range(1, 6):   # 1,2,3,4,5  (end number NOT included)
    print(i)
```
| You write | You get |
|---|---|
| `range(5)` | 0,1,2,3,4 |
| `range(1, 6)` | 1,2,3,4,5 |
| `range(0, 10, 2)` | 0,2,4,6,8 |

<div class="viz" data-viz="forloop"></div>

**Loop over a list directly:**
```python
browsers = ["chrome", "firefox", "safari"]
for b in browsers:
    print("Testing on", b)
```
**while loop** – repeat while a condition is true:
```python
count = 3
while count > 0:
    print(count)
    count = count - 1
```
`break` stops the loop, `continue` skips to the next round.

---

## 5. Functions ⭐
```python
def add(a, b):        # def, name, inputs (parameters), colon
    return a + b      # send the result back

result = add(2, 5)    # values come from the CALL
print(result)         # 7
```
❌ Common mistake – overwriting inputs inside the function:
```text
def add(a, b):
    a = 2        # now add(10, 20) would still use 2!
    b = 5
    return a + b
```
Default values:
```python
def greet(name="Tester"):
    return f"Hello {name}"
print(greet())          # Hello Tester
print(greet("Ravi"))    # Hello Ravi
```

---

## 6. Lists – ordered collection
```python
bugs = ["login", "cart", "payment"]
print(bugs[0])        # login  (index starts at 0)
print(bugs[-1])       # payment (last item)
bugs.append("search") # add
bugs.remove("cart")   # remove
print(len(bugs))      # 3
print("login" in bugs)  # True
```

## 7. Dictionaries – key : value pairs
```python
user = {"name": "Ravi", "role": "QA", "exp": 3}
print(user["name"])        # Ravi
user["exp"] = 4            # update
user["city"] = "Pune"      # add new key
for key, value in user.items():
    print(key, "=", value)
```
API responses (JSON) look exactly like dictionaries – that's why they matter for testers!

## 8. Strings – useful methods
```python
s = "  Hello Tester  "
print(s.strip())          # remove spaces at ends
print(s.lower(), s.upper())
print("Tester" in s)      # True
print("a,b,c".split(","))  # ['a', 'b', 'c']
print(len("tester"))      # 6
```

---

## 9. Errors – try / except
```python
try:
    num = int("abc")
except ValueError:
    print("That is not a number")
```

## 10. assert – the heart of testing
```python
expected = 7
actual = add(2, 5)
assert actual == expected, "add() is broken"
print("Test passed")
```
If the condition is False, Python raises `AssertionError` – that's how pytest marks a test as **failed**.

## 11. Classes (basics, used in Page Object Model)
```python
class LoginPage:
    def __init__(self, url):
        self.url = url
    def open(self):
        print("Opening", self.url)

page = LoginPage("https://example.com/login")
page.open()
```
""",
    "resources": [
        {"kind": "link", "title": "Official Python tutorial", "url": "https://docs.python.org/3/tutorial/"},
        {"kind": "link", "title": "W3Schools Python", "url": "https://www.w3schools.com/python/"},
        {"kind": "pdf", "title": "Think Python (free book, PDF)", "url": "https://greenteapress.com/thinkpython2/thinkpython2.pdf"},
        {"kind": "link", "title": "Automate the Boring Stuff (free online book)", "url": "https://automatetheboringstuff.com/"},
        {"kind": "youtube", "title": "Python for beginners full course (search)", "url": "https://www.youtube.com/results?search_query=python+for+beginners+full+course"},
        {"kind": "youtube", "title": "Python for testers (search)", "url": "https://www.youtube.com/results?search_query=python+for+software+testers"},
    ],
    "theory": {
        "easy": [
            {"q": "What does range(1, 6) produce?", "options": ["1 to 6", "1 to 5", "0 to 5", "1 and 6 only"], "answer": 1, "explain": "The end number is NOT included: 1,2,3,4,5."},
            {"q": "Which keyword defines a function?", "options": ["function", "func", "def", "define"], "answer": 2, "explain": "def name(params):"},
            {"q": "x = 5 does what?", "options": ["Checks if x is 5", "Stores 5 in x", "Prints 5", "Error"], "answer": 1, "explain": "= assigns. == compares."},
            {"q": "What is printed by print(len('tester'))?", "options": ["5", "6", "7", "tester"], "answer": 1, "explain": "t-e-s-t-e-r = 6 characters."},
        ],
        "medium": [
            {"q": "What does Python use instead of { } to mark a block?", "options": ["Semicolons", "Indentation", "Brackets ()", "END keyword"], "answer": 1, "explain": "Indentation (usually 4 spaces) after a colon defines the block."},
            {"q": "bugs = ['a','b','c']; bugs[-1] is…", "options": ["'a'", "'b'", "'c'", "Error"], "answer": 2, "explain": "-1 is the last item."},
            {"q": "Best description of a dictionary?", "options": ["Ordered numbers only", "Key–value pairs like {'name': 'Ravi'}", "A list of lists", "A text file"], "answer": 1, "explain": "Access values by key: user['name']."},
            {"q": "What does a function return if it has no return statement?", "options": ["0", "Empty string", "None", "Error"], "answer": 2, "explain": "Functions without return give None."},
        ],
        "advanced": [
            {"q": "Which statement makes a pytest test fail when values differ?", "options": ["print(a == b)", "assert a == b", "if a == b: pass", "return a == b"], "answer": 1, "explain": "assert raises AssertionError when False – pytest reports a failure."},
            {"q": "Which error does int('abc') raise?", "options": ["TypeError", "ValueError", "KeyError", "IndexError"], "answer": 1, "explain": "The type (str) is fine for int(), but the value can't be converted → ValueError."},
            {"q": "Output of [x*2 for x in range(3)]?", "options": ["[0, 2, 4]", "[2, 4, 6]", "[0, 1, 2]", "[1, 2, 3]"], "answer": 0, "explain": "List comprehension over 0,1,2 doubled."},
            {"q": "What is self in a class method?", "options": ["A keyword for loops", "The current object (instance)", "The class name", "A global variable"], "answer": 1, "explain": "self refers to the object the method is called on."},
        ],
        "expert": [
            {"q": "Why is def f(items=[]) risky?", "options": ["Syntax error", "The same list is shared across calls, so it keeps old values", "Lists can't be parameters", "It's slow"], "answer": 1, "explain": "Mutable defaults are created once. Use items=None and create a new list inside."},
            {"q": "What does a pytest fixture do?", "options": ["Fixes bugs automatically", "Provides reusable setup/teardown (e.g. open browser) to tests", "Generates reports", "Runs tests in parallel"], "answer": 1, "explain": "Fixtures supply setup like a logged-in page or DB connection, injected by name."},
            {"q": "with open('f.txt') as f: … What's the benefit of 'with'?", "options": ["Faster reading", "File is closed automatically even if an error happens", "Encrypts the file", "Allows writing"], "answer": 1, "explain": "Context managers clean up automatically."},
            {"q": "What does @pytest.mark.parametrize help with?", "options": ["Skipping tests", "Running one test with many sets of input data", "Measuring speed", "Mocking APIs"], "answer": 1, "explain": "Data-driven testing: same test, different inputs."},
        ],
    },
    "practical": {
        "easy": [
            {"type": "python", "q": "Print the numbers 1 to 5, each on its own line, using a for loop.", "starter": "# write your loop here\n", "test": "", "expected": "1\n2\n3\n4\n5", "solution": "for i in range(1, 6):\n    print(i)", "hint": "for i in range(1, 6):"},
            {"type": "python", "q": "Write a function add(a, b) that returns the sum of a and b.", "starter": "def add(a, b):\n    # your code\n    pass\n", "test": "print(add(2, 5))\nprint(add(10, -3))", "expected": "7\n7", "solution": "def add(a, b):\n    return a + b", "hint": "return a + b"},
            {"type": "python", "q": "Write is_pass(marks) that returns 'Pass' if marks >= 40, else 'Fail'.", "starter": "def is_pass(marks):\n    pass\n", "test": "print(is_pass(72))\nprint(is_pass(40))\nprint(is_pass(12))", "expected": "Pass\nPass\nFail", "solution": "def is_pass(marks):\n    if marks >= 40:\n        return 'Pass'\n    return 'Fail'", "hint": "if marks >= 40: return 'Pass'"},
        ],
        "medium": [
            {"type": "python", "q": "Write count_status(bugs, status) that returns how many items in the list bugs equal status.", "starter": "def count_status(bugs, status):\n    pass\n", "test": "b = ['Open','Closed','Open','Fixed','Open']\nprint(count_status(b, 'Open'))\nprint(count_status(b, 'Fixed'))\nprint(count_status(b, 'Rejected'))", "expected": "3\n1\n0", "solution": "def count_status(bugs, status):\n    count = 0\n    for b in bugs:\n        if b == status:\n            count += 1\n    return count", "hint": "Loop, compare with ==, add 1 to a counter."},
            {"type": "python", "q": "Write get_names(users) that takes a list of dictionaries like {'name': 'Ravi', 'age': 30} and returns a list of just the names.", "starter": "def get_names(users):\n    pass\n", "test": "print(get_names([{'name':'Ravi','age':30},{'name':'Neha','age':25}]))\nprint(get_names([]))", "expected": "['Ravi', 'Neha']\n[]", "solution": "def get_names(users):\n    return [u['name'] for u in users]", "hint": "Loop and append u['name'] to a new list."},
            {"type": "python", "q": "Write reverse_text(s) that returns the string reversed.", "starter": "def reverse_text(s):\n    pass\n", "test": "print(reverse_text('tester'))\nprint(reverse_text(''))", "expected": "retset\n", "solution": "def reverse_text(s):\n    return s[::-1]", "hint": "Slicing: s[::-1]"},
        ],
        "advanced": [
            {"type": "python", "q": "Write is_valid_password(p): True if length is 8–16 AND it has at least one digit, else False.", "starter": "def is_valid_password(p):\n    pass\n", "test": "for p in ['abc12345','abcdefgh','a1','abcdefghijklmnop1','Pass@1234']:\n    print(is_valid_password(p))", "expected": "True\nFalse\nFalse\nFalse\nTrue", "solution": "def is_valid_password(p):\n    return 8 <= len(p) <= 16 and any(c.isdigit() for c in p)", "hint": "len(p) and c.isdigit() for each character."},
            {"type": "python", "q": "Write count_words(text) that returns a dictionary of word → count (lowercase, split on spaces).", "starter": "def count_words(text):\n    pass\n", "test": "r = count_words('Bug fixed bug reopened BUG')\nprint(sorted(r.items()))", "expected": "[('bug', 3), ('fixed', 1), ('reopened', 1)]", "solution": "def count_words(text):\n    counts = {}\n    for w in text.lower().split():\n        counts[w] = counts.get(w, 0) + 1\n    return counts", "hint": "counts[w] = counts.get(w, 0) + 1"},
            {"type": "python", "q": "Write safe_int(value) that returns int(value), or None if it can't be converted.", "starter": "def safe_int(value):\n    pass\n", "test": "print(safe_int('42'))\nprint(safe_int('abc'))\nprint(safe_int('7'))", "expected": "42\nNone\n7", "solution": "def safe_int(value):\n    try:\n        return int(value)\n    except ValueError:\n        return None", "hint": "try / except ValueError"},
        ],
        "expert": [
            {"type": "python", "q": "Write find_duplicates(items) returning a sorted list of values that appear more than once.", "starter": "def find_duplicates(items):\n    pass\n", "test": "print(find_duplicates(['a@x.com','b@x.com','a@x.com','c@x.com','b@x.com']))\nprint(find_duplicates([1,2,3]))", "expected": "['a@x.com', 'b@x.com']\n[]", "solution": "def find_duplicates(items):\n    seen, dup = set(), set()\n    for i in items:\n        if i in seen:\n            dup.add(i)\n        seen.add(i)\n    return sorted(dup)", "hint": "Use a set of seen values."},
            {"type": "python", "q": "Create class Cart with add(item, price) and total() methods. total() returns the sum of prices.", "starter": "class Cart:\n    pass\n", "test": "c = Cart()\nc.add('Mouse', 700)\nc.add('Bag', 1800)\nprint(c.total())\nprint(Cart().total())", "expected": "2500\n0", "solution": "class Cart:\n    def __init__(self):\n        self.items = []\n    def add(self, item, price):\n        self.items.append((item, price))\n    def total(self):\n        return sum(p for _, p in self.items)", "hint": "Store items in self.items inside __init__."},
            {"type": "python", "q": "Write check_response(resp) for an API response dict. Return a list of error messages: 'bad status' if resp['status'] != 200, 'missing id' if 'id' not in resp['body'], 'bad email' if body email has no '@'. Return [] if all good.", "starter": "def check_response(resp):\n    pass\n", "test": "print(check_response({'status':200,'body':{'id':1,'email':'a@b.com'}}))\nprint(check_response({'status':404,'body':{'email':'abc'}}))", "expected": "[]\n['bad status', 'missing id', 'bad email']", "solution": "def check_response(resp):\n    errors = []\n    body = resp.get('body', {})\n    if resp.get('status') != 200:\n        errors.append('bad status')\n    if 'id' not in body:\n        errors.append('missing id')\n    if '@' not in body.get('email', ''):\n        errors.append('bad email')\n    return errors", "hint": "Build an errors list and append in order."},
        ],
    },
}

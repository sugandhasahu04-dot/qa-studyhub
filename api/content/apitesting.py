TOPIC = {
    "slug": "api",
    "title": "API Testing & Postman",
    "icon": "🔌",
    "summary": "HTTP methods, status codes, JSON, Postman tests, requests in Python",
    "lesson": r"""
## What is an API?
An **API** is how two programs talk. When you tap "Login" in an app, the app sends a **request** to the server's API, and the server sends back a **response**.

> Restaurant example: You (app) → Waiter (API) → Kitchen (server). The waiter brings back your food (response).

API testing checks the server **directly**, without the UI – faster and finds bugs earlier.

---



<div class="viz" data-viz="http"></div>

## 1. Parts of a request
| Part | Example |
|---|---|
| **URL / endpoint** | `https://reqres.in/api/users/2` |
| **Method** | GET, POST, PUT, PATCH, DELETE |
| **Headers** | `Content-Type: application/json`, `Authorization: Bearer <token>` |
| **Query params** | `?page=2` |
| **Body** (POST/PUT) | `{"name": "Ravi", "job": "QA"}` |

## 2. HTTP methods (CRUD)
| Method | Meaning | Example |
|---|---|---|
| **GET** | Read | Get user 2 |
| **POST** | Create | Create a new user |
| **PUT** | Replace / update whole record | Update user 2 completely |
| **PATCH** | Update part of record | Change only the job |
| **DELETE** | Remove | Delete user 2 |

## 3. Status codes ⭐
| Code | Meaning | When |
|---|---|---|
| **200** OK | Success | GET worked |
| **201** Created | New record created | POST worked |
| **204** No Content | Success, nothing returned | DELETE worked |
| **400** Bad Request | Your input is wrong | Missing field |
| **401** Unauthorized | Not logged in / bad token | No token |
| **403** Forbidden | Logged in but not allowed | User tries admin API |
| **404** Not Found | Resource doesn't exist | /users/9999 |
| **500** Internal Server Error | Server crashed | Bug on server side |

Easy rule: **2xx = good, 4xx = client (your) mistake, 5xx = server mistake.**

## 4. JSON
Responses usually come as JSON – it looks like a Python dictionary:
```json
{ "id": 2, "email": "janet@reqres.in", "first_name": "Janet" }
```

---

## 5. What to check in API testing
1. Status code is correct (200, 201…)
2. Response body has the right fields and values
3. Data types are right (id is a number, email is text)
4. Response time is acceptable (e.g. < 1 second)
5. **Negative cases**: missing fields → 400, wrong token → 401, wrong id → 404

## 6. Postman basics
1. Install Postman → **New → HTTP Request**.
2. Choose method, paste URL, click **Send**.
3. For POST: **Body → raw → JSON** and type the JSON.
4. Save requests in a **Collection**.
5. Use **Environments/variables**: `{{baseUrl}}/users` so you can switch dev/test servers.

### Writing tests in Postman (Scripts → Post-response tab)
```javascript
pm.test("Status is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Email is correct", function () {
    const body = pm.response.json();
    pm.expect(body.data.email).to.eql("janet.weaver@reqres.in");
});

pm.test("Response time under 1s", function () {
    pm.expect(pm.response.responseTime).to.be.below(1000);
});
```
Run the whole collection with **Collection Runner**, or from the command line with **Newman**.

---

## 7. API test in Python (requests + pytest)
```python
import requests

def test_get_user():
    r = requests.get("https://reqres.in/api/users/2")
    assert r.status_code == 200
    body = r.json()
    assert body["data"]["id"] == 2

def test_create_user():
    r = requests.post("https://reqres.in/api/users",
                      json={"name": "Ravi", "job": "QA"})
    assert r.status_code == 201
    assert r.json()["name"] == "Ravi"
```
> Note: the Console in this app runs in your browser and can't install `requests`. Practise this on your laptop: `pip install requests pytest` then `pytest`.

## 8. Authentication types
- **API key** – a fixed key in header or URL.
- **Bearer token / JWT** – log in once, get a token, send `Authorization: Bearer <token>`.
- **Basic auth** – username:password encoded in header.
- **OAuth 2.0** – login via Google etc., returns a token.
""",
    "resources": [
        {"kind": "link", "title": "Postman Learning Center", "url": "https://learning.postman.com/"},
        {"kind": "link", "title": "ReqRes – free practice API", "url": "https://reqres.in/"},
        {"kind": "link", "title": "JSONPlaceholder – free fake API", "url": "https://jsonplaceholder.typicode.com/"},
        {"kind": "link", "title": "MDN – HTTP status codes", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status"},
        {"kind": "youtube", "title": "Postman API testing tutorial (search)", "url": "https://www.youtube.com/results?search_query=postman+api+testing+tutorial+for+beginners"},
        {"kind": "youtube", "title": "API testing with Python requests (search)", "url": "https://www.youtube.com/results?search_query=api+testing+python+requests+pytest"},
    ],
    "theory": {
        "easy": [
            {"q": "Which method is used to READ data?", "options": ["POST", "GET", "DELETE", "PUT"], "answer": 1, "explain": "GET reads. POST creates. PUT/PATCH update. DELETE removes."},
            {"q": "Status 404 means…", "options": ["Success", "Server crashed", "Resource not found", "Created"], "answer": 2, "explain": "404 = Not Found."},
            {"q": "Which status code usually means a record was created?", "options": ["200", "201", "400", "500"], "answer": 1, "explain": "201 Created is the typical POST success."},
            {"q": "API responses are usually in which format?", "options": ["PDF", "JSON", "Excel", "PNG"], "answer": 1, "explain": "JSON – key/value text, like a Python dict."},
        ],
        "medium": [
            {"q": "4xx codes indicate…", "options": ["Server errors", "Client-side errors (bad request, auth)", "Success", "Redirects"], "answer": 1, "explain": "4xx = request problem; 5xx = server problem."},
            {"q": "PUT vs PATCH?", "options": ["Same", "PUT replaces the whole resource; PATCH updates part of it", "PATCH deletes", "PUT only reads"], "answer": 1, "explain": "PATCH = partial update."},
            {"q": "No token sent to a protected API. Expected status?", "options": ["200", "401", "404", "500"], "answer": 1, "explain": "401 Unauthorized = not authenticated."},
            {"q": "In Postman, where do you write assertions?", "options": ["Headers tab", "Post-response script (Tests) tab", "Body tab", "Params tab"], "answer": 1, "explain": "pm.test(...) scripts run after the response arrives."},
        ],
        "advanced": [
            {"q": "Logged-in normal user calls an admin-only API. Correct status?", "options": ["401", "403", "404", "200"], "answer": 1, "explain": "403 Forbidden: authenticated but not allowed."},
            {"q": "Which HTTP method should be idempotent (same result if repeated)?", "options": ["POST", "PUT", "Both POST and PUT", "Neither"], "answer": 1, "explain": "PUT, GET and DELETE are idempotent; POST creates a new record each time."},
            {"q": "What is Newman?", "options": ["A Postman competitor", "Command-line runner for Postman collections (used in CI)", "A JSON validator", "A load testing tool"], "answer": 1, "explain": "Newman runs collections from the terminal / Jenkins."},
            {"q": "{{baseUrl}} in Postman is…", "options": ["A comment", "A variable from an environment", "A header", "An error"], "answer": 1, "explain": "Variables let you switch environments (dev/QA/prod) easily."},
        ],
        "expert": [
            {"q": "What does JSON schema validation check?", "options": ["Response speed", "Structure: required fields and data types", "Server logs", "Database indexes"], "answer": 1, "explain": "It verifies the response shape matches a contract."},
            {"q": "A JWT token usually contains…", "options": ["The user's password", "Encoded claims (user id, expiry) signed by the server", "The database URL", "Nothing"], "answer": 1, "explain": "Header.Payload.Signature; testers check expiry and tampering."},
            {"q": "Best test for rate limiting?", "options": ["Send one request", "Send many requests quickly and expect 429 Too Many Requests", "Check 404", "Delete the API"], "answer": 1, "explain": "429 is the standard rate-limit response."},
            {"q": "Why mock an external API in tests?", "options": ["To make tests slower", "To make tests stable and independent of a third-party service", "To skip assertions", "To test UI colors"], "answer": 1, "explain": "Mocks remove flakiness from systems you don't control."},
        ],
    },
    "practical": {
        "easy": [
            {"type": "scenario", "q": "You send POST /api/users with valid data. Which assertion is MOST correct?", "options": ["Status is 404", "Status is 201 and body contains the new id", "Status is 500", "Body is empty"], "answer": 1, "explain": "Creation → 201 + created record."},
            {"type": "scenario", "q": "GET /api/users/9999 (doesn't exist). Expected?", "options": ["200 with empty body", "404 Not Found", "201", "500"], "answer": 1, "explain": "A missing resource should return 404."},
        ],
        "medium": [
            {"type": "scenario", "q": "Signup API: which is a good NEGATIVE test?", "options": ["Valid name + email", "Missing email field → expect 400", "Check response time", "Send GET instead of POST and expect 200"], "answer": 1, "explain": "Required field missing should give 400 with a clear error message."},
            {"type": "scenario", "q": "Which Postman test checks the status code?", "options": ["pm.response.to.have.status(200);", "pm.status == 200", "assert status 200", "check(200)"], "answer": 0, "explain": "pm.response.to.have.status(code) inside pm.test(...)."},
        ],
        "advanced": [
            {"type": "scenario", "q": "API returns 200 but body says {\"error\": \"invalid user\"}. What do you do?", "options": ["Pass – status is 200", "Log a bug: error responses should use a proper 4xx code", "Ignore it", "Change the test to expect 200"], "answer": 1, "explain": "Status codes must match the result; clients depend on them."},
            {"type": "scenario", "q": "You need the token from /login in all later requests. Best Postman approach?", "options": ["Copy-paste it manually each time", "Save it to an environment variable in the login test script and use {{token}}", "Hard-code it in every request", "Use a new token per request manually"], "answer": 1, "explain": "pm.environment.set('token', ...) then Authorization: Bearer {{token}}."},
        ],
        "expert": [
            {"type": "scenario", "q": "Update API: user A can change user B's profile by changing the id in the URL. This is…", "options": ["Expected behaviour", "A security bug (broken object-level authorization / IDOR) – critical", "A performance issue", "A UI bug"], "answer": 1, "explain": "IDOR / BOLA is a top API security risk – report as critical."},
            {"type": "scenario", "q": "Your API tests fail randomly because test data is shared. Best fix?", "options": ["Rerun until green", "Each test creates its own data and cleans up after", "Delete the failing tests", "Run tests slower"], "answer": 1, "explain": "Independent test data removes flakiness."},
        ],
    },
}

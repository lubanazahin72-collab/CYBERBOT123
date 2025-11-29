# CYBERBOTDJANGO2

Futuristic cyber‑themed Django 5 project that demonstrates:
- Custom user model (`Cyberbot.CustomUser`)
- Animated landing + themed login & tool pages
- Password strength + (stub) breach check endpoint
- Basic URL safety heuristic endpoint (placeholder for Google Safe Browsing)

---
## 1. Quick Start (Windows / macOS / Linux)

```bash
git clone <your-fork-or-repo-url>
cd CYBERBOTDJANGO2/CYBERBOTDJANGO2

# 1. Create & activate virtual environment (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# (cmd.exe)  .venv\Scripts\activate.bat
# (Linux/macOS)  source .venv/bin/activate

# 2. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Create .env file (see section below)

# 4. Run migrations (fresh DB)
python manage.py migrate

# 5. Create superuser (admin panel access)
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver
```

Open: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

---
## 2. Project Layout

```
CYBERBOTDJANGO2/
  manage.py
  requirements.txt
  CYBERBOTDJANGO2/              ← Django project package (settings, urls, wsgi/asgi)
  Cyberbot/                     ← Main app
    models.py (CustomUser)
    views.py
    urls.py
    templates/Cyberbot/*.html
    migrations/
  (legacy root settings.py, urls.py etc. can be deleted once comfortable)
```

> NOTE: There is an older top‑level `settings.py` and related files kept during refactor. The canonical settings module now is `CYBERBOTDJANGO2.settings` used by `manage.py`, `asgi.py`, and `wsgi.py` inside the inner package.

---
## 3. Environment Variables (`.env`)

Create a `.env` file in the project root (same folder as `manage.py`). Example:

```
SECRET_KEY=replace-this-with-a-secure-random-string
DEBUG=True
GOOGLE_SAFE_BROWSING_API_KEY=YOUR_KEY_OR_LEAVE_BLANK
```

If you do not have a Google API key yet, leave it blank; the current URL safety endpoint uses only internal heuristics.

Generate a secure key (Python snippet):

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

---
## 4. Installed Packages

| Package | Purpose |
|---------|---------|
| Django 5.2.x | Web framework |
| djangorestframework | (Future) richer API responses / serializers |
| python-decouple | Environment variable management |

---
## 5. Custom User Model

Defined in `Cyberbot/models.py` as `CustomUser` (subclasses `AbstractUser`). This allows future extension (add profile fields, etc.). Because a custom user model is used, create it BEFORE first migration in any new environment (already done here). When starting from scratch with a clean clone + new DB, normal `migrate` is sufficient—no extra steps.

---
## 6. Pages & Routes

Current user‑facing routes:

| Path | Template | Description |
|------|----------|-------------|
| `/` | `homepage.html` | Animated splash → JS redirect to `cyber.html` |
| `/cyber.html` | `cyber.html` | Secondary page after splash |
| `/login.html` | `login.html` | Futuristic modal signup/login (localStorage demo) |
| `/cyberbot.html` | `cyberbot.html` | Main interactive panel |
| `/chatbot.html` & `/chatbot/` | `chatbot.html` | Chatbot / security tools UI |

Admin: `/admin/`

> Later you can replace `.html` suffixes with semantic routes (e.g. `/login/`) by adjusting `Cyberbot/urls.py`.

---
## 7. API Endpoints (Heuristic / Stub)

Mounted under `/api/` via `CYBERBOTDJANGO2/urls.py` + `Cyberbot/urls.py`.

| Method | Path | Body JSON | Description |
|--------|------|-----------|-------------|
| POST | `/api/check-password-complete/` | `{ "password": "string" }` | Returns strength label, score, stub breach info, recommendation |
| POST | `/api/check-url-safety/` | `{ "url": "string" }` | Heuristic URL safety (keywords, length, symbols) |
| GET | `/api/` | — | Simple JSON index of available endpoints |

Example response (password):
```json
{
  "strength": {"label": "Good", "score": 4},
  "breach": {"breached": false, "count": 0},
  "recommendation": "Add special symbols"
}
```

Example response (url):
```json
{ "safe": true, "threats": [] }
```

> If you see `Unexpected token <` in the browser console: the fetch probably hit a 404 (HTML error page). Verify the URL path matches above and the server reloaded.

---
## 8. CSRF Notes

The prototype API views are decorated with `@csrf_exempt` for simplicity while testing raw `fetch`. In production you should:
1. Remove `@csrf_exempt`.
2. Include the CSRF token in AJAX headers (`X-CSRFToken`).
3. Ensure templates include `{% csrf_token %}` inside a form or provide token via cookie.

---
## 9. Running Tests (Placeholder)

No formal tests yet. Suggested structure to add later:
```
Cyberbot/tests/test_api.py
Cyberbot/tests/test_pages.py
```
Use: `python manage.py test`.

---
## 10. Common Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Unexpected token '<'` parsing JSON | 404/500 HTML returned instead of JSON | Check endpoint path & server log |
| `ModuleNotFoundError: CYBERBOTDJANGO2` | Wrong `DJANGO_SETTINGS_MODULE` | Ensure `manage.py` sets `CYBERBOTDJANGO2.settings` |
| Admin login fails after custom user add | DB created before custom user model migration | Delete `db.sqlite3` + migrations re-run in a new environment |
| Static files not loading (future) | No `STATICFILES_DIRS` folder | Create `static/` then run `collectstatic` in production |

---
## 11. Production Checklist (Future)

- Set `DEBUG=False`
- Add domain to `ALLOWED_HOSTS`
- Provide a strong `SECRET_KEY` via environment
- Serve via gunicorn/uvicorn + reverse proxy (Nginx/Caddy)
- Enable HTTPS
- Implement real password breach check (Have I Been Pwned k‑Anonymity API)
- Implement real Google Safe Browsing call (sign request with API key)
- Add rate limiting / throttling for API endpoints

---
## 12. Roadmap Ideas

1. Replace localStorage auth mock with Django `AuthenticationForm` + session login/logout.
2. Integrate DRF serializers & class-based API views.
3. Add WebSocket (channels) for live security scan feed.
4. Add unit & integration tests (pytest + coverage).
5. Dockerfile + docker-compose (PostgreSQL instead of SQLite).
6. Centralized logging & structured JSON logs.
7. Add user profile enhancements (2FA, password history, security events).

---
## 13. Security Notes

This code is a learning / prototype environment:
- Do not trust client‑side password strength alone.
- Always hash passwords (Django already uses PBKDF2 by default).
- Remove `@csrf_exempt` in production.
- Validate and sanitize any external API responses.

---
## 14. Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push branch: `git push origin feature/my-feature`
5. Open Pull Request

---
## 15. License

Specify a license (e.g. MIT) here. Until then, assume "All rights reserved".

---
## 16. Quick Commands Reference

```bash
# Start dev server
python manage.py runserver

# Make migrations (after model changes)
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell
```

---
## 17. Sample API Calls (curl)

```bash
curl -X POST http://127.0.0.1:8000/api/check-password-complete/ \
  -H "Content-Type: application/json" \
  -d '{"password": "MyP@ssw0rd!"}'

curl -X POST http://127.0.0.1:8000/api/check-url-safety/ \
  -H "Content-Type: application/json" \
  -d '{"url": "example.com/login"}'
```

---
### Enjoy exploring CyberBot ⚡

If you run into any setup issue not covered here, open an issue or ask for help.

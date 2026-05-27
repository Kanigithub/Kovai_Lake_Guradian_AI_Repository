# Kovai Lake Guardians

A volunteer coordination platform for lake cleanup drives in Coimbatore, Tamil Nadu.
Built with Django 6+ and Bootstrap 5.

---

## Features

| Module | Capabilities |
|---|---|
| **Volunteers** | Individual & NGO registration, profiles, skills, availability |
| **Events** | Create / edit events, QR-code check-in, check-out WorkLog |
| **Lakes** | Lake explorer, photo gallery (before / after), pollution level |
| **Organizer Dashboard** | Volunteer management, announcements, direct messaging, badge awards, bulk import from Excel |
| **Leaderboard & Badges** | Points-based ranking, automatic and manual badge awards |
| **AI Lake Scan** | Upload a lake photo and get an AI-generated condition report (Gemini API) |

---

## Prerequisites

- **Python 3.11 or later** — [Download](https://www.python.org/downloads/)
- **pip** — bundled with Python 3.11+
- **Git** — [Download](https://git-scm.com/downloads)
- *(Optional)* A [Google Gemini API key](https://aistudio.google.com/app/apikey) for the AI Lake Scan feature

---

## Installation & Local Setup

### Step 1 — Clone the repository

```bash
git clone <repository-url>
cd Kovai_Lake_Guradian_AI_Repository
```

---

### Step 2 — Create a virtual environment

A virtual environment isolates project dependencies from your global Python installation.

**Windows (Command Prompt)**
```cmd
python -m venv venv
```

**Windows (PowerShell) / macOS / Linux**
```bash
python -m venv venv
```

> This creates a `venv/` folder in the project root. It is already listed in `.gitignore` and will not be committed.

---

### Step 3 — Activate the virtual environment

You must activate the venv before installing packages or running the server.

**Windows — Command Prompt**
```cmd
venv\Scripts\activate
```
You will see `(venv)` prepended to your prompt when active.

**Windows — PowerShell**

PowerShell blocks scripts by default. Run this **once** to allow local scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then activate:
```powershell
venv\Scripts\Activate.ps1
```

**Windows — PowerShell (no policy change needed)**

If you cannot or do not want to change the execution policy, call the venv's Python executable directly for every command:
```powershell
# Replace   python manage.py <cmd>   with:
venv\Scripts\python.exe manage.py <cmd>

# Replace   pip install ...   with:
venv\Scripts\python.exe -m pip install ...
```

**macOS / Linux**
```bash
source venv/bin/activate
```

**Deactivate the venv at any time**
```bash
deactivate
```

---

### Step 4 — Install dependencies

With the venv active:
```bash
pip install -r requirements.txt
```

`requirements.txt` installs:

| Package | Purpose |
|---|---|
| `Django>=6.0` | Web framework |
| `Pillow` | Image processing (profile pictures, lake photos) |
| `openpyxl` | Bulk volunteer import from Excel |
| `python-dotenv` | Load environment variables from `.env` |
| `google-genai` | Gemini AI integration for Lake Scan |

Verify the installation:
```bash
pip list
```

---

### Step 5 — Configure environment variables

Create a `.env` file in the project root (the same folder as `manage.py`):

```
# .env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

- Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).
- If you skip this, the app runs normally — only the **AI Lake Scan** feature will be unavailable.
- **Never commit `.env` to version control.** It is already listed in `.gitignore`.

---

### Step 6 — Apply database migrations

```bash
python manage.py migrate
```

This creates the `db.sqlite3` database and applies all schema migrations.

---

### Step 7 — Seed sample data

```bash
python manage.py seed_data
```

Creates demo data including:
- 6 Coimbatore lakes with photos and pollution levels
- Multiple upcoming and past cleanup events
- 6 badge types
- 1 organizer account and several volunteer accounts

---

### Step 8 — Run the development server

```bash
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000/**

---

## Quick-start Checklist

```
[ ] Python 3.11+ installed
[ ] Repository cloned
[ ] Virtual environment created  (python -m venv venv)
[ ] Virtual environment activated
[ ] Dependencies installed       (pip install -r requirements.txt)
[ ] .env file created            (GEMINI_API_KEY=...)
[ ] Migrations applied           (python manage.py migrate)
[ ] Sample data seeded           (python manage.py seed_data)
[ ] Dev server running           (python manage.py runserver)
```

---

## Demo Login Credentials

| Role | Username | Password | Access |
|---|---|---|---|
| Organizer | `organizer` | `organizer123` | Full dashboard, admin tools |
| Volunteer | `arun_kumar` | `volunteer123` | Events, profile, leaderboard |

> The Django admin panel is available at **http://127.0.0.1:8000/admin/** using the organizer credentials (`organizer` / `organizer123`). The organizer account has `is_staff = True`.

---

## Project Structure

```
manage.py                         # Django project entry point
requirements.txt                  # Python dependencies
.env                              # Environment variables (create manually, not committed)
db.sqlite3                        # SQLite database (auto-created on migrate)
venv/                             # Virtual environment (not committed)
clean_lakes_project/              # Project settings, root URLs, WSGI
volunteers_app/                   # Registration, profiles, badges, leaderboard, signals
events_app/                       # Events, roles, registrations, WorkLog (check-in/out)
lakes_app/                        # Lakes, photos, pollution tracking, explorer
dashboard_app/                    # Organizer dashboard, announcements, messages, AI scan
templates/                        # Shared base templates (base.html, home.html)
static/                           # Global CSS / JS / images
media/                            # Uploaded files (auto-created on first upload)
```

---

## Key URLs

| Path | Description |
|---|---|
| `/` | Home page |
| `/volunteers/register/` | Volunteer / NGO registration |
| `/volunteers/login/` | Login |
| `/volunteers/leaderboard/` | Points leaderboard |
| `/volunteers/profile/` | Logged-in user's profile |
| `/events/` | Event listing |
| `/events/create/` | Create an event (organizer) |
| `/lakes/` | Lake explorer |
| `/dashboard/` | Organizer dashboard (login required) |
| `/dashboard/scan-lake/` | AI Lake Scan (Gemini API) |
| `/admin/` | Django admin panel |

---

## Common Commands

```bash
# Create a Django superuser manually
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic

# Reset the database and re-seed
del db.sqlite3                   # Windows CMD
python manage.py migrate
python manage.py seed_data

# Run on a different port
python manage.py runserver 8080
```

---

## Notes

- The default database is **SQLite** (`db.sqlite3`), suitable for local development. No additional database setup is required.
- Media uploads (profile pictures, lake photos) are stored in the `media/` directory, created automatically on first upload.
- `DEBUG = True` is set by default in `settings.py`. Do **not** deploy to production with this setting.
- The `SECRET_KEY` in `settings.py` is a placeholder. Replace it with a strong random key before any public deployment.

# ALIREZA — Motion Portfolio

A cinematic bilingual portfolio for a motion designer and film editor. The public site uses plain HTML, CSS and JavaScript; Django powers projects, inquiries, media uploads and the admin panel.

## Features

- English by default with instant Persian/RTL switch and saved preference
- Dark black/purple and light white/purple themes
- One continuous, smooth-scrolling page: Hero → Work → About → Services → Contact
- GSAP page entrances, card reveals, menu motion and polished route transitions
- Structured responsive layouts with native Persian/RTL typography and restrained pointer motion
- Smooth transition between black/purple and white/purple/black themes
- Accessible, responsive and reduced-motion friendly
- Persistent inquiry form with AJAX enhancement and spam honeypot
- Admin-managed work categories and YouTube video projects with bilingual titles/descriptions
- Customized Django admin at `/studio-control/`

## Run locally

1. Install Python 3.13 (the version used on Vercel).
2. Open a terminal in this folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Only if .env does not already exist:
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. All public sections live on this page. Manage work categories, YouTube projects and contact messages at `http://127.0.0.1:8000/studio-control/`.

In Studio Control, create a **Work category** first. Then create a **Work**, choose its category, paste the YouTube URL, and add the title and description. New contact-form submissions appear under **Inbox messages** immediately.

Public copy is editable under **Site texts**. Filter by section, open a row, and edit its English and Persian values. Structural keys and per-field character limits are locked so content edits cannot break the visual layout; submitted HTML is rendered as plain text.

The repeating cards shown in the Services section are managed separately under **Service cards**. Cards can be created, removed, reordered, translated, or temporarily hidden; the responsive grid adapts automatically to the number of active cards.

The site displays four designed demo projects until the first real featured project is added in the admin.

## Deploy to Vercel

See [DEPLOYMENT.md](DEPLOYMENT.md) for the Persian deployment guide, required environment variables, database migrations, admin setup, and persistent image storage.

The repository uses Vercel's native Django integration, Python 3.13, PostgreSQL in production, and automatic static collection. `vercel.json` runs migrations at build time; requests use `motionfolio/asgi.py`. No custom rewrites or API wrapper are needed.

Secrets are loaded from environment variables, then `.env.local` and `.env` for local work. Local files never override existing environment variables and are excluded from Git and Vercel uploads. Without `DATABASE_URL`, local development uses SQLite; Vercel requires PostgreSQL. Production requires `DJANGO_SECRET_KEY` and disables debug mode.

## Tests

Run tests against an isolated SQLite test database, without loading local database credentials:

```powershell
$env:PYTHON_DOTENV_DISABLED = "1"
$env:DATABASE_URL = ""
$env:DJANGO_DEBUG = "1"
python manage.py test --noinput
Remove-Item Env:PYTHON_DOTENV_DISABLED, Env:DATABASE_URL, Env:DJANGO_DEBUG
```

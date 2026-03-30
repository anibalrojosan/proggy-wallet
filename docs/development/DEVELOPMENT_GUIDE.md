# Development Guide

Instructions for setting up and working on the Proggy Wallet **Django** project.

## Local environment setup

### Prerequisites

- **uv**: Python package and project manager.
- **Docker Desktop** (or compatible engine): for PostgreSQL via Compose.
- **WSL2** (if on Windows): ensure Docker integration works for your distro.

### Database

PostgreSQL runs via Docker Compose for local development.

```bash
# Start the database in the background
docker compose up -d

# View database logs
docker logs proggy_wallet_db

# Stop and remove containers and volumes (reset data)
docker compose down -v
```

Ensure `.env` contains `DB_URL` (and `SECRET_KEY`) as expected by `config/settings/base.py`.

### Python dependencies

```bash
uv sync
```

Default Django settings for `manage.py` are **`config.settings.local`** (see `manage.py`).

### Run the development server

```bash
uv run python manage.py runserver
```

Open the app (typically `http://127.0.0.1:8000/`). Root URL redirects to **`/menu/`** after configuration in `config/urls.py`.

### Migrations

```bash
uv run python manage.py migrate
```

## Code quality

```bash
# Lint (PEP 8 and selected rules via Ruff)
uv run ruff check .

# Format
uv run ruff format .
```

To scope to one app: `uv run ruff check wallet/` (or `profiles/`, `reports/`).

## Testing

Primary workflow uses Django’s test runner (same discovery as in CI-friendly setups):

```bash
# All discovered tests
uv run python manage.py test

# By app
uv run python manage.py test wallet
uv run python manage.py test profiles
uv run python manage.py test reports
```

Tests use **`config.settings.test`** when invoked through pytest; `manage.py` uses `local` unless you override:

```bash
DJANGO_SETTINGS_MODULE=config.settings.test uv run python manage.py test
```

Optional: **pytest** with **pytest-django** (configured in `pyproject.toml`):

```bash
uv run pytest
uv run pytest reports/
```

If PostgreSQL raises prompts about an existing test database, use `--keepdb` after the first successful run:

```bash
uv run python manage.py test --keepdb
```

## Project layout (quick reference)

- **`wallet/`** — ledger, menu, deposit, transfer, transaction history.
- **`profiles/`** — `UserProfile`, `/profile/me/`, `/profile/me/edit/`.
- **`reports/`** — `/reports/dashboard/`, `/reports/export/` (CSV).
- **`docs/`** — PRD, architecture, MODULES, FLOWS, DATABASE, etc.

Canonical routes are listed in [MODULES.md](../MODULES.md).

---

*Last updated: 30 March, 2026 — Django stack; uv, Ruff, `manage.py test`, and pytest.*

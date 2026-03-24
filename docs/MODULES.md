# Module Architecture (Phase 3)

This document describes the responsibilities and dependencies of the system modules in the Django-based architecture.

## Project Structure Overview

```text
proggy-wallet/
├── config/               # Django project: settings, root URLconf, WSGI/ASGI
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── wallet/               # Wallet app (models, views, forms, tests)
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── registration/
│   │   │   └── login.html
│   │   └── wallet/
│   │       ├── menu.html
│   │       ├── deposit.html
│   │       ├── sendmoney.html   # served by URL name transfer → path transfer/
│   │       └── transactions.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── templates/            # Optional project-level templates (e.g. index.html)
├── static/               # STATICFILES_DIRS in settings (project static assets)
├── docs/
├── scripts/
├── .env
├── docker-compose.yml
├── pyproject.toml
└── manage.py
```

**Template loading:** `config/settings.py` sets `TEMPLATES['DIRS']` to `[]` and uses `APP_DIRS: True`, so app templates are resolved from `wallet/templates/` (and other installed apps).

## Wallet application (`wallet/`)

- **`models.py`**: **(Data layer)** `Account`, `Transaction`, and `User` provisioning signal. Validators (**layer 5**) and `CheckConstraint` (**layer 6**) match `wallet/models.py`.
- **`views.py`**: **(Logic layer)** `menu`, `deposit`, `transfer` (function views), and `TransactionHistoryView` (class-based list with pagination and query filters). Uses `transaction.atomic()` for deposits and transfers.
- **`forms.py`**: **(Validation layer)** `DepositForm`, `TransferForm` — server-side rules before writes.
- **`admin.py`**: Admin registration for wallet models.
- **`tests.py`**: Tests for wallet behaviour.

## Global configuration (`config/`)

- **`settings.py`**: Database (`DB_URL` via `django-environ`), `INSTALLED_APPS` (includes `wallet`), middleware, `STATIC_URL` / `STATICFILES_DIRS`, auth redirects (`LOGIN_REDIRECT_URL = 'menu'`, `LOGOUT_REDIRECT_URL = 'login'`), custom `PASSWORD_HASHERS` list.
- **`urls.py`**: Root routes (see below).

### URL map (root `config/urls.py`)

| Path | View / handler |
| --- | --- |
| `admin/` | Django admin |
| `accounts/` | `django.contrib.auth.urls` (login, logout, password reset, etc.) |
| `menu/` | `wallet.views.menu` |
| `deposit/` | `wallet.views.deposit` |
| `transfer/` | `wallet.views.transfer` → template `wallet/sendmoney.html` |
| `history/` | `wallet.views.TransactionHistoryView` → `wallet/transactions.html` |
| `''` | Redirect to named route `menu` |

## Presentation layer

- **DTL**: Bootstrap-oriented pages under `wallet/templates/`; login under `wallet/templates/registration/` for `auth` URLs.
- **Static files**: Served from the project `static/` directory per `STATICFILES_DIRS`.

---

*Last updated: 23 March, 2026 — Phase 3; aligned with `config/` and `wallet/`.*

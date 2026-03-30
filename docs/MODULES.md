# Module Architecture (Phase 3 + 3.1)

This document describes the responsibilities and dependencies of the system modules in the Django-based architecture.

## Project Structure Overview

```text
proggy-wallet/
├── config/               # Django project: settings package, root URLconf, WSGI/ASGI
│   ├── settings/         # base.py, local.py, production.py, test.py
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
│   │       └── transactions.html  # My Movements; includes link to Reports dashboard
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── profiles/             # Phase 3.1 — UserProfile, avatar, edit profile (shipped)
│   ├── migrations/
│   ├── templates/
│   │   └── profiles/
│   ├── models.py         # UserProfile (OneToOne User)
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── reports/              # Phase 3.1 — insights, charts, CSV export (shipped)
│   ├── migrations/       # Empty at v1 (read-only from wallet)
│   ├── templates/
│   │   └── reports/
│   ├── services.py       # Aggregation and filter helpers (_filtered_user_transactions, etc.)
│   ├── chart_payloads.py # JSON-safe chart data for Chart.js
│   ├── forms.py          # ReportsFilterForm (dashboard + CSV query params)
│   ├── views.py          # DashboardView, TransactionCsvExportView
│   ├── urls.py
│   └── tests.py
├── static/               # STATICFILES_DIRS (e.g. js/reports_dashboard.js)
├── docs/
├── scripts/
├── .env
├── docker-compose.yml
├── pyproject.toml
└── manage.py
```

**Template loading:** `config/settings/base.py` sets `TEMPLATES['DIRS']` to `[]` and uses `APP_DIRS: True`, so app templates resolve from each installed app’s `templates/` package (`wallet`, `profiles`, `reports`).

### App dependencies

| App | Depends on | Notes |
| --- | --- | --- |
| `wallet` | `django.contrib.auth` | Core ledger and accounts. |
| `profiles` | `auth.User` | `UserProfile` one-to-one; media files via `MEDIA_URL` / `MEDIA_ROOT`. |
| `reports` | `wallet` (read-only) | Query `Transaction` / `Account`; no duplicate write path for money movement. |

## Wallet application (`wallet/`)

- **`models.py`**: **(Data layer)** `Account`, `Transaction`, and `User` provisioning signal. Validators and `CheckConstraint` match the ORM.
- **`views.py`**: **(Logic layer)** `menu`, `deposit`, `transfer` (function views), and `TransactionHistoryView` (class-based list with pagination and query filters). Uses `transaction.atomic()` for deposits and transfers.
- **`forms.py`**: **(Validation layer)** `DepositForm`, `TransferForm` — server-side rules before writes.
- **`admin.py`**: Admin registration for wallet models.
- **`tests.py`**: Tests for wallet behaviour.

## Profiles application (`profiles/`)

- **`models.py`**: `UserProfile` (`OneToOne` to `User`): `bio`, optional `avatar`, timestamps.
- **`views.py`**: `ProfileDetailView`, `ProfileUpdateView` (`LoginRequiredMixin`).
- **`forms.py`**: `ProfileForm` for edit (including optional image).
- **`urls.py`**: Included under `/profile/` (see URL map below).

## Reports application (`reports/`)

- **`services.py`**: User-scoped filtered querysets and aggregates; `get_filtered_transactions_for_user` feeds CSV export.
- **`views.py`**: `DashboardView` (filters via GET + charts); `TransactionCsvExportView` (`text/csv` attachment).
- **`forms.py`**: `ReportsFilterForm` — field names `date_from`, `date_to`, `filter` (flow), `tx_type`; shared by dashboard and export.
- **`chart_payloads.py`**, **`templates/reports/dashboard.html`**, **`static/js/reports_dashboard.js`**: Chart.js integration.

## Global configuration (`config/`)

- **`settings/`**: Database (`DB_URL` via `django-environ`), `INSTALLED_APPS` includes `wallet`, `profiles`, `reports`, middleware, static/media, auth redirects (`LOGIN_REDIRECT_URL = 'menu'`, `LOGOUT_REDIRECT_URL = 'login'`).
- **`urls.py`**: Root routes (see below).

### URL map (root `config/urls.py`)

| Path | Name / namespace | Purpose |
| --- | --- | --- |
| `admin/` | — | Django admin |
| `accounts/` | — | `django.contrib.auth.urls` (login, logout, password reset) |
| `menu/` | `menu` | Wallet menu after login |
| `deposit/` | `deposit` | Deposit form |
| `transfer/` | `transfer` | Transfer form → `sendmoney.html` |
| `history/` | `history` | My Movements (`transactions.html`); **Reports** button → `reports:dashboard` |
| `profile/me/` | `profiles:profile_detail` | View profile |
| `profile/me/edit/` | `profiles:profile_edit` | Edit profile / avatar |
| `reports/dashboard/` | `reports:dashboard` | Insights dashboard (filters, charts) |
| `reports/export/` | `reports:export` | CSV download (same GET filter params as dashboard) |
| `''` | `root_redirect` | Redirect to `menu` |

## Presentation layer

- **DTL**: Bootstrap-oriented pages under app templates; login under `wallet/templates/registration/` for `auth` URLs.
- **Static files**: Project `static/` per `STATICFILES_DIRS` (e.g. reports JS).

---

*Last updated: 30 March, 2026 — Phase 3.1 shipped (`profiles`, `reports`, CSV export, navigation from My Movements to Reports).*

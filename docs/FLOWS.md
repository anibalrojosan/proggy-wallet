# System Flows (Phase 3)

This document contains the visual representation of the main business processes in the Django-based architecture using Mermaid sequence diagrams. Paths match `config/urls.py` and behaviour in `wallet/views.py`.

## 1. User Authentication Flow (Session-Based)

Login uses Django’s built-in views under `/accounts/` (e.g. `POST /accounts/login/`). On success, `LOGIN_REDIRECT_URL` sends the user to the named route **`menu`** (`/menu/`).

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Django as Django Auth
    participant DB as PostgreSQL

    User->>Browser: Enters credentials
    Browser->>Django: POST /accounts/login/ (with CSRF Token)
    Django->>Django: Validate CSRF (Layer 2)
    Django->>DB: Query user by username
    DB-->>Django: User data (hashed password)
    Django->>Django: Verify password (configured hashers, e.g. PBKDF2)
    alt Success
        Django->>Django: Create Session
        Django-->>Browser: Set Session Cookie / Redirect to /menu/
        Browser->>User: Show menu (dashboard)
    else Failure
        Django-->>Browser: Show error message (invalid credentials)
        Browser->>User: Show error
    end
```

## 2. Deposit Flow

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant View as wallet.views.deposit
    participant Form as DepositForm
    participant Model as Account / Transaction
    participant DB as PostgreSQL

    User->>Browser: Enters amount
    Browser->>Browser: Validate HTML5 (Layer 1)
    Browser->>View: POST /deposit/ (with CSRF)
    View->>Form: is_valid()
    alt Form Valid
        View->>View: transaction.atomic()
        View->>Model: add to balance, save Account
        View->>Model: Transaction.objects.create(to_user, type=deposit, balance_after, ...)
        Model->>DB: UPDATE wallet_account, INSERT wallet_transaction
        DB-->>View: Commit
        View->>View: messages.success
        View-->>Browser: Redirect to menu
        Browser->>User: Flash success + menu
    else Form Invalid
        View-->>Browser: Re-render deposit.html with errors
        Browser->>User: Show validation errors
    end
```

## 3. Peer-to-Peer Transfer Flow (Layered Integrity)

Template: `wallet/sendmoney.html`. URL path: **`/transfer/`**.

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant View as wallet.views.transfer
    participant Form as TransferForm
    participant Model as Account / Transaction
    participant DB as PostgreSQL

    User->>Browser: Selects recipient & amount
    Browser->>Browser: Validate HTML5 (Layer 1: min, required)
    Browser->>View: POST /transfer/ (with CSRF)
    View->>Form: is_valid() (Layer 3)
    alt Form Valid
        View->>View: BEGIN transaction.atomic (Layer 4)
        View->>Model: decrement sender balance, increment receiver balance
        View->>Model: Transaction.objects.create(from_user, to_user, type=transfer, balance_after, ...)
        Model->>Model: Run Validators (Layer 5: MinValueValidator)
        Model->>DB: SQL UPDATE / INSERT
        DB->>DB: Check Constraints (Layer 6: balance >= 0, amount > 0)
        alt DB Success
            DB-->>View: Commit
            View->>View: messages.success
            View-->>Browser: Redirect to menu
            Browser->>User: Show success on menu
        else DB Failure (e.g. IntegrityError)
            DB-->>View: Rollback
            View-->>Browser: Error message via messages / template
        end
    else Form Invalid
        View-->>Browser: Re-render sendmoney.html with errors
        Browser->>User: Show error message
    end
```

## 4. Transaction History Flow

`TransactionHistoryView`: `GET /history/` (optional query `?filter=income` or `?filter=expense`). Queryset: transactions where the user is `from_user` OR `to_user`, ordered by `-created_at`, paginated (`paginate_by = 10`).

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant View as TransactionHistoryView
    participant DB as PostgreSQL

    User->>Browser: Open history (optional filter)
    Browser->>View: GET /history/?filter=...
    View->>View: LoginRequiredMixin
    View->>DB: SELECT transactions for user (with optional filter)
    DB-->>View: Page of rows
    View-->>Browser: Render transactions.html (page_obj, current_filter)
    Browser->>User: Show paginated ledger
```

From **My Movements**, the user may open **Reports** via a link to `GET /reports/dashboard/` (named route `reports:dashboard`).

## 5. Root URL

`GET /` triggers a redirect to the named route **`menu`** (`/menu/`), implemented in `config/urls.py`.

---

## 6. Phase 3.1 flows — `profiles` and `reports` (implemented)

Paths match [MODULES.md](MODULES.md) and `config/urls.py`.

### 6.1 View / edit profile and avatar

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant View as profiles.views
    participant Form as ProfileForm
    participant Storage as MediaStorage
    participant DB as PostgreSQL

    User->>Browser: Open profile or edit
    Browser->>View: GET /profile/me/ or GET /profile/me/edit/
    View->>View: LoginRequiredMixin
    View->>DB: Load or create UserProfile for request.user
    View-->>Browser: Render profile_detail or profile_form
    User->>Browser: Submit profile optional image
    Browser->>View: POST /profile/me/edit/ CSRF multipart if file
    View->>Form: is_valid()
    alt Valid
        View->>DB: Save UserProfile
        opt Avatar present
            View->>Storage: Save under MEDIA_ROOT per ADR-04
        end
        View-->>Browser: Redirect to profile detail
    else Invalid
        View-->>Browser: Re-render with errors
    end
```

### 6.2 Reports dashboard (read-only)

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant View as reports.views.DashboardView
    participant Form as ReportsFilterForm
    participant Svc as reports.services
    participant ORM as Django ORM
    participant DB as PostgreSQL

    User->>Browser: Open reports dashboard
    Browser->>View: GET /reports/dashboard/?date_from=... optional
    View->>View: LoginRequiredMixin
    View->>Form: bind request.GET
    alt Form valid
        View->>Svc: summaries monthly rows type breakdown filtered user
        Svc->>ORM: read only queries on Transaction
        ORM->>DB: SELECT aggregates
        DB-->>View: context for charts and KPIs
        View-->>Browser: Render dashboard.html Chart.js payloads
    else Form invalid
        View-->>Browser: Re-render with errors unfiltered aggregates
    end
```

### 6.3 CSV export (user-scoped)

Same filter contract as the dashboard: query params `date_from`, `date_to`, `filter` (income or expense), `tx_type`. Invalid date range returns **400** with form errors (no CSV body). Empty result set returns **200** with header row only. Anonymous users are redirected to login.

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant View as TransactionCsvExportView
    participant Form as ReportsFilterForm
    participant Svc as reports.services
    participant DB as PostgreSQL

    User->>Browser: Apply filters optional click Export CSV
    Browser->>View: GET /reports/export/? same params as dashboard form
    View->>View: LoginRequiredMixin
    View->>Form: bind request.GET
    alt Form invalid
        View-->>Browser: 400 Bad Request text plain
    else Form valid
        View->>Svc: get_filtered_transactions_for_user request.user
        Svc->>DB: SELECT transactions read only
        DB-->>View: rows
        View-->>Browser: 200 text csv charset utf 8 attachment transactions_export.csv
    end
```

The dashboard **Export CSV** button submits the filter form with `formaction` pointing to `reports:export` so current field values are sent as GET parameters.

---

*Last updated: 30 March, 2026 — Phase 3.1 flows implemented (profiles, reports, CSV).*

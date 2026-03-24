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

## 5. Root URL

`GET /` triggers a redirect to the named route **`menu`** (`/menu/`), implemented in `config/urls.py`.

---

*Last updated: 23 March, 2026 — Phase 3; aligned with `config/urls.py` and `wallet/views.py`.*

# System Flows (Phase 3)

This document contains the visual representation of the main business processes in the Django-based architecture using Mermaid sequence diagrams.

## 1. User Authentication Flow (Session-Based)

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
    Django->>Django: Verify PBKDF2 hash
    alt Success
        Django->>Django: Create Session
        Django-->>Browser: Set Session Cookie / Redirect to Dashboard
        Browser->>User: Show Dashboard
    else Failure
        Django-->>Browser: Show error message (invalid credentials)
        Browser->>User: Show error
    end
```

## 2. Peer-to-Peer Transfer Flow (Layered Integrity)

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant View as Django View
    participant Form as Django Form
    participant Model as Django Model
    participant DB as PostgreSQL

    User->>Browser: Selects recipient & amount
    Browser->>Browser: Validate HTML5 (Layer 1: min, required)
    Browser->>View: POST /transfer/ (with CSRF)
    View->>Form: is_valid() (Layer 3: clean_amount)
    alt Form Valid
        View->>View: BEGIN transaction.atomic (Layer 4)
        View->>Model: update balance / create transaction
        Model->>Model: Run Validators (Layer 5: MinValueValidator)
        Model->>DB: SQL UPDATE / INSERT
        DB->>DB: Check Constraints (Layer 6: balance >= 0)
        alt DB Success
            DB-->>View: Commit
            View-->>Browser: 200 OK / Success Message
            Browser->>User: Show success & update UI
        else DB Failure (IntegrityError)
            DB-->>View: Rollback
            View-->>Browser: Show error message
        end
    else Form Invalid
        Form-->>Browser: Show validation errors
        Browser->>User: Show error message
    end
```

---

*Last updated: 11 March, 2026 - Phase 3 - Sprint 26: Cleanup and Local Deployment*

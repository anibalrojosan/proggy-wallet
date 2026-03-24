# 🏗️ System Architecture: Proggy Wallet

This document serves as one of the three documents that makes up the single source of truth of this project, along with [PRD.md](PRD.md) and [DATABASE.md](DATABASE.md). Here its defined the *architecture* of the project, *how* the components interact with each other and how the data flows to accomplish the business logic defined in the PRD.

## 1. Overview

**Proggy Wallet** is a virtual wallet application designed to manage personal finances through a simple and secure web interface. The system enables users to perform core banking operations (deposits, transfers, and transaction history tracking) within a session-based, server-rendered environment.

The architecture follows a **classic Django web application** model: the browser exchanges HTML form posts and GET navigations with the server; the server is the **single source of truth** for balances and ledger data.

## 2. System Components

### 2.1 Frontend (The Client)

* **Responsibility:** Data presentation, user input capture, and session cookie handling.
* **State Management:** The client does not compute authoritative balances; it displays values returned by the server.
* **Technologies:** `HTML5`, `Bootstrap 5` (responsive UI), and `jQuery` (DOM manipulation and UX effects).

### 2.2 Backend (The Server)

* **Responsibility:** Authentication, validation, business orchestration, and persistence.
* **Interface:** **Django** — URL routing, views (function- and class-based), Django Forms, Django ORM, and Django Templates.
* **Technologies:** `Python 3.12+`, **Django**, **PostgreSQL**.

### 2.3 Planned apps (Phase 3.1)

* **`profiles`:** `UserProfile` linked to `User`; profile edit and **avatar** uploads. Media storage strategy: [ADR-04](adr/04-user-avatar-storage-local-vs-object-storage.md).
* **`reports`:** Read-only **insights** over `wallet` models (aggregations, charts, CSV export). Does not introduce a second ledger; writes remain in `wallet`.

## 3. Data Flow (Request / Response)

Typical cycle for wallet actions:

1. **Trigger:** The user submits a form or opens a protected page.
2. **Request:** The browser sends HTTP **GET** or **POST** (with **CSRF** token on posts) to Django.
3. **Routing:** `config.urls` dispatches to the appropriate view in `wallet`, `profiles`, or `reports`.
4. **Auth:** `LoginRequiredMixin` or `@login_required` ensures identity where required.
5. **Validation:** Django **Forms** (and model `full_clean()` / validators) enforce input rules.
6. **Business logic:** Views orchestrate changes; financial mutations use **`transaction.atomic()`** where multiple rows must succeed or fail together.
7. **Persistence:** Django ORM persists to PostgreSQL.
8. **Response:** Redirect with **messages** framework and/or re-render template with context (errors, lists, aggregates).

## 4. Backend Structure (Django-oriented)

Dependencies point **inward**: URLconf → views → (forms / models) → ORM → database. Optional **service modules** inside an app (e.g. `reports/services.py`) may encapsulate query logic without bypassing the ORM.

```text
    [ config/urls.py ]
             │
             ▼
    [ App views + forms (wallet | profiles | reports) ]
             │
             ▼
    [ Django ORM (models, constraints, signals) ]
             │
             ▼
    [ PostgreSQL ]
```

| Layer | Responsibility |
| :--- | :--- |
| **URLconf** | Map paths to views; include per-app `urls.py` as the project grows. |
| **Views** | HTTP entry, permission checks, orchestration, response type. |
| **Forms** | Request validation and user-facing field errors. |
| **Models** | Schema, invariants, `CheckConstraint`, relations. |
| **Templates** | Render HTML; no business calculations for money. |

### 4.1 Error handling

| Situation | Typical handling |
| :--- | :--- |
| Invalid form | Re-render template with form errors. |
| Business rule violation | Message or error string; avoid silent failure. |
| Missing resource | `Http404` where appropriate. |

## 5. Technology Stack

| Technology | Rationale |
| :--- | :--- |
| **Django** | Integrated ORM, auth, forms, admin, and migration workflow for a cohesive monolith. |
| **PostgreSQL** | ACID compliance, relational integrity, and scalable querying. |
| **uv** | Reproducible environments and fast dependency management. |
| **Docker** (Phase 4) | Consistent dev/prod parity and deployment artifacts. |

## 6. ADRs (Architecture Decision Records)

| ID | Decision | Status | Key justification (summary) |
| :--- | :--- | :--- | :--- |
| [ADR-01](adr/01-use-fastapi-for-backend-integration.md) | FastAPI (Phase 1 history) | **Superseded** | Historical; product now uses Django only. |
| [ADR-02](adr/02-use-csv-for-initial-persistence.md) | **CSV/JSON** | Superseded | Phase 1 prototyping; replaced by SQL/ORM. |
| [ADR-03](adr/03-use-postgresql-for-persistent-storage.md) | **PostgreSQL** | Accepted | Integrity, ACID, relational model. |
| [ADR-04](adr/04-user-avatar-storage-local-vs-object-storage.md) | **Avatar storage** | Accepted | Local media in dev; durable object storage (or persistent volume) in cloud prod. |

---

*Last updated: 23 March, 2026 — Django architecture; Phase 3.1 apps documented.*

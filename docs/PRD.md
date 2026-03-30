# Project Requirements Document (PRD)

This document serves as one of the three documents that makes up the single source of truth of this project, along with [ARCHITECTURE.md](ARCHITECTURE.md) and [DATABASE.md](DATABASE.md). Here its defined *what* does the project do and what are the business logic.

## **1. Project Scope & Origins**

This project is developed as a self-authored solution based on real-world fintech industry challenges.
* **Core Base**: The initial Functional Requirements (MVP) were based on a dynamic frontend and Python data management.
* **Evolution**: The project evolved from a flat-file prototype (Phase 1) to PostgreSQL and structured domain concepts (Phase 2), then to a **Django** web application (Phase 3). **Phase 3.1** adds user profile and reporting capabilities on top of the wallet core.

## **2. Project Vision**

To develop a reference architecture for a digital wallet application. The primary goal is technical excellence, utilizing a modern tech stack to validate inputs, manage financial states securely, and ensure code quality through continuous integration and relational data integrity.

## **3. Tech Stack & Tools**

| Area | Technology | Specific Purpose |
|---|---|---|
| **Frontend**       | **HTML5 / Bootstrap 5** | Semantic structure and responsive design (Mobile-first). |
|                    | **JavaScript / jQuery** | DOM manipulation and client-side logic. |
| **Backend**        | **Python 3.12+ / Django** | Server-side logic, routing, ORM, forms, session auth, admin. |
| **Database**       | **PostgreSQL** | Relational data persistence and integrity. |
| **Quality (QA)**   | **Ruff**; **Django `TestCase`** via `manage.py test`; **Pytest** (optional, `pytest-django` in dev) | Linting, formatting, and automated tests. |
| **Management**     | **uv** | High-performance dependency and project manager. |
| **Validation**     | **Django Forms / ORM** | Server-side validation and model constraints. |
| **Infrastructure** | **Docker** (Phase 4) | Containerization for consistent environments and deployment. |

## **4. Functional Requirements**

### **4.1 Phase 3 — Wallet core (delivered)**

**A. Authenticated web experience**
1. **Login / logout**: Django session-based authentication.
2. **Menu / dashboard**: Entry point after login; navigation to wallet actions.
3. **Deposits**: Form to add funds with immediate persistence on the user’s `Account`.
4. **Transfers**: Peer-to-peer transfers with balance validation and atomic updates.
5. **History**: Transaction ledger scoped to the current user, with filtering and pagination; link from My Movements to the **Reports** dashboard.

**B. Data and integrity**
1. **Single source of truth** for balances on `Account`; immutable-style ledger on `Transaction` as implemented in Django.
2. **Financial logic**: Atomic operations for transfers and deposits (database transaction boundaries).
3. **Constraints**: Non-negative balances, strictly positive transaction amounts, enforced in ORM and DB where defined.

### **4.2 Phase 3.1 — Profiles & insights (delivered)**

**A. `profiles` app**
1. **UserProfile**: Extended data linked **one-to-one** to Django `User` (`bio`, optional `avatar`, timestamps).
2. **Avatar**: Optional profile image upload; storage per [ADR-04](adr/04-user-avatar-storage-local-vs-object-storage.md).
3. **Edit flow**: Authenticated user views `/profile/me/` and edits `/profile/me/edit/` (demo guest account may be restricted from editing).

**B. `reports` app (insights)**
1. **Summaries**: Aggregated views over the user’s wallet activity (period, flow, type), **read-only** over `wallet.Transaction` / `Account`.
2. **Visualization**: Bootstrap layout, KPI cards, Chart.js bar and doughnut charts, filterable via GET (`/reports/dashboard/`).
3. **Export — CSV contract (transaction rows)**  
   - **Endpoint:** `GET /reports/export/` (authenticated); same query parameters as the dashboard filter form.  
   - **Parameters:** `date_from`, `date_to` (optional dates); `filter` optional values `income`, `expense`; `tx_type` optional `deposit`, `transfer`, `withdrawal`. Invalid range (e.g. start after end) → **400** with plain-text form errors.  
   - **Response:** `Content-Type: text/csv; charset=utf-8`; `Content-Disposition: attachment`; filename `transactions_export.csv`.  
   - **Columns (header row, in order):** `id`, `created_at` (ISO 8601), `type`, `amount` (decimal string), `flow` (`income` / `expense` from the viewer’s perspective), `from_username`, `to_username`, `description`, `balance_after` (empty if null).  
   - **Scope:** Only transactions involving the current user after filters; empty set → **200** with headers only.

### **4.3 Phase 5 — Out of current MVP**

Features listed under **Phase 5** in [ROADMAP.md](ROADMAP.md) (preferences, notifications, support, budgets, etc.) are **not** part of Phase 3.1 unless explicitly pulled into a future milestone.

## **5. Non-Functional Requirements**

- **Data Integrity**: Database-level constraints (CHECK, UNIQUE, FK) and Django validators to prevent invalid financial states.
- **Security**: Password hashing, CSRF on state-changing requests, environment-based secrets (`.env` / platform config).
- **Modularity**: Separate Django apps for wallet core, profiles, and reports with clear dependencies (`reports` reads `wallet` data; does not duplicate ledger writes).
- **Performance**: Efficient ORM queries for history and reports; pagination where lists are large.

## **6. Phase Deliverables**

- **PostgreSQL schema**: Documented in [DATABASE.md](DATABASE.md); Django migrations in-repo.
- **Django application**: Wallet flows (Phase 3); profiles and reports (Phase 3.1).
- **Technical documentation**: PRD, ARCHITECTURE, DATABASE, MODULES, FLOWS, ADRs.
- **Dockerized environment** (Phase 4): Portable runtime via `Dockerfile` / `docker-compose` and CI.

---

*Last updated: 30 March, 2026 — Phase 3.1 delivered; CSV contract and navigation documented.*

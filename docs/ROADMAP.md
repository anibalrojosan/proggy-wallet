# Technical Roadmap: ``Proggy Wallet``

This document outlines the strategic technical progression from a basic Frontend/Python prototype to a professional Full-Stack Enterprise Application. It serves as a guide for development, tooling, and infrastructure scaling.

**Current product stack:** **Django** (MVT), **PostgreSQL**, server-rendered templates (Bootstrap 5 / jQuery). No separate FastAPI service in scope for the wallet product.

## Tech Stack

| Category | Tool / Technology | Purpose | Implementation Phase |
| --- | --- | --- | --- |
| **Languages** | **HTML5 / CSS3** | Structure and responsive styling. | Phase 1 |
|  | **JavaScript (ES6+)** | Client-side interactivity. | Phase 1 |
|  | **Python 3.12+** | Backend logic and data processing. | Phase 1 - 5 |
|  | **SQL** | Relational database querying. | Phase 2 - 4 |
| **Frameworks & Libraries** | **Bootstrap 5** | CSS Framework for responsive UI components. | Phase 1 |
|  | **jQuery** | DOM manipulation and visual effects. | Phase 1 |
|  | **Django** | Web framework (MVT), ORM, auth, forms, admin. | Phase 3+ |
| **Tooling & Quality (DX)** | **uv** | Blazing fast Python package and project manager (replaces `pip`/`venv`). | **All Phases** |
|  | **Ruff** | Extremely fast Python linter and formatter (strict **PEP 8** compliance). | **All Phases** |
|  | **Pytest** | Framework for scalable and simple unit/integration testing. | Phase 2 - 4 |
| **DevOps & Infrastructure** | **Git & GitHub** | Version control and collaborative hosting. | All Phases |
|  | **Docker** | Containerization for consistent development and production environments. | Phase 4 |
|  | **GitHub Actions** | Automated CI/CD pipelines (Linting, Testing, Building). | Phase 4 |
|  | **Render / Railway** | Modern cloud platform for automated container deployment. | Phase 4 |
| **Persistence** | **CSV / JSON** | Initial flat-file data persistence. | Phase 1 |
|  | **PostgreSQL** | Open Source Relational Database Management System. | Phase 2 - 4 |

---

## 🟢 Phase 1: Foundations & Prototyping

**Goal:** Establish a dynamic Frontend interface and core Python scripting logic with a focus on code quality.

### Frontend Requirements

* **Views Implementation:** `login`, `menu`, `deposit`, `sendmoney`, `transactions`.
* **UI/UX:** Responsive design using **Bootstrap 5**; interactive elements powered by **jQuery**.

### Backend Requirements

* **Core Logic:** Python scripts for transaction processing and user management.
* **Data Persistence:** Input/Output handling using **CSV/JSON** files.
* **Tooling Setup:**
* Initialize project with **`uv`** for dependency management.
* Configure **`Ruff`** to enforce **PEP 8** standards from the first commit.

---

## 🟡 Phase 2: Robustness & Architecture

**Goal:** Refactor procedural scripts into robust Object-Oriented Programming (OOP), implement a web API with FastAPI, and migrate to a relational database.

### Architecture & Logic

* **API Implementation:** Create a modern REST API using **FastAPI** to handle requests from the frontend.
* **OOP Refactoring:** Transform standalone functions into classes (`User`, `Account`, `Transaction`) with proper inheritance.
* **Data Validation:** Implement **Pydantic** models to strictly validate user inputs and transaction amounts, replacing manual `if/else` checks.

### Data Layer

* **Database Design:** Create an Entity-Relationship Diagram (ERD) and implement the schema in **PostgreSQL**.
* **Integration:** Replace file-based persistence with SQL queries (`SELECT`, `INSERT`, `UPDATE`).

### Quality Assurance

* **Testing:** Introduce **Pytest** to create unit tests for core financial logic (e.g., ensuring `deposit()` correctly updates balance).

---

## 🟠 Phase 3: Enterprise Ecosystem (Web Framework)

**Goal:** Transform the script-based application into a fully-fledged Web App using the Django Framework.

### Framework Integration

* **MVC Architecture:** **Django MVT** — views, templates, and URL routing.
* **ORM Implementation:** Django ORM for PostgreSQL (models, constraints, migrations).
* **Authentication:** Django’s built-in auth (login, sessions, password hashing).
* **Connectivity:** HTML forms and class-based/function views for deposits, transfers, and history.

---

## 🟣 Phase 3.1: Profiles & Insights (delivered)

**Goal:** Extend the product with **`profiles`** and **`reports`** apps without changing core ledger rules in `wallet`.

### `profiles` app

* **`UserProfile`** model (`OneToOne` to `User`): optional **bio**, optional **avatar**; timestamps.
* Views and templates for **view/edit profile** (`/profile/me/`, `/profile/me/edit/`); image validation in forms.
* Avatar storage strategy: see [ADR-04](adr/04-user-avatar-storage-local-vs-object-storage.md) (local dev vs object storage in production).

### `reports` app (insights)

* **Read-only** aggregations over existing `wallet` data (no duplicate source of truth for balances).
* UI: `/reports/dashboard/` — KPIs, monthly and type charts, GET filters aligned with history semantics; entry link from **My Movements** (`/history/`).
* **Export:** `GET /reports/export/` — CSV of **filtered transactions** for the current user (columns and query parameters in [PRD.md](PRD.md) §4.2).

### Deliverables checklist

* [x] `profiles` registered in `INSTALLED_APPS`, migrations, URLs, templates.
* [x] `reports` registered, URLs, templates, tests for aggregation/export boundaries.
* [x] `MEDIA_ROOT` / `MEDIA_URL` configured for development (`config/settings/base.py`); production path documented per ADR-04.

---

## 🔵 Phase 4: Cloud Deployment and CI/CD

**Goal:** Containerize, automate, and deploy the application to a public cloud environment to establish a robust, production-ready infrastructure governed by automated CI/CD workflows.

### Infrastructure & Deployment

* **Containerization:**
    * Create `Dockerfile` for the Django application.
    * Define services (Web + DB) in `docker-compose.yml` for local development.

* **CI/CD Pipeline (GitHub Actions):**
    * **Linting Job:** Fail build if **Ruff** detects code style violations.
    * **Testing Job:** Run **Pytest** suite automatically on every push.

* **Cloud Deployment:**
    * Configure automated deployment to **Render** or **Railway** connected to the GitHub repository.
    * Align **static and media** configuration with ADR-04 for avatars where applicable.

---

## ⚪ Phase 5: Future improvements (post-MVP)

**Goal:** Capture product ideas **not** scheduled for Phase 3.1. Scope here is indicative; each item may become its own app or module later.

| Area | Indicative scope |
| --- | --- |
| **Preferences / settings** | Display currency, locale, date/number formatting; optional theme. |
| **Notifications** | In-app and/or email for transfers, security events. |
| **Support / help** | FAQ, contact form, lightweight tickets. |
| **Security extras** | Session management UX, 2FA hooks, audit-friendly settings. |
| **Budgets / categories** | Labels on transactions, monthly limits, spending views. |
| **External accounts / cards** | Linked payment methods metadata (educational / non-PCI scope). |
| **Formal statements** | Period “statement” PDFs or printable views (beyond ad-hoc CSV). |

---

*Last updated: 30 March, 2026 — Phase 3 complete; Phase 3.1 delivered (`profiles`, `reports`, CSV).*

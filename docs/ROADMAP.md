# Technical Roadmap: ``Proggy Wallet``

This document outlines the strategic technical progression from a basic Frontend/Python prototype to a professional Full-Stack Enterprise Application. It serves as a guide for development, tooling, and infrastructure scaling.

## Tech Stack

| Category | Tool / Technology | Purpose | Implementation Phase |
| --- | --- | --- | --- |
| **Languages** | **HTML5 / CSS3** | Structure and responsive styling. | Phase 1 |
|  | **JavaScript (ES6+)** | Client-side interactivity. | Phase 1 |
|  | **Python 3.12+** | Backend logic and data processing. | Phase 1 - 4 |
|  | **SQL** | Relational database querying. | Phase 2 - 3 |
| **Frameworks & Libraries** | **Bootstrap 5** | CSS Framework for responsive UI components. | Phase 1 |
|  | **jQuery** | DOM manipulation and visual effects. | Phase 1 |
|  | **Django** | High-level Python Web Framework (MVC/MVT). | Phase 3 |
|  | **Pydantic** | Data validation and schema management using Python type hints. | Phase 2 |
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

**Goal:** Refactor procedural scripts into robust Object-Oriented Programming (OOP) and migrate to a relational database.

### Architecture & Logic

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

* **MVC Architecture:** Port Python logic to **Django's MVT** (Model-View-Template) pattern.
* **ORM Implementation:** Use Django ORM to interact with PostgreSQL, removing raw SQL queries.
* **Authentication:** Implement Django's built-in Auth System for secure login and session management.
* **Connectivity:** Connect existing HTML forms to Django Views.

---

## 🔵 Phase 4: Production & DevOps

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
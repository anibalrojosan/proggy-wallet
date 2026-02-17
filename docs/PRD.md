# Project Requirements Document (PRD)

This document serves as one of the three documents that makes up the single source of truth of this project, along with [ARCHITECTURE.md](ARCHITECTURE.md) and [DATABASE.md](DATABASE.md). Here its defined *what* does the project do and what are the business logic.

## **1. Project Scope & Origins**

This project is developed as a self-authored solution based on real-world fintech industry challenges.
* **Core Base**: The initial Functional Requirements (MVP) were based on a dynamic frontend and Python data management.
* **Evolution**: The project has evolved from a flat-file prototype (Phase 1) to a robust relational architecture (Phase 2), with a roadmap towards a full-stack Django enterprise application (Phase 3 & 4).

## **2. Project Vision**

To develop a reference architecture for a digital wallet application. The primary goal is technical excellence, utilizing a modern tech stack to validate inputs, manage financial states securely, and ensure code quality through continuous integration and relational data integrity.

## **3. Tech Stack & Tools**

| Area | Technology | Specific Purpose |
|---|---|---|
| **Frontend**       | **HTML5 / Bootstrap 5** | Semantic structure and responsive design (Mobile-first). |
|                    | **JavaScript / jQuery** | DOM manipulation and client-side logic. |
| **Backend**        | **Python 3.12+ / FastAPI** | Business logic, API endpoints, and data processing. |
| **Database**       | **PostgreSQL 18** | Relational data persistence and integrity. |
| **Quality (QA)**   | **Ruff / Pytest** | Strict linting and unit testing suite. |
| **Management**     | **uv** | High-performance dependency and project manager. |
| **Validation**     | **Pydantic** | Data Schema definition and runtime validation. |
| **Infrastructure** | **Docker** | Containerization for consistent environments. |

## **4. Functional Requirements (Phase 2 - Robustness)**

**A. Frontend Module**
1. **Login**: Secure authentication flow.
2. **Dashboard**: Real-time balance display and navigation.
3. **Deposits**: Form to add funds with immediate database update.
4. **Transfers**: Peer-to-peer money transfers with balance validation.
5. **History**: Detailed transaction ledger fetched from PostgreSQL.

**B. Backend & Data Module**
1. **API Layer (FastAPI)**: RESTful endpoints to connect Frontend and Database.
2. **Relational Persistence**: Full migration from JSON/CSV to PostgreSQL.
3. **Financial Logic**: Atomic transactions to ensure data consistency during transfers.
4. **Type Validation**: Strict Pydantic models for all incoming and outgoing data.

## **5. Non-Functional Requirements**

- **Data Integrity**: Database-level constraints (CHECK, UNIQUE, FK) to prevent invalid financial states.
- **Security**: Password hashing (BCrypt/Argon2) and environment variable management (.env).
- **Modularity**: Clean separation between API routes, business logic, and database repositories.
- **Performance**: Efficient querying and containerized execution.

## **6. Phase Deliverables**

- **PostgreSQL Schema**: Documented ERD and SQL migrations.
- **FastAPI Backend**: Functional API with Pydantic validation.
- **Technical Documentation**: Comprehensive guides for development, modules, and flows.
- **Dockerized Environment**: Fully portable setup via `docker-compose`.

---

*Last updated: 16 February, 2026 - Phase 2 - Sprint 16: Database Design & Setup*
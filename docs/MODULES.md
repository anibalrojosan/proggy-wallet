# Module Architecture

This document describes the responsibilities and dependencies of the system modules.

## Project Structure Overview

```text
proggy-wallet/
├── backend/            # Python Backend (FastAPI)
│   ├── database/       # SQL schemas and DB connection logic
│   ├── modules/        # Business logic and Pydantic models
│   └── app.py          # API Entry point and routes
├── frontend/           # Static Web Files
├── docs/               # Technical Documentation
└── docker-compose.yml  # Infrastructure definition
```

## Backend Modules (`backend/modules/`)

- **`auth.py`**: Handles user authentication, credential validation, and password hashing.
- **`services.py`**: **(Service Layer)** Orchestrates business flows like transfers and deposits, coordinating between repositories and entities.
- **`models.py`**: **(Schemas/DTOs)** Pydantic models used for API request/response validation and data contracts.
- **`entities.py`**: **(Domain Layer)** Pure OOP classes representing core business entities (User, Account) and their internal rules.
- **`wallet.py`**: (Legacy/Refactoring) Core business logic being migrated into `services.py` and `entities.py`.

## Database Layer (`backend/database/`)

- **`schema.sql`**: Definition of PostgreSQL tables and constraints.
- **`repository.py`**: **(Data Access Layer)** Handles all SQL queries and maps database rows to Domain Entities.
- **`connection.py`**: Database connection pooling and session management.

## Frontend (`frontend/`)

- **HTML/CSS**: Responsive UI built with Bootstrap 5.
- **JavaScript**: Client-side logic and API interaction using jQuery/Fetch API.

---

*Last updated: 16 February, 2026 - Phase 2 - Sprint 16: Database Design & Setup*
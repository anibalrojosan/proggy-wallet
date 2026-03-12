# Module Architecture (Phase 3)

This document describes the responsibilities and dependencies of the system modules in the Django-based architecture.

## Project Structure Overview

```text
proggy-wallet/
├── core/                 # Global Django settings and URL routing
├── wallet/               # Main application (Models, Views, Forms, Tests)
│   ├── migrations/       # Database version control
│   ├── admin.py          # Admin interface configuration
│   ├── forms.py          # Form validation logic (Layer 3)
│   ├── models.py         # Data models and constraints (Layers 5 & 6)
│   ├── tests.py          # Integration and unit tests
│   └── views.py          # Business logic and orchestration (Layer 4)
├── templates/            # UI Views (Django Template Language)
│   ├── base.html         # Master layout
│   ├── registration/     # Auth templates (Login)
│   └── *.html            # Dashboard, Deposit, Transfer views
├── static/               # Static assets (CSS, JS, Images)
├── docs/                 # Comprehensive documentation and ADRs
├── scripts/              # Utility scripts for development
├── .env                  # Environment variables (DB, SECRET_KEY)
├── docker-compose.yml    # PostgreSQL container configuration
├── pyproject.toml        # Project configuration & dependencies (uv)
└── manage.py             # Django management entry point
```

## Core Application (`wallet/`)

- **`models.py`**: **(Data Layer)** Defines the relational schema using Django ORM. Implements **Layer 5 (Validators)** and **Layer 6 (Database Constraints)** to ensure financial data integrity.
- **`views.py`**: **(Logic Layer)** Orchestrates business flows. Implements **Layer 4 (Business Logic)** using `transaction.atomic()` to guarantee atomicity in transfers and deposits.
- **`forms.py`**: **(Validation Layer)** Handles server-side sanitization and business rule validation (**Layer 3**). Ensures clean data entry before reaching the models.
- **`admin.py`**: Provides a secure interface for managing users, accounts, and transactions.
- **`tests.py`**: Comprehensive suite of integration tests verifying the 6-layer security strategy.

## Global Configuration (`core/`)

- **`settings.py`**: Centralized configuration for the Django framework, including database connections, installed apps, and security middleware (**Layer 2**).
- **`urls.py`**: Global URL routing, connecting web requests to the appropriate views in the `wallet` app.

## Presentation Layer (`templates/` & `static/`)

- **DTL Templates**: Responsive UI built with Bootstrap 5 and Django Template Language. Implements **Layer 1 (Frontend UX)** with native HTML5 validations.
- **Static Assets**: Centralized CSS and JavaScript files served by Django.

---

*Last updated: 11 March, 2026 - Phase 3 - Sprint 26: Cleanup and Local Deployment*

# Proggy Wallet 🪙

![Python](https://img.shields.io/badge/Python-3.12-green)
![Django](https://img.shields.io/badge/Django-v6.0-092e20)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

> This project it's currently under development and has successfully transitioned from a file-based prototype to a robust **PostgreSQL-backed Django Monolith**.
>
> Current focus: **Phase 4: Cloud Deployment and CI/CD**.

**Proggy Wallet** is a comprehensive engineering roadmap designed to architect a production-ready **Full-Stack Fintech solution**. This project documents the complete lifecycle of modern software development, bridging the gap between a dynamic **Frontend prototype** and a scalable **Django ecosystem**.

It serves as a definitive technical reference for industry best practices, implementing a **Monolithic Architecture** through Django’s **MTV (Model-Template-View)** pattern. By consolidating logic and presentation, the project integrates advanced **Python logic**, **SQL persistence**, and automated **DevOps workflows** (Docker & CI/CD) to demonstrate the rigorous evolution from initial code to global cloud deployment.

## 📑 Index
1. [🔑 Key Features](#key-features)
2. [🚀 Quick Start](#quick-start)
3. [📝 Documentation](#documentation)
4. [📂 Project Structure](#project-structure)
5. [🏗️ Architecture & Security](#architecture--security)
6. [🛠️ Tech Stack](#tech-stack)

## Key Features

**Proggy Wallet** combines a modern user experience with a robust backend engine. The system is designed to handle the core requirements of a digital wallet while maintaining high standards of data integrity and security:

- **Financial Integrity:** Multi-layered validation including PostgreSQL `CheckConstraints`, Django `Validators`, and atomic transactions (`transaction.atomic`).
- **Advanced Security:** 
  - Django's built-in Authentication system with secure password hashing.
  - CSRF protection and route authorization.
- **Real-time SQL History:** Dynamic transaction history with server-side sorting and filtering using the Django ORM.
- **Modern UI:** Responsive design using Bootstrap 5 and Django Template Language (DTL).
- **Clean Architecture:** Separation of concerns through Django's MTV pattern and layered security.

## Quick Start

### 1. Prerequisites
This project uses [**uv**](https://docs.astral.sh/uv/) for blazing-fast Python package and project management. If you don't have it installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Installation & Setup
Clone the repository and sync the environment:

```bash
git clone https://github.com/anibalrojosan/proggy-wallet.git
cd proggy-wallet
uv sync
```

### 3. Environment Configuration
Copy the example environment file and adjust if needed (e.g., change `DB_PASSWORD`):

```bash
cp .env.example .env
```

### 4. Execution

#### 4.1 **Database Setup (Docker):**
Ensure Docker is running and start the PostgreSQL container:

```bash
docker compose up -d
```

#### 4.2 **Apply Migrations:**
Initialize the database schema and security constraints:

```bash
uv run python manage.py migrate
```

#### 4.3 **Create a User:**
Create an admin/superuser to log in. You will use these credentials at http://localhost:8000/accounts/login/

```bash
uv run python manage.py createsuperuser
```

#### 4.4 **Run Development Server:**
Start the Django server. It will be available at http://localhost:8000 by default.

```bash
uv run python manage.py runserver
```

#### 4.5 **Quality Control & Testing:**
This project follows strict PEP 8 standards and is fully tested.

```bash
# Linting
uv run ruff check .
# Formatting
uv run ruff format .
# Tests
uv run pytest
```

## Documentation

The design process and the implementation of this project are documented in the following documents:

- **[ARCHITECTURE](docs/ARCHITECTURE.md)**: Deep dive into the system design and ADRs.
- **[CLASS_DIAGRAM](docs/CLASS_DIAGRAM.md)**: Class diagram of the project.
- **[DATABASE](docs/DATABASE.md)**: Database schema and constraints.
- **[DEVLOG](docs/development/DEVLOG.md)**: Daily technical logs, hurdles, and solutions.
- **[FLOWS](docs/FLOWS.md)**: System flows of the project.
- **[MODULES](docs/MODULES.md)**: Module architecture of the project.
- **[PRD](docs/PRD.md)**: Requirements document.
- **[ROADMAP](docs/ROADMAP.md)**: Path from prototype to production.

## Project Structure (Phase 3)
```text
proggy-wallet/
├── core/                 # ⚙️ Global Django settings and URL routing
├── wallet/               # 💰 Main application (Models, Views, Forms, Tests)
│   ├── migrations/       # 🗄️ Database version control
│   ├── admin.py          # 🛡️ Admin interface configuration
│   ├── forms.py          # 📝 Form validation logic (Layer 3)
│   ├── models.py         # 🧠 Data models and constraints (Layers 5 & 6)
│   ├── tests.py          # 🧪 Integration and unit tests
│   └── views.py          # 🌐 Business logic and orchestration (Layer 4)
├── templates/            # 🖥️ UI Views (Django Template Language)
│   ├── base.html         # 🏗️ Master layout
│   ├── registration/     # 🔑 Auth templates (Login)
│   └── *.html            # 📱 Dashboard, Deposit, Transfer views
├── static/               # 🎨 Static assets (CSS, JS, Images)
├── docs/                 # 📝 Comprehensive documentation and ADRs
├── .env.example          # 🔐 Environment variables (DB, SECRET_KEY)
├── docker-compose.yml    # 🐳 PostgreSQL container configuration
├── pyproject.toml        # ⚙️ Project configuration & dependencies (uv)
└── manage.py             # 🚀 Django management entry point
```

## Architecture & Security (Defense in Depth)

Proggy Wallet implements a **6-layer security strategy** to ensure financial data integrity:

1.  **Layer 1 (Frontend)**: Native HTML5 validation (`min`, required) for immediate feedback.
2.  **Layer 2 (Middleware)**: Django's CSRF and Authentication protection.
3.  **Layer 3 (Forms)**: Server-side sanitization and business rule validation.
4.  **Layer 4 (Logic)**: Atomic operations using `transaction.atomic()` to prevent partial updates.
5.  **Layer 5 (Models)**: Django `Validators` to protect the ORM and Admin entry points.
6.  **Layer 6 (Database)**: PostgreSQL `CheckConstraints` as the final physical line of defense.

## Tech Stack
* **Framework:** `Django 6.0+`.
* **Frontend:** `Bootstrap 5` + `Django Template Language (DTL)`.
* **Database:** `PostgreSQL`.
* **Security:** Django Auth, `CheckConstraints`, `Validators`.
* **Tooling:** `uv` (Package Manager), `Ruff` (Linter/Formatter), `Pytest`.
* **Infrastructure:** `Docker`.

> Done with ❤️ by [Aníbal Rojo](https://github.com/anibalrojosan).

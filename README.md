# Proggy Wallet 🪙

![Python](https://img.shields.io/badge/Python-3.12-green)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.110-009688)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

> This project is under active development. Currently it has successfully transitioned from a file-based prototype to a robust **PostgreSQL-backed OOP architecture**.
> Current Focus: **Phase 3: Enterprise Ecosystem (Web Framework)** where the project will be refactored to use the Django Framework.
>
> You can check the [DEVLOG](docs/development/DEVLOG.md) to follow my progress, technical hurdles, and implemented solutions while building this app.

**Proggy Wallet** is a comprehensive engineering roadmap designed to architect a production-ready **Full-Stack Fintech solution**. This project documents the complete lifecycle of modern software development, bridging the gap between a dynamic **Frontend prototype** and a scalable **Django ecosystem**.

It serves as a definitive technical reference for industry best practices, implementing a **Monolithic Architecture** through Django’s **MTV (Model-Template-View)** pattern. By consolidating logic and presentation, the project integrates advanced **Python logic**, **SQL persistence**, and automated **DevOps workflows** (Docker & CI/CD) to demonstrate the rigorous evolution from initial code to global cloud deployment.

## 📑 Index
1. [🔑 Key Features](#key-features)
2. [🚀 Quick Start](#quick-start)
3. [📈 Project Evolution](#project-evolution)
4. [📂 Project Structure](#project-structure)
5. [🏗️ Architecture & Security](#architecture--security)
6. [🛠️ Tech Stack](#tech-stack)

## Key Features

Proggy Wallet combines a modern user experience with a robust backend engine. The system is designed to handle the core requirements of a digital wallet while maintaining high standards of data integrity and security:

- **Financial Integrity:** All operations are managed by a `TransactionManager` service, ensuring atomic updates between accounts and persistent ledger records.
- **Advanced Security:** 
  - Password hashing using **bcrypt**.
  - Strict data validation and API schemas using **Pydantic** models.
- **Real-time SQL History:** Dynamic transaction history with server-side sorting and filtering, replacing static file reads.
- **Live User Directory:** A dynamic recipient selector for transfers that reflects the real-time state of the database.
- **OOP Architecture:** Clean separation of concerns using Domain Entities, Services, and Repositories.

## Quick Start

### 1. Prerequisites
This project uses [**uv**](https://docs.astral.sh/uv/) for blazing-fast Python package and project management. If you don't have it installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Installation & Setup
Clone the repository and sync the environment:

```bash
git clone https://github.com/your-username/proggy-wallet.git
cd proggy-wallet
uv sync
```

### 3. Execution
#### 3.1 **API Server (FastAPI):** 

Start the FastAPI server. It will be available at http://localhost:8000.

```bash
uv run uvicorn backend.app:app --reload
```

#### 3.2 **Frontend:** 
Open `frontend/index.html` in your browser (Recommended: Use VS Code 'Live Server').

#### 3.3 **Database Setup:**

#### 3.3.1 **Option A: Manual Setup**

Configure the environment variables: You can edit .env.example to your liking, or just copy it to .env and edit it.

   ```bash
   cp .env.example .env
   ```

Initialize the database:

   ```bash
   uv run python scripts/init_db.py
   ```

#### 3.3.2 **Option B: Docker Setup (Recommended for Development)**

If you have Docker and Docker Compose installed, you can skip manual installation:

```bash
# It will be initialized with the schema from backend/database/schema.sql.
docker-compose up -d
```

#### 3.4 **Quality Control & Testing:**
This project follows strict PEP 8 standards and is fully tested.

```bash
# Linting
uv run ruff check
# Tests
uv run pytest
```

## Project Evolution

This document provides a comprehensive overview of the project's evolution, from the initial prototype to the current state:

- 📝 **[DEVLOG](docs/development/DEVLOG.md)**: Daily technical logs, hurdles, and solutions.
- 🗺️ **[ROADMAP](docs/ROADMAP.md)**: Our path from prototype to production.
- 🏗️ **[ARCHITECTURE](docs/ARCHITECTURE.md)**: Deep dive into our system design and ADRs.

## Project Structure
```text
proggy-wallet/
├── backend/
│   ├── database/         # 🗄️ Persistence layer (PostgreSQL)
│   ├── modules/          # 🧠 Core business logic (Auth, Services, Entities, Repositories)
│   ├── tests/            # 🧪 Automated Unit Test suite (Pytest)
│   └── app.py            # 🌐 FastAPI REST entry point
├── docs/              
│   ├── adr/              # 📝 Architecture Decision Records (ADRs)
│   ├── development/      # 📝 Development guide and DEVLOG
│   └── ARCHITECTURE.md   # 📝 System design & Layer map
│   └── DATABASE.md       # 📝 Database schema and data model
│   └── PRD.md            # 📝 Project Requirements Document
│   └── ROADMAP.md        # 📝 Technical Roadmap
├── frontend/
│   ├── css/              # 🎨 Custom styles & Bootstrap 5
│   ├── js/               # ⚡ Interactive logic (jQuery & Fetch API)
│   └── *.html            # 🖥️ UI Views (Login, Dashboard, Transfers)
├── scripts/              # 📝 Scripts for DB initialization
├── .env.example          # 📝 Environment variables example
├── docker-compose.yml    # 🐳 Docker Compose configuration
├── pyproject.toml        # ⚙️ Project configuration & dependencies
└── README.md             # 🏠 Project documentation
```

## Architecture & Security (Implemented in Phase 2)

Proggy Wallet is built with a focus on **maintainability** and **financial integrity**. It's currently transitioning to a professional enterprise architecture:

*   **🏛️ Layered Architecture**: Clear separation of concerns between API, Service Layer (`TransactionManager`), and Domain Entities to ensure the system is easy to scale and test.
*   **💎 Software Atomicity**: Financial transactions follow the "all-or-nothing" principle. Manual rollback mechanisms are implemented to prevent data corruption during failures.
*   **🛡️ Industry-Standard Security**: User protection is paramount. `bcrypt` is used for secure, non-reversible password hashing and Pydantic for strict schema enforcement.
*   **📦 Repository Pattern**: Abstracting data access to allow a seamless migration from flat files to **PostgreSQL** without touching the core business logic.

## Tech Stack
* **Frontend:** `Bootstrap 5` + `jQuery`.
* **Backend:** `Python 3.12+` `FastAPI`, `Pydantic V2`.
* **Core:** Domain-Driven Design (Entities, Services, Repositories).
* **Database:** `PostgreSQL`.
* **Security:** `bcrypt` password hashing.
* **Tooling:** `uv` (Package Manager), `Ruff` (Linter/Formatter), `Pytest`.
* **Infrastructure:** `Docker`, `GitHub Actions` (Coming soon).

> Done with ❤️ by [Aníbal Rojo](https://github.com/anibalrojosan).

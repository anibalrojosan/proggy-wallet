# Proggy Wallet 🪙

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

> This project is under active development. Currently it's in **Phase 2: Robustness & Architecture**, where I'm refactoring the previous codebase to implement a **Repository Pattern** and migrate to **PostgreSQL** as the primary relational database management system.
>
> You can check the [DEVLOG](docs/development/DEVLOG.md) to follow my progress, technical hurdles, and implemented solutions while building this app.

**Proggy Wallet** is a comprehensive engineering roadmap designed to architect a production-ready **Full-Stack Fintech solution**. This project documents the complete lifecycle of modern software development, bridging the gap between a dynamic **Frontend prototype** and a scalable **Django ecosystem**.

It serves as a definitive technical reference for industry best practices, implementing a **Monolithic Architecture** through Django’s **MTV (Model-Template-View)** pattern. By consolidating logic and presentation, the project integrates advanced **Python logic**, **SQL persistence**, and automated **DevOps workflows** (Docker & CI/CD) to demonstrate the rigorous evolution from initial code to global cloud deployment.

## 📑 Index
1. [🚀 Quick Start](#quick-start)
2. [🔑 Key Features](#key-features)
3. [📈 Project Evolution](#project-evolution)
4. [🧪 Quality Control & Testing](#quality-control--testing)
5. [📂 Project Structure](#project-structure)
6. [🏗️ Architecture & Security](#architecture--security)
7. [🛠️ Tech Stack](#tech-stack)

## Key Features

Proggy Wallet combines a modern user experience with a robust backend engine. The system is designed to handle the core requirements of a digital wallet while maintaining high standards of data integrity and security:

*   🚀 **FastAPI REST API**: High-performance asynchronous backend with automatic documentation.
*   🔐 **Secure Auth**: Industry-standard password hashing with `bcrypt` to protect user identities.
*   💰 **Atomic Transactions**: Financial integrity ensured through manual rollback logic for transfers.
*   ✅ **Strict Validation**: Fail-fast data integrity using `Pydantic` models for all incoming requests.
*   📱 **Responsive UI**: A mobile-first web interface built with Bootstrap 5 and jQuery.

## Project Evolution

This document provides a comprehensive overview of the project's evolution, from the initial prototype to the current state:

- 📝 **[DEVLOG](docs/development/DEVLOG.md)**: Daily technical logs, hurdles, and solutions.
- 🗺️ **[ROADMAP](docs/ROADMAP.md)**: Our path from prototype to production.
- 🏗️ **[ARCHITECTURE](docs/ARCHITECTURE.md)**: Deep dive into our system design and ADRs.

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
*   **API Server (FastAPI):** Start the backend for frontend communication:
    ```bash
    uv run uvicorn backend.app:app --reload
    ```
*   **Frontend:** Open `frontend/index.html` in your browser (Recommended: Use VS Code 'Live Server').
*   **CLI Simulation:** Run a full end-to-end logic test:
    ```bash
    uv run python -m backend.main
    ```

## Quality Control & Testing
This project follows strict PEP 8 standards and is fully tested.
- **Linting**: `uv run ruff check`
- **Tests**: `uv run pytest`
> 💡 Full contribution guide available in [CONTRIBUTING.md](CONTRIBUTING.md)

## Project Structure
```text
proggy-wallet/
├── backend/
│   ├── data/              # 🗄️ Persistence layer (Secure CSV/JSON)
│   ├── modules/           # 🧠 Core business logic (Auth, Services, Entities)
│   ├── tests/             # 🧪 Automated Unit Test suite (Pytest)
│   ├── app.py             # 🌐 FastAPI REST entry point
│   └── main.py            # 🚀 Integration test script
├── docs/              
│   ├── adr/               # 📝 Architecture Decision Records (ADRs)
│   ├── development/       # 📝 Development guide and DEVLOG
│   └── ARCHITECTURE.md    # 📝 System design & Layer map
│   └── DATABASE.md        # 📝 Database schema and data model
│   └── PRD.md             # 📝 Project Requirements Document
│   └── ROADMAP.md         # 📝 Technical Roadmap
├── frontend/
│   ├── css/               # 🎨 Custom styles & Bootstrap 5
│   ├── js/                # ⚡ Interactive logic (jQuery & Fetch API)
│   └── *.html             # 🖥️ UI Views (Login, Dashboard, Transfers)
├── pyproject.toml         # ⚙️ Project configuration & dependencies
├── LICENSE                # ⚖️ MIT License
├── CONTRIBUTING.md        # 🤝 Contribution guidelines
└── README.md              # 🏠 Project documentation
```

## Architecture & Security (Phase 2)

Proggy Wallet is built with a focus on **maintainability** and **financial integrity**. It's currently transitioning to a professional enterprise architecture:

*   **🏛️ Layered Architecture**: Clear separation of concerns between API, Service Layer (`TransactionManager`), and Domain Entities to ensure the system is easy to scale and test.
*   **💎 Software Atomicity**: Financial transactions follow the "all-or-nothing" principle. Manual rollback mechanisms are implemented to prevent data corruption during failures.
*   **🛡️ Industry-Standard Security**: User protection is paramount. `bcrypt` is used for secure, non-reversible password hashing and Pydantic for strict schema enforcement.
*   **📦 Repository Pattern**: Abstracting data access to allow a seamless migration from flat files to **PostgreSQL** without touching the core business logic.

## Tech Stack
* **Frontend:** `HTML5`, `CSS/Bootstrap 5`, `JavaScript/jQuery`.
* **Backend:** `Python 3.12+`, `FastAPI`, `Pydantic V2`.
* **Security:** `Bcrypt` password hashing.
* **Tooling:** `uv` (Package Manager), `Ruff` (Linter/Formatter), `Pytest`.
* **Infrastructure:** `Docker` (Coming soon), `GitHub Actions`.

> Done with ❤️ by [Aníbal Rojo](https://github.com/anibalrojosan).

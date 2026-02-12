# Proggy Wallet 🪙

> This project is currently under development. You can check the [DEVLOG](docs/DEVLOG.md) to follow my progress, technical hurdles, and implemented solutions while building this app.

**Proggy Wallet** is a comprehensive engineering roadmap designed to architect a production-ready **Full-Stack Fintech solution**. This project documents the complete lifecycle of modern software development, bridging the gap between a dynamic **Frontend prototype** and a scalable **Django ecosystem**.

It serves as a definitive technical reference for industry best practices, implementing a **Monolithic Architecture** through Django’s **MTV (Model-Template-View)** pattern. By consolidating logic and presentation, the project integrates advanced **Python logic**, **SQL persistence**, and automated **DevOps workflows** (Docker & CI/CD) to demonstrate the rigorous evolution from initial code to global cloud deployment.

## 📑 Index
1. [🚀 Quick Start](#quick-start)
2. [🧪 Quality Control & Testing](#quality-control--testing)
3. [📂 Project Structure](#project-structure)
4. [🏗️ Architecture & Security](#architecture--security)
5. [🛠️ Tech Stack](#tech-stack)



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
We enforce high code quality standards using **Ruff** and **Pytest**.

*   **Run Unit Tests:**
    ```bash
    uv run pytest
    ```
*   **Linting Check (PEP 8):**
    ```bash
    uv run ruff check backend/
    ```
*   **Auto-Formatting:**
    ```bash
    uv run ruff format backend/
    ```

## Project Structure
```text
proggy-wallet/
├── backend/
│   ├── data/          # 🗄️ Persistence layer (Secure CSV/JSON)
│   ├── modules/       # 🧠 Core business logic (Auth, Services, Entities)
│   ├── tests/         # 🧪 Automated Unit Test suite (Pytest)
│   ├── app.py         # 🌐 FastAPI REST entry point
│   └── main.py        # 🚀 Integration test script
├── docs/              # 📖 Architecture, Roadmap, and ADRs
├── frontend/
│   ├── css/           # 🎨 Custom styles & Bootstrap 5
│   ├── js/            # ⚡ Interactive logic (jQuery & Fetch API)
│   └── *.html         # 🖥️ UI Views (Login, Dashboard, Transfers)
├── pyproject.toml     # ⚙️ Project configuration & dependencies
└── README.md          # 🏠 Project documentation
```

## Architecture & Security
Currently, the project is in **Phase 2: Robustness & Architecture**, focusing on:
*   **Layered Architecture:** Clear separation between API, Service Layer (`TransactionManager`), and Domain Entities.
*   **OOP Core:** Financial logic encapsulated within `Account` and `User` classes.
*   **Software Atomicity:** Manual rollback mechanisms to ensure financial transactions are "all-or-nothing".
*   **Security:** Industry-standard password hashing using `bcrypt`.
*   **Data Validation:** Strict schema enforcement with `Pydantic` (Fail-Fast principle).

## Tech Stack
* **Frontend:** `HTML5`, `CSS/Bootstrap 5`, `JavaScript/jQuery`.
* **Backend:** `Python 3.12+`, `FastAPI`, `Pydantic V2`.
* **Security:** `Bcrypt` password hashing.
* **Tooling:** `uv` (Package Manager), `Ruff` (Linter/Formatter), `Pytest`.
* **Infrastructure:** `Docker` (Coming soon), `GitHub Actions`.

> Done with ❤️ by [Aníbal Rojo](https://github.com/anibalrojosan).

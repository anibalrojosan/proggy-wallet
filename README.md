# Proggy Wallet 🪙

> This project is currently under development. You can check the [DEVLOG](docs/DEVLOG.md) to follow my progress, technical hurdles, and implemented solutions while building this app.

**Proggy Wallet** is a comprehensive engineering roadmap designed to architect a production-ready **Full-Stack Fintech solution**. This project documents the complete lifecycle of modern software development, bridging the gap between a dynamic **Frontend prototype** and a scalable **Django ecosystem**.

It serves as a definitive technical reference for industry best practices, implementing a **Monolithic Architecture** through Django’s **MTV (Model-Template-View)** pattern. By consolidating logic and presentation, the project integrates advanced **Python logic**, **SQL persistence**, and automated **DevOps workflows** (Docker & CI/CD) to demonstrate the rigorous evolution from initial code to global cloud deployment.

---

## 🚀 Getting Started

### 1. Prerequisites
This project uses [**uv**](https://docs.astral.sh/uv/) for blazing-fast Python package and project management. If you don't have it installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Installation
Clone the repository and sync the environment:

```bash
git clone https://github.com/your-username/proggy-wallet.git
cd proggy-wallet
uv sync
```

---

## 💻 How to Run

### Backend (Python)
You can run the system in two ways:

*   **Main Integration Script (CLI Simulation):**
    To run a full end-to-end simulation of the backend logic:
    ```bash
    uv run python -m backend.main
    ```
*   **API Server (FastAPI):**
    To start the server for frontend communication:
    ```bash
    uv run uvicorn backend.app:app --reload
    ```

### Frontend (Web Interface)
Since the frontend is built with HTML5 and jQuery, you can simply:
1.  Navigate to the `frontend/` folder.
2.  Open `index.html` in any modern web browser.

*Note: For the best experience while the API is running, using a local server extension (like VS Code 'Live Server') is recommended.*

---

## 🛠 Quality Control & Testing
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

---

## 📂 Project Structure Overview
```text
proggy-wallet/
├── backend/
│   ├── data/          # Persistence layer (CSV/JSON)
│   ├── modules/       # Core business logic (Auth, Wallet, Utils)
│   ├── tests/         # Unit tests suite (Pytest)
│   ├── app.py         # FastAPI entry point
│   └── main.py        # Integration test script
├── docs/              # Architecture, Roadmap, and ADRs
├── frontend/
│   ├── css/           # Custom styles & Bootstrap
│   ├── js/            # Interactive logic (jQuery/Fetch API)
│   └── *.html         # UI Views (Login, Menu, Transactions)
├── pyproject.toml     # Project configuration & dependencies
└── README.md          # Project documentation
```

---

### Tech Stack
* **Frontend:** `HTML5`, `CSS/Bootstrap 5`, `JavaScript/jQuery`.
* **Backend:** `Python`, `FastAPI` (Phase 1), `Django` (Phase 3).
* **Modern Tooling:** `uv` (Manager), `Ruff` (Linter), `Pydantic` (Validation), `Pytest` (Testing).
* **Infrastructure:** `Docker`, `GitHub Actions`.

> Done with ❤️ by Aníbal Rojo.

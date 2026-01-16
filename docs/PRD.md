# Project Requirements Document (PRD)

Project Name: `proggy-wallet`

## **1. Project Scope & Origins**

This project is developed as a self-authored solution based on real-world fintech industry challenges.
* Core Base: The initial Functional Requirements (MVP) are strictly based on the specifications for Dynamic Frontend and Python Data Management (previously referred to as Modules 2 & 3).
* Evolution: While the roadmap contemplates a future expansion to a Full Stack architecture (Django/SQL), this document defines the scope for the Foundation Phase, where the objective is to achieve a clean, modular, and professional architecture that serves as a solid baseline for future integrations.

## **2. Project Vision**

To develop a reference architecture for a digital wallet application. The primary goal is not just functionality, but technical excellence, utilizing a modern tech stack to validate inputs, manage financial states, and ensure code quality through continuous integration.

## **3. Tech Stack & Tools**

Development will be governed by a suite of modern tools ("Modern Python Stack") to ensure quality and maintainability.

| Area | Technology | Specific Purpose |
|---|---|---|
| **Frontend**       | **HTML5 / Bootstrap 5** | Semantic structure and responsive design (Mobile-first). |
|                    | **JavaScript / jQuery** | DOM manipulation and client-side logic (Login, visual validations). |
| **Backend**        | **Python 3.12+** | Business logic and data processing. |
| **Quality (QA)**   | **Ruff** | Strict linter and formatter (PEP 8) for all Python code. |
| **Management**     | **uv** | High-performance dependency and virtual environment manager. |
| **Validation**     | **Pydantic** | Data Schema definition to ensure integrity of transactions and users. |
| **Testing**        | **Pytest** | Unit testing suite to validate financial logic. |
| **Infrastructure** | **Docker** | Containerization of development and production environments. |
| **CI/CD**          | **GitHub Actions** | Automated testing and style validation on every commit. |

## **4. Functional Requirements (MVP - Foundation Phase)**

**A. Frontend Module (User Interface)**

The application must feature 5 interconnected and responsive views:
1. **Login** (`login.html`): User authentication. Must validate basic credentials via JS before allowing access.
2. **Dashboard** (`menu.html`): Main view displaying current balance and quick access shortcuts.
3. **Deposits** (`deposit.html`): Form to add funds. Must visually update the balance.
4. **Transfers** (`sendmoney.html`): Simulation of sending money to contacts. Requires contact selection and available amount validation.
5. **History** (`transactions.html`): Detailed table of movements (income and expenses).

**B. Logic & Data Module (Python Core)**

The backend (initially modular scripts) must handle the system's "hard" logic:

**1. Transaction Management**:

* Implement functions (and subsequently Classes) to calculate new balances.
* Validate that `transfer_amount <= available_balance`.

**2. Data Persistence**:
* Ability to read and write transaction history to flat files (`.csv` or `.json`) to simulate persistence.

**3. Type Validation**:
* Use of Pydantic to ensure amounts are positive and user data follows the correct format.

## **5. Non-Functional Requirements (Engineering Quality)**

- **Modularity**: Python code must be separated into distinct modules (`auth.py`, `transactions.py`, `utils.py`) rather than a single script.
- **Code Style**: The project must pass **Ruff** validation with zero errors or warnings.
- **Testing**: Critical functions (e.g., balance calculation) must have at least one unit test in **Pytest**.
- **Portability**: The project must include a `Dockerfile` allowing the Python logic to run in any isolated environment.

## **6. Phase Deliverables**

* **GitHub Repository**: With structured branches (`main`, `feature/auth`, `feature/transactions`).
* **Documentation**: Professional `README.md` explaining installation via `uv` and `Docker`.
* **Functional Prototype**: Navigate web application where user actions trigger Python logic (connected or simulated).
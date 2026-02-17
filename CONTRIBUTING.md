# Contributing to Proggy Wallet 🐧

First off, thank you for considering contributing to this project! I believe in open source software and collaboration to make communities that help people learn, get inspired and create amazing things. So i'm glad that you're here.

If you have any questions, please feel free to ask. You can reach me on [X](https://x.com/anibalrojosan) or [LinkedIn](https://www.linkedin.com/in/anibalrojosan/).

## 🛠 Development Environment Setup

This project uses [**uv**](https://docs.astral.sh/uv/) for dependency management.

1.  **Fork and Clone**: Fork the repository and clone it locally.
    ```
    git clone https://github.com/anibalrojosan/proggy-wallet
    cd proggy-wallet
    ```

2.  **Install Dependencies**: `uv sync`

3.  **Run the Application**: Use **Docker Compose** for the database: `docker compose up -d`.

4.  **Create a Branch**: Use a descriptive name for your branch:
    *   `feat/feature-name`
    *   `fix/bug-name`
    *   `docs/documentation-change`

## 📏 Coding Standards

We enforce high code quality standards using **Ruff**. Before submitting a Pull Request, please ensure your code passes all checks:

*   **Linting**: `uv run ruff check backend/`
*   **Formatting**: `uv run ruff format backend/`

## 🧪 Testing

All new features and bug fixes should include unit tests using **Pytest**.

*   **Run Tests**: `uv run pytest`

## 📥 Pull Request Process

1.  Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2.  Update the `README.md` or `docs/` with details of changes to the interface, this includes new environment variables, exposed ports, or location of data files.
3.  The PR will be merged once it has been reviewed and passes all CI checks.

## 📝 Commit Message Convention
We follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New features (e.g., `feat(db): add transactions table`)
- `fix:` Bug fixes
- `docs:` Documentation only changes
- `refactor:` Code changes that neither fix a bug nor add a feature
- `test:` Adding or correcting tests

## 🏗️ Architecture Standards
- Follow the **Layered Architecture** defined in `docs/ARCHITECTURE.md`.
- Use **Pydantic** for all data validation.
- Ensure all financial transactions are **atomic**.

---

*Last updated: 16 February, 2026 - Phase 2 - Sprint 16: Database Design & Setup*
# Development Guide

This document contains instructions for setting up and working on the Proggy Wallet project.

## Local Environment Setup

### Prerequisites
- **uv**: Python package and project manager.
- **Docker Desktop**: For running the PostgreSQL database.
- **WSL2**: (If on Windows) Ensure Docker integration is enabled for your distro.

### Database Infrastructure
We use PostgreSQL 18 via Docker Compose for local development.

```bash
# Start the database in the background
sudo docker compose up -d

# View database logs
sudo docker logs proggy_wallet_db

# Stop the database and remove data (Reset)
sudo docker compose down -v
```

### Python Development
We use `uv` for dependency management and `ruff` for code quality.

```bash
# Sync dependencies and create virtual environment
uv sync

# Run the FastAPI development server
uv run fastapi dev backend/app.py

# Run linter and formatter
uv run ruff check .
uv run ruff format .
```

### Testing
```bash
# Run all unit tests
uv run pytest
```

---

*Last updated: 16 February, 2026 - Phase 2 - Sprint 16: Database Design & Setup*
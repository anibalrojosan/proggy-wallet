[2026-01-16]

## Initial Project Setup - Tooling Configuration

• Installed and configured `uv` for Python dependency management
  - Installed uv. Verified installation with `uv --version`

• Created and configured `pyproject.toml` using uv
  - Project: `proggy-wallet`
  - Python >=3.12 requirement set
  - Main dependencies: `pydantic>=2.12.5`
  - Development dependencies in `[dependency-groups]`: `pytest>=9.0.2`, `ruff>=0.14.13`
  - Generated `uv.lock` file with exact dependency versions

• Configured Ruff for linting and formatting
  - Added `[tool.ruff]` section in `pyproject.toml`
  - Configuration: line-length 88, target-version py312
  - Selected rules: E, F, I, N, W, UP (strict PEP 8 compliance)
  - Formatting: double quotes, space indentation
  - Exception for `__init__.py` files (allows unused imports)

• Created project folder structure
  - `backend/modules/` - For Python modules (e.g. auth.py, wallet.py, utils.py)
  - `backend/data/` - For CSV/JSON persistence files
  - `backend/tests/` - For unit tests with pytest
  - `frontend/assets/`, `frontend/css/`, `frontend/js/` - For frontend resources
  - `docs/` - Existing documentation (PRD.md, ROADMAP.md)

• Configured `.gitignore`
  - Ignoring `.venv/`, `__pycache__/`, `*.pyc`, etc.
  - Ensuring `pyproject.toml` and `uv.lock` are committed

• Planned Phase 1: Foundations & Prototyping
  - Reviewed PRD.md and ROADMAP.md documents
  - Planned 10 sprints for Phase 1
  - Naming convention: issues `phase1-XX: description`, branches `feat/feature-name`
  - Organized sprints in logical order (backend first, then frontend, integration)

• Configured GitHub Projects
  - Created Kanban board linked to proggy-wallet repository
  - Structured issues will be used to make tickets for a clear development of the project.

**Current Status:** Setup complete, ready to start feature development. Next step: create `feat/backend-utils` branch for Sprint 1.

---

[2026-01-17]

## Phase1-01 and Phase1-02 Done

Created utility functions in `backend/modules/utils.py`
  
- Add read_json_file() and write_json_file() for JSON file I/O
- Add read_csv_file() and write_csv_file() for CSV file I/O
- Add validate_amount() function for positive amount validation

Create authentication functions in `backend/modules/auth.py`

- Add load_user() to load all users data from the JSON file.
- Add get_user() to get the user data by username.
- Add validate_credentials() to validate the username and password.

**Next steps**: continue with the wallet transactions module in branch `backend-wallet`.

---

[2026-01-18]

## Phase1-03: Wallet Transactions Module Completed

• Implemented complete wallet transactions module in `backend/modules/wallet.py`
  - `calculate_balance()` - Calculates balance from transaction history
  - `deposit()` - Processes deposit transactions with configurable source identifier
  - `transfer()` - Handles user-to-user transfers (creates transfer_out and transfer_in records)
  - `validate_transfer_balance()` - Validates sufficient balance before transfers
  - `record_transaction()` - Saves transactions to CSV file
  - `get_transaction_history()` - Retrieves all transactions for a user

• Defined CSV structure for transaction persistence
  - Columns: `date`, `type`, `from_user`, `to_user`, `amount`, `balance`
  - Transaction types: `deposit`, `transfer_in`, `transfer_out`
  - CSV file automatically created on first transaction

• Implemented validation logic
  - Positive amount validation using `utils.validate_amount()`
  - Balance sufficiency check to prevent overdrafts on transfers
  - User existence validation for deposits and transfers

• Deposit function with source identifier
  - Defined `from_user` to a configurable source parameter
  - Default source: `"external"`, supports custom sources (e.g., `"bank"`, `"card"`, `"cash"`)


• Manual testing and validation
  - Created comprehensive test script to validate all wallet functions
  - Tested edge cases: negative amounts, insufficient balance, non-existent users
  - Verified transaction CSV creation and data persistence
  - Confirmed balance calculations are accurate across all transaction types

**Current Status:** Phase1-03 complete. All acceptance criteria met. Ready to proceed with Phase1-04 (main script integration) or move to frontend sprints.

---
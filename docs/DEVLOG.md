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

[2026-01-21]

### Phase1-04: Create main script and integrate modules - Done

#### **Work Accomplished:**
*   **Entry Point Creation**: Implemented `backend/main.py` to orchestrate communication between the `auth`, `wallet`, and `utils` modules.
*   **Full Flow Simulation**: Achieved a complete end-to-end flow: Login → Balance Inquiry → Deposit → Transfer → History.
*   **Structural Refactoring**: Redesigned the `transactions.csv` file by adding `owner` and `description` columns to improve data traceability.
*   **Logic Correction**: Resolved a "double-counting" bug in balance calculations and addressed record redundancy in the transaction history.

#### **Key Learnings & Insights:**
1.  **Importance of data structure**: Maintaining a clear CSV with strategic columns like `owner` significantly helps to **simplify mathematical logic and functions**. By knowing exactly which user each record belongs to, the code becomes more declarative and less prone to interpretation errors.
2.  **Visual debugging and auditing**: Periodically reviewing how data is physically stored in the CSV is a fundamental practice. This manual inspection helps to **identify logic bugs** (such as balance "rebounds" or duplicate records) that might go unnoticed by automated tests, allowing for quick and efficient fixes.
3.  **Module-based execution**: Reinforced the understanding of how Python manages `sys.path`. Running the script as a module using `python -m backend.main` from the root directory ensures all absolute imports resolve correctly, maintaining architectural consistency.

**Current Status:** Phase 1-04 successfully completed. Backend is robust and ready for Frontend integration.

---

[2026-01-23] 
### Frontend Foundations & Login Implementation

#### **Added**:
- **Base Frontend Structure**: Created `index.html` and `css/custom.css` using **Bootstrap 5**.
- **Branding**: Defined a custom color scheme (Finance Green `#2ecc71`) and integrated a Penguin (🐧) SVG favicon.
- **Login View**: Implemented `login.html` with a responsive card-based design and form validation.
- **Interactive Logic**: Created `js/login.js` using **jQuery** to handle form submission and basic field validation.
- **Navigation Flow**: Connected the landing page "Start now" button to the login view and established a temporary redirect to `menu.html`.

#### Technical Notes
- **Bootstrap 5 Integration**: Used CDN for rapid prototyping of responsive components (Navbar, Cards, Forms).
- **jQuery for DOM Manipulation**: Implemented `event.preventDefault()` to handle form logic on the client side before future Django integration.
- **Mobile-First Approach**: Ensured all views are responsive, including specific UX tweaks like right-aligned menu items on mobile.

**Current Status:** Phases 1-05 and 1-06 completed. Next: further improvements to the frontend, add more page for transfers, transactions, etc.
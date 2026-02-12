# DEVLOG

This document outlines the development process of the `proggy-wallet` project. It is a record of the decisions made, the learnings gained, and the progress made.
It is a living document that will be updated as the project evolves.

# [2026-01-16]

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

# [2026-01-17]

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

# [2026-01-18]

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

# [2026-01-21]

## Phase1-04: Create main script and integrate modules - Done

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

# [2026-01-23] 
## Frontend Foundations & Login Implementation

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

# [2026-01-24]

## Phase1-07: Dashboard Menu Implementation

• **Dashboard View**: Created `menu.html` as the central hub of the application.
  - Implemented responsive navigation cards using Bootstrap 5 for Deposit, Transfer, and Movements.
  - Added user greeting and real-time balance display.

• **Interactive Logic**: Developed `js/menu.js` to handle session verification.
  - Added logic to redirect unauthorized users to the login page.
  - Implemented logout functionality to clear `localStorage` session data.

**Current Status**: Dashboard functional. Next: implementing specific wallet operations.

# [2026-01-25]

## Phase1-08 & Phase1-09: Wallet Operations (Deposits & Transfers)

• **Phase1-08: Deposits View**: Implemented `deposit.html` and `js/deposit.js`.
  - Created a simple form for loading funds with positive amount validation.
  - Integrated jQuery animations (fadeOut/fadeIn) for visual balance updates.

• **Phase1-09: Send Money View**: Developed `sendmoney.html` and `js/sendmoney.js`.
  - Implemented a dynamic recipient selector with a mock contact list.
  - **Overdraft Protection**: Added critical validation to prevent transfers exceeding the available balance.
  - Added a native browser confirmation dialog before processing transactions.

**Current Status**: Core wallet functionalities implemented on the frontend. Data persists in `localStorage`.

# [2026-01-26]

## Phase1-10: Transaction History View

• **History Interface**: Created `transactions.html` featuring a professional transaction table.
  - Implemented responsive design for mobile devices using scrollable containers.
  - Added a button group for quick filtering (All/Income/Expenses).

• **Data Management**: Developed `js/transactions.js` with advanced UI logic.
  - **Filtering & Sorting**: Implemented dynamic array filtering and a date-based sorting toggle (ASC/DESC).
  - **Dynamic Rendering**: Used Template Literals to inject HTML rows based on the user's transaction history.
  - Included a "No movements" state for empty transaction lists.

  **Next**: finally integrate the frontend with the backend and test the app.


## JS Concepts Review

While doing tickets 07 to 10, I needed to review a lot of concepts of JS and jQuery, and how to manipulate the DOM. Some of the most important concepts were:

### 1. Modern JavaScript Concepts (ES6+)
* **Template Literals (`Backticks`):** Technique for creating dynamic HTML by mixing text and variables without using concatenation with the plus sign (+).
* **Interpolation (`${}`):** The way to insert values inside a dynamic string.
* **Array Methods (`.filter()`, `.sort()`, `.forEach()`):** Tools to transform, order, and iterate through data lists efficiently.
* **Arrow Functions (`=>`):** Shorthand syntax for writing functions, widely used in filters and sorting.
* **Ternary Operator (`Condition ? True : False`):** A way to make quick decisions in a single line of code.
* **Object Destructuring (Pending):** An even cleaner way to extract data from objects like amounts or dates.

### 2. Logic and Execution
* **Hoisting:** JS behavior that allows defining functions at the bottom of the code and calling them from the top. This behavior it's fundamentally different to how Python reads and executes every line of code in a file.
* **Scope and Closures:** How variables and functions share a common space within document.ready and communicate with each other. Also, this if fundamentally different to how Python works (identation)
* **Date Handling (`new Date`):** Conversion of technical strings into date objects that can be compared or formatted.
* **Asynchrony (Callback concept):** Understanding that the code within a click event does not execute immediately, but when the action occurs in the future.

### 3. jQuery and DOM Manipulation
* **Selectors (`$('#id')`, `$('.class')`):** How JS locates specific HTML elements to interact with them.
* **DOM Injection (`.append()`, `.empty()`):** The process of clearing and writing new HTML content from the script.
* **Class Management (`.addClass()`, `.removeClass()`):** To dynamically change Bootstrap's visual design.
* **Event Handlers (`.click()`):** Creating interactivity by making the page respond to user actions.
* **Context (`$(this)`):** A way to refer to the exact element that received the click without repeating its name or ID.
* **Dollar sign `$` variable convention:** Using the $ symbol at the start of a variable to identify that it stores a jQuery element.

### 4. Browser APIs (Web APIs)
* **LocalStorage:** A system for saving data in the browser that persists even after refreshing the page.
* **JSON (`.parse()` and `.stringify()`):** The format for converting complex objects into text and vice versa.

# [2026-01-27]

## Phase1-11: Full-Stack Integration with FastAPI

#### **Work Accomplished:**
*   **Backend API Implementation**: Developed a robust REST API using **FastAPI** to replace standalone script execution.
    *   Created `backend/app.py` as the central entry point.
    *   Implemented **Pydantic** models (`LoginRequest`, `DepositRequest`, `TransferRequest`) for strict data validation.
    *   Configured **CORS Middleware** to allow secure communication with the frontend.
*   **Frontend Refactoring**: Migrated the entire frontend from `localStorage` mock data to real-time server communication.
    *   Implemented **Fetch API** with `async/await` in all JS modules (`login.js`, `menu.js`, `deposit.js`, `sendmoney.js`, `transactions.js`).
    *   Established a **Session Management** system using `localStorage` only for user identification, keeping financial data on the server.
*   **Architecture Documentation**: Established a professional documentation standard for the project's evolution.
    *   Created `docs/ARCHITECTURE.md` to outline the system's decoupled structure.
    *   Implemented **ADRs (Architecture Decision Records)** to document the rationale behind choosing FastAPI and initial flat-file persistence. Later changes in the arquitecture while improving the app will be documented this way.

#### **Key Learnings & Concepts Review:**

While doing issue #11, I had to investigate and learn a lot of topics of web dev and how to communicate the  Frontend and Backend of the app. Some of those topics were:

### 1. Modern Backend Architecture (FastAPI)
*   **ASGI & Uvicorn**: Understanding the asynchronous server standard that allows high-performance Python web apps.
*   **API Contracts**: Designing endpoints with semantic HTTP methods (`GET` for retrieval, `POST` for actions/creation, `PUT` for updates, `DELETE` for deletions).
*   **Pydantic Validation**: Leveraging "Fail Fast" principles where the server rejects invalid data (e.g., negative amounts) automatically before processing.
*   **HTTP Exceptions**: Using standard status codes (401 Unauthorized, 404 Not Found, 422 Validation Error) to communicate with the client.

### 2. Frontend Integration
*   **Asynchronous JavaScript**: Mastering `async/await` to handle server latency without freezing the UI.
*   **Fetch API & Headers**: Using `Content-Type: application/json` to ensure the frontend and backend speak the same language.
*   **Single Source of Truth**: Shifting the authority of data from the browser's `localStorage` to the server's CSV/JSON files.
*   **Defensive Programming**: Implementing `parseFloat()` and `.get()` to handle data type conversions between CSV strings and JavaScript numbers. This is a good practice to avoid errors and unexpected behavior. `.get()` is a good way to handle the case where the data is not found.

### 3. Engineering Best Practices
*   **CORS Security**: Understanding why browsers block cross-origin requests and how to safely enable them during development.
*   **Living Documentation**: The importance of documenting the "Why" (ADRs) and the "How" (Architecture) while the code is still fresh.
*   **Decoupled Design**: Realizing that the Frontend is just a "viewer" while the Backend is the "brain and memory" of the system. it's important to keep the frontend and backend separated to make the app more maintainable and scalable.

**Current Status:** Phase1-11 successfully completed. The application is now a fully functional Full-Stack system. Next step: add unit tests for critical functions and update documentation.

# [2026-01-30]

## Phase1-12: Quality Assurance & Unit Testing (Part 1)

• **Testing Infrastructure**: Configured `pytest` as the primary testing framework.
  - Implemented the first set of unit tests for `backend/modules/utils.py` focusing on amount validation.

• **Authentication Testing**: Developed a comprehensive test suite for `auth.py`.
  - Leveraged `pytest.fixture` and `monkeypatch` to simulate user data without relying on physical JSON files.
  - Covered scenarios: successful login, incorrect password, and non-existent users.

**Current Status**: Backend core (Utils & Auth) protected by tests. Ready to proceed with the Wallet module.

# [2026-01-31]

## Phase1-12: Wallet Testing & Project Finalization (Phase 1 Done)

• **Wallet Module Robustness**: Completed the test suite for `backend/modules/wallet.py`.
  - **Logic Testing**: Implemented `TestCalculateBalance` to verify mathematical accuracy across multiple transaction types.
  - **Security Testing**: Created `TestTransfer` with edge case coverage (insufficient balance, negative amounts, invalid users).
  - **Persistence Testing**: Added tests for `deposit` and `get_transaction_history` using mocked environments to ensure data integrity.

• **Code Quality & Standards**:
  - Ran `Ruff` for project-wide linting and formatting.
  - Adjusted `line-length` to 110 in `pyproject.toml` to better accommodate descriptive docstrings and complex logic.
  - Achieved zero linting errors across the entire backend.

• **Documentation & UX**:
  - Refactored `README.md` into a professional technical guide.Included a Quick Start guide, installation instructions with `uv`, and a detailed project structure overview.
  - Added clear commands for running the CLI simulation, the FastAPI server, and the test suite.

**Current Status**: Phase 1 officially completed. The project has a robust, tested, and well-documented foundation. 

**Next Step**: Transition to Phase 2 (Architecture & Robustness), starting with **Class Diagrams** and **ERD design** for OOP refactoring and PostgreSQL integration.

# [2026-02-10]

## Phase 2: Initiation & Data Modeling (Sprint 13)

#### **Task 1: Architecture Design & Documentation**
*   **OOP Blueprint**: Designed the core class structure for Phase 2 using Mermaid.js.
*   **Decoupling Strategy**: Established the separation between `User` (identity) and `Account` (financial state) to follow the Single Responsibility Principle.
*   **Documentation**: Created `docs/CLASS_DIAGRAM.md` explaining the rationale behind the new architecture and the DTO (Data Transfer Object) pattern.

#### **Task 2: Data Validation with Pydantic**
*   **Schema Definition**: Implemented `backend/modules/models.py` with strict Pydantic models for `User` and `Transaction`.
*   **Fail-Fast Validation**: Integrated automatic checks for email formatting (`EmailStr`), positive amounts (`gt=0`), and restricted transaction types (`Literal`).
*   **Modern Python Standards**: Adopted Python 3.10+ syntax (`| None` for unions) and enforced strict linting with Ruff.

#### **Concepts that I learned:**
*   **DTO (Data Transfer Objects) Pattern**: Understanding why we split models into `Base`, `Create`, and `Final` versions. This prevents sensitive data leaks (like passwords) and follows the **DRY** principle by sharing common fields across different stages of the data lifecycle.
*   **Refactoring Strategy**: Learned that a professional refactor involves restructuring code without changing its external behavior. The "Build and Replace" strategy allows for a smooth transition from procedural functions to OOP without breaking the application.
*   **Pydantic Power Features**: Explored how `Field` constraints (like `gt=0` or `min_length`) and `Literal` types act as "guards" for the application, ensuring data integrity before it even reaches the business logic.
*   **Modern Python Typing**: Transitioned from the old `Optional[T]` syntax to the modern Python 3.10+ Pipe operator (`T | None`), making the code cleaner and more readable.

**Current Status:** Data layer is now robust and self-validating. Ready to transition from procedural logic to Object-Oriented entities.

# [2026-02-11]

## Phase 2: Core Entities & Security Layer (Sprint 14)

#### **Task 1: OOP Entity Implementation**
*   **Financial Engine**: Created the `Account` entity in `backend/modules/entities.py`, encapsulating balance management and internal business rules (e.g., preventing insufficient funds).
*   **Identity Management**: Implemented the `User` entity with 'composition', where each user automatically owns and manages an `Account` instance.
*   **Encapsulation**: Moved logic from standalone functions to class methods, ensuring that the internal state of objects can only be modified through authorized behaviors.

#### **Task 2: Secure Authentication Upgrade**
*   **Password Hashing**: Integrated `bcrypt` for industry-standard security. Replaced legacy plain-text passwords with non-reversible cryptographic hashes.
*   **Data Migration**: Developed and executed `migrate_passwords.py` to transform the existing `users.json` database into a secure hashed format.
*   **Auth Refactoring**: Updated `auth.py` to leverage the `User` entity's `check_password` method, ensuring the entire login flow is now secure and OOP-compliant.

#### **Task 3: API Integration & Bug Fixing**
*   **Model Compatibility**: Refactored `backend/app.py` to handle the transition from dictionary-based data to Pydantic objects, resolving "subscriptable" type errors.
*   **Dependency Management**: Successfully managed new library installations (`bcrypt`, `email-validator`) using `uv`.

**Current Status:** Sprint 14 core entities are functional and secure. The system successfully validates hashed credentials and manages state via objects.

#### **Task 4: Wallet Module Refactoring (OOP Integration)**
*   **Account Entity Integration**: Refactored `backend/modules/wallet.py` to use the new `Account` entity. 
    *   In `deposit`: Replaced manual addition with `account.add_funds(amount)`.
    *   In `transfer`: Implemented a dual-account flow using `sender_account.remove_funds(amount)` and `receiver_account.add_funds(amount)`.
*   **Logic Consolidation**: Eliminated the redundant `validate_transfer_balance` function, centralizing business rules (like overdraft protection) within the `Account` class (Single Source of Truth).
*   **Data Access Upgrade**: Updated code to use dot notation (`user_data.balance`) for Pydantic models, improving consistency with the new type system.

#### **Task 5: Critical Bug Fix - CSV Persistence Error**
*   **Issue**: After the refactor, deposits and transfers were failing with a `400 Bad Request` or `500 Internal Server Error`. The backend logs showed: `ValueError: dict contains fields not in fieldnames: 'id'`.
*   **Root Cause Analysis**: 
    1.  The `record_transaction` function was manually injecting an `id` field into the transaction dictionary before saving.
    2.  The `Transaction` Pydantic model had `extra: "allow"`, which masked the issue during validation.
    3.  The `csv.DictWriter` in `utils.py` strictly enforces that the data dictionary keys must match the CSV headers. Since `id` was not a column in `transactions.csv`, the writer crashed.
*   **Resolution**: Removed the manual `id` injection in `wallet.py`. This ensured the transaction data structure remains perfectly aligned with the CSV schema.

#### **Key Learnings & Insights:**
1.  **The Hidden Cost of `extra: "allow"`**: While flexible, allowing extra fields in Pydantic models can hide data integrity issues that only surface during persistence (like writing to a strict CSV). Now I opted to set `"extra": "forbid"` so Pydantic will raise an error if a field is not in the model.
2.  **Strict CSV Contracts**: The Python `csv` module is very sensitive to dictionary keys. When refactoring towards OOP/Pydantic, it's crucial to ensure that the "dumped" dictionaries don't contain metadata fields that aren't present in the storage file. This sensitivity is due to the behavior of `csv.DictWriter` (it creates a 'contract'), which raises a `ValueError` if a field is not in the headers.
3.  **Frontend Debugging**: Encountered an issue where the browser would refresh too quickly to read error messages. 
    *   *Pro-tip*: Using "Preserve Log" in DevTools is essential when debugging forms that trigger page reloads.

## Phase 2: Layered Architecture Refactor & Critical Bug Fixes

#### **Task 6: Backend Layered Architecture Implementation**
*   **Data Layer Refinement**: Introduced `UserInDB` in `models.py` to strictly separate persistence data (including password hashes) from public user profiles.
*   **Service Layer Upgrade**: Refactored `AuthService` in `auth.py` to handle the transition from raw JSON dictionaries to Pydantic models and Domain Entities.
*   **Domain Logic Consolidation**: Updated `entities.py` to ensure the `User` entity correctly maps password hashes from the database model, enabling secure authentication.

#### **Task 7: System-Wide Bug Resolution**
*   **App Balance Fix**: Resolved a critical UI bug where the balance displayed "Error loading balance". Fixed the `app.get("/wallet/status/{username}")` endpoint to correctly access the `Account` entity within the `User` object.
*   **Deposit & Transfer Restoration**: Fixed a `500 Internal Server Error` in wallet operations caused by legacy calls to non-existent functions. Replaced all procedural calls with the new `AuthService.get_user_entity()` pattern.
*   **JSON Parsing Fix**: Corrected a data structure mismatch in `AuthService._load_users_data()` that was preventing the system from iterating over the user list correctly.

#### **Task 8: Architecture Documentation**
*   **Internal Design Standards**: Updated `docs/ARCHITECTURE.md` to include a detailed map of the new layered architecture (API -> Orchestration -> Persistence -> Domain).
*   **Error Handling Policy**: Documented a standardized exception propagation strategy to ensure technical errors are gracefully converted into meaningful HTTP responses for the frontend.

#### **Key Learnings & Insights:**
1.  **Decoupling for Stability**: This refactor proved that decoupling the "how" (JSON storage) from the "what" (Business Rules) makes the system much easier to debug. Once the `AuthService` was fixed, multiple bugs across the app were resolved simultaneously.
2.  **The Role of DTOs**: Using `UserInDB` as a specific model for database operations prevented security leaks and made the code more declarative. It acts as a "security gate" between the raw storage and the application logic.
3.  **Layered Error Propagation**: Moving from generic `except Exception` blocks to specific error catching (e.g., `ValueError` for business rules, `FileNotFoundError` for data) significantly improved the API's reliability and the quality of frontend feedback.

**Current Status:** The system is now fully stable under the new layered architecture. All core features (Login, Balance, Deposits, Transfers, History) are operational. **Next:** Proceed to Sprint 15.



# [2026-02-12]

## Phase 2: Transaction Engine & Service Layer (Sprint 15)

#### **Task 1: Transaction Manager Implementation**
*   **Service Layer Creation**: Developed `backend/modules/services.py` to house the `TransactionManager` class, centralizing the orchestration of financial movements.
*   **Atomic Transfer Logic**: Implemented a "Rollback" mechanism in `execute_transfer`. If the deposit into the destination account fails, the system automatically reverts the withdrawal from the sender's account, ensuring no money is lost during technical failures.
*   **Encapsulated Deposits**: Created `execute_deposit` to handle fund injections, ensuring all entries are validated and recorded through a single authorized path.

#### **Task 2: Persistence & Validation Integration**
*   **CSV Append Logic**: Upgraded `backend/modules/utils.py` with `append_csv_file()`. This new utility uses Python's `"a"` (append) mode to ensure transaction history is cumulative and not overwritten.
*   **Pydantic Enforcement**: Integrated `TransactionCreate` model validation within the recording flow. Every transaction is now validated against business rules (e.g., positive amounts) before touching the physical disk.
*   **Audit Trail**: Standardized the `_record` method to ensure consistent data across all transaction types (`date`, `type`, `from_user`, `to_user`, `amount`, `balance`).

#### **Key Learnings & Insights:**
Why the transaction manager was designed this way:
1.  **Orchestration vs. Entity Logic**: 
    -   **Service Layer Pattern**: this pattern was used to decouple the "how" (CSV storage) from the "what" (Business Rules). 
    - While the `Account` entity (from Sprint 14) knows *how* to change its own balance, it shouldn't know about other accounts or how to write to a CSV. 
    - The `TransactionManager` coordinates the transfer between two accounts and the storage system.
2.  **Software Atomicity**: In a system without a formal SQL database, we must simulate "All-or-Nothing" operations. 
    - **'Atomicity'** means that a complex operation must be a unique unit of work and must be indivisible. In other words, a complex operation must be completed correctly and if not, the operation must not be executed at all. For this wallet case, the manual rollback logic ensures data integrity even when errors occur mid-process. 
    - For example, if the deposit into the destination account fails, the system automatically reverts the withdrawal from the sender's account, ensuring no money is lost during technical failures. 
    - This is a very important concept to understand and apply in any system, not only in this one.
3.  **Single Responsibility Principle (SRP)**: 
    - By moving transaction logic out of `wallet.py` and into a dedicated service, we've made the code easier to test and maintain. 
    - `wallet.py` is now becoming a legacy bridge, while `services.py` represents the future-proof core of the app.
4.  **Defensive Persistence**: 
    - Using a specific `append` function instead of a generic `write` function prevents catastrophic data loss. 
    - The logic to write the CSV header only when the file is new ensures the history remains a valid, readable dataset for the frontend.
5. **Using services for escalability**
    - Separating the logic in services allows for easier scalability and maintenance of the code.
    - This way it's easier to migrate the data from a flat file to a database in the future.
6. **Data integrity**:
    - Using append_csv_file() instead of write_csv_file() ensures that the data is added to the file and not overwritten.
    - This way, the movements history (audit trail) is not lost and the history is preserved.

**Current Status:** Sprint 15 completed. The core financial engine is now robust, atomic, and follows professional OOP standards. Ready for Sprint 16 (Database Setup).
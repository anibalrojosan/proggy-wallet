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

---

[2026-01-23] 
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

---

[2026-01-24]

## Phase1-07: Dashboard Menu Implementation

• **Dashboard View**: Created `menu.html` as the central hub of the application.
  - Implemented responsive navigation cards using Bootstrap 5 for Deposit, Transfer, and Movements.
  - Added user greeting and real-time balance display.

• **Interactive Logic**: Developed `js/menu.js` to handle session verification.
  - Added logic to redirect unauthorized users to the login page.
  - Implemented logout functionality to clear `localStorage` session data.

**Current Status**: Dashboard functional. Next: implementing specific wallet operations.

---

[2026-01-25]

## Phase1-08 & Phase1-09: Wallet Operations (Deposits & Transfers)

• **Phase1-08: Deposits View**: Implemented `deposit.html` and `js/deposit.js`.
  - Created a simple form for loading funds with positive amount validation.
  - Integrated jQuery animations (fadeOut/fadeIn) for visual balance updates.

• **Phase1-09: Send Money View**: Developed `sendmoney.html` and `js/sendmoney.js`.
  - Implemented a dynamic recipient selector with a mock contact list.
  - **Overdraft Protection**: Added critical validation to prevent transfers exceeding the available balance.
  - Added a native browser confirmation dialog before processing transactions.

**Current Status**: Core wallet functionalities implemented on the frontend. Data persists in `localStorage`.

---

[2026-01-26]

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

---

[2026-01-27]

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

---
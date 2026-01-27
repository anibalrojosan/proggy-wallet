# 🏗️ System Architecture: Proggy Wallet

## 1. Overview
**Proggy Wallet** is a virtual wallet application designed to manage personal finances through a simple and secure web interface. The system enables users to perform core banking operations (deposits, transfers, and transaction history tracking) within a dynamic, real-time environment.

The architecture follows a **Decoupled Client-Server model**, ensuring that the User Interface (UI) and the Business Logic can evolve independently.

## 2. System Components

### 2.1 Frontend (The Client)
*   **Responsibility:** Data presentation, user input capture, and local session management.
*   **State Management:** The client is "stateless" regarding financial data. It does not calculate balances; it only requests and displays data provided by the server.
*   **Technologies:** `HTML5`, `Bootstrap 5` (Responsive UI), and `jQuery` (DOM manipulation and UX effects).

### 2.2 Backend (The Server)
*   **Responsibility:** The "Single Source of Truth." It handles data validation, transaction processing, and persistence.
*   **Interface:** It exposes a RESTful API using FastAPI.
*   **Technologies:** `Python 3.12+`, `FastAPI`, and `Pydantic` (Schema validation).

## 3. Data Flow (HTTP Request/Response Cycle)

Communication between components follows an asynchronous pattern:

1.  **Trigger:** The user performs an action (e.g., clicking "Transfer").
2.  **Request:** The Frontend emits an asynchronous `fetch` request, sending a JSON object in the `body` and specifying `Content-Type: application/json` in the headers.
3.  **Validation:** FastAPI receives the request and utilizes **Pydantic Models** to ensure data types and constraints (e.g., positive amounts) are met before execution.
4.  **Business Logic:** Python modules (`auth.py`, `wallet.py`) process the operation.
5.  **Persistence:** Flat files (`users.json`, `transactions.csv`) are updated on the server.
6.  **Response:** The Backend returns an HTTP status code (e.g., 200: OK, 400: Bad Request) and a JSON response object.
7.  **UI Update:** The Frontend receives the response and updates the DOM dynamically without a page reload.

## 4. Technology Stack (Phase 1 Decisions)

| Technology | Rationale |
| :--- | :--- |
| **FastAPI** | Chosen for its high performance (ASGI), automatic Pydantic validation, and instant OpenAPI (Swagger) documentation. |
| **jQuery** | Used to simplify DOM manipulation and Fetch API handling in this initial prototype, keeping the codebase lightweight. |
| **CSV/JSON** | Selected for Phase 1 to prototype persistence without the overhead of a relational database management system. |
| **uv** | A next-generation Python package manager ensuring reproducible environments and ultra-fast dependency resolution. |

---
*Last Updated: January 27, 2026 - Issue #11 (Frontend-Backend Integration)*
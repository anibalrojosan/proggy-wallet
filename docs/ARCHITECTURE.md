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

## 4. Backend Internal Architecture (Layered Design)

During the OOP refactor (Phase 2), the backend is organized into specialized layers to ensure separation of concerns and maintainability.

### 4.1 Layer Map & Dependencies
Dependencies always point **inwards**. Inner layers (Entities/Models) are "pure" and do not know about outer layers (API/Services).

```text
    [ API (app.py) ]
           │
           ▼
    [ Orchestration (wallet.py) ]
           │
           ▼
    [ Persistence (auth.py) ] ──────┐
           │                        │
           ▼                        ▼
    [ Domain (entities.py) ] ──▶ [ Schemas (models.py) ]
```

| Layer | Component | Responsibility | Dependencies |
| :--- | :--- | :--- | :--- |
| **API** | `app.py` | HTTP Entry point, routing, and JSON responses. | Wallet, AuthService, Models |
| **Orchestration** | `wallet.py` | Coordinates complex flows (e.g., transfers between two accounts). | Entities, AuthService, Models |
| **Persistence** | `auth.py` | Data access logic. Bridges JSON files with Domain Entities. | Models, Entities |
| **Domain (Core)** | `entities.py` | Pure Business Logic (Rules for money, account behavior). | Models |
| **Schemas** | `models.py` | Data structure definitions and Pydantic validation. | (None) |

### 4.2 Core Components Description

*   **Schemas (`models.py`)**: Defines the "shape" of data. `UserInDB` ensures that data loaded from JSON is complete and valid before it touches any logic.
*   **Domain Entities (`entities.py`)**: The "Truth" of the system. Classes like `Account` encapsulate rules (e.g., "insufficient funds" validation) that are independent of how data is stored.
*   **Services (`auth.py`)**: The only layer aware of `users.json`. It handles authentication and transforms raw JSON data into rich Domain Entities.
*   **Orchestrator (`wallet.py`)**: Manages the interaction between entities and records the results in the transaction history (`transactions.csv`).

### 4.3 Error Handling Policy

To prevent generic "Internal Server Errors", the following policy is applied across layers:

#### Exception Mapping
| Layer | Action | Example |
| :--- | :--- | :--- |
| **Domain** | Raise semantic Python exceptions | `raise ValueError("Insufficient funds")` |
| **Persistence** | Raise data-related exceptions | `raise FileNotFoundError("User not found")` |
| **API** | Catch and convert to `HTTPException` | `raise HTTPException(status_code=400, detail=...)` |

#### Error Propagation Flow
When an error occurs, it travels upwards as follows:

1.  **Domain (`entities.py`)**: Detects a rule violation (e.g., negative deposit) and **raises** `ValueError`.
2.  **Orchestration (`wallet.py`)**: Does not catch the error (letting it bubble up) or adds context.
3.  **API (`app.py`)**:
    *   `except ValueError`: Returns **400 Bad Request** (Client error).
    *   `except FileNotFoundError`: Returns **404 Not Found** (Resource missing).
    *   `except Exception`: Returns **500 Internal Server Error** (Unexpected bug).

This ensures the Frontend receives a clear `detail` message to show the user, instead of a generic failure.

## 5. Technology Stack (Phase 1 & 2 Decisions)

| Technology | Rationale |
| :--- | :--- |
| **FastAPI** | Chosen for its high performance (ASGI), automatic Pydantic validation, and instant OpenAPI (Swagger) documentation. |
| **jQuery** | Used to simplify DOM manipulation and Fetch API handling in this initial prototype, keeping the codebase lightweight. |
| **CSV/JSON** | Used for Phase 1 & 2 prototyping. Architecture is now decoupled (via `auth.py`) to allow a seamless migration to **PostgreSQL** in Phase 3 without touching business logic. |
| **uv** | A next-generation Python package manager ensuring reproducible environments and ultra-fast dependency resolution. |


---
*Last Updated: 11 February, 2026 - Phase 2 - OOP Refactor & Layered Architecture*

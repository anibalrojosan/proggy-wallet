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
4.  **Business Logic:** Python modules process the operation via the Service Layer.
5.  **Persistence:** Data is persisted in PostgreSQL via the Repository layer.
6.  **Response:** The Backend returns an HTTP status code (e.g., 200: OK, 400: Bad Request) and a JSON response object.
7.  **UI Update:** The Frontend receives the response and updates the DOM dynamically without a page reload.

## 4. Backend Internal Architecture (Layered Design)

The backend follows a **Layered Architecture** to ensure separation of concerns. This allows us to change the database engine or the API framework with minimal impact on business logic.

### 4.1 Layer Map & Dependencies
Dependencies always point **inwards**. Outer layers (API) depend on inner layers (Services/Repositories), but the Domain (Entities) remains pure and independent.

```text
    [ API Layer (app.py) ]
             │
             ▼
    [ Service Layer (services.py, auth.py) ]
             │
             ▼
    [ Repository Layer (repository.py) ]
             │
             ▼
    [ Infrastructure Layer (PostgreSQL) ]
             │
             └───────────▶ [ Domain Entities (entities.py) ]
                                      │
                                      ▼
                           [ Schemas (models.py) ]
```

| Layer | Component | Responsibility | Dependencies |
| :--- | :--- | :--- | :--- |
| **API** | `app.py` | HTTP Entry point, routing, and JSON responses. | Services, Models |
| **Service** | `services.py`, `auth.py` | **Orchestration**: Business flows (Transfers) and **Identity Logic** (Authentication/Login). | Repositories, Entities, Models |
| **Repository** | `repository.py` | **Data Access**: Handles SQL queries and maps DB rows to Domain Entities. | Models, Entities |
| **Domain** | `entities.py` | **Core Logic**: Pure business rules (e.g., "how an account calculates its state"). | Models |
| **Schemas** | `models.py` | **Data Contracts**: Pydantic models for validation and DTOs. | (None) |

### 4.2 Why this Layer Map? (Justification)
This specific design (API -> Service -> Repository -> DB) is the industry standard for robust applications because:
1. **Decoupling**: The `Service Layer` doesn't know *how* data is saved (SQL or CSV), it only knows *what* it wants to do.
2. **Testability**: We can test the `Service Layer` by "mocking" the `Repository` without needing a real database.
3. **Maintainability**: If we move from PostgreSQL to another DB, we only change the `Repository` layer. The `Service` and `API` layers remain untouched.
4. **Consistency**: The `Repository` ensures that everything coming out of the database is converted into a valid `Entity` or `Model` before reaching the rest of the app.

### 4.3 Error Handling Policy

To prevent generic "Internal Server Errors", the following policy is applied across layers:

#### Exception Mapping
| Layer | Action | Example |
| :--- | :--- | :--- |
| **Domain** | Raise semantic Python exceptions | `raise ValueError("Insufficient funds")` |
| **Repository** | Raise data-related exceptions | `raise DBError("Connection failed")` |
| **API** | Catch and convert to `HTTPException` | `raise HTTPException(status_code=400, detail=...)` |

---

## 5. Technology Stack

| Technology | Rationale |
| :--- | :--- |
| **FastAPI** | High performance (ASGI), automatic Pydantic validation, and instant OpenAPI documentation. |
| **PostgreSQL** | **(Phase 2 Upgrade)** Provides ACID compliance, relational integrity, and professional scalability. |
| **Pydantic** | Strict schema enforcement and data validation (Fail-Fast principle). |
| **uv** | Next-generation package manager for reproducible environments. |
| **Docker** | Used to containerize the PostgreSQL instance for consistent development environments. |

---

## 6. ADRs (Architecture Decision Records)

| ID | Decision | Status | Key Justification (Summary) |
| :--- | :--- | :--- | :--- |
| [ADR-01](adr/01-use-fastapi-for-backend-integration.md) | **FastAPI** | Accepted | Quick and asynchronous integration with automatic validation. |
| [ADR-02](adr/02-use-csv-for-initial-persistence.md) | **CSV/JSON** | Superado | Useful for rapid prototyping in Phase 1. Replaced by SQL in Phase 2. |
| [ADR-03](adr/03-use-postgresql-for-persistent-storage.md) | **PostgreSQL** | Accepted | Needed for data integrity, ACID transactions, and professional scalability. |

---
*Last Updated: 13 February, 2026 - Phase 2 - Sprint 16: Database Design & Setup*

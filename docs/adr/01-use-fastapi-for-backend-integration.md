# ADR 01: Use FastAPI for Backend Integration

## Status
Accepted

## Context
In Phase 1 of the Proggy Wallet project, I needed to transition from standalone Python scripts to a connected web application. I required a backend framework that could bridge the gap between our Python logic (`auth.py`, `wallet.py`) and the jQuery-based frontend.

The primary candidates were **Flask** (a traditional micro-framework) and **FastAPI** (a modern ASGI framework).

## Decision
I decided to use **FastAPI** as the core web framework for the backend.

## Rationale
The decision was based on several key factors relevant to modern development standards in 2026:

1.  **Automatic Data Validation:** Unlike Flask, FastAPI uses Pydantic for data validation. This allows us to define strict schemas (e.g., `LoginRequest`, `TransferRequest`) that automatically reject malformed data before it reaches our business logic.
2.  **Performance:** FastAPI is built on Starlette and Uvicorn, making it one of the fastest Python frameworks available. Its native support for `async/await` aligns with our goal of building a scalable system.
3.  **Developer Experience (DX):** FastAPI automatically generates interactive API documentation using Swagger UI. This significantly simplified testing the endpoints during the integration phase without needing external tools like Postman.
4.  **Type Safety:** By leveraging Python type hints, FastAPI reduces bugs related to incorrect data types, which is critical for a financial application handling currency and user balances.

## Consequences
*   **Positive:** I have a self-documenting API that is easy to test and highly robust against invalid inputs.
*   **Positive:** The transition to more complex architectures (like Phase 2's OOP refactor) will be smoother due to the structured nature of FastAPI.
*   **Negative:** There is a slightly steeper learning curve for developers only familiar with synchronous WSGI frameworks like Flask.
*   **Neutral:** We must ensure the server is run using an ASGI server like `uvicorn` instead of standard Python execution.

---
*Date: January 27, 2026* | *Author: Aníbal Rojo*
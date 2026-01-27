# ADR 0002: Use CSV and JSON for Initial Data Persistence

## Status
Accepted

## Context
During Phase 1 (Foundations & Prototyping) of the Proggy Wallet project, we needed a way to persist user data and transaction history. The system requires storing user credentials, balances, and a record of every financial movement (deposits, transfers).

I had to choose between starting immediately with a Relational Database (like PostgreSQL) or using flat files (CSV/JSON).

## Decision
I decided to use **JSON** for user management and **CSV** for transaction history as the initial persistence layer.

## Rationale
The decision to use flat files for the prototype phase was driven by several strategic factors:

1.  **Development Speed:** Setting up a PostgreSQL database, managing migrations, and writing SQL queries would have significantly slowed down the initial development of the core business logic and frontend integration.
2.  **Ease of Inspection:** CSV and JSON files are human-readable and can be edited directly with any text editor. This made it easy to debug transaction logic and verify data integrity during the early stages of development.
3.  **Portability:** Flat files do not require an external database server to be running, making the project easier to set up and run in different environments (like WSL2) without extra configuration.
4.  **Proof of Concept:** The goal of Phase 1 was to validate the user flow and the communication between Frontend and Backend. Flat files provided a sufficient "Single Source of Truth" for this purpose.

## Consequences
*   **Positive:** We achieved a functional full-stack prototype in a very short amount of time.
*   **Positive:** The logic for reading/writing files is encapsulated in a `utils.py` module, which will make the future transition to an ORM or SQL database more manageable.
*   **Negative:** Flat files do not support ACID properties (Atomicity, Consistency, Isolation, Durability) or concurrent writes, which makes them unsuitable for a production financial application.
*   **Negative:** Searching and filtering data (e.g., getting a specific user's history) is less efficient than using SQL indexes as the data grows.
*   **Neutral:** This persistence layer is temporary and is scheduled to be replaced by **PostgreSQL** in Phase 2 of the Roadmap.

---
*Date: January 27, 2026* | *Author: Aníbal Rojo*
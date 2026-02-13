# ADR-03: Use PostgreSQL for Persistent Storage

## Status
Accepted

## Context
During Phase 1 and the beginning of Phase 2, flat files (CSV and JSON) were used for data persistence. This approach was ideal for rapid prototyping (as documented in ADR-02) because it required zero infrastructure setup.

However, while moving towards a production-ready fintech application, flat files present significant limitations:
1. **Lack of Atomicity**: While we implemented manual rollbacks in the Service Layer, true ACID transactions should be handled at the database level.
2. **Concurrency Issues**: Flat files are not designed for simultaneous read/write operations from multiple users.
3. **Data Integrity**: Enforcing relationships (e.g., a transaction must belong to an existing user) is difficult and error-prone with manual file parsing.
4. **Scalability**: Querying large CSV files becomes inefficient as the number of transactions grows.

## Decision
I decided to implement **PostgreSQL** as the primary relational database management system (RDBMS). 

To maintain the clean architecture established in previous sprints, I introduced a **Repository Pattern**. This layer will abstract the SQL logic, allowing the Service Layer to remain agnostic of the underlying storage engine.

## Consequences
- **Infrastructure**: A PostgreSQL instance will be required (initially via Docker for development).
- **New Dependencies**: I will need to add a database driver (like `psycopg`) and potentially an ORM or query builder.
- **Migration Path**: I will need a strategy to securely migrate existing data from `users.json` and `transactions.csv` to the new SQL schema.
- **Improved Security**: Database-level constraints and better handling of sensitive data.
- **Performance**: Faster queries and better handling of concurrent requests.

*Date: 13 February, 2026* | *Author: Aníbal Rojo*

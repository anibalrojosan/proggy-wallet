# System Flows

This document contains the visual representation of the main business processes using Mermaid sequence diagrams.

## 1. User Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API as FastAPI
    participant DB as PostgreSQL

    User->>Frontend: Enters credentials
    Frontend->>API: POST /login
    API->>DB: Query user by username
    DB-->>API: User data (hashed password)
    API->>API: Verify password hash
    alt Success
        API-->>Frontend: JWT Token / Success
        Frontend->>User: Redirect to Dashboard
    else Failure
        API-->>Frontend: Error 401
        Frontend->>User: Show error message
    end
```

## 2. Peer-to-Peer Transfer Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API as FastAPI
    participant DB as PostgreSQL

    User->>Frontend: Selects recipient & amount
    Frontend->>API: POST /transfer
    API->>API: Validate amount > 0 (Pydantic)
    API->>DB: Check sender balance
    DB-->>API: Balance data
    alt Sufficient Funds
        API->>DB: BEGIN TRANSACTION
        API->>DB: UPDATE sender balance
        API->>DB: UPDATE recipient balance
        API->>DB: INSERT into transactions ledger
        API->>DB: COMMIT
        DB-->>API: Success
        API-->>Frontend: 200 OK
        Frontend->>User: Show success & update UI
    else Insufficient Funds
        API-->>Frontend: Error 400 (Insufficient Funds)
        Frontend->>User: Show error message
    end
```

---

*Last updated: 16 February, 2026 - Phase 2 - Sprint 16: Database Design & Setup*
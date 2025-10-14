flowchart TD
    U[User] -->|F1: HTTPS /auth| A[Auth Service]
    U -->|F2: HTTPS /features| GW[API Gateway]
    U -->|F3: HTTPS /vote| GW

    subgraph Edge[Trust Boundary: Edge]
        GW -->|F4: HTTP| SVC[Feature Service]
        A -->|F5: JWT| GW
    end

    subgraph Core[Trust Boundary: Core]
        SVC -->|F6: SQL| DB[(Postgres)]
        SVC -->|F7: Redis| CACHE[(Redis)]
    end

    style GW stroke:#ff0000,stroke-width:2px
    style A stroke:#ff0000,stroke-width:2px

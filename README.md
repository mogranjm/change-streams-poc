# Proof of Concept: Cloud Spanner Change Streams

### Purpose: Realtime Data Replication between Cloud Spanner & BigQuery

|              | Cloud Spanner             | BigQuery                     | 
|--------------|---------------------------|------------------------------|
| Processing   | OLTP (Read/Write)         | OLAP (Read)                  |
| Purpose      | Transactions (Operations) | Data Warehousing (Analytics) |
| Availability | Multi-regional            | Single Region                |

## Architecture
### Spanner Change Streams Basics
```mermaid
flowchart LR
    DML{DML Changes} --> API[SpannerIO] & HTTP[REST/RPC] --> SDB[(Spanner Database)]
    subgraph Spanner Instance 
        SDB -.- ChangeStream
        subgraph ChangeStream
            direction TB
            CR[[ChangeRecord]] --o CR2[[ChangeRecord]] --o CR3[[ChangeRecord]]
        end
    end
```

---

### Change Stream to BigQuery "Out of the Box" DataFlow Template
```mermaid
flowchart LR
    CRJ[[Cloud Run Jobs]] -- Do DML changes --> CS[(Cloud Spanner)] --> ChS[[ChangeStream]] 
    CS <-- realtime replication of DML changes --> BQ
    ChS --> DCR
    
    subgraph DataFlow
        DCR[[Data Change Record]] --> FailSafe
        DLQ[Dead Letter Queue]
    subgraph FailSafe
        ModJS[Model JSON]
    end
    DLQ --> Merge --> TDR[JSON to TableRow]
    end
    
    ModJS --> Merge{Merge}
    
    
    TDR[JSON to TableRow] --> BQ[(BigQuery)]
```
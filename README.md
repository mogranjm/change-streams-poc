# Proof of Concept: Cloud Spanner Change Streams

## Purpose: Realtime Data Replication between Cloud Spanner & BigQuery

#### Spanner vs BigQuery

|              | Cloud Spanner             | BigQuery                     | 
|--------------|---------------------------|------------------------------|
| Processing   | OLTP (Read/Write)         | OLAP (Read)                  |
| Purpose      | Transactions (Operations) | Data Warehousing (Analytics) |
| Availability | Multi-regional            | Single Region                |

##### Cloud Spanner

An RDBMS, designed for transactional workloads (insert, update) that require high reliability, and availability on a massive (unlimited) scale. 

Spanner is perfect for e-commerce (AusPost parcel tracking), banking, etc. But exhibits (very, very) poor performance for analytical workloads (don't even try to `GROUP BY`).

##### BigQuery

A columnar formatted (non-relational) Data Warehousing solution.

BQ is an absolute no-brainer for any kind of BI/Analytics application, but is terrible for transactional workloads. It does not handle `UPDATE` queries very well (columnar structure requires each column of a record to be retrieved individually).

#### Desired Outcome - ETL for CDC
```mermaid
flowchart LR
    S[(Spanner)] -.- &#x1F440 -.- CS[ChangeStream] -- &#x1f3c9 ETL --> BQ[(BigQuery)]
    S <-- Realtime Replication --> BQ
```

---

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

## Architecture

### "Out of the Box" Solution: Dataflow

GCP Provides a readymade Dataflow Template
```mermaid
flowchart LR
    DML{DML changes} --> CS[(Cloud Spanner)] -.- ChS[[ChangeStream]] 
    CS -- Realtime Replication --> BQ
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

### Proposed Alternative
```mermaid
flowchart LR
    S -- Realtime Replication --> BQ
    DML{Data Factory} --> S[(Spanner)] -.- CS[ChangeStreams] 
    CS o--o W[Watcher]
    W --> PS{PubSub} -- Push Sub --> CR[Cloud Run] -- BQ write API --> BQ[(BigQuery)]
```


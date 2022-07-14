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

```mermaid
flowchart LR
    CRJ[[Cloud Run Jobs]] -- Do DML changes --> CS[(Cloud Spanner)] -- ChangeStreams --> PS{PubSub} -- Push Sub --> CR[Cloud Run] -- BQ write API --> BQ[(BigQuery)]
    CS <-- realtime replication of DML changes --> BQ
```
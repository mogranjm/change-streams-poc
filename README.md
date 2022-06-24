# change-streams-poc


# Architecture

```mermaid
flowchart LR
    CRJ[[Cloud Run Jobs]] -- Do DML changes --> CS[(Cloud Spanner)] -- ChangeStreams --> PS{PubSub} -- Push Sub --> CR[Cloud Run] -- BQ write API --> BQ[(BigQuery)]
    CS <-- realtime replication of DML changes --> BQ
```
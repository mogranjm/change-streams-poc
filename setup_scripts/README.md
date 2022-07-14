# gcloud Scripts to set up testing environment

# Spanner 

### Start Instance

Cloud Spanner requires a compute instance to provide and manage resources for the database service(s)
```shell
gcloud spanner instances create changestream-test-instance  \
  --config="regional-us-central1" \
  --description="Test Instance" \
  --nodes=1
```

### Create Database
Create Spanner database, provide DDL script to create table(s) & changestream

```shell
gcloud spanner databases create changestream-to-bq \
  --instance changestream-test-instance \             # Specify parent instance
  --database-dialect GOOGLE_STANDARD_SQL \            # PostgreSQL option does not support ChangeStreams
  --ddl-file spanner_setup.ddl                        # Create Customers table, Create ChangeStream
```

```
# spanner_setup.ddl

CREATE TABLE Customers (
    CustomerID INT64 NOT NULL,
    fname STRING(1024),
    lname STRING(1024),
    email STRING(1024),
    created DATE DEFAULT (CURRENT_DATE()),
    subscribed BOOL
) PRIMARY KEY (CustomerID);

CREATE CHANGE STREAM test_stream
    FOR Customers
```

# IAM
Generate Service account with relevant privileges to interact with relevant resources (For use with Spanner, PubSub, BigQuery)

### Get GCP Project ID from gcloud config
```shell
PROJECT_ID=$(gcloud config list --format='value(core.project)')
```

### Create service account
```shell
gcloud iam service-accounts create change-stream-service \
    --display-name="ChangeStream Service" \
    --description="Service account for ChangeStream POC"
```

### Bind service account to Spanner Instance
```shell
gcloud spanner instances add-iam-policy-binding changestream-test-instance \
    --member="serviceAccount:change-stream-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role='roles/spanner.databaseUser'
```

# Generate authentication credentials for service account
```shell
gcloud iam service-accounts keys create "change_stream_service_key.json" \
    --iam-account="change-stream-service@$PROJECT_ID.iam.gserviceaccount.com"
```

# Spanner-to-BQ Dataflow template
```shell
gcloud dataflow flex-template run cloudstream-spanner-to-bq \
  --template-file-gcs-location gs://dataflow-templates-us-central1/latest/flex/Spanner_Change_Streams_to_BigQuery \
  --region us-central1 \    # Same region as Spanner Instance
  --parameters \            # Flow requires information about the data the changestream is watching and the location of the CDC metadata
    spannerInstanceId=changestream-test-instance, \
    spannerDatabase=changestream-to-bq, \
    spannerMetadataInstanceId=changestream-test-instance, \
    spannerMetadataDatabase=changestream-to-bq, \
    spannerChangeStreamName=test_stream, \
    bigQueryDataset=bq_changestream_test
```

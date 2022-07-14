#!/bin/zsh

gcloud config configurations activate alt

PROJECT_ID=$(gcloud config list --format='value(core.project)')

# Cloud Spanner requires a compute instance to provide and manage resources for the database service(s)
gcloud spanner instances create changestream-test-instance \
    --config="regional-us-central1" \
    --description="Test Instance" \
    --nodes=1

# Create Spanner database, provide DDL script to create tables
    # Specify parent instance
    # PostgreSQL option does not support ChangeStreams
    # Create Customers table, Create ChangeStream
gcloud spanner databases create changestream-to-bq \
    --instance=changestream-test-instance \
    --database-dialect=GOOGLE_STANDARD_SQL \
    --ddl-file=spanner_setup.ddl

gcloud spanner instances add-iam-policy-binding changestream-test-instance \
    --member="serviceAccount:change-stream-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role='roles/spanner.databaseUser'

gcloud scheduler jobs resume spanner-insert-random-user-trigger

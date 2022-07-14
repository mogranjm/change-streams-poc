#!/bin/zsh

# gcloud spanner backups create base \
#   --instance=changestream-test-instance
#   --database=changestream-to-bq
#   --retention-period=1w

gcloud spanner instances delete --quiet changestream-test-instance && \

gcloud scheduler jobs pause spanner-read-changestream-trigger \
    --location=us-central1

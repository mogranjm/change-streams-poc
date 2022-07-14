#!/bin/zsh
PROJECT_ID=$(gcloud config list --format='value(core.project)')

gcloud iam service-accounts create change-stream-service \
    --display-name="ChangeStream Service" \
    --description="Service account for ChangeStream POC"

gcloud iam service-accounts keys create "change_stream_service_key.json" \
    --iam-account="change-stream-service@$PROJECT_ID.iam.gserviceaccount.com"

#!/bin/zsh

gcloud functions deploy read-changestream \
    --region=us-central1 \
    --runtime=python39 \
    --trigger-topic=spanner-query-changestream \
    --source=https://source.developers.google.com/projects/$PROJECT_ID/repos/github_mogranjm_change-streams-poc/moveable-aliases/main/paths/ \
    --entry-point=read_changestream \
    --service-account=change-stream-service@$PROJECT_ID.iam.gserviceaccount.com \
    --set-env-vars=SPANNER_INSTANCE=changestream-test-instance,SPANNER_DATABASE=changestream-to-bq

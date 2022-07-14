#!/bin/zsh

gcloud scheduler jobs create pubsub spanner-insert-random-user-trigger \
    --location=us-central1 \
    --topic=spanner-insert-random-user \
    --schedule='* * * * *' \
    --message-body='new-user'

gcloud pubsub topics create spanner-insert-random-user

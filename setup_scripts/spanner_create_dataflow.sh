#!/bin/zsh

# Run Spanner-to-BQ Dataflow template
#   Same region as Spanner Instance
#   Flow requires information about:
#       Data the changestream is watching.
#       Location of the CDC metadata
gcloud dataflow flex-template run cloudstream-spanner-to-bq \
    --template-file-gcs-location gs://dataflow-templates-us-central1/latest/flex/Spanner_Change_Streams_to_BigQuery \
    --region us-central1 \
    --parameters \
        spannerInstanceId=changestream-test-instance,spannerDatabase=changestream-to-bq,spannerMetadataInstanceId=changestream-test-instance,spannerMetadataDatabase=changestream-to-bq,spannerChangeStreamName=test_stream,bigQueryDataset=bq_changestream_test

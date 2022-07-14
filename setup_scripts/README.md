# gcloud Scripts to set up testing environment

# Spanner 
### Start Spanner Instance, Create Database

Cloud Spanner requires a compute instance to provide and manage resources for the database service(s)
```shell
gcloud spanner instances create changestream-test-instance  \
  --config="regional-us-central1" \
  --description="Test Instance" \
  --nodes=1
```

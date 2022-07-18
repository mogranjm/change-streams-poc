terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.28.0"
    }
  }
}

provider "google" {
  credentials = file(var.PATH_TO_CREDENTIALS)

  project = var.GOOGLE_PROJECT_ID
  region  = var.REGION
  zone    = "us-central1-c"

}

resource "google_spanner_instance" "spanner_instance" {
  name         = "changestreams-test-instance"
  config       = "regional-us-central1"
  display_name = "Test Spanner Instance"
  num_nodes    = 1
}

resource "google_spanner_database" "database" {
  instance = google_spanner_instance.spanner_instance.name
  name     = "changestream-to-bq"
  ddl = [
    <<EOF
      CREATE TABLE Customers (
        CustomerID INT64 NOT NULL,
        fname STRING(1024),
        lname STRING(1024),
        username STRING(1024),
        phone STRING(1024),
        email STRING(1024),
        addr_street STRING(1024),
        addr_city STRING(1024),
        addr_state STRING(1024),
        addr_country STRING(1024),
        addr_pc STRING(1024),
        registered DATE DEFAULT (CURRENT_DATE()),
        subscribed BOOL
        ) PRIMARY KEY (CustomerID);,
    "CREATE CHANGE STREAM test_stream FOR Customers"
    EOF
  ]
  #  file("setup_scripts/spanner_setup.ddl")
  deletion_protection = false
}

resource "google_service_account" "change_stream_service" {
  account_id   = "change-stream-service"
  display_name = "ChangeStream Service"
  description  = "Service account for ChangeStream POC"
}

resource "google_spanner_instance_iam_binding" "database_user" {
  instance = google_spanner_instance.spanner_instance.name
  role     = "roles/databaseUser"
  members = [
    "serviceAccount:change-stream-service@${var.GOOGLE_PROJECT_ID}.iam.gserviceaccount.com"
  ]
}

resource "google_pubsub_topic" "trigger_changestream_query" {
  name = "spanner-query-changestream"
}

resource "google_cloudfunctions_function" "trigger_read_change_stream" {
  name        = "read-change-stream"
  description = "Query a Cloud Spanner Change Stream and pass CDC data to PubSub"
  region      = var.REGION

  service_account_email = "${google_service_account.change_stream_service.name}@${var.GOOGLE_PROJECT_ID}.iam.gserviceaccount.com"
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.trigger_changestream_query.name
  }

  runtime     = "python39"
  entry_point = "read_changestream"

  source_repository {
    url = "https://source.developers.google.com/projects/${var.GOOGLE_PROJECT_ID}/repos/github_mogranjm_change-streams-poc/moveable-alias/main/paths"
  }

  environment_variables = {
    SPANNER_INSTANCE = google_spanner_instance.spanner_instance.name
    SPANNER_DATABASE = google_spanner_database.database.name
  }

}
# TODO resource "google_pubsub_topic" ""
# TODO resource "google_pubsub_subscription" ""
# TODO resource "google_pubsub_schema" ""

variable "GOOGLE_PROJECT_ID" {
  type    = string
  default = ""
}

variable "PATH_TO_CREDENTIALS" {
  type    = string
  default = ""
}

variable "REGION" {
  type    = string
  default = "us-central1"
}

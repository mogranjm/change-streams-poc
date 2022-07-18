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
  region  = "us-central1"
  zone    = "us-central1-c"

}


resource "google_service_account" "change_stream_service" {
  account_id   = change-stream-service
  display_name = "ChangeStream Service"
}

resource "google_spanner_instance" "spanner_instance" {
  config       = "regional-us-central1"
  display_name = "Test Spanner Instance"
  num_nodes    = 1
}

resource "google_spanner_database" "database" {
  instance     = google_spanner_instance.spanner_instance.name
  name         = "changestream-to-bq"
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

variable "GOOGLE_PROJECT_ID" {
  type    = string
  default = ""
}

variable "PATH_TO_CREDENTIALS" {
  type    = string
  default = ""
}

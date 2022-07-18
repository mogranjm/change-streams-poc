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

resource "google_spanner_instance" "spanner_instance" {
  config       = "regional-us-central1"
  display_name = "Test Spanner Instance"
  num_nodes    = 1
}

resource "google_spanner_database" "database" {
  instance            = google_spanner_instance.changestream-test-instance
  display_name        = "Test Spanner Database"
  name                = "changestream-to-bq"
  ddl                 = file("setup_scripts/spanner_setup.ddl")
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

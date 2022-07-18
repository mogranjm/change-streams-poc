terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.28.0"
    }
  }
}

provider "google" {
  credentials = file("${var.PATH_TO_CREDENTIALS}")

  project = var.GOOGLE_PROJECT_ID
  region  = "us-central1"
  zone    = "us-central1-c"

}

variable "GOOGLE_PROJECT_ID" {
  type    = string
  default = ""
}

variable "PATH_TO_CREDENTIALS" {
  type = string
  default = ""
}

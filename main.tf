terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.28.0"
    }
  }
}

provider "google" {
  credentials = file("/Users/jamesmorgan/Documents/gcp/servian-u-practice-79b61e33b0ae.json")

  project = "servian-u-practice"
  region  = "us-central1"
  zone    = "us-central1-c"

}

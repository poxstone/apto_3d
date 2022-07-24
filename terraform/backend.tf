terraform {
  backend "gcs" {
    bucket  = "scientific-crow-353414-tfback"
    prefix  = "terraform/state"
  }
}
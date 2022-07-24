provider "google" {
  project     = var.GOOGLE_CLOUD_PROJECT
  region      = var.REGION
  zone        = var.ZONE
  #credentials = var.GOOGLE_APPLICATION_CREDENTIALS
}

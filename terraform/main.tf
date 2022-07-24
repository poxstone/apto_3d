resource "google_project_service" "project_services" {
  for_each =  toset([
    "compute.googleapis.com",
    "artifactregistry.googleapis.com",
    "ml.googleapis.com",
    "storage-component.googleapis.com",
    "containerregistry.googleapis.com",
    "cloudbuild.googleapis.com",
  ])
  service = each.key
  timeouts {
    create = "30m"
    update = "40m"
  }
  disable_dependent_services = true
}

resource "google_storage_bucket" "bucket_3dmodels" {
  name          = "${provider.google.project}-3dmodels"
  location      = provider.google.region
  force_destroy = true
  uniform_bucket_level_access = true
  depends_on = [google_project_service.project_services]
}

resource "google_storage_bucket" "bucket_3dmodels" {
  name          = "${provider.google.project}-tfback"
  location      = provider.google.region
  force_destroy = true
  uniform_bucket_level_access = true
  depends_on = [google_project_service.project_services]
}

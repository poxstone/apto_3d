resource "google_project_service" "project_services" {
  for_each =  toset([
    "compute.googleapis.com",
    "artifactregistry.googleapis.com",
    "ml.googleapis.com",
    "storage-component.googleapis.com",
    "containerregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "iam.googleapis.com",
  ])
  service = each.key
  timeouts {
    create = "30m"
    update = "40m"
  }
  disable_dependent_services = true
}

resource "google_storage_bucket" "bucket_3dmodels" {
  name          = "${var.GOOGLE_CLOUD_PROJECT}-3dmodels"
  location      = var.REGION
  force_destroy = true
  uniform_bucket_level_access = true
  depends_on = [google_project_service.project_services]
}

resource "google_storage_bucket" "bucket_tfback" {
  name          = "${var.GOOGLE_CLOUD_PROJECT}-tfback"
  location      = var.REGION
  force_destroy = true
  uniform_bucket_level_access = true
  depends_on = [google_project_service.project_services]
}

resource "google_service_account" "service_account_3dmodels" {
  account_id   = "sa-3dmodels"
  display_name = "sa-3dmodels"
  depends_on = [google_project_service.project_services]
}

resource "null_resource" "service_account_key_json_download_1" {
  provisioner "local-exec" {
    command = "gcloud iam service-accounts keys create 'service-key.json' --iam-account='${google_service_account.service_account_3dmodels.email}' --project='${var.GOOGLE_CLOUD_PROJECT}';mv service-key.json ../"
  }
  depends_on = [google_service_account.service_account_3dmodels]
}

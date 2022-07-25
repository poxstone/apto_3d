# Render in Container AI Platform

> **note:** get to "https://github.com/poxstone/blender-boycup" for more details
> **note** Create and download "./service-key.json" from GCP

***files***
- **3D**: main.blend, referencias, render, 3d_models/*,
- **Container**:  Dockerfile, Dockerfile_master_blender, README.md, blender_init.py, entrypoint.sh, variables.sh

## Variables
```bash
source varibles.sh;
```

## Terraform (0.13)
```bash
source ./main.sh "export_variables";
cd ./terraform;
terraform init;
terraform plan;
terraform apply;
```

## Build

- Render frame:
- Build master blender images
```bash
docker build -t "${CONTAINER_IMAGE_MASTER}" -f "Dockerfile_master_blender" ".";
```
- Build from master
```bash
docker build -t "${CONTAINER_IMAGE_NAME}" --build-arg "MASTER_IMAGE=${CONTAINER_IMAGE_MASTER}" --build-arg "BUCKET_EXPORT=${BUCKET_EXPORT}" -f Dockerfile ".";
```


## Local test

- Local run
```bash
docker run -it --rm --gpus all "${CONTAINER_IMAGE_NAME}";
# customize local arguments
LOCAL_JOB="{\"args\":[${CLOUD_ML_JOB}]}";
docker run -it --rm --name "3dmodel" -v "$(pwd)/:/3dmodel" -e "MODEL3D_FILE=main.blend" -e "LOCAL_JOB=${LOCAL_JOB}" "${CONTAINER_IMAGE_NAME}";
```


## GCP

- Copy blender model to Cloud Storage
```bash
gsutil -m cp -r "./*" "${BUCKET_MODEL_SAVED}";
gsutil rm "${BUCKET_MODEL_SAVED}*.json";
```

- upload containers
```bash
gcloud auth configure-docker;
docker push "${CONTAINER_IMAGE_MASTER}";
docker push "${CONTAINER_IMAGE_NAME}";
```

- Render K8 X 1 (38 min 32 sec)
```bash
gcloud ai-platform jobs submit training "${JOB_NAME}day" --project "${GOOGLE_CLOUD_PROJECT}" \
--region "${REGION}" \
--master-image-uri "${CONTAINER_IMAGE_NAME}" \
--scale-tier "${SCALE_TIER}" \
--stream-logs \
-- \
"${CLOUD_ML_JOB}"
```

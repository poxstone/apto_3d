# Render in Container AI Platform

> **note:** get to "https://github.com/poxstone/blender-boycup" for more details

***files***
- **3D**: main.blend, referencias, render, 3d_models/*,
- **Container**:  Dockerfile, Dockerfile_master_blender, README.md, blender_init.py, entrypoint.sh, variables.sh

## Variables
```bash
source varibles.sh;
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
# customize files
docker run -it --rm --name "3dmodel" -v "$(pwd)/3dmodel:/3dmodel" -e "MODEL3D_FILE=main.blend" -v "$(pwd)/entrypoint.sh:/3dmodel/entrypoint.sh"  "${CONTAINER_IMAGE_NAME}";
```

- Run multiple render and simulate GCP AI platform parameters
```bash
docker run -it --rm --name "3dmodel" --gpus all -e "CLOUD_ML_JOB=${CLOUD_ML_JOB}" "${CONTAINER_IMAGE_NAME}";

# customize local arguments
LOCAL_JOB='{"args":[{ "renders":[ { "blender_params":"--python ./blender_init.py --background ./main.blend --render-output ./render/image_ --render-format PNG --use-extension 1 --engine CYCLES --threads 8 --frame-start 1 --frame-end 1 --render-anim"}] }]}';
docker run -it --rm --name "3dmodel" -v "/home/poxstone/3DObjects/apto/:/3dmodel" -v "$(pwd)/entrypoint.sh:/3dmodel/entrypoint.sh" -e "MODEL3D_FILE=main.blend" -e "LOCAL_JOB=${LOCAL_JOB}" "${CONTAINER_IMAGE_NAME}";
```


## GCP

- Copy blender model to Cloud Storage
```bash
gsutil -m cp -r "./*" "${BUCKET_MODEL_SAVED}";
```

- upload containers
```bash
gcloud auth configure-docker;
docker push "${CONTAINER_IMAGE_MASTER}";
docker push "${CONTAINER_IMAGE_NAME}";
```

- Render K8 X 1 (38 min 32 sec)
```bash
gcloud ai-platform jobs submit training "${JOB_NAME}" --project "${GOOGLE_CLOUD_PROJECT}" \
--region "${REGION}" \
--master-image-uri "${CONTAINER_IMAGE_NAME}" \
--scale-tier "${SCALE_TIER}" \
--stream-logs \
-- \
"${CLOUD_ML_JOB}"
```

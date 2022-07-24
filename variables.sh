export GOOGLE_CLOUD_PROJECT="scientific-crow-353414";
export BUCKET_EXPORT="gs://${GOOGLE_CLOUD_PROJECT}-3dmodels";
export BUCKET_MODEL_SAVED="${BUCKET_EXPORT}/3dmodel/";

export CONTAINER_IMAGE_MASTER="gcr.io/${GOOGLE_CLOUD_PROJECT}/blender-master:v2.9.3";
export CONTAINER_IMAGE_NAME="gcr.io/${GOOGLE_CLOUD_PROJECT}/model3d-gpu:1.0";
export REGION="us-east1";
export SCALE_TIER="basic-gpu";  # standard_p100 o n1-standard-8-p100x1
export JOB_NAME="render$(date '+%Y%m%d%H%M')";
# Videom (saved to vdeos previously)
export CLOUD_ML_JOB='{ "renders":[ { "bucket_model":"'${BUCKET_MODEL_SAVED}'", "blender_params":"--python ./blender_init.py -b ./main.blend -o ./render/render_ -x 1 -E CYCLES -t 8 -s 0 -e 520 -j 1 -a"}] }'
# Images export -  engines: BLENDER_EEVEE BLENDER_WORKBENCH CYCLES
export CLOUD_ML_JOB='{ "renders":[ { "bucket_model":"'${BUCKET_MODEL_SAVED}'", "blender_params":"--python ./blender_init.py -b ./main.blend -o ./render/render_ -F PNG -x 1 -E CYCLES -t 8 -s 0 -e 520 -j 40 -a"}] }'

# second project
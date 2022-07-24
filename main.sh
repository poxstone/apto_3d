#!/bin/bash
# source ../resources/scripts/main.sh "export_variables" prd

echo "SCRIPT_STEEP: "${0}" "${1}" ${@}";

export RESOURCES_PATH="./";
export VARIABLES_PATH="${RESOURCES_PATH}/variables.sh";
export MAIN_PATH="${RESOURCES_PATH}/main.sh";

if [[ "${1}" == "export_variables" ]];then
  # export for scripts
  source "${VARIABLES_PATH}";
  # export for terraform
  count=0;
  for i in $(cat $VARIABLES_PATH);do
    count=$(( $count + 1 ));
    #eval `echo LINE:${count}`;
    eval `echo export "${i}"`;
    eval `echo export "TF_VAR_${i}"`;
  done;
fi;

if [[ "${1}" == "update_terraform" ]];then
  # load variables
  export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/../credentials.json";
  terraform init;
  terraform plan;
  terraform apply -auto-approve;
fi;

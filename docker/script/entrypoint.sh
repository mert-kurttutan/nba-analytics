#!/usr/bin/env bash

# set_conda_env

function set_python_env(){

  echo "Started setting conda python environment"
  source ${HOME}/miniconda3/etc/profile.d/conda.sh
  conda activate speech-to-text
  echo "Finished setting conda environment!"

}

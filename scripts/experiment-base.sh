#!/bin/sh
#SBATCH -N 1	  # nodes requested
#SBATCH -n 1	  # tasks requested
#SBATCH --partition=Short
#SBATCH --gres=gpu:4
#SBATCH --mem=12000  # memory in Mb
#SBATCH --time=0-03:59:00

export CUDA_HOME=/opt/cuda-9.0.176.1/

export CUDNN_HOME=/opt/cuDNN-7.0/

export STUDENT_ID=$(whoami)

export LD_LIBRARY_PATH=${CUDNN_HOME}/lib64:${CUDA_HOME}/lib64:$LD_LIBRARY_PATH

export LIBRARY_PATH=${CUDNN_HOME}/lib64:$LIBRARY_PATH

export CPATH=${CUDNN_HOME}/include:$CPATH

export PATH=${CUDA_HOME}/bin:${PATH}

export PYTHON_PATH=$PATH

mkdir -p /disk/scratch/${STUDENT_ID}


export TMPDIR=/disk/scratch/${STUDENT_ID}/
export TMP=/disk/scratch/${STUDENT_ID}/

mkdir -p ${TMP}/data/
rsync -ua /home/${STUDENT_ID}/image-colorization/data/ ${TMP}/data/
export DATASET_DIR=${TMP}/data/

# Activate the relevant virtual environment:
source /home/${STUDENT_ID}/miniconda3/bin/activate mlp
python /home/${STUDENT_ID}/image-colorization/train.py --experiment-name=experiment_001 --model-name=unet32 --dataset-name=cifar10 --train-batch-size=100 --val-batch-size=1000 --batch-output-frequency=10 --max-images=10

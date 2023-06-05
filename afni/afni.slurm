srun --account fmri --partition=g40 --gpus=1 --time=01:00:00 --comment fmri-foundation \
    --container-image=afni/afni_make_build --container-mounts=/fsx/proj-medarc/fmri/dingliyu:/home/afni_user/fmri \
    --pty /bin/bash -i




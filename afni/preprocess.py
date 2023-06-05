import os

# walk through the openneuro directory and find all files end with _bold.nii.gz
for root, dirs, files in sorted(os.walk('../openneuro')):
    for name in files:
        if '_bold.nii.gz' in name:
            # run command 'run.sh filename'
            if os.path.exists(os.path.join(root, name[:-len('.nii.gz')] + '_aligned.nii.gz')):
                print('File ' + os.path.join(root, name[:-len('.nii.gz')] + '_aligned.nii.gz') + ' already exists.')
            else:
                os.system('bash run.sh ' + os.path.join(root, name[:-len('.nii.gz')]))  
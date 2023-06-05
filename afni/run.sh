func=$1
suffix='_aligned'

echo "Aligning $func"

align_epi_anat.py -anat tpl-MNI152NLin2009cAsym_res-03_T1w_brain.nii.gz -epi $func".nii.gz" -epi_base 0 -epi2anat -rigid_body -ginormous_move -anat_has_skull no -epi_strip None -suffix $suffix -volreg on -tshift off -save_resample -master_epi 3.00

base=$(basename "$func")

# transform AFNI outputs to nifti file
3dAFNItoNIFTI -prefix $func$suffix".nii.gz" $base$suffix"+tlrc"

# remove unnecessary AFNI outputs
rm *+tlrc.* 
rm *vr_motion* 
rm *mat.aff*

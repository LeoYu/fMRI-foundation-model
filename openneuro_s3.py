import os
import sys
import numpy as np
import boto3
import webdataset as wds
import nibabel as nib
import pickle as pkl

NUM_DATASETS = 2

# Connect to S3
s3 = boto3.client('s3')

# Set the bucket name and folder name
bucket_name = 'openneuro.org'

# List all folders in the parent directory
response = s3.list_objects_v2(Bucket=bucket_name, Prefix='', Delimiter='/')

# Extract the folder names from the response
folder_names = [x['Prefix'].split('/')[-2] for x in response.get('CommonPrefixes', [])]
print(folder_names)

for folder_name in folder_names[:NUM_DATASETS]:
    # List all objects in the folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

    # Process each object in the folder
    webdataset_items = []
    for obj in response.get('Contents', []):
        obj_key = obj['Key']

        if '_T1w.nii.gz' in obj_key or '_bold.nii.gz' in obj_key:
            print(folder_name, obj['Key'])
        if '_T1w.nii.gz' in obj_key: # Anatomical
            # Store subject number to verify anat/func match
            anat_subj = obj_key.split('/')[1]
            
            # Download the object to tmp location
            filename = os.path.join('openneuro', obj_key)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            s3.download_file(bucket_name, obj_key, filename)

            # store the head of anat_subj
            anat_header = nib.load(filename).header
            
        elif '_bold.nii.gz' in obj_key: # Functional bold
            # Verify func/anat subject number match
            func_subj = obj_key.split('/')[1]
            if anat_subj != func_subj:
                raise ValueError('Incompatible subject number found.')

            # Get the object key and download the object to tmp location
            filename = os.path.join('openneuro', obj_key)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            s3.download_file(bucket_name, obj_key, filename)

            anat_header_name = filename[:-len('.nii.gz')] + '_header'
            pkl.dump(anat_header, open(anat_header_name, 'wb'))

            

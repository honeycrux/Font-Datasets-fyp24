# Make casia-dataset-source directory
mkdir fyp23-dataset-source
chmod 777 fyp23-dataset-source

# Make casia-dataset directory
mkdir fyp23-dataset
chmod 777 fyp23-dataset

# Download the dataset
# Coming soon

# Create content and target images
python -m scripts.fyp23.step_0_create_content_and_target_images

# Make casia-dataset-source directory
mkdir fyp23-dataset-source
chmod 777 fyp23-dataset-source

# Make casia-dataset directory
mkdir fyp23-dataset
chmod 777 fyp23-dataset

# Download the dataset
wget "https://github.com/honeycrux/Font-Datasets-fyp24/raw/refs/heads/main/releases/fyp23-dataset-source.zip?download=" -O fyp23-dataset-source/fyp23-dataset.zip
unzip -qq fyp23-dataset-source/fyp23-dataset.zip -d fyp23-dataset-source
rm -f fyp23-dataset-source/fyp23-dataset.zip
chmod -R 777 fyp23-dataset-source

# Create content and target images
python -m scripts.fyp23.step_0_create_content_and_target_images

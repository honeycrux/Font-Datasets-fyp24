# Make neumason-dataset-source directory
mkdir neumason-dataset-source
chmod 777 neumason-dataset-source

# Make neumason-dataset directory
mkdir neumason-dataset
chmod 777 neumason-dataset

# Download the dataset
git clone https://github.com/neumason/Chinese-Fonts-Dataset neumason-dataset-source
chmod -R 777 neumason-dataset-source

# Create the neumason dataset structure
python -m scripts.neumason.step_0_create_content_and_target_images

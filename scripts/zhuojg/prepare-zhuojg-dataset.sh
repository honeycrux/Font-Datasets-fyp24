# Make zhuojg-dataset-source directory
mkdir zhuojg-dataset-source
chmod 777 zhuojg-dataset-source

# Make zhuojg-dataset directory
mkdir zhuojg-dataset
chmod -R 777 zhuojg-dataset

# Download the dataset
# (The following URL should be the second dataset on the README of https://github.com/zhuojg/chinese-calligraphy-dataset)
wget "https://drive.usercontent.google.com/download?id=10QJrw0Qdk4O1bIrehCLmdiCkwpLbGVe8&export=download&confirm=t" -O zhuojg-dataset-source/zhuojg-dataset.zip
unzip -qq zhuojg-dataset-source/zhuojg-dataset.zip -d zhuojg-dataset-source
rm -f zhuojg-dataset-source/zhuojg-dataset.zip
rm -rf zhuojg-dataset-source/__MACOSX
chmod -R 777 zhuojg-dataset-source

# Create target images
python -m scripts.zhuojg.step_0_create_target_images

# Create content images
python -m scripts.zhuojg.step_1_create_content_images_from_target_images

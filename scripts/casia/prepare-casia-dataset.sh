# Make casia-dataset-source directory
mkdir casia-dataset-source
chmod 777 casia-dataset-source

# Make casia-dataset directory
mkdir casia-dataset
chmod 777 casia-dataset

# Download the dataset
# (Download links are from https://nlpr.ia.ac.cn/databases/handwriting/Download.html)
wget https://nlpr.ia.ac.cn/databases/Download/Offline/CharData/Gnt1.0TrainPart1.zip -O casia-dataset-source/Gnt1.0TrainPart1.zip
unzip -qq casia-dataset-source/Gnt1.0TrainPart1.zip -d casia-dataset-source
rm -f casia-dataset-source/Gnt1.0TrainPart1.zip
wget https://nlpr.ia.ac.cn/databases/Download/Offline/CharData/Gnt1.0TrainPart2.zip -O casia-dataset-source/Gnt1.0TrainPart2.zip
unzip -qq casia-dataset-source/Gnt1.0TrainPart2.zip -d casia-dataset-source
rm -f casia-dataset-source/Gnt1.0TrainPart2.zip
wget https://nlpr.ia.ac.cn/databases/Download/Offline/CharData/Gnt1.0TrainPart3.zip -O casia-dataset-source/Gnt1.0TrainPart3.zip
unzip -qq casia-dataset-source/Gnt1.0TrainPart3.zip -d casia-dataset-source
rm -f casia-dataset-source/Gnt1.0TrainPart3.zip
chmod -R 777 casia-dataset-source

# Create target images
python -m scripts.casia.step_0_create_target_images

# Create content images
python -m scripts.casia.step_1_create_content_images_from_target_images

# This script generates a summary report of the dataset's target images.

# Dataset format:
# xxx-dataset/
# ├── TargetImage/
# │   ├── fontA/
# │   │   ├── fontA+char1.png
# │   │   ├── fontA+char2.png
# │   ├── fontB/
# │   │   ├── fontB+char1.png
# │   │   ├── fontB+char2.png


import statistics
from pathlib import Path


def report_dataset_summary(target_image_dir):
    target_image_path = Path(target_image_dir)

    font_character_counts = []

    total_font_directories = len(list(target_image_path.iterdir()))

    for subdirectory_path in target_image_path.iterdir():
        sub_dir_file_count = len(list(subdirectory_path.iterdir()))
        font_character_counts.append(sub_dir_file_count)

    if total_font_directories == 0:
        return "No fonts found in the dataset."

    summary = (
        f"Total number of fonts: {total_font_directories}\n"
        f"Range of characters per font: {min(font_character_counts)}-{max(font_character_counts)}\n"
        f"Average number of characters per font: {sum(font_character_counts) / total_font_directories:.2f}\n"
        f"Standard deviation of characters per font: {statistics.stdev(font_character_counts):.2f}\n"
        f"Total number of characters: {sum(font_character_counts)}"
    )

    return summary


def main():
    target_image_dir = "xxx-dataset/TargetImage"
    print(report_dataset_summary(target_image_dir))


if __name__ == "__main__":
    main()

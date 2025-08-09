# This script is used to balance a dataset.
# A balanced dataset is one where each character appears in every font style.
# This script will find characters that are missing in some styles and delete them from the dataset.

# Dataset format
# xxx-dataset/
# ├── ContentImage/
# │   ├── char1.png
# │   ├── char2.png
# ├── TargetImage/
# │   ├── fontA/
# │   │   ├── fontA+char1.png
# │   │   ├── fontA+char2.png
# │   ├── fontB/
# │   │   ├── fontB+char1.png
# │   │   ├── fontB+char2.png


from collections import defaultdict
from pathlib import Path

from tqdm import tqdm


def parse_target_image_name(target_image_name: str):
    # Input Format: style+content[+optional-suffix]
    target_components = target_image_name.split("+")
    style = target_components[0]
    content = target_components[1]
    return style, content


def find_content_characters(content_image_dir: str | Path) -> set[str]:
    content_image_path = Path(content_image_dir)
    content_characters = set()

    total_files = len(list(content_image_path.iterdir()))

    for img_file in tqdm(
        content_image_path.iterdir(), total=total_files, desc="Scan content images"
    ):
        if img_file.is_file():
            img_name = img_file.stem
            content_characters.add(img_name)

    return content_characters


def find_common_target_characters(target_image_dir: str | Path) -> set[str]:
    target_image_path = Path(target_image_dir)
    character_to_fonts_mapping = defaultdict(set)

    total_fonts = len(list(target_image_path.iterdir()))

    for font_path in tqdm(
        target_image_path.iterdir(), total=total_fonts, desc="Scan target images"
    ):
        if font_path.is_dir():
            font_name = font_path.stem

            total_files = len(list(font_path.iterdir()))

            for img_file in tqdm(
                font_path.iterdir(), total=total_files, desc=f"{font_name}", leave=False
            ):
                if img_file.is_file():
                    img_name = img_file.stem
                    _, char_name = parse_target_image_name(img_name)

                    character_to_fonts_mapping[char_name].add(font_name)

    all_available_fonts = {
        font_path.stem
        for font_path in target_image_path.iterdir()
        if font_path.is_dir()
    }

    common_target_characters = {
        char_name
        for char_name, font_names in character_to_fonts_mapping.items()
        if font_names == all_available_fonts
    }

    return common_target_characters


def find_preserved_characters(
    content_image_dir: str | Path, target_image_dir: str | Path
) -> set[str]:
    content_characters = find_content_characters(content_image_dir)

    common_target_characters = find_common_target_characters(target_image_dir)

    preserved_characters = common_target_characters.intersection(content_characters)

    return preserved_characters


def delete_non_common_content_images(
    content_image_dir: str | Path, preserved_characters: set[str]
) -> set[str]:
    removed_characters = set()

    content_image_path = Path(content_image_dir)

    total_files = len(list(content_image_path.iterdir()))

    for img_file in (
        progress_bar := tqdm(
            content_image_path.iterdir(),
            total=total_files,
            desc="Scan for deletion in content images",
        )
    ):
        if img_file.is_file():
            img_name = img_file.stem

            if img_name not in preserved_characters:
                progress_bar.write(f"Deleting {img_file}")
                img_file.unlink()
                removed_characters.add(img_name)

    return removed_characters


def delete_non_common_target_images(
    target_image_dir: str | Path, preserved_characters: set[str]
) -> set[str]:
    removed_characters = set()
    target_image_path = Path(target_image_dir)

    total_fonts = len(list(target_image_path.iterdir()))

    for font_path in tqdm(
        target_image_path.iterdir(),
        total=total_fonts,
        desc="Scan for deletion in target images",
    ):
        if font_path.is_dir():

            total_files = len(list(font_path.iterdir()))

            for img_file in (
                progress_bar := tqdm(
                    font_path.iterdir(),
                    total=total_files,
                    desc=f"{font_path.stem}",
                    leave=False,
                )
            ):
                if img_file.is_file():
                    img_name = img_file.stem
                    _, char_name = parse_target_image_name(img_name)

                    if char_name not in preserved_characters:
                        progress_bar.write(f"Deleting {img_file}")
                        img_file.unlink()
                        removed_characters.add(char_name)

    return removed_characters


def balance_dataset(
    content_image_dir: str | Path,
    target_image_dir: str | Path,
):
    preserved_characters = find_preserved_characters(
        content_image_dir, target_image_dir
    )

    removed_content_characters = delete_non_common_content_images(
        content_image_dir, preserved_characters
    )

    removed_target_characters = delete_non_common_target_images(
        target_image_dir, preserved_characters
    )

    removed_characters = removed_content_characters.union(removed_target_characters)

    return preserved_characters, removed_characters


def main():
    content_image_dir = "xxx-dataset/ContentImage"
    target_image_dir = "xxx-dataset/TargetImage"

    preserved, removed = balance_dataset(
        content_image_dir,
        target_image_dir,
    )

    print(f"Removed characters: {', '.join(removed)}")


if __name__ == "__main__":
    main()

# In the scenario that content images are generated from target images, but some characters failed to generate into content images.
# This script detects and deletes target images that do not have corresponding content images.

from pathlib import Path

from tqdm import tqdm


def parse_target_image_name(target_image_name: str):
    # Input Format: style+content[+optional-suffix]
    target_components = target_image_name.split("+")
    style = target_components[0]
    content = target_components[1]
    return style, content


def find_preserved_characters(content_image_dir: str | Path) -> set[str]:
    content_image_path = Path(content_image_dir)

    preserved_characters = set()

    for image_file in content_image_path.iterdir():
        preserved_characters.add(image_file.stem)

    return preserved_characters


def delete_failed_characters(
    target_image_dir: str | Path, preserved_characters: set[str]
) -> set[str]:
    target_image_path = Path(target_image_dir)

    delete_count = 0
    removed_characters = set()

    for font_dir in target_image_path.iterdir():
        total_files = len(list(font_dir.iterdir()))
        for target_image_file in tqdm(
            font_dir.iterdir(), total=total_files, desc="Validating target images"
        ):
            if target_image_file.is_file():
                target_image_name = target_image_file.stem
                _, char_name = parse_target_image_name(target_image_name)

                if char_name not in preserved_characters:
                    print(f"Deleting {target_image_file}")
                    target_image_file.unlink()
                    delete_count += 1
                    removed_characters.add(char_name)

    return removed_characters


def delete_target_images_without_content_image(
    content_image_dir: str | Path, target_image_dir: str | Path
):
    preserved_characters = find_preserved_characters(content_image_dir)

    removed_characters = delete_failed_characters(
        target_image_dir=target_image_dir,
        preserved_characters=preserved_characters,
    )

    return preserved_characters, removed_characters


def main():
    content_image_dir = "xxx-dataset/ContentImage"
    target_image_dir = "xxx-dataset/TargetImage"

    preserved, removed = delete_target_images_without_content_image(
        content_image_dir, target_image_dir
    )

    print(f"Removed characters: {', '.join(removed)}")


if __name__ == "__main__":
    main()

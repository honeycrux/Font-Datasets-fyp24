# This script processes the fyp23 dataset

# Dataset format:
# fyp23-dataset-source/
# ├── content/
# │   ├── token1.png
# │   ├── token2.png
# ├── data/
# │   ├── fontA/
# │   │   ├── token1.png
# │   │   ├── token2.png
# │   ├── fontB/
# │   │   ├── token1.png
# │   │   ├── token2.png

# Output format:
# fyp23-dataset/
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


import shutil
from pathlib import Path

from tqdm import tqdm


def ensure_dir_exists_with_perms(path: str | Path):
    # Create a Path object
    base_path = Path(path)

    # Create the directory if it doesn't exist
    base_path.mkdir(parents=True, exist_ok=True)

    # Change permissions of the base directory itself
    base_path.chmod(0o777)

    # Traverse up the directory tree and change permissions
    for parent in base_path.parents:
        if parent != Path("."):
            parent.chmod(0o777)


def get_word_from_token(wordlist: str, token: str) -> str:
    index = int(token)
    return wordlist[index]


def copy_target_images(
    source_target_dir: str | Path, output_target_image_dir: str | Path, wordlist: str
):
    source_target_path = Path(source_target_dir)
    target_image_path = Path(output_target_image_dir)

    total_fonts = len(list(source_target_path.iterdir()))

    for source_font_path in tqdm(
        source_target_path.iterdir(), total=total_fonts, desc="Copy target images"
    ):
        font_name = source_font_path.stem

        target_font_path = target_image_path / font_name
        target_font_path.mkdir(parents=True, exist_ok=True)
        target_font_path.chmod(0o777)

        total_files = len(list(source_font_path.iterdir()))

        for source_img_file in tqdm(
            source_font_path.iterdir(),
            total=total_files,
            desc=f"{font_name}",
            leave=False,
        ):
            word = get_word_from_token(wordlist, source_img_file.stem)
            new_img_file = (
                target_font_path / f"{font_name}+{word}{source_img_file.suffix}"
            )
            shutil.copy(source_img_file, new_img_file)
            new_img_file.chmod(0o777)

    font_list = [
        source_font_path.stem for source_font_path in source_target_path.iterdir()
    ]

    return font_list


def copy_content_images(
    source_content_dir: str | Path, output_content_image_dir: str | Path, wordlist: str
):
    source_content_path = Path(source_content_dir)
    content_image_path = Path(output_content_image_dir)

    total_files = len(list(source_content_path.iterdir()))

    for source_img_file in tqdm(
        source_content_path.iterdir(), total=total_files, desc="Copy content images"
    ):
        if source_img_file.is_file():
            word = get_word_from_token(wordlist, source_img_file.stem)
            new_img_file = content_image_path / f"{word}{source_img_file.suffix}"
            shutil.copy(source_img_file, new_img_file)
            new_img_file.chmod(0o777)


def create_content_and_target_images(
    source_dir: str | Path,
    source_wordlist: str | Path,
    output_dir: str | Path,
):
    source_content_dir = Path(source_dir) / "content"
    source_target_dir = Path(source_dir) / "data"

    output_content_image_dir = Path(output_dir) / "ContentImage"
    output_target_image_dir = Path(output_dir) / "TargetImage"

    ensure_dir_exists_with_perms(output_target_image_dir)
    ensure_dir_exists_with_perms(output_content_image_dir)

    with open(source_wordlist, "r", encoding="utf-8") as f:
        wordlist = f.read().strip()

    copy_content_images(
        source_content_dir=source_content_dir,
        output_content_image_dir=output_content_image_dir,
        wordlist=wordlist,
    )

    font_list = copy_target_images(
        source_target_dir=source_target_dir,
        output_target_image_dir=output_target_image_dir,
        wordlist=wordlist,
    )

    print(f"Number of target fonts: {len(font_list)}")


def main():
    source_dir = "fyp23-dataset-source"

    source_wordlist = "fyp23-dataset-source/wordlist.txt"

    output_dir = "fyp23-dataset"

    create_content_and_target_images(
        source_dir=source_dir,
        source_wordlist=source_wordlist,
        output_dir=output_dir,
    )


if __name__ == "__main__":
    main()

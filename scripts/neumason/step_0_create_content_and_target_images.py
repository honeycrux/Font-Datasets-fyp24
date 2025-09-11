# This script processes the neumason dataset

# Dataset format:
# neumason-dataset-source/png9169/
# ├── 汉仪书宋二S.ttf  <-- one font is used for content images
# │   ├── char1.png
# │   ├── char2.png
# ├── fontA01000000100001000.ttf  <-- all other fonts are used for target images
# │   ├── char1.png
# │   ├── char2.png
# ├── fontB01000000100001000.ttf
# │   ├── char1.png
# │   ├── char2.png

# Output format:
# neumason-dataset/
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


class Font:
    font_name: str
    source_path: Path

    def __init__(self, folder_path: Path):
        self.font_name = self.process_name(folder_path.name)
        self.source_path = folder_path

    @staticmethod
    def process_name(name: str) -> str:
        def is_valid_right_side_char(c: str):
            return c not in "01"

        # Remove ".ttf" from the name
        name = name.replace(".ttf", "")

        # Remove all 0s and 1s from the right
        while not is_valid_right_side_char(name[-1]):
            name = name[:-1]

        # Remove all whitespaces
        name = "".join(filter(lambda c: not c.isspace(), name))

        return name


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


def get_font_list(
    source_dir: str | Path, content_font_dir: str, rejected_font_dirs: list[str]
):
    source_path = Path(source_dir)

    content_font = Font(source_path / content_font_dir)

    assert (
        content_font.source_path.is_dir()
    ), f"Content font file {content_font_dir} not found."

    # Get list of target fonts
    target_fonts = [
        Font(font_folder)
        for font_folder in source_path.iterdir()
        if font_folder.is_dir()
        and font_folder.name != content_font_dir
        and font_folder.name not in rejected_font_dirs
    ]

    return content_font, target_fonts


def copy_content_images(output_content_image_dir: str | Path, content_font: Font):
    content_image_path = Path(output_content_image_dir)

    total_files = len(list(content_font.source_path.iterdir()))
    for source_file in tqdm(
        content_font.source_path.iterdir(),
        total=total_files,
        desc="Copy content images",
    ):
        if source_file.is_file():
            new_file = content_image_path / source_file.name
            shutil.copy(source_file, new_file)
            new_file.chmod(0o777)


def copy_target_images(output_target_image_dir: str | Path, target_fonts: list[Font]):
    total_fonts = len(target_fonts)
    for target_font in tqdm(target_fonts, total=total_fonts, desc="Copy target images"):
        font_destination_path = Path(output_target_image_dir) / target_font.font_name

        font_destination_path.mkdir(exist_ok=True)
        font_destination_path.chmod(0o777)

        total_files = len(list(target_font.source_path.iterdir()))
        for source_file in tqdm(
            target_font.source_path.iterdir(),
            total=total_files,
            desc=f"{target_font.font_name}",
            leave=False,
        ):
            if source_file.is_file():
                char_name = source_file.stem
                new_file = (
                    font_destination_path / f"{target_font.font_name}+{char_name}.png"
                )
                shutil.copy(source_file, new_file)
                new_file.chmod(0o777)


def create_content_and_target_images(
    source_dir: str | Path,
    output_dir: str | Path,
    content_font_dir: str,
    rejected_font_dirs: list[str],
):
    output_content_image_dir = Path(output_dir) / "ContentImage"
    output_target_image_dir = Path(output_dir) / "TargetImage"

    ensure_dir_exists_with_perms(output_content_image_dir)
    ensure_dir_exists_with_perms(output_target_image_dir)

    content_font, target_fonts = get_font_list(
        source_dir=source_dir,
        content_font_dir=content_font_dir,
        rejected_font_dirs=rejected_font_dirs,
    )

    print(f"Content font: {content_font.font_name}")
    print(f"Number of target fonts: {len(target_fonts)}")

    copy_content_images(
        output_content_image_dir=output_content_image_dir, content_font=content_font
    )
    copy_target_images(
        output_target_image_dir=output_target_image_dir, target_fonts=target_fonts
    )


def main():
    source_dir = "neumason-dataset-source/png9169/"

    output_dir = "neumason-dataset/"

    # Make sure this font has all the characters you need
    content_font_dir = "汉仪书宋二S10000000000000000.ttf"

    # Remove duplicate or problematic fonts
    rejected_font_dirs = [
        "汉仪粗仿宋简01000000100001000.ttf",  # duplicate
        "汉仪新蒂棉花糖黑板报00001010000000000.ttf",  # has 1 char more than any other font
    ]

    create_content_and_target_images(
        source_dir=source_dir,
        output_dir=output_dir,
        content_font_dir=content_font_dir,
        rejected_font_dirs=rejected_font_dirs,
    )


if __name__ == "__main__":
    main()

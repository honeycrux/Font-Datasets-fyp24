# This script reads GNT files from the CASIA dataset and converts them into images.

# Dataset format:
# casia-dataset-source/
# ├── 001-f.gnt
# ├── 002-f.gnt

# Output format:
# casia-dataset/TargetImage/
# ├── style_1
# │   ├── style_1+char1.png
# │   ├── style_1+char2.png
# ├── style_2
# │   ├── style_2+char1.png
# │   ├── style_2+char2.png


import struct
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
from PIL import Image
from tqdm import tqdm


class CharacterGlyph:
    sample_size: int
    tag_code: int
    width: int
    height: int
    bitmap: bytes

    def __init__(
        self, sample_size: int, tag_code: int, width: int, height: int, bitmap: bytes
    ):
        self.sample_size = sample_size
        self.tag_code = tag_code
        self.width = width
        self.height = height
        self.bitmap = bitmap

    def to_image(self):
        img_array = np.frombuffer(self.bitmap, dtype=np.uint8).reshape(
            (self.height, self.width)
        )
        return Image.fromarray(img_array)

    def get_character(self):
        try:
            return bytes([self.tag_code >> 8, self.tag_code & 0xFF]).decode("gb2312")
        except UnicodeDecodeError:
            return None

    def get_chinese_character(self):
        character = self.get_character()
        if character and self.is_chinese_character(character):
            return character
        return None

    @staticmethod
    def is_chinese_character(character: str) -> bool:
        return (
            "\u4e00" <= character <= "\u9fff"
            and character.isprintable()
            and character not in r'\/:*?"<>|'
        )


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


def list_gnt_files(source_dir: str | Path):
    source_path = Path(source_dir)

    source_gnt_files = [
        source_gnt_file
        for source_gnt_file in source_path.iterdir()
        if source_gnt_file.is_file() and source_gnt_file.suffix == ".gnt"
    ]

    return source_gnt_files


def generate_target_images_from_gnt_files(
    output_target_image_dir: str | Path, source_gnt_files: Sequence[str | Path]
):
    success_characters: set[str] = set()
    skipped_characters: set[str] = set()

    for source_gnt_file in (
        progress_bar := tqdm(
            source_gnt_files, total=len(source_gnt_files), desc="Processing fonts"
        )
    ):
        style_number = Path(source_gnt_file).stem.split("-")[0]
        font_name = f"style_{style_number}"

        target_font_path = Path(output_target_image_dir) / font_name
        target_font_path.mkdir(exist_ok=True)
        target_font_path.chmod(0o777)

        progress_bar.set_postfix({"dir": target_font_path})

        for character_glyph in tqdm(
            read_gnt_file(source_gnt_file), desc=f"{font_name}", leave=False
        ):
            success = save_character(character_glyph, target_font_path, font_name)
            character = character_glyph.get_character()

            if character is not None:
                remove_null_bytes: Callable[[str], str] = lambda char: char.rstrip(
                    "\x00"
                )
                if success:
                    success_characters.add(remove_null_bytes(character))
                else:
                    skipped_characters.add(remove_null_bytes(character))

    return success_characters, skipped_characters


def read_gnt_file(file_path: str | Path):

    with open(file_path, "rb") as f:
        while True:
            header = f.read(10)
            if not header:
                break
            sample_size = struct.unpack("<I", header[:4])[0]
            tag_code = struct.unpack(">H", header[4:6])[0]
            width = struct.unpack("<H", header[6:8])[0]
            height = struct.unpack("<H", header[8:10])[0]
            bitmap = f.read(width * height)
            yield CharacterGlyph(sample_size, tag_code, width, height, bitmap)


def save_character(
    character_glyph: CharacterGlyph, target_font_path: str | Path, font_name: str
):
    chinese_character = character_glyph.get_chinese_character()

    if not chinese_character:
        return False

    img = character_glyph.to_image()

    img_file = Path(target_font_path) / f"{font_name}+{chinese_character}.png"
    img.save(img_file)
    img_file.chmod(0o777)

    return True


def create_target_images(source_dir: str | Path, output_target_image_dir: str | Path):
    ensure_dir_exists_with_perms(output_target_image_dir)

    assert Path(source_dir).exists(), f"Source directory {source_dir} does not exist."

    source_gnt_files = list_gnt_files(source_dir)

    success_characters, skipped_characters = generate_target_images_from_gnt_files(
        output_target_image_dir=output_target_image_dir,
        source_gnt_files=source_gnt_files,
    )

    return success_characters, skipped_characters


def main():
    source_dir = "casia-dataset-source"
    output_target_image_dir = "casia-dataset/TargetImage"

    success, skipped = create_target_images(
        source_dir=source_dir, output_target_image_dir=output_target_image_dir
    )

    print(f"Skipped characters: {' '.join(skipped)}")


if __name__ == "__main__":
    main()

# This script processes the zhuojg dataset

# Dataset format:
# zhuojg-dataset-source/
# ├── font1
# │   ├── char1
# │   │   ├── image1.gif
# │   │   ├── image2.gif
# │   ├── char2
# │   │   ├── image1.gif
# │   │   ├── image2.gif
# ├── font2
# │   ├── char1
# │   │   ├── image1.gif
# │   │   ├── image2.gif
# │   ├── char2
# │   │   ├── image1.gif
# │   │   ├── image2.gif

# Output format:
# zhuojg-dataset/TargetImage/
# ├── font1
# │   ├── font1+char1.png
# │   ├── font1+char1+1.png
# │   ├── font1+char2.png
# │   ├── font1+char2+1.png
# ├── font2
# │   ├── font2+char1.png
# │   ├── font2+char1+1.png
# │   ├── font2+char2.png
# │   ├── font2+char2+1.png

from pathlib import Path

from PIL import Image
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


def generate_target_images_from_source_font_path(
    source_font_path: Path,
    output_target_font_path: Path,
):
    success_characters: set[str] = set()
    skipped_characters: set[str] = set()

    source_char_paths = [
        source_char_path
        for source_char_path in source_font_path.iterdir()
        if source_char_path.is_dir()
    ]

    font_name = source_font_path.name

    for source_char_path in (
        progress_bar := tqdm(
            source_char_paths,
            total=len(source_char_paths),
            desc=f"{font_name}",
            leave=False,
        )
    ):
        char_name = source_char_path.name

        source_image_files = list(source_char_path.iterdir())

        new_image_names = [
            (
                f"{font_name}+{char_name}.png"
                if i == 0
                else f"{font_name}+{char_name}+{i}.png"
            )
            for i in range(len(source_image_files))
        ]

        new_image_paths = [
            output_target_font_path / new_image_name
            for new_image_name in new_image_names
        ]

        # Convert and save images
        for source_image_file, new_image_path in zip(
            source_image_files, new_image_paths
        ):
            try:
                with Image.open(source_image_file) as img:
                    img.convert("RGB").save(new_image_path, "PNG")

                new_image_path.chmod(0o777)

                success_characters.add(char_name)

            except Exception as e:
                progress_bar.write(
                    f'Exception "{type(e).__name__}" occurred on image {source_image_file} -> {new_image_path}'
                )

                skipped_characters.add(char_name)

    return success_characters, skipped_characters


def create_target_images(source_dir: str | Path, output_target_image_dir: str | Path):
    ensure_dir_exists_with_perms(output_target_image_dir)

    source_path = Path(source_dir)
    output_target_image_path = Path(output_target_image_dir)

    success_characters: set[str] = set()
    skipped_characters: set[str] = set()

    total_fonts = len(list(source_path.iterdir()))

    # Iterate through each font directory
    for source_font_path in tqdm(
        source_path.iterdir(), total=total_fonts, desc="Create target images"
    ):

        if source_font_path.is_dir():
            font_name = source_font_path.name

            # Create a subdirectory for the font in the target directory
            output_target_font_path = output_target_image_path / font_name
            output_target_font_path.mkdir(parents=True, exist_ok=True)
            output_target_font_path.chmod(0o777)

            success, skipped = generate_target_images_from_source_font_path(
                source_font_path=source_font_path,
                output_target_font_path=output_target_font_path,
            )

            success_characters.update(success)
            skipped_characters.update(skipped)

    return success_characters, skipped_characters


def main():
    # Input and output directory paths
    source_dir = "zhuojg-dataset-source/"  # Change this to your actual input directory
    output_target_image_dir = (
        "zhuojg-dataset/TargetImage/"  # Change this to your desired output directory
    )

    create_target_images(
        source_dir=source_dir, output_target_image_dir=output_target_image_dir
    )


if __name__ == "__main__":
    main()

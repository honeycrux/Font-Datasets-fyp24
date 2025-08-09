# This script generates content images from a valid target image directory

# Dataset format:
# xxx-dataset/
# ├── TargetImage/
# │   ├── fontA
# │   │   ├── fontA+char1.png
# │   │   ├── fontA+char2.png
# │   ├── fontB
# │   │   ├── fontB+char1.png
# │   │   ├── fontB+char2.png

# Output format:
# xxx-dataset/
# ├── ContentImage/
# │   ├── char1.png
# │   ├── char2.png


from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import table__c_m_a_p as CmapTable
from PIL import Image, ImageDraw, ImageFont
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


def parse_target_image_name(target_image_name: str):
    # Input Format: style+content[+optional-suffix]
    target_components = target_image_name.split("+")
    style = target_components[0]
    content = target_components[1]
    return style, content


def load_font(font_path: str | Path, font_size: int):
    try:
        return ImageFont.truetype(font_path, font_size), TTFont(font_path)
    except Exception as e:
        print(f"Cannot load font: {font_path}, error: {e}")
        return None


def is_char_in_font(char: str, tt_font: TTFont) -> bool:
    cmap = tt_font["cmap"]
    assert type(cmap) is CmapTable
    for subtable in cmap.tables:
        if ord(char) in subtable.cmap:
            return True
    return False


def find_required_characters(target_image_dir: str | Path) -> set[str]:
    target_image_path = Path(target_image_dir)

    required_characters = set()

    total_fonts = len(list(target_image_path.iterdir()))

    for target_font_path in tqdm(
        target_image_path.iterdir(), total=total_fonts, desc="Scan for characters"
    ):
        font_name = target_font_path.name
        total_files = len(list(target_font_path.iterdir()))

        for image_file in tqdm(
            target_font_path.iterdir(),
            total=total_files,
            desc=f"{font_name}",
            leave=False,
        ):
            if image_file.is_file():
                _, char_name = parse_target_image_name(image_file.stem)

                if len(char_name) == 0:
                    raise ValueError(
                        f"Empty character name in file: {image_file.as_posix()}"
                    )

                if len(char_name) > 1:
                    raise ValueError(
                        f'Character name "{char_name}" should be a single character: {image_file.as_posix()}'
                    )

                required_characters.add(char_name)

    return required_characters


def render_character(
    character: str,
    output_dir: str | Path,
    image_size: tuple[int, int],
    free_type_font: ImageFont.FreeTypeFont,
    tt_font: TTFont,
) -> bool | str:
    if not is_char_in_font(character, tt_font):
        return f"Character {character} not found in font."

    try:
        # Create a new image with white background
        image = Image.new("RGB", image_size, "white")
        draw = ImageDraw.Draw(image)

        # Compute text size and position
        bbox = draw.textbbox((0, 0), character, font=free_type_font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        text_x = (image_size[0] - text_width) // 2
        text_y = (image_size[1] - text_height) // 2 - bbox[1]  # Adjust for baseline

        # Draw the character on the image
        draw.text((text_x, text_y), character, fill="black", font=free_type_font)

        # Save the image
        image.save(output_dir)
        Path(output_dir).chmod(0o777)

    except Exception as e:
        return f"Exception in character image generation: {character}, error: {e}"

    return True


def create_content_images(
    output_content_image_dir: str | Path,
    required_characters: set[str],
    free_type_font: ImageFont.FreeTypeFont,
    tt_font: TTFont,
    image_size: tuple[int, int],
):
    successful_characters = set()
    unsuccessful_characters = set()

    for character in (
        progress_bar := tqdm(
            required_characters,
            total=len(required_characters),
            desc="Create content images",
        )
    ):
        output_path = Path(output_content_image_dir) / f"{character}.png"

        if not output_path.exists():
            result = render_character(
                character, output_path, image_size, free_type_font, tt_font
            )

            if type(result) is bool:
                successful_characters.add(character)
            else:
                progress_bar.write(result)
                unsuccessful_characters.add(character)

    return successful_characters, unsuccessful_characters


def create_content_images_from_target_images(
    output_content_image_dir: str | Path,
    target_image_dir: str | Path,
    font_dir: str | Path,
    image_size: tuple[int, int],
    font_size: int,
):
    ensure_dir_exists_with_perms(output_content_image_dir)

    font_result = load_font(font_dir, font_size)
    if not font_result:
        return False
    free_type_font, tt_font = font_result

    required_characters = find_required_characters(target_image_dir)

    successful_characters, unsuccessful_characters = create_content_images(
        output_content_image_dir=output_content_image_dir,
        required_characters=required_characters,
        image_size=image_size,
        free_type_font=free_type_font,
        tt_font=tt_font,
    )

    return successful_characters, unsuccessful_characters


def main():
    content_image_dir = "xxx-dataset/ContentImage"
    target_image_dir = "xxx-dataset/TargetImage"
    font_dir = "ttf/SourceHanSansSC-VF.ttf"
    image_size = (128, 128)
    font_size = 100

    result = create_content_images_from_target_images(
        output_content_image_dir=content_image_dir,
        target_image_dir=target_image_dir,
        font_dir=font_dir,
        image_size=image_size,
        font_size=font_size,
    )

    if not result:
        print("Failed to create content images.")
        return

    successful, unsuccessful = result

    print(f"Unsuccessful characters: {', '.join(unsuccessful)}")


if __name__ == "__main__":
    main()

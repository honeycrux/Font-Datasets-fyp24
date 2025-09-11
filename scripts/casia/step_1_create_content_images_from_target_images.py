from ..common.create_content_images_from_target_images import (
    create_content_images_from_target_images,
)
from ..common.delete_target_images_without_content_image import (
    delete_target_images_without_content_image,
)


def main():
    content_image_dir = "casia-dataset/ContentImage"
    target_image_dir = "casia-dataset/TargetImage"
    font_dir = "ttf/SourceHanSerifTC-VF.ttf"
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

    if unsuccessful:
        print(
            f"Content images for some characters could not be created: {', '.join(unsuccessful)}"
        )

        while True:
            to_retry = (
                input(
                    "Do you want to delete target images associated with no content images? (Warning: This action is irreversible.) ([y]/n): "
                )
                .strip()
                .lower()
            )

            if to_retry in ["", "y", "yes"]:
                preserved, removed = delete_target_images_without_content_image(
                    content_image_dir=content_image_dir,
                    target_image_dir=target_image_dir,
                )

                print(f"Removed characters: {', '.join(removed)}")

            elif to_retry in ["n", "no"]:
                print("No target images will be deleted.")
                break

            else:
                print("Invalid input. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()

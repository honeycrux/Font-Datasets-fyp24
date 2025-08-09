import shutil
from pathlib import Path

import pytest

from scripts.common.create_content_images_from_target_images import (
    create_content_images_from_target_images,
)
from scripts.util.compare_directories import compare_directories_and_return_summary

test_reference_path = (
    Path("tests") / "common" / "create_content_images_from_target_images_test_data"
)

test_output_path = Path("test_outputs")

test_font_dir = "ttf/SourceHanSerifTC-VF.ttf"

test_image_size = (128, 128)

test_font_size = 100


@pytest.fixture(scope="session", autouse=True)
def create_empty_target_images():
    # We need to create empty directories for the test
    # because git does not track empty directories.

    empty_dir = test_reference_path / "empty_target_images"
    if empty_dir.exists():
        shutil.rmtree(empty_dir)
    empty_dir.mkdir(exist_ok=True, parents=True)

    empty_dir_result = test_reference_path / "empty_target_images_result"
    if empty_dir_result.exists():
        shutil.rmtree(empty_dir_result)
    empty_dir_result.mkdir(exist_ok=True, parents=True)


@pytest.fixture(scope="session", autouse=True)
def create_target_images_with_empty_fonts():
    # We need to create empty directories for the test
    # because git does not track empty directories.

    empty_dir = test_reference_path / "target_images_with_empty_fonts"

    if empty_dir.exists():
        shutil.rmtree(empty_dir)

    empty_dir_font_1 = empty_dir / "font1"
    empty_dir_font_2 = empty_dir / "font2"
    empty_dir_font_1.mkdir(exist_ok=True, parents=True)
    empty_dir_font_2.mkdir(exist_ok=True, parents=True)

    empty_dir_result = test_reference_path / "target_images_with_empty_fonts_result"

    if empty_dir_result.exists():
        shutil.rmtree(empty_dir_result)

    empty_dir_result.mkdir(exist_ok=True, parents=True)


@pytest.fixture
def target_image_dir(dataset_name: str):
    target_image_dir = test_reference_path / dataset_name

    return target_image_dir


@pytest.fixture
def output_content_image_dir(dataset_name: str):
    content_images_dir = test_output_path / dataset_name

    if content_images_dir.exists():
        shutil.rmtree(content_images_dir)

    content_images_dir.mkdir(exist_ok=True, parents=True)

    yield content_images_dir

    if content_images_dir.exists():
        shutil.rmtree(content_images_dir)


@pytest.mark.parametrize("dataset_name", ["empty_target_images"])
def test_create_with_missing_font(output_content_image_dir):
    bad_font_dir = "non_existent_font.ttf"

    target_image_dir = test_reference_path / "empty_target_images"

    result = create_content_images_from_target_images(
        output_content_image_dir=output_content_image_dir,
        target_image_dir=target_image_dir,
        font_dir=bad_font_dir,
        image_size=test_image_size,
        font_size=test_font_size,
    )

    assert result is False


@pytest.mark.parametrize("dataset_name", ["empty_target_images"])
def test_create_empty_target_images(target_image_dir, output_content_image_dir):
    expected_content_images_dir = test_reference_path / "empty_target_images_result"

    result = create_content_images_from_target_images(
        target_image_dir=target_image_dir,
        output_content_image_dir=output_content_image_dir,
        font_dir=test_font_dir,
        image_size=test_image_size,
        font_size=test_font_size,
    )

    assert type(result) is tuple
    successful, unsuccessful = result
    assert successful == set()
    assert unsuccessful == set()

    directories_are_equal, message = compare_directories_and_return_summary(
        output_content_image_dir, expected_content_images_dir
    )

    assert directories_are_equal, message


@pytest.mark.parametrize("dataset_name", ["target_images_with_empty_fonts"])
def test_create_target_images_with_empty_fonts(
    target_image_dir, output_content_image_dir
):
    expected_content_images_dir = (
        test_reference_path / "target_images_with_empty_fonts_result"
    )

    result = create_content_images_from_target_images(
        output_content_image_dir=output_content_image_dir,
        target_image_dir=target_image_dir,
        font_dir=test_font_dir,
        image_size=test_image_size,
        font_size=test_font_size,
    )

    assert type(result) is tuple
    successful, unsuccessful = result
    assert successful == set()
    assert unsuccessful == set()

    directories_are_equal, message = compare_directories_and_return_summary(
        output_content_image_dir, expected_content_images_dir
    )

    assert directories_are_equal, message


@pytest.mark.parametrize("dataset_name", ["target_images_with_valid_characters"])
def test_target_images_with_valid_characters_can_be_created(
    target_image_dir, output_content_image_dir
):
    expected_content_images_dir = (
        test_reference_path / "target_images_with_valid_characters_result"
    )

    result = create_content_images_from_target_images(
        output_content_image_dir=output_content_image_dir,
        target_image_dir=target_image_dir,
        font_dir=test_font_dir,
        image_size=test_image_size,
        font_size=test_font_size,
    )

    assert type(result) is tuple
    successful, unsuccessful = result
    assert successful == {"書", "法"}
    assert unsuccessful == set()

    directories_are_equal, message = compare_directories_and_return_summary(
        output_content_image_dir, expected_content_images_dir
    )

    assert directories_are_equal, message


@pytest.mark.parametrize(
    "dataset_name", ["target_images_with_characters_not_found_in_font"]
)
def test_characters_not_found_in_font_cannot_be_created(
    target_image_dir, output_content_image_dir
):
    expected_content_images_dir = (
        test_reference_path / "target_images_with_characters_not_found_in_font_result"
    )

    result = create_content_images_from_target_images(
        output_content_image_dir=output_content_image_dir,
        target_image_dir=target_image_dir,
        font_dir=test_font_dir,
        image_size=test_image_size,
        font_size=test_font_size,
    )

    assert type(result) is tuple
    successful, unsuccessful = result
    assert successful == {"劍"}
    assert unsuccessful == {"☣"}

    directories_are_equal, message = compare_directories_and_return_summary(
        output_content_image_dir, expected_content_images_dir
    )

    assert directories_are_equal, message


@pytest.mark.parametrize("dataset_name", ["target_images_with_zero_characters"])
def test_zero_character_target_images_results_in_value_error(
    target_image_dir, output_content_image_dir
):
    with pytest.raises(ValueError) as exc_info:
        create_content_images_from_target_images(
            output_content_image_dir=output_content_image_dir,
            target_image_dir=target_image_dir,
            font_dir=test_font_dir,
            image_size=test_image_size,
            font_size=test_font_size,
        )

    assert (
        str(exc_info.value) == "Empty character name in file: "
        f"{target_image_dir.as_posix()}/fontA/fontA+.txt"
    )


@pytest.mark.parametrize("dataset_name", ["target_images_with_multiple_characters"])
def test_multi_character_target_images_results_in_value_error(
    target_image_dir, output_content_image_dir
):
    with pytest.raises(ValueError) as exc_info:
        create_content_images_from_target_images(
            output_content_image_dir=output_content_image_dir,
            target_image_dir=target_image_dir,
            font_dir=test_font_dir,
            image_size=test_image_size,
            font_size=test_font_size,
        )

    assert (
        str(exc_info.value) == 'Character name "非單字" should be a single character: '
        f"{target_image_dir.as_posix()}/fontA/fontA+非單字.txt"
    )

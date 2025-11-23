import shutil
from pathlib import Path

import pytest

from scripts.neumason.step_0_create_content_and_target_images import (
    create_content_and_target_images,
)
from scripts.util.compare_directories import compare_directories_and_return_summary

test_reference_path = (
    Path("tests") / "neumason" / "create_content_and_target_images_test_data"
)

test_output_path = Path("test_outputs")

test_wordlist_file = test_reference_path / "wordlist.txt"


@pytest.fixture(scope="session", autouse=True)
def create_empty_source():
    # We need to create an empty directory for the test
    # because git does not track empty directories.

    empty_dir = test_reference_path / "empty_source"

    if empty_dir.exists():
        shutil.rmtree(empty_dir)

    empty_dir_font_1 = empty_dir / "fontA.ttf"
    empty_dir_font_1.mkdir(exist_ok=True, parents=True)

    empty_dir_result = test_reference_path / "empty_source_result"

    if empty_dir_result.exists():
        shutil.rmtree(empty_dir_result)

    empty_dir_result_content = empty_dir_result / "ContentImage"
    empty_dir_result_content.mkdir(exist_ok=True, parents=True)

    empty_dir_result_target = empty_dir_result / "TargetImage"
    empty_dir_result_target.mkdir(exist_ok=True, parents=True)


@pytest.fixture
def output_dir(dataset_name: str):
    target_image_dir = test_output_path / dataset_name

    if target_image_dir.exists():
        shutil.rmtree(target_image_dir)

    target_image_dir.mkdir(exist_ok=True, parents=True)

    yield target_image_dir

    if target_image_dir.exists():
        shutil.rmtree(target_image_dir)


@pytest.mark.parametrize(
    "dataset_name", ["empty_source", "source_with_chinese_characters"]
)
def test_create_content_and_target_images(output_dir, dataset_name):
    source_dir = test_reference_path / dataset_name

    create_content_and_target_images(
        source_dir=source_dir,
        output_dir=output_dir,
        content_font_dir="fontA.ttf",
        rejected_font_dirs=[],
    )

    directories_are_equal, message = compare_directories_and_return_summary(
        output_dir, test_reference_path / (dataset_name + "_result")
    )

    assert directories_are_equal, message


@pytest.mark.parametrize("dataset_name", ["source_with_rejected_fonts"])
def test_create_target_images_with_rejected_fonts(output_dir, dataset_name):
    source_dir = test_reference_path / dataset_name

    create_content_and_target_images(
        source_dir=source_dir,
        output_dir=output_dir,
        content_font_dir="fontA.ttf",
        rejected_font_dirs=["fontC.ttf"],
    )

    directories_are_equal, message = compare_directories_and_return_summary(
        output_dir, test_reference_path / (dataset_name + "_result")
    )

    assert directories_are_equal, message

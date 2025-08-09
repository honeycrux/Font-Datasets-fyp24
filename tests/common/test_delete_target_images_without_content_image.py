import shutil
from pathlib import Path

import pytest

from scripts.common.delete_target_images_without_content_image import (
    delete_target_images_without_content_image,
)
from scripts.util.compare_directories import compare_directories_and_return_summary

test_reference_path = (
    Path("tests") / "common" / "delete_target_images_without_content_image_test_data"
)

test_output_path = Path("test_outputs")


@pytest.fixture(scope="session", autouse=True)
def create_empty_dataset():
    # because git does not track empty directories.
    # We need to create empty directories for the test

    empty_dir = test_reference_path / "empty_dataset"

    if (empty_dir).exists():
        shutil.rmtree(empty_dir)

    empty_dir_content_images = empty_dir / "ContentImage"
    empty_dir_target_images = empty_dir / "TargetImage"
    empty_dir_content_images.mkdir(exist_ok=True, parents=True)
    empty_dir_target_images.mkdir(exist_ok=True, parents=True)

    empty_dir_result = test_reference_path / "empty_dataset_result"

    if empty_dir_result.exists():
        shutil.rmtree(empty_dir_result)

    empty_dir_content_images_result = empty_dir_result / "ContentImage"
    empty_dir_target_images_result = empty_dir_result / "TargetImage"
    empty_dir_content_images_result.mkdir(exist_ok=True, parents=True)
    empty_dir_target_images_result.mkdir(exist_ok=True, parents=True)


@pytest.fixture
def test_dataset_path(dataset_name: Path):
    dataset_path = test_reference_path / dataset_name
    test_dataset_path = test_output_path / dataset_name

    if test_dataset_path.exists():
        shutil.rmtree(test_dataset_path)

    shutil.copytree(dataset_path, test_dataset_path)

    yield test_dataset_path

    if test_dataset_path.exists():
        shutil.rmtree(test_dataset_path)


@pytest.mark.parametrize("dataset_name", ["empty_dataset"])
def test_does_not_delete_target_images_in_empty_dataset(test_dataset_path: Path):
    content_image_path = test_dataset_path / "ContentImage"
    target_image_path = test_dataset_path / "TargetImage"

    expected_result_path = test_reference_path / "empty_dataset_result"

    preserved, removed = delete_target_images_without_content_image(
        content_image_path, target_image_path
    )

    assert preserved == set()
    assert removed == set()

    directories_are_equal, message = compare_directories_and_return_summary(
        test_dataset_path, expected_result_path
    )

    assert directories_are_equal, message


@pytest.mark.parametrize("dataset_name", ["dataset_with_no_missing_content_images"])
def test_does_not_delete_target_images_with_content_images(test_dataset_path: Path):
    content_image_path = test_dataset_path / "ContentImage"
    target_image_path = test_dataset_path / "TargetImage"

    expected_result_path = (
        test_reference_path / "dataset_with_no_missing_content_images_result"
    )

    preserved, removed = delete_target_images_without_content_image(
        content_image_path, target_image_path
    )

    assert preserved == {"char1", "char2"}
    assert not removed

    directories_are_equal, message = compare_directories_and_return_summary(
        test_dataset_path, expected_result_path
    )

    assert directories_are_equal, message


@pytest.mark.parametrize("dataset_name", ["dataset_with_missing_content_images"])
def test_deletes_target_images_without_content_images(test_dataset_path: Path):
    content_image_path = test_dataset_path / "ContentImage"
    target_image_path = test_dataset_path / "TargetImage"

    expected_result_path = (
        test_reference_path / "dataset_with_missing_content_images_result"
    )

    preserved, removed = delete_target_images_without_content_image(
        content_image_path, target_image_path
    )

    assert preserved == {"char1"}
    assert removed == {"char2"}

    directories_are_equal, message = compare_directories_and_return_summary(
        test_dataset_path, expected_result_path
    )

    assert directories_are_equal, message
    assert directories_are_equal, message

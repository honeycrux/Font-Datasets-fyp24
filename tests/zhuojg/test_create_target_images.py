import shutil
from pathlib import Path

import pytest

from scripts.util.compare_directories import compare_directories_and_return_summary
from scripts.zhuojg.step_0_create_target_images import create_target_images

test_reference_path = Path("tests") / "zhuojg" / "create_target_images_test_data"

test_output_path = Path("test_outputs")


@pytest.fixture(scope="session", autouse=True)
def create_empty_source():
    # We need to create an empty directory for the test
    # because git does not track empty directories.

    empty_dir = test_reference_path / "empty_source"

    if empty_dir.exists():
        shutil.rmtree(empty_dir)

    empty_dir.mkdir(exist_ok=True, parents=True)

    empty_dir_result = test_reference_path / "empty_source_result"

    if empty_dir_result.exists():
        shutil.rmtree(empty_dir_result)

    empty_dir_result.mkdir(exist_ok=True, parents=True)


@pytest.fixture
def output_target_image_dir(dataset_name: str):
    target_image_dir = test_output_path / dataset_name

    if target_image_dir.exists():
        shutil.rmtree(target_image_dir)

    target_image_dir.mkdir(exist_ok=True, parents=True)

    yield target_image_dir

    if target_image_dir.exists():
        shutil.rmtree(target_image_dir)


@pytest.mark.parametrize("dataset_name", ["empty_source"])
def test_create_target_images_of_empty_source(output_target_image_dir):
    source_dir = test_reference_path / "empty_source"

    success, skipped = create_target_images(
        source_dir=source_dir, output_target_image_dir=output_target_image_dir
    )

    assert success == set()
    assert skipped == set()

    directories_are_equal, message = compare_directories_and_return_summary(
        output_target_image_dir,
        test_reference_path / "empty_source_result",
    )

    assert directories_are_equal, message


@pytest.mark.parametrize("dataset_name", ["source_with_gifs"])
def test_create_target_images_of_source_with_gifs(output_target_image_dir):
    source_dir = test_reference_path / "source_with_gifs"

    success, skipped = create_target_images(
        source_dir=source_dir, output_target_image_dir=output_target_image_dir
    )

    assert success == {"書", "法"}
    assert skipped == set()

    directories_are_equal, message = compare_directories_and_return_summary(
        output_target_image_dir,
        test_reference_path / f"source_with_gifs_result",
    )

    assert directories_are_equal, message

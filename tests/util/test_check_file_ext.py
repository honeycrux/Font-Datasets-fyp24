import shutil
from pathlib import Path

import pytest

from scripts.util.check_file_ext import extract_file_extensions

test_reference_path = Path("tests") / "util" / "check_file_ext_test_data"


@pytest.fixture(scope="module", autouse=True)
def create_empty_dataset():
    # We need to create empty directories for the test
    # because git does not track empty directories.

    if (test_reference_path / "empty_dataset").exists():
        shutil.rmtree(test_reference_path / "empty_dataset")

    empty_dir_1 = test_reference_path / "empty_dataset" / "dir1"
    empty_dir_1.mkdir(exist_ok=True, parents=True)

    empty_dir_2 = test_reference_path / "empty_dataset" / "dir2"
    empty_dir_2.mkdir(exist_ok=True, parents=True)


@pytest.mark.parametrize(
    "dataset_name, expected_result",
    [
        ("empty_dataset", set()),
        ("dataset_with_empty_extensions", {""}),
        ("dataset_with_txt_files", {"txt"}),
        ("dataset_with_multiple_image_formats", {"png", "gif", "jpeg"}),
    ],
)
def test_check_file_extensions(dataset_name: str, expected_result: set[str]):
    dataset_path = test_reference_path / dataset_name

    result = extract_file_extensions(dataset_path)

    assert (
        result == expected_result
    ), f"Expected {expected_result} but got {result} for dataset {dataset_name}"

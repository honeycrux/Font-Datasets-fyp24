import shutil
from pathlib import Path

import pytest
from scripts.util.report_dataset_summary import report_dataset_summary

test_reference_path = Path("tests") / "util" / "report_dataset_summary_test_data"


@pytest.fixture(scope="session", autouse=True)
def create_empty_dataset():
    # We need to create empty directories for the test
    # because git does not track empty directories.

    empty_dir = test_reference_path / "empty_dataset"

    if empty_dir.exists():
        shutil.rmtree(empty_dir)

    empty_dir.mkdir(exist_ok=True, parents=True)


@pytest.fixture(scope="session", autouse=True)
def create_dataset_with_two_empty_fonts():
    # We need to create empty directories for the test
    # because git does not track empty directories.

    empty_dir = test_reference_path / "dataset_with_two_empty_fonts"

    if empty_dir.exists():
        shutil.rmtree(empty_dir)

    empty_dir_font_1 = empty_dir / "font1"
    empty_dir_font_1.mkdir(exist_ok=True, parents=True)

    empty_dir_font_2 = empty_dir / "font2"
    empty_dir_font_2.mkdir(exist_ok=True, parents=True)


def test_summarize_empty_dataset():
    target_image_dir = test_reference_path / "empty_dataset"
    expected_summary = "No fonts found in the dataset."
    assert report_dataset_summary(target_image_dir) == expected_summary


def test_summarize_dataset_with_two_empty_fonts():
    target_image_dir = test_reference_path / "dataset_with_two_empty_fonts"
    expected_summary = (
        "Total number of fonts: 2\n"
        "Range of characters per font: 0-0\n"
        "Average number of characters per font: 0.00\n"
        "Standard deviation of characters per font: 0.00\n"
        "Total number of characters: 0"
    )
    assert report_dataset_summary(target_image_dir) == expected_summary


def test_summarize_dataset_with_two_to_three_chars():
    target_image_dir = test_reference_path / "dataset_with_two_to_three_chars"
    expected_summary = (
        "Total number of fonts: 2\n"
        "Range of characters per font: 2-3\n"
        "Average number of characters per font: 2.50\n"
        "Standard deviation of characters per font: 0.71\n"
        "Total number of characters: 5"
    )
    assert report_dataset_summary(target_image_dir) == expected_summary

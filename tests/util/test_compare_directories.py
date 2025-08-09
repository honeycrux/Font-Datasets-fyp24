import shutil
from pathlib import Path

from scripts.util.compare_directories import compare_directories_and_return_summary

test_reference_path = Path("tests") / "util" / "compare_directories_test_data"


def compare_empty_directories():
    # We need to create empty directories for the test
    # because git does not track empty directories.

    if (test_reference_path / "empty_directories").exists():
        shutil.rmtree(test_reference_path / "empty_directories")

    empty_dir_1 = test_reference_path / "empty_directories" / "dir1"
    empty_dir_1.mkdir(exist_ok=True, parents=True)

    empty_dir_2 = test_reference_path / "empty_directories" / "dir2"
    empty_dir_2.mkdir(exist_ok=True, parents=True)

    return compare_directories_and_return_summary(empty_dir_1, empty_dir_2)


def test_empty_directories_are_equal():
    directories_are_equal, message = compare_empty_directories()
    assert directories_are_equal


def test_equal_directories_result_message():
    directories_are_equal, message = compare_empty_directories()
    assert message == "Directories are identical."
    pass


def compare_directories_with_same_files():
    dir1 = test_reference_path / "directories_with_same_files" / "dir1"
    dir2 = test_reference_path / "directories_with_same_files" / "dir2"
    return compare_directories_and_return_summary(dir1, dir2)


def test_directories_with_same_files_are_equal():
    directories_are_equal, message = compare_directories_with_same_files()
    assert directories_are_equal


def compare_directories_with_outer_differences():
    dir1 = test_reference_path / "directories_with_outer_differences" / "dir1"
    dir2 = test_reference_path / "directories_with_outer_differences" / "dir2"
    return compare_directories_and_return_summary(dir1, dir2)


def test_directories_with_outer_differences_are_not_equal():
    directories_are_equal, message = compare_directories_with_outer_differences()
    assert not directories_are_equal


def test_outer_differences_result_message():
    directories_are_equal, message = compare_directories_with_outer_differences()
    assert (
        message == "Files not present in both directories:\n"
        "tests/util/compare_directories_test_data/directories_with_outer_differences/dir1/file1.txt\n"
        "tests/util/compare_directories_test_data/directories_with_outer_differences/dir2/file2.txt"
    )


def compare_directories_with_inner_differences():
    dir1 = test_reference_path / "directories_with_inner_differences" / "dir1"
    dir2 = test_reference_path / "directories_with_inner_differences" / "dir2"
    return compare_directories_and_return_summary(dir1, dir2)


def test_directories_with_inner_differences_are_not_equal():
    directories_are_equal, message = compare_directories_with_inner_differences()
    assert not directories_are_equal


def test_inner_differences_result_message():
    directories_are_equal, message = compare_directories_with_inner_differences()
    assert (
        message == "Files with different content:\n"
        "tests/util/compare_directories_test_data/directories_with_inner_differences/dir1/file1.txt and "
        "tests/util/compare_directories_test_data/directories_with_inner_differences/dir2/file1.txt"
    )


def compare_directories_with_all_problems():
    dir1 = test_reference_path / "directories_with_all_problems" / "dir1"
    dir2 = test_reference_path / "directories_with_all_problems" / "dir2"
    return compare_directories_and_return_summary(dir1, dir2)


def test_directories_with_all_problems_are_not_equal():
    directories_are_equal, message = compare_directories_with_all_problems()
    assert not directories_are_equal


def test_all_problems_message():
    directories_are_equal, message = compare_directories_with_all_problems()
    assert (
        message == "Files not present in both directories:\n"
        "tests/util/compare_directories_test_data/directories_with_all_problems/dir1/file2.txt\n"
        "tests/util/compare_directories_test_data/directories_with_all_problems/dir2/file3.txt\n"
        "Files with different content:\n"
        "tests/util/compare_directories_test_data/directories_with_all_problems/dir1/file4.txt and "
        "tests/util/compare_directories_test_data/directories_with_all_problems/dir2/file4.txt"
    )


# I do not know how to create uncomparable files (funny files) to write the following tests.
# https://docs.python.org/3.13/library/filecmp.html#filecmp.dircmp.funny_files


# def compare_directories_with_uncomparable_files():
#     pass


# def test_directories_with_uncomparable_files_are_not_equal():
#     directories_are_equal, message = compare_directories_with_uncomparable_files()
#     assert not directories_are_equal


# def test_uncomparable_files_result_message():
#     directories_are_equal, message = compare_directories_with_uncomparable_files()
#     assert (
#         message == "Failed to compare files:\n"
#         "tests/util/directories_with_uncomparable_files/dir1/file1.txt and "
#         "tests/util/directories_with_uncomparable_files/dir2/file1.txt\n"
#     )

# This script is used for testing.
# It compares two directories and reports differences, mismatched files, and uncomparable files.


import filecmp
from pathlib import Path

import numpy as np
from PIL import Image

image_file_extensions = {".png", ".jpg", ".jpeg"}


def images_are_equal(img1_path: Path, img2_path: Path) -> bool:
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    arr1 = np.frombuffer(img1.tobytes(), dtype=np.uint8)
    arr2 = np.frombuffer(img2.tobytes(), dtype=np.uint8)
    return np.array_equal(arr1, arr2)


def compare_directories(
    dir1: str | Path,
    dir2: str | Path,
    outer_differences: list[Path],
    inner_differences: list[tuple[Path, Path]],
    uncomparable_files: list[tuple[Path, Path]],
) -> None:
    assert Path(dir1).exists(), f"{dir1} does not exist."
    assert Path(dir2).exists(), f"{dir2} does not exist."
    assert Path(dir1).is_dir(), f"{dir1} is not a directory."
    assert Path(dir2).is_dir(), f"{dir2} is not a directory."

    dcmp = filecmp.dircmp(
        dir1, dir2, shallow=False
    )  # `shallow` is available since Python 3.13

    # Files that are only in one directory
    outer_differences.extend(
        [Path(dir1) / file for file in dcmp.left_only]
        + [Path(dir2) / file for file in dcmp.right_only]
    )

    # Files that are different
    for file in dcmp.diff_files:
        is_image_file = Path(file).suffix.lower() in image_file_extensions

        path1 = Path(dir1) / file
        path2 = Path(dir2) / file

        if not is_image_file:
            inner_differences.append((path1, path2))
            continue

        if not images_are_equal(path1, path2):
            inner_differences.append((path1, path2))

    # Files that cannot be compared
    uncomparable_files.extend(
        [(Path(dir1) / file, Path(dir2) / file) for file in dcmp.funny_files]
    )

    # Recursively compare subdirectories
    for sub_dcmp in dcmp.subdirs.values():
        compare_directories(
            sub_dcmp.left,
            sub_dcmp.right,
            outer_differences,
            inner_differences,
            uncomparable_files,
        )


def create_comparison_summary(
    outer_differences: list[Path],
    inner_differences: list[tuple[Path, Path]],
    uncomparable_files: list[tuple[Path, Path]],
) -> tuple[bool, str]:
    has_outer_differences = len(outer_differences) > 0
    has_inner_difference = len(inner_differences) > 0
    has_uncomparable_files = len(uncomparable_files) > 0

    if not (has_outer_differences or has_inner_difference or has_uncomparable_files):
        return True, "Directories are identical."

    output: list[str] = []

    if has_outer_differences:
        sorted_outer_differences = sorted(outer_differences)
        output.append("Files not present in both directories:")
        for file in sorted_outer_differences:
            output.append(f"{file.as_posix()}")

    if has_inner_difference:
        sorted_inner_differences = sorted(inner_differences)
        output.append("Files with different content:")
        for file1, file2 in sorted_inner_differences:
            output.append(f"{file1.as_posix()} and {file2.as_posix()}")

    if has_uncomparable_files:
        sorted_uncomparable_files = sorted(uncomparable_files)
        output.append("Failed to compare files:")
        for file1, file2 in sorted_uncomparable_files:
            output.append(f"{file1.as_posix()} and {file2.as_posix()}")

    return False, "\n".join(output)


def compare_directories_and_return_summary(dir1: str | Path, dir2: str | Path):
    compare_directories(
        dir1,
        dir2,
        outer_differences := [],
        inner_differences := [],
        uncomparable_files := [],
    )

    directories_are_equal, message = create_comparison_summary(
        outer_differences, inner_differences, uncomparable_files
    )

    return directories_are_equal, message

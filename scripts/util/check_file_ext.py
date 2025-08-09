# This script scans the whole directory tree of a specified source directory
# and checks for unique file extensions.
# This helps identifying any missing or unsupported file types.


from pathlib import Path


def extract_file_extensions(source_dir: str | Path):
    # Set to hold unique file extensions
    extensions = set()

    # Walk through the directory recursively using Path.walk (Python 3.12+)
    for root, dirs, files in Path(source_dir).walk():
        for file in files:
            file_path = root / file
            ext = file_path.suffix
            extension = ext.lower().lstrip(".")
            extensions.add(extension)

    return extensions


def main():
    # Input directory path
    source_dir = "xxx-dataset-source/"  # Change this to your actual source directory

    extensions = extract_file_extensions(source_dir)

    # Print the unique extensions found
    print("Unique file extensions found:")
    for ext in sorted(extensions):
        print(ext)


if __name__ == "__main__":
    main()

"""File Organizer — scan a directory and move files into category subfolders."""

import argparse
import logging
import shutil
from pathlib import Path

CATEGORIES: dict[str, list[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Video": [".mp4", ".mov", ".avi", ".mkv"],
    "Archives": [".zip", ".tar", ".gz", ".rar"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".yaml"],
}

_EXT_MAP: dict[str, str] = {
    ext: category
    for category, exts in CATEGORIES.items()
    for ext in exts
}


def get_category(extension: str) -> str:
    return _EXT_MAP.get(extension.lower(), "Other")


def scan_files(directory: Path, recursive: bool = True) -> list[Path]:
    pattern = "**/*" if recursive else "*"
    return [p for p in directory.glob(pattern) if p.is_file()]


def handle_duplicate(destination: Path) -> Path:
    if not destination.exists():
        return destination
    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def resolve_destination(file: Path, base_dir: Path) -> Path:
    category = get_category(file.suffix)
    dest_dir = base_dir / category
    return handle_duplicate(dest_dir / file.name)


def setup_logging(log_path: Path) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def organize(directory: Path, dry_run: bool = True, recursive: bool = True) -> None:
    files = scan_files(directory, recursive=recursive)

    if not files:
        logging.info("No files found in %s", directory)
        return

    mode = "DRY-RUN" if dry_run else "MOVE"
    logging.info("Mode: %s | Directory: %s | Files found: %d", mode, directory, len(files))

    moved = skipped = errors = 0

    for file in files:
        # Skip files that are already inside a category subfolder we created
        if file.parent.name in {*CATEGORIES, "Other"} and file.parent.parent == directory:
            logging.info("SKIP (already organised)  %s", file.name)
            skipped += 1
            continue

        destination = resolve_destination(file, directory)

        if dry_run:
            logging.info("WOULD MOVE  %s  →  %s", file, destination)
        else:
            try:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file), str(destination))
                logging.info("MOVED  %s  →  %s", file, destination)
                moved += 1
            except PermissionError as exc:
                logging.error("PERMISSION ERROR  %s  — %s", file, exc)
                errors += 1
            except OSError as exc:
                logging.error("ERROR  %s  — %s", file, exc)
                errors += 1

    logging.info("Done. moved=%d  skipped=%d  errors=%d", moved, skipped, errors)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organise files in a directory into category subfolders."
    )
    parser.add_argument("directory", type=Path, help="Target directory to organise.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview planned operations without moving any files.",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Scan only the top level (recursive is on by default).",
    )
    args = parser.parse_args()

    target: Path = args.directory.resolve()

    if not target.exists():
        parser.error(f"Directory does not exist: {target}")
    if not target.is_dir():
        parser.error(f"Path is not a directory: {target}")

    log_path = target / "organizer.log"
    setup_logging(log_path)

    organize(target, dry_run=args.dry_run, recursive=not args.no_recursive)


if __name__ == "__main__":
    main()

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


def scan_files(directory: Path) -> list[Path]:
    return [p for p in directory.iterdir() if p.is_file()]


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


def organize(directory: Path, dry_run: bool = True) -> None:
    files = scan_files(directory)

    if not files:
        logging.info("No files found in %s", directory)
        return

    mode = "DRY-RUN" if dry_run else "MOVE"
    logging.info("Mode: %s | Directory: %s | Files found: %d", mode, directory, len(files))

    moved = skipped = errors = 0

    for file in files:
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
    parser.add_argument("directory", nargs="?", type=Path, help="Target directory to organise.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview planned operations without moving any files.",
    )
    args = parser.parse_args()

    directory = args.directory
    if directory is None:
        while True:
            raw = input("Enter the target directory path: ").strip()
            if not raw:
                print("Path cannot be empty. Please try again.")
                continue
            candidate = Path(raw).resolve()
            if not candidate.exists():
                print(f"Directory does not exist: {candidate}. Please try again.")
                continue
            if not candidate.is_dir():
                print(f"Not a directory: {candidate}. Please try again.")
                continue
            directory = candidate
            break
        target = directory
    else:
        target = directory.resolve()
        if not target.exists():
            parser.error(f"Directory does not exist: {target}")
        if not target.is_dir():
            parser.error(f"Path is not a directory: {target}")

    logs_dir = target / "logs"
    logs_dir.mkdir(exist_ok=True)
    log_path = logs_dir / "organizer.log"
    setup_logging(log_path)

    organize(target, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

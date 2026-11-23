"""File Organizer — implement your solution here."""

# TODO: Implement the file organizer.
#
# SAFETY: Never move files without first confirming the target directory.
# Always implement and test dry-run mode before testing actual moves.
#
# Suggested structure:
#   CATEGORIES: dict[str, list[str]] = { ... }
#
#   def get_category(extension: str) -> str: ...
#   def scan_files(directory: Path) -> list[Path]: ...
#   def resolve_destination(file: Path, base_dir: Path) -> Path: ...
#   def handle_duplicate(destination: Path) -> Path: ...
#   def organize(directory: Path, dry_run: bool = True) -> None: ...
#   def main() -> None: ...


def main() -> None:
    raise NotImplementedError("Implement the main() function.")


if __name__ == "__main__":
    main()

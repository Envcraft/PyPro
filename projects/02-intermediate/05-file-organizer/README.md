# Project 05: File Organizer

**Level:** Intermediate
**Estimated Time:** 10–14 hours

---

## Overview

Build a CLI tool that scans a target directory, categorises files by extension, and moves them into organised subdirectories. Supports a dry-run mode that previews changes without modifying any files.

---

## Objectives

- Use `pathlib` for file system operations.
- Handle file conflicts safely.
- Implement dry-run mode.
- Log operations to a file.

---

## Python Concepts Practised

- `pathlib.Path`
- `shutil`
- File categorisation
- Logging (`logging` module)
- Exception handling
- Dry-run pattern

---

## Functional Requirements

1. Accept a target directory path as an argument.
2. Scan for all files (non-recursive by default, recursive optional).
3. Categorise by extension:
   - Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`
   - Documents: `.pdf`, `.doc`, `.docx`, `.txt`, `.md`, `.xlsx`, `.csv`
   - Audio: `.mp3`, `.wav`, `.flac`, `.aac`
   - Video: `.mp4`, `.mov`, `.avi`, `.mkv`
   - Archives: `.zip`, `.tar`, `.gz`, `.rar`
   - Code: `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.yaml`
   - Other: everything else
4. Create destination subdirectories as needed.
5. Move files to the appropriate subdirectory.
6. Handle duplicate filenames by appending a counter.
7. Support `--dry-run` to preview operations without moving files.
8. Log all operations (moved, skipped, errors) to `organizer.log`.

---

## Non-Functional Requirements

- Never overwrite an existing file silently.
- Must have dry-run mode before any file is moved.
- Operations must be logged.

---

## Safety Requirements

- Never modify files outside the specified target directory.
- Always implement and test dry-run mode before testing actual moves.

---

## Edge Cases

- Empty directory.
- Files with no extension.
- Duplicate filenames.
- Directory with subdirectories.
- Target directory does not exist.
- Insufficient permissions.

---

## Acceptance Criteria

- [ ] Files are moved to the correct category folder.
- [ ] Dry-run lists all planned operations without moving anything.
- [ ] Duplicates are renamed, not overwritten.
- [ ] Log file contains a record of all operations.
- [ ] Invalid target path produces a clear error.

---

## Suggested Implementation Steps

1. Write the extension-to-category mapping.
2. Write the file scanning function.
3. Write the destination path resolution function.
4. Write the duplicate filename handler.
5. Write the move function.
6. Add logging.
7. Add dry-run mode.
8. Build the CLI interface.
9. Write tests (without moving real files — use temporary directories).

---

## Testing Requirements

Use `tmp_path` pytest fixture to create temporary directories.

- Test categorisation for each file type.
- Test duplicate filename handling.
- Test dry-run does not move files.
- Test files with no extension go to "Other".

---

## Constraints

- Standard library only (`pathlib`, `shutil`, `logging`).
- No third-party packages.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] Tests use `tmp_path`, not real user directories.
- [ ] Tests written and passing.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Recursive scanning option.
- Undo last operation (move files back).
- Configuration file for custom category mappings.

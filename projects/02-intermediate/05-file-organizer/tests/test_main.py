"""Tests for File Organizer.

Use tmp_path fixture — never test against real user directories.
"""

from pathlib import Path

import pytest

from src.main import get_category, handle_duplicate, organize, scan_files  # noqa: E501


class TestGetCategory:
    def test_image_extension(self) -> None:
        assert get_category(".jpg") == "Images"
        assert get_category(".PNG") == "Images"  # case-insensitive

    def test_document_extension(self) -> None:
        assert get_category(".pdf") == "Documents"
        assert get_category(".docx") == "Documents"

    def test_audio_extension(self) -> None:
        assert get_category(".mp3") == "Audio"

    def test_video_extension(self) -> None:
        assert get_category(".mp4") == "Video"

    def test_archive_extension(self) -> None:
        assert get_category(".zip") == "Archives"

    def test_code_extension(self) -> None:
        assert get_category(".py") == "Code"

    def test_unknown_extension(self) -> None:
        assert get_category(".xyz") == "Other"

    def test_no_extension(self) -> None:
        assert get_category("") == "Other"


class TestScanFiles:
    def test_finds_files(self, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("x")
        (tmp_path / "b.jpg").write_text("x")
        files = scan_files(tmp_path)
        assert len(files) == 2

    def test_empty_directory(self, tmp_path: Path) -> None:
        assert scan_files(tmp_path) == []

    def test_skips_nested_files(self, tmp_path: Path) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "nested.txt").write_text("x")
        assert scan_files(tmp_path) == []

    def test_does_not_return_subdirectories(self, tmp_path: Path) -> None:
        (tmp_path / "sub").mkdir()
        assert scan_files(tmp_path) == []


class TestHandleDuplicate:
    def test_no_conflict(self, tmp_path: Path) -> None:
        dest = tmp_path / "file.txt"
        assert handle_duplicate(dest) == dest

    def test_renames_duplicate(self, tmp_path: Path) -> None:
        dest = tmp_path / "file.txt"
        dest.write_text("original")
        result = handle_duplicate(dest)
        assert result == tmp_path / "file_1.txt"

    def test_renames_multiple_duplicates(self, tmp_path: Path) -> None:
        (tmp_path / "file.txt").write_text("1")
        (tmp_path / "file_1.txt").write_text("2")
        result = handle_duplicate(tmp_path / "file.txt")
        assert result == tmp_path / "file_2.txt"


class TestDryRun:
    def test_dry_run_does_not_move_files(self, tmp_path: Path) -> None:
        (tmp_path / "photo.jpg").write_text("img")
        (tmp_path / "report.pdf").write_text("doc")
        organize(tmp_path, dry_run=True)
        # files must still be in the original location
        assert (tmp_path / "photo.jpg").exists()
        assert (tmp_path / "report.pdf").exists()
        # category folders must NOT be created
        assert not (tmp_path / "Images").exists()
        assert not (tmp_path / "Documents").exists()

    def test_dry_run_does_not_create_log_entries_as_moves(self, tmp_path: Path) -> None:
        (tmp_path / "song.mp3").write_text("audio")
        organize(tmp_path, dry_run=True)
        assert (tmp_path / "Audio").exists() is False


class TestOrganize:
    def test_moves_files_to_correct_category(self, tmp_path: Path) -> None:
        (tmp_path / "photo.jpg").write_text("img")
        (tmp_path / "report.pdf").write_text("doc")
        (tmp_path / "song.mp3").write_text("audio")
        organize(tmp_path, dry_run=False)
        assert (tmp_path / "Images" / "photo.jpg").exists()
        assert (tmp_path / "Documents" / "report.pdf").exists()
        assert (tmp_path / "Audio" / "song.mp3").exists()

    def test_unknown_extension_goes_to_other(self, tmp_path: Path) -> None:
        (tmp_path / "data.xyz").write_text("?")
        organize(tmp_path, dry_run=False)
        assert (tmp_path / "Other" / "data.xyz").exists()

    def test_no_extension_goes_to_other(self, tmp_path: Path) -> None:
        (tmp_path / "README").write_text("text")
        organize(tmp_path, dry_run=False)
        assert (tmp_path / "Other" / "README").exists()

    def test_duplicate_files_renamed_not_overwritten(self, tmp_path: Path) -> None:
        (tmp_path / "Images").mkdir()
        (tmp_path / "Images" / "photo.jpg").write_text("existing")
        (tmp_path / "photo.jpg").write_text("new")
        organize(tmp_path, dry_run=False)
        assert (tmp_path / "Images" / "photo.jpg").read_text() == "existing"
        assert (tmp_path / "Images" / "photo_1.jpg").read_text() == "new"

    def test_empty_directory(self, tmp_path: Path) -> None:
        organize(tmp_path, dry_run=False)  # should not raise

    def test_subfolders_are_not_touched(self, tmp_path: Path) -> None:
        sub = tmp_path / "misc"
        sub.mkdir()
        (sub / "clip.mp4").write_text("video")
        organize(tmp_path, dry_run=False)
        # file inside subfolder must stay where it is
        assert (sub / "clip.mp4").exists()
        assert not (tmp_path / "Video" / "clip.mp4").exists()

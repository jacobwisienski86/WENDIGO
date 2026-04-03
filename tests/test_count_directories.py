# tests/test_count_directories.py
# Tests for count_directories in openmc_internal_functions.py

import pytest

from src.WINDIGO.openmc_internal_functions import count_directories


class FakeDirEntry:
    """Simple fake object to mimic os.DirEntry."""
    def __init__(self, path, is_dir):
        self.path = path
        self._is_dir = is_dir

    def is_dir(self):
        return self._is_dir


def test_count_directories_basic(monkeypatch):
    """Count only directories, skipping any with 'input' in the path."""

    entries = [
        FakeDirEntry("/path/0001", True),
        FakeDirEntry("/path/0002", True),
        FakeDirEntry("/path/input_files", True),     # should be skipped
        FakeDirEntry("/path/0003", False),           # file, not directory
        FakeDirEntry("/path/INPUT_extra", True),     # should be skipped (case-insensitive)
    ]

    monkeypatch.setattr("os.scandir", lambda p: entries)

    result = count_directories("/path")
    assert result == 2  # only 0001 and 0002


def test_count_directories_no_directories(monkeypatch):
    """Return 0 when no valid directories exist."""

    entries = [
        FakeDirEntry("/path/file1", False),
        FakeDirEntry("/path/file2", False),
        FakeDirEntry("/path/input_data", False),
    ]

    monkeypatch.setattr("os.scandir", lambda p: entries)

    result = count_directories("/path")
    assert result == 0


def test_count_directories_all_filtered(monkeypatch):
    """All directories contain 'input' → count should be 0."""

    entries = [
        FakeDirEntry("/path/input1", True),
        FakeDirEntry("/path/INPUT2", True),
        FakeDirEntry("/path/inPut3", True),
    ]

    monkeypatch.setattr("os.scandir", lambda p: entries)

    result = count_directories("/path")
    assert result == 0


def test_count_directories_mixed_case(monkeypatch):
    """Ensure case-insensitive filtering of 'input' works correctly."""

    entries = [
        FakeDirEntry("/path/0001", True),
        FakeDirEntry("/path/InPuT_folder", True),  # should be skipped
        FakeDirEntry("/path/0002", True),
    ]

    monkeypatch.setattr("os.scandir", lambda p: entries)

    result = count_directories("/path")
    assert result == 2
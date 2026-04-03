# tests/test_create_direct_perturbation_list.py
# Tests for the function: create_direct_perturbation_list

import builtins
import pytest

from src.WINDIGO.frendy_internal_functions import create_direct_perturbation_list


def test_create_direct_perturbation_list_basic(monkeypatch):
    """Test that the list file is created and contains the expected lines."""

    written_path = None
    written_lines = []

    class FakeFile:
        def __init__(self, path, mode):
            nonlocal written_path
            written_path = path

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def writelines(self, lines):
            written_lines.extend(lines)

        def close(self):
            pass

    monkeypatch.setattr(builtins, "open", lambda p, m: FakeFile(p, m))

    lines = ["file1\n", "file2\n"]

    result = create_direct_perturbation_list(
        nuclide="U235",
        mt_Number=102,
        perturbation_list_lines=lines,
    )

    expected_filename = "perturbation_list_U235_MT_102Direct.inp"
    assert result == expected_filename
    assert written_path == expected_filename
    assert written_lines == lines


def test_create_direct_perturbation_list_empty(monkeypatch):
    """Test that an empty list still produces a valid file."""

    written_path = None
    written_lines = []

    class FakeFile:
        def __init__(self, path, mode):
            nonlocal written_path
            written_path = path

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def writelines(self, lines):
            written_lines.extend(lines)

        def close(self):
            pass

    monkeypatch.setattr(builtins, "open", lambda p, m: FakeFile(p, m))

    result = create_direct_perturbation_list(
        nuclide="Fe56",
        mt_Number=51,
        perturbation_list_lines=[],
    )

    expected_filename = "perturbation_list_Fe56_MT_51Direct.inp"
    assert result == expected_filename
    assert written_path == expected_filename
    assert written_lines == []
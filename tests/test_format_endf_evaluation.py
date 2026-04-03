# tests/test_format_endf_evaluation.py
# Tests for the function: format_endf_evaluation

import shutil
import pytest

from src.WINDIGO.frendy_internal_functions import format_endf_evaluation


def test_format_endf_evaluation_basic(monkeypatch):
    """Ensure .dat filename is created correctly and shutil.copy2 is called."""

    copied = []

    def fake_copy2(src, dst):
        copied.append((src, dst))

    monkeypatch.setattr("src.WINDIGO.frendy_internal_functions.shutil.copy2", fake_copy2)

    result = format_endf_evaluation("/path/to/U235.endf")

    assert result == "/path/to/U235.dat"
    assert copied == [
        ("/path/to/U235.endf", "/path/to/U235.dat")
    ]


def test_format_endf_evaluation_relative_path(monkeypatch):
    """Ensure relative .endf paths are handled correctly."""

    copied = []

    monkeypatch.setattr(
        "src.WINDIGO.frendy_internal_functions.shutil.copy2",
        lambda src, dst: copied.append((src, dst)),
    )

    result = format_endf_evaluation("Th232.endf")

    assert result == "Th232.dat"
    assert copied == [
        ("Th232.endf", "Th232.dat")
    ]


def test_format_endf_evaluation_filename_with_dots(monkeypatch):
    """Ensure filenames containing multiple dots still convert correctly."""

    copied = []

    monkeypatch.setattr(
        "src.WINDIGO.frendy_internal_functions.shutil.copy2",
        lambda src, dst: copied.append((src, dst)),
    )

    result = format_endf_evaluation("/lib/n-092.U235.v1.endf")

    assert result == "/lib/n-092.U235.v1.dat"
    assert copied == [
        ("/lib/n-092.U235.v1.endf", "/lib/n-092.U235.v1.dat")
    ]
# tests/test_direct_perturbation_folder_check.py
# Tests for the function: direct_perturbation_folder_check

import pytest

from src.WINDIGO.frendy_internal_functions import direct_perturbation_folder_check


def test_direct_perturbation_folder_check_all_exist(monkeypatch):
    """All expected folders exist → return False."""

    # Capture which paths are checked
    checked_paths = []

    def fake_exists(path):
        checked_paths.append(path)
        return True

    monkeypatch.setattr("os.path.exists", fake_exists)

    energy_grid = [1.0, 2.0, 3.0]  # 2 intervals → 0001, 0002
    base = "/perturbed"

    result = direct_perturbation_folder_check(base, energy_grid)

    assert result is False
    assert checked_paths == [
        "/perturbed/0001",
        "/perturbed/0002",
    ]


def test_direct_perturbation_folder_check_missing_folder(monkeypatch):
    """If any folder is missing, return True and stop checking further."""

    checked_paths = []

    def fake_exists(path):
        checked_paths.append(path)
        # First exists, second missing
        return path.endswith("0001")

    monkeypatch.setattr("os.path.exists", fake_exists)

    energy_grid = [1.0, 2.0, 3.0]  # 2 intervals
    base = "/perturbed"

    result = direct_perturbation_folder_check(base, energy_grid)

    assert result is True
    # Should stop after the missing folder
    assert checked_paths == [
        "/perturbed/0001",
        "/perturbed/0002",
    ]


def test_direct_perturbation_folder_check_padding_ranges(monkeypatch):
    """Verify correct folder naming for <9, 9–98, and ≥99 index ranges."""

    monkeypatch.setattr("os.path.exists", lambda path: True)

    # 101 intervals → indices 0–100
    energy_grid = list(range(102))
    base = "/perturbed"

    direct_perturbation_folder_check(base, energy_grid)

    # Build expected folder names
    expected = []
    for ii in range(101):
        if ii < 9:
            expected.append(f"{base}/000{ii+1}")
        elif 9 <= ii <= 98:
            expected.append(f"{base}/00{ii+1}")
        else:
            expected.append(f"{base}/0{ii+1}")

    # Now verify that os.path.exists was called with these paths
    # We capture calls by wrapping exists
    calls = []

    def capture_exists(path):
        calls.append(path)
        return True

    monkeypatch.setattr("os.path.exists", capture_exists)

    direct_perturbation_folder_check(base, energy_grid)

    assert calls == expected


def test_direct_perturbation_folder_check_single_interval(monkeypatch):
    """A grid with one interval should check exactly one folder."""

    checked = []
    monkeypatch.setattr("os.path.exists", lambda p: checked.append(p) or True)

    energy_grid = [10.0, 20.0]  # 1 interval → 0001
    base = "/perturbed"

    result = direct_perturbation_folder_check(base, energy_grid)

    assert result is False
    assert checked == ["/perturbed/0001"]


def test_direct_perturbation_folder_check_empty_grid(monkeypatch):
    """Empty or single-point grid → no intervals → no checks → return False."""

    monkeypatch.setattr("os.path.exists", lambda p: True)

    assert direct_perturbation_folder_check("/perturbed", []) is False
    assert direct_perturbation_folder_check("/perturbed", [1.0]) is False
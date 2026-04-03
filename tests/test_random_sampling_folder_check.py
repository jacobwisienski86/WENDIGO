# tests/test_random_sampling_folder_check.py
# Tests for the function: random_sampling_folder_check

import pytest

from src.WINDIGO.frendy_internal_functions import random_sampling_folder_check


def test_random_sampling_folder_check_all_exist(monkeypatch):
    """All expected folders exist → return False."""

    checked = []

    monkeypatch.setattr("os.path.exists", lambda p: checked.append(p) or True)

    sample_size = 3
    base = "/ace/U235"

    result = random_sampling_folder_check(sample_size, base)

    assert result is False
    assert checked == [
        "/ace/U235/0001",
        "/ace/U235/0002",
        "/ace/U235/0003",
    ]


def test_random_sampling_folder_check_missing(monkeypatch):
    """If any folder is missing, return True and stop checking further."""

    checked = []

    def fake_exists(path):
        checked.append(path)
        return path.endswith("0001")  # only the first exists

    monkeypatch.setattr("os.path.exists", fake_exists)

    sample_size = 3
    base = "/ace/U235"

    result = random_sampling_folder_check(sample_size, base)

    assert result is True
    assert checked == [
        "/ace/U235/0001",
        "/ace/U235/0002",
    ]


def test_random_sampling_folder_check_padding(monkeypatch):
    """Verify correct folder naming for <9, 9–98, and ≥99 index ranges."""

    calls = []

    monkeypatch.setattr("os.path.exists", lambda p: calls.append(p) or True)

    sample_size = 105
    base = "/ace/X"

    random_sampling_folder_check(sample_size, base)

    expected = []
    for ii in range(sample_size):
        if ii < 9:
            expected.append(f"{base}/000{ii+1}")
        elif 9 <= ii <= 98:
            expected.append(f"{base}/00{ii+1}")
        else:
            expected.append(f"{base}/0{ii+1}")

    assert calls == expected


def test_random_sampling_folder_check_zero_samples(monkeypatch):
    """Zero samples → no checks → return False."""

    monkeypatch.setattr("os.path.exists", lambda p: True)

    result = random_sampling_folder_check(0, "/ace")
    assert result is False
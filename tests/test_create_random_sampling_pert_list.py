# tests/test_create_random_sampling_pert_list.py
# Tests for the function: create_random_sampling_pert_list

import builtins
import pytest

from src.WINDIGO.frendy_internal_functions import (
    create_random_sampling_pert_list,
)


def test_create_random_sampling_pert_list_basic(monkeypatch):
    """Test correct filename and contents for a small sample size."""

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

    nuclide = "U235"
    mt = 102
    directory = "U235_RandomSamplingInputs"
    sample_size = 3

    result = create_random_sampling_pert_list(
        nuclide,
        mt,
        directory,
        sample_size,
    )

    expected_filename = "perturbation_list_U235_MT_102.inp"
    assert result == expected_filename
    assert written_path == expected_filename

    expected_lines = [
        f"{directory}/U235_0001\n",
        f"{directory}/U235_0002\n",
        f"{directory}/U235_0003\n",
    ]

    assert written_lines == expected_lines


def test_create_random_sampling_pert_list_padding(monkeypatch):
    """Test correct zero-padding for indices <9, 9–98, and ≥99."""

    written_lines = []

    class FakeFile:
        def __init__(self, path, mode):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def writelines(self, lines):
            written_lines.extend(lines)

        def close(self):
            pass

    monkeypatch.setattr(builtins, "open", lambda p, m: FakeFile(p, m))

    nuclide = "X"
    mt = 1
    directory = "X_Random"
    sample_size = 105  # covers all padding ranges

    create_random_sampling_pert_list(
        nuclide,
        mt,
        directory,
        sample_size,
    )

    # Extract filenames without newline
    filenames = [line.strip() for line in written_lines]

    # Check padding rules
    assert filenames[0].endswith("X_0001")      # ii = 0
    assert filenames[8].endswith("X_0009")      # ii = 8
    assert filenames[9].endswith("X_0010")      # ii = 9
    assert filenames[98].endswith("X_0099")     # ii = 98
    assert filenames[99].endswith("X_0100")     # ii = 99
    assert filenames[104].endswith("X_0105")    # ii = 104
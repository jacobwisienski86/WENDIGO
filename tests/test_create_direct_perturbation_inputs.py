# tests/test_create_direct_perturbation_inputs.py
# Tests for the function: create_direct_perturbation_inputs

import builtins
import pytest

from src.WINDIGO.frendy_internal_functions import create_direct_perturbation_inputs


def test_create_direct_perturbation_inputs_basic(monkeypatch):
    """Test correct folder name, file names, and file contents for a small grid."""

    # Capture mkdir calls
    created_dirs = []
    monkeypatch.setattr("os.mkdir", lambda path: created_dirs.append(path))

    # Capture file writes
    written_files = {}

    class FakeFile:
        def __init__(self, path, mode):
            self.path = path
            written_files[self.path] = ""

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def write(self, text):
            written_files[self.path] += text

        def close(self):
            pass

    monkeypatch.setattr(builtins, "open", lambda p, m: FakeFile(p, m))

    energy_grid = [1.0, 2.0, 3.0]
    perturb_coeff = 1.05

    perturb_list, folder_name = create_direct_perturbation_inputs(
        nuclide="U235",
        mt_Number=102,
        energy_grid=energy_grid,
        perturbation_coefficient=perturb_coeff,
    )

    expected_folder = "U235_DirectPerturbationInputs_ReactionMT_102"
    assert folder_name == expected_folder
    assert created_dirs == [expected_folder]

    # Expected filenames (2 intervals → 2 files)
    expected_files = [
        f"{expected_folder}/U235_0001",
        f"{expected_folder}/U235_0002",
    ]

    # Returned list should contain filenames with newline
    assert perturb_list == [f"{name}\n" for name in expected_files]

    # File contents should match MT, lower bound, upper bound, coefficient
    assert written_files[expected_files[0]] == "102     1.0     2.0     1.05"
    assert written_files[expected_files[1]] == "102     2.0     3.0     1.05"


def test_create_direct_perturbation_inputs_padding_ranges(monkeypatch):
    """Test filename padding logic for indices <9, 9–98, and ≥99."""

    monkeypatch.setattr("os.mkdir", lambda path: None)

    class FakeFile:
        def __init__(self, path, mode):
            self.path = path

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def write(self, text):
            pass

        def close(self):
            pass

    monkeypatch.setattr(builtins, "open", lambda p, m: FakeFile(p, m))

    # Construct a grid with 101 intervals → indices 0–100
    energy_grid = list(range(102))

    perturb_list, folder_name = create_direct_perturbation_inputs(
        nuclide="X",
        mt_Number=1,
        energy_grid=energy_grid,
        perturbation_coefficient=1.0,
    )

    # Extract filenames without newline
    filenames = [line.strip() for line in perturb_list]

    # Check padding rules
    assert filenames[0].endswith("X_0001")      # ii = 0
    assert filenames[8].endswith("X_0009")      # ii = 8
    assert filenames[9].endswith("X_0010")      # ii = 9
    assert filenames[98].endswith("X_0099")     # ii = 98
    assert filenames[99].endswith("X_0100")     # ii = 99
    assert filenames[100].endswith("X_0101")    # ii = 100


def test_create_direct_perturbation_inputs_single_interval(monkeypatch):
    """A grid with only one interval should produce exactly one file."""

    monkeypatch.setattr("os.mkdir", lambda path: None)

    written_files = {}

    class FakeFile:
        def __init__(self, path, mode):
            self.path = path
            written_files[self.path] = ""

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def write(self, text):
            written_files[self.path] = text

        def close(self):
            pass

    monkeypatch.setattr(builtins, "open", lambda p, m: FakeFile(p, m))

    energy_grid = [10.0, 20.0]

    perturb_list, folder_name = create_direct_perturbation_inputs(
        nuclide="Fe56",
        mt_Number=51,
        energy_grid=energy_grid,
        perturbation_coefficient=0.9,
    )

    expected_folder = "Fe56_DirectPerturbationInputs_ReactionMT_51"
    assert folder_name == expected_folder

    expected_file = f"{expected_folder}/Fe56_0001"
    assert perturb_list == [expected_file + "\n"]
# tests/test_create_random_sampling_tool_inputs.py
# Tests for the function: create_random_sampling_tool_inputs

import builtins
import pytest

from src.WINDIGO.frendy_internal_functions import (
    create_random_sampling_tool_inputs,
)


def test_create_random_sampling_tool_inputs_basic(monkeypatch):
    """Test creation of the random sampling input file with a small energy grid."""

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

    sample_size = 10
    seed = 777
    cov_path = "/tmp/rel_cov.csv"
    energy_grid = [0.01, 0.02]
    nuclide = "Xe135"
    mt = 18

    result = create_random_sampling_tool_inputs(
        sample_size,
        seed,
        cov_path,
        energy_grid,
        nuclide,
        mt,
    )

    assert result == "sample_copy.inp"
    assert written_path == "sample_copy.inp"

    expected_lines = [
        "<sample_size>         10\n",
        "\n",
        "<seed>                777\n",
        "\n",
        "<relative_covariance> /tmp/rel_cov.csv\n",
        "\n",
        "<energy_grid>          (0.01\n",
        "                       0.02)\n",
        "\n",
        "<nuclide>             (Xe135)\n",
        "\n",
        "<reaction>            (18)\n",
        "\n",
    ]

    assert written_lines == expected_lines


def test_create_random_sampling_tool_inputs_three_points(monkeypatch):
    """Test energy grid formatting for 3 points (middle point has no parentheses)."""

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

    energy_grid = [1.0, 2.0, 3.0]

    create_random_sampling_tool_inputs(
        5,
        42,
        "cov.csv",
        energy_grid,
        "Mo95",
        51,
    )

    # Energy grid lines start after:
    # sample_size, blank, seed, blank, cov, blank → index 6 onward
    grid_lines = written_lines[6:9]

    assert grid_lines == [
        "<energy_grid>          (1.0\n",
        "                       2.0\n",
        "                       3.0)\n",
    ]
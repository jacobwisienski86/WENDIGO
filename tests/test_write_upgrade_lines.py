# tests/test_write_upgrade_lines.py
# Tests for the function: write_upgrade_lines

import pytest

from src.WINDIGO.frendy_internal_functions import write_upgrade_lines


def test_write_upgrade_lines_low_energy():
    """Energy < 99.99 should use ±1e-6 offsets."""

    energy_grid = [1.0, 2.0, 3.0]

    result = write_upgrade_lines(energy_grid)

    # Expected upgrade bounds:
    # index 0 → +1e-6
    # index 1 → -1e-6, +1e-6
    # index 2 → -1e-6
    expected_bounds = [
        1.0 + 1e-6,
        2.0 - 1e-6,
        2.0 + 1e-6,
        3.0 - 1e-6,
    ]

    # Convert output lines back to floats for comparison
    extracted = []
    for line in result:
        num = float(line.strip().replace("add_grid_data    (", "").replace(")", ""))
        extracted.append(num)

    assert extracted == expected_bounds

    # Check formatting of first and last lines
    assert result[0].startswith("    add_grid_data    (")
    assert result[-1].endswith(")\n")


def test_write_upgrade_lines_mid_energy():
    """99.99 ≤ energy < 99990 should use ±0.1 offsets."""

    energy_grid = [100.0, 200.0, 300.0]

    result = write_upgrade_lines(energy_grid)

    expected_bounds = [
        100.0 + 0.1,
        200.0 - 0.1,
        200.0 + 0.1,
        300.0 - 0.1,
    ]

    extracted = []
    for line in result:
        num = float(line.strip().replace("add_grid_data    (", "").replace(")", ""))
        extracted.append(num)

    assert extracted == expected_bounds


def test_write_upgrade_lines_high_energy():
    """Energy ≥ 99990 should use ±1000 offsets."""

    energy_grid = [100000.0, 200000.0, 300000.0]

    result = write_upgrade_lines(energy_grid)

    expected_bounds = [
        100000.0 + 1000,
        200000.0 - 1000,
        200000.0 + 1000,
        300000.0 - 1000,
    ]

    extracted = []
    for line in result:
        num = float(line.strip().replace("add_grid_data    (", "").replace(")", ""))
        extracted.append(num)

    assert extracted == expected_bounds


def test_write_upgrade_lines_empty():
    """Empty energy grid should return an empty list."""

    result = write_upgrade_lines([])

    assert result == []
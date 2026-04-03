# tests/test_move_random_sampling_files.py
# Tests for the function: move_random_sampling_files

import pytest

from src.WINDIGO.frendy_internal_functions import move_random_sampling_files


def test_move_random_sampling_files(monkeypatch):
    """Test that the two shutil.move calls are made with correct paths."""

    moves = []

    # Patch shutil.move globally (correct target)
    monkeypatch.setattr(
        "shutil.move",
        lambda src, dst: moves.append((src, dst)),
    )

    random_dir = "/tmp/random_tool"
    nuclide = "U235"
    frendy_path = "/opt/frendy"
    mt = 102

    result = move_random_sampling_files(
        random_sampling_tool_directory=random_dir,
        nuclide=nuclide,
        frendy_Path=frendy_path,
        mt_Number=mt,
    )

    expected_new_name = "U235_RandomSamplingInputs_ReactionMT_102_Inputs"
    assert result == expected_new_name

    # Expected move operations
    expected_moves = [
        # First move: random_tool/U235 → /opt/frendy
        (f"{random_dir}/{nuclide}", frendy_path),

        # Second move: /opt/frendy/U235 → /opt/frendy/U235_RandomSamplingInputs_ReactionMT_102_Inputs
        (
            f"{frendy_path}/{nuclide}",
            f"{frendy_path}/{expected_new_name}",
        ),
    ]

    assert moves == expected_moves
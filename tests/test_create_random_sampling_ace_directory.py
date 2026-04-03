# tests/test_create_random_sampling_ace_directory.py
# Tests for the function: create_random_sampling_ace_directory

import pytest

from src.WINDIGO.frendy_internal_functions import (
    create_random_sampling_ace_directory,
)


def test_create_random_sampling_ace_directory(monkeypatch):
    """Test directory creation and correct move operations."""

    mkdir_calls = []
    move_calls = []

    # Patch os.mkdir globally
    monkeypatch.setattr("os.mkdir", lambda path: mkdir_calls.append(path))

    # Patch shutil.move globally
    monkeypatch.setattr(
        "shutil.move",
        lambda src, dst: move_calls.append((src, dst)),
    )

    frendy_path = "/opt/frendy"
    nuclide = "U235"
    mt = 102
    pert_list = "perturbation_list_U235_MT_102.inp"
    new_inputs = "U235_RandomSamplingInputs_ReactionMT_102_Inputs"

    result = create_random_sampling_ace_directory(
        frendy_Path=frendy_path,
        nuclide=nuclide,
        mt_Number=mt,
        perturbation_list_filename=pert_list,
        new_inputs_directory_name=new_inputs,
    )

    expected_dir = "/opt/frendy/U235_RandomSamplingACEFiles_ReactionMT_102"

    # Returned directory must match
    assert result == expected_dir

    # mkdir must be called once with the new directory
    assert mkdir_calls == [expected_dir]

    # Expected move operations
    expected_moves = [
        # Move perturbation list file
        (
            f"{frendy_path}/{pert_list}",
            f"{expected_dir}/{pert_list}",
        ),
        # Move inputs directory
        (
            f"{frendy_path}/{new_inputs}",
            f"{expected_dir}/{new_inputs}",
        ),
    ]

    assert move_calls == expected_moves
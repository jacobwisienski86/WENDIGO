# tests/test_generate_random_sampling_ace_files.py
# Tests for the main function: generate_random_sampling_ace_files

import builtins
import pytest

from src.WINDIGO.frendy_main_functions import (
    generate_random_sampling_ace_files,
)


def test_generate_random_sampling_ace_files_success(monkeypatch):
    """Test full workflow when all ACE files generate successfully."""

    # -----------------------------
    # Mock internal helper functions
    # -----------------------------
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_tool_execution_file",
        lambda **kwargs: "run_make_perturbation_factor.csh",
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_tool_inputs",
        lambda **kwargs: "sample_copy.inp",
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.generate_random_sampling_factors",
        lambda **kwargs: None,
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.move_random_sampling_files",
        lambda **kwargs: "U235_RandomSamplingInputs_ReactionMT_102_Inputs",
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_pert_list",
        lambda **kwargs: "perturbation_list_U235_MT_102.inp",
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_ace_directory",
        lambda **kwargs: "/opt/frendy/U235_RandomSamplingACEFiles_ReactionMT_102",
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_ace_execution_file",
        lambda **kwargs: "run_create_perturbed_ace_file.csh",
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.random_sampling_folder_check",
        lambda **kwargs: False,  # success
    )

    # -----------------------------
    # Mock OS operations
    # -----------------------------
    calls = {
        "getcwd": [],
        "chdir": [],
        "system": [],
        "remove": [],
        "rmtree": [],
        "print": [],
    }

    monkeypatch.setattr("os.getcwd", lambda: calls["getcwd"].append("cwd") or "cwd")
    monkeypatch.setattr("os.chdir", lambda p: calls["chdir"].append(p))
    monkeypatch.setattr("os.system", lambda cmd: calls["system"].append(cmd))
    monkeypatch.setattr("os.remove", lambda p: calls["remove"].append(p))
    monkeypatch.setattr("shutil.rmtree", lambda p: calls["rmtree"].append(p))
    monkeypatch.setattr(builtins, "print", lambda msg: calls["print"].append(msg))

    # -----------------------------
    # Run the function
    # -----------------------------
    frendy_path = "/opt/frendy"
    result = generate_random_sampling_ace_files(
        frendy_Path=frendy_path,
        relative_covariance_matrix_path="/data/cov.csv",
        unperturbed_ACE_file_path="/data/U235.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        seed=999,
        sample_size=5,
        cleanup_Flag=True,
    )

    expected_dir = "/opt/frendy/U235_RandomSamplingACEFiles_ReactionMT_102"
    assert result == expected_dir

    # -----------------------------
    # Validate directory switching
    # -----------------------------
    assert calls["chdir"] == [
        "/opt/frendy/tools/make_perturbation_factor",  # enter tool dir
        "/opt/frendy",                                 # move to FRENDY root
        expected_dir,                                  # enter ACE directory
        "cwd",                                         # return to original
    ]

    # -----------------------------
    # Validate system call
    # -----------------------------
    assert calls["system"] == ["csh ./run_create_perturbed_ace_file.csh"]

    # -----------------------------
    # Validate cleanup
    # -----------------------------
    assert "perturbation_list_U235_MT_102.inp" in calls["remove"]
    assert "run_create_perturbed_ace_file.csh" in calls["remove"]
    assert "results.log" in calls["remove"]
    assert "U235_RandomSamplingInputs_ReactionMT_102_Inputs" in calls["rmtree"]

    # -----------------------------
    # Validate success message
    # -----------------------------
    assert any("generated successfully" in msg for msg in calls["print"])


def test_generate_random_sampling_ace_files_failure(monkeypatch):
    """Test behavior when ACE files fail to generate."""

    # Mock helpers
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_tool_execution_file",
        lambda **kwargs: "run_make_perturbation_factor.csh",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_tool_inputs",
        lambda **kwargs: "sample_copy.inp",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.generate_random_sampling_factors",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.move_random_sampling_files",
        lambda **kwargs: "U235_RandomSamplingInputs_ReactionMT_102_Inputs",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_pert_list",
        lambda **kwargs: "perturbation_list.inp",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_ace_directory",
        lambda **kwargs: "/opt/frendy/U235_RandomSamplingACEFiles_ReactionMT_102",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_ace_execution_file",
        lambda **kwargs: "run_create_perturbed_ace_file.csh",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.random_sampling_folder_check",
        lambda **kwargs: True,  # failure
    )

    calls = {"print": [], "remove": [], "rmtree": []}

    monkeypatch.setattr("os.getcwd", lambda: "cwd")
    monkeypatch.setattr("os.chdir", lambda p: None)
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("os.remove", lambda p: calls["remove"].append(p))
    monkeypatch.setattr("shutil.rmtree", lambda p: calls["rmtree"].append(p))
    monkeypatch.setattr(builtins, "print", lambda msg: calls["print"].append(msg))

    frendy_path = "/opt/frendy"

    result = generate_random_sampling_ace_files(
        frendy_Path=frendy_path,
        relative_covariance_matrix_path="/data/cov.csv",
        unperturbed_ACE_file_path="/data/U235.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        sample_size=5,
        cleanup_Flag=True,
    )

    assert result is None
    assert any("not generated successfully" in msg for msg in calls["print"])


def test_generate_random_sampling_ace_files_no_cleanup(monkeypatch):
    """Ensure no cleanup occurs when cleanup_Flag=False."""

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_tool_execution_file",
        lambda **kwargs: "run_make_perturbation_factor.csh",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_tool_inputs",
        lambda **kwargs: "sample_copy.inp",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.generate_random_sampling_factors",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.move_random_sampling_files",
        lambda **kwargs: "U235_RandomSamplingInputs_ReactionMT_102_Inputs",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_pert_list",
        lambda **kwargs: "perturbation_list.inp",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_ace_directory",
        lambda **kwargs: "/opt/frendy/U235_RandomSamplingACEFiles_ReactionMT_102",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_random_sampling_ace_execution_file",
        lambda **kwargs: "run_create_perturbed_ace_file.csh",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.random_sampling_folder_check",
        lambda **kwargs: False,
    )

    calls = {"remove": [], "rmtree": []}

    monkeypatch.setattr("os.getcwd", lambda: "cwd")
    monkeypatch.setattr("os.chdir", lambda p: None)
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("os.remove", lambda p: calls["remove"].append(p))
    monkeypatch.setattr("shutil.rmtree", lambda p: calls["rmtree"].append(p))
    monkeypatch.setattr(builtins, "print", lambda msg: None)

    frendy_path = "/opt/frendy"

    generate_random_sampling_ace_files(
        frendy_Path=frendy_path,
        relative_covariance_matrix_path="/data/cov.csv",
        unperturbed_ACE_file_path="/data/U235.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        sample_size=5,
        cleanup_Flag=False,
    )

    assert calls["remove"] == []
    assert calls["rmtree"] == []
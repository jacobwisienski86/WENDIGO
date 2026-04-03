# tests/test_generate_direct_perturbation_ace_files.py
# Tests for the main function: generate_direct_perturbation_ace_files

import builtins
import pytest

from src.WINDIGO.frendy_main_functions import (
    generate_direct_perturbation_ace_files,
)


def test_generate_direct_perturbation_ace_files_success(monkeypatch):
    """Test full workflow when all ACE files generate successfully."""

    # -----------------------------
    # Mock internal helper functions
    # -----------------------------
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_direct_perturbation_inputs",
        lambda **kwargs: (["line1", "line2"], "input_folder"),
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_direct_perturbation_list",
        lambda **kwargs: "pert_list.inp",
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_direct_perturbation_command_file",
        lambda **kwargs: "run_create_perturbed_ace_file.csh",
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.direct_perturbation_folder_check",
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
        "exists": [],
        "makedirs": [],
    }

    monkeypatch.setattr("os.getcwd", lambda: calls["getcwd"].append("cwd") or "cwd")
    monkeypatch.setattr("os.chdir", lambda p: calls["chdir"].append(p))
    monkeypatch.setattr("os.system", lambda cmd: calls["system"].append(cmd))
    monkeypatch.setattr("os.remove", lambda p: calls["remove"].append(p))
    monkeypatch.setattr("os.path.exists", lambda p: calls["exists"].append(p) or True)
    monkeypatch.setattr("os.makedirs", lambda p: calls["makedirs"].append(p))
    monkeypatch.setattr("shutil.rmtree", lambda p: calls["rmtree"].append(p))
    monkeypatch.setattr(builtins, "print", lambda msg: calls["print"].append(msg))

    # -----------------------------
    # Run the function
    # -----------------------------
    frendy_path = "/opt/frendy"
    energy_grid = [1, 2, 3]

    result = generate_direct_perturbation_ace_files(
        frendy_Path=frendy_path,
        unperturbed_ACE_file_path="/data/U235.ace",
        energy_grid=energy_grid,
        mt_Number=102,
        nuclide="U235",
        perturbation_coefficient=1.05,
        cleanup_Flag=True,
    )

    expected_dir = "/opt/frendy/U235_DirectPerturbationACEFiles_ReactionMT_102"
    assert result == expected_dir

    # -----------------------------
    # Validate directory creation
    # -----------------------------
    assert calls["makedirs"] == [expected_dir]

    # -----------------------------
    # Validate directory switching
    # -----------------------------
    assert calls["chdir"] == [
        "/opt/frendy",          # enter FRENDY root
        expected_dir,           # enter perturbed ACE folder
        "cwd",                  # return to original directory
    ]

    # -----------------------------
    # Validate system call
    # -----------------------------
    assert calls["system"] == ["csh ./run_create_perturbed_ace_file.csh"]

    # -----------------------------
    # Validate cleanup
    # -----------------------------
    assert "pert_list.inp" in calls["remove"]
    assert "run_create_perturbed_ace_file.csh" in calls["remove"]
    assert f"{expected_dir}/results.log" in calls["remove"]
    assert "input_folder" in calls["rmtree"]

    # -----------------------------
    # Validate success message
    # -----------------------------
    assert any("All ACE files have successfully generated" in msg for msg in calls["print"])


def test_generate_direct_perturbation_ace_files_failure(monkeypatch):
    """Test behavior when some ACE files fail to generate."""

    # Mock helpers
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_direct_perturbation_inputs",
        lambda **kwargs: (["line"], "input_folder"),
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_direct_perturbation_list",
        lambda **kwargs: "pert_list.inp",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_direct_perturbation_command_file",
        lambda **kwargs: "run_create_perturbed_ace_file.csh",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.direct_perturbation_folder_check",
        lambda **kwargs: True,  # failure
    )

    calls = {"print": [], "remove": [], "rmtree": []}

    monkeypatch.setattr("os.getcwd", lambda: "cwd")
    monkeypatch.setattr("os.chdir", lambda p: None)
    monkeypatch.setattr("os.makedirs", lambda p: None)
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("os.remove", lambda p: calls["remove"].append(p))
    monkeypatch.setattr("shutil.rmtree", lambda p: calls["rmtree"].append(p))
    monkeypatch.setattr("os.path.exists", lambda p: True)
    monkeypatch.setattr(builtins, "print", lambda msg: calls["print"].append(msg))

    frendy_path = "/opt/frendy"

    result = generate_direct_perturbation_ace_files(
        frendy_Path=frendy_path,
        unperturbed_ACE_file_path="/data/U235.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        perturbation_coefficient=1.05,
        cleanup_Flag=True,
    )

    # Failure → function returns None
    assert result is None

    assert any("failed to generate" in msg for msg in calls["print"])


def test_generate_direct_perturbation_ace_files_no_cleanup(monkeypatch):
    """Ensure no cleanup occurs when cleanup_Flag=False."""

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_direct_perturbation_inputs",
        lambda **kwargs: (["line"], "input_folder"),
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_direct_perturbation_list",
        lambda **kwargs: "pert_list.inp",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_direct_perturbation_command_file",
        lambda **kwargs: "run_create_perturbed_ace_file.csh",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.direct_perturbation_folder_check",
        lambda **kwargs: False,
    )

    calls = {"remove": [], "rmtree": []}

    monkeypatch.setattr("os.getcwd", lambda: "cwd")
    monkeypatch.setattr("os.chdir", lambda p: None)
    monkeypatch.setattr("os.makedirs", lambda p: None)
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("os.remove", lambda p: calls["remove"].append(p))
    monkeypatch.setattr("shutil.rmtree", lambda p: calls["rmtree"].append(p))
    monkeypatch.setattr("os.path.exists", lambda p: True)
    monkeypatch.setattr(builtins, "print", lambda msg: None)

    frendy_path = "/opt/frendy"

    generate_direct_perturbation_ace_files(
        frendy_Path=frendy_path,
        unperturbed_ACE_file_path="/data/U235.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        perturbation_coefficient=1.05,
        cleanup_Flag=False,
    )

    # No cleanup should occur
    assert calls["remove"] == []
    assert calls["rmtree"] == []
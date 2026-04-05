import os
import pytest
from WINDIGO.frendy_main_functions import generate_random_sampling_ace_files


MODULE_PATH = "WINDIGO.frendy_main_functions"


@pytest.fixture
def mock_os(monkeypatch):
    """Mock os functions used in the function."""
    monkeypatch.setattr(os, "getcwd", lambda: "/start")
    monkeypatch.setattr(os, "chdir", lambda path: None)
    monkeypatch.setattr(os, "system", lambda cmd: 0)
    monkeypatch.setattr(os, "remove", lambda path: None)
    return os


@pytest.fixture
def mock_shutil(monkeypatch):
    """Mock shutil functions."""
    import shutil
    monkeypatch.setattr(shutil, "move", lambda src, dst: None)
    monkeypatch.setattr(shutil, "rmtree", lambda path: None)
    return shutil


@pytest.fixture
def mock_helpers(monkeypatch):
    """Mock all helper functions imported inside frendy_main_functions."""
    monkeypatch.setattr(
        f"{MODULE_PATH}.create_random_sampling_tool_execution_file",
        lambda **kwargs: "exec_tool.sh"
    )
    monkeypatch.setattr(
        f"{MODULE_PATH}.create_random_sampling_tool_inputs",
        lambda **kwargs: "inputs.txt"
    )
    monkeypatch.setattr(
        f"{MODULE_PATH}.generate_random_sampling_factors",
        lambda **kwargs: None
    )
    monkeypatch.setattr(
        f"{MODULE_PATH}.move_random_sampling_files",
        lambda **kwargs: "inputs_dir"
    )
    monkeypatch.setattr(
        f"{MODULE_PATH}.create_random_sampling_pert_list",
        lambda **kwargs: "pert_list.txt"
    )
    monkeypatch.setattr(
        f"{MODULE_PATH}.create_random_sampling_ace_directory",
        lambda **kwargs: "/ace_dir"
    )
    monkeypatch.setattr(
        f"{MODULE_PATH}.create_random_sampling_ace_execution_file",
        lambda **kwargs: "ace_exec.sh"
    )
    return monkeypatch


def test_covariance_matrix_moved(monkeypatch, mock_os, mock_shutil, mock_helpers):
    """Test that the covariance matrix is moved when not already in the tool directory."""
    moved = {}

    def fake_move(src, dst):
        moved["src"] = src
        moved["dst"] = dst

    monkeypatch.setattr(f"{MODULE_PATH}.shutil.move", fake_move)

    generate_random_sampling_ace_files(
        frendy_Path="/frendy",
        relative_covariance_matrix_path="cov.csv",
        unperturbed_ACE_file_path="ace.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        seed=1,
        sample_size=5,
        cleanup_Flag=False
    )

    assert moved["src"] == "cov.csv"
    assert moved["dst"] == "/frendy/tools/make_perturbation_factor/cov.csv"


def test_covariance_matrix_not_moved(monkeypatch, mock_os, mock_shutil, mock_helpers):
    """Test that covariance matrix is NOT moved when already in the tool directory."""
    moved = {"called": False}

    def fake_move(src, dst):
        moved["called"] = True

    monkeypatch.setattr(f"{MODULE_PATH}.shutil.move", fake_move)

    generate_random_sampling_ace_files(
        frendy_Path="/frendy",
        relative_covariance_matrix_path="/frendy/tools/make_perturbation_factor/cov.csv",
        unperturbed_ACE_file_path="ace.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        seed=1,
        sample_size=5,
        cleanup_Flag=False
    )

    assert moved["called"] is False


def test_successful_generation(monkeypatch, mock_os, mock_shutil, mock_helpers):
    """Test the successful path where no failures occur."""
    monkeypatch.setattr(
        f"{MODULE_PATH}.random_sampling_folder_check",
        lambda **kwargs: False  # no failures
    )

    result = generate_random_sampling_ace_files(
        frendy_Path="/frendy",
        relative_covariance_matrix_path="cov.csv",
        unperturbed_ACE_file_path="ace.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        seed=1,
        sample_size=5,
        cleanup_Flag=False
    )

    assert result == "/ace_dir"


def test_failure_path(monkeypatch, mock_os, mock_shutil, mock_helpers, capsys):
    """Test the failure branch where ACE files are not generated."""
    monkeypatch.setattr(
        f"{MODULE_PATH}.random_sampling_folder_check",
        lambda **kwargs: True  # failure
    )

    result = generate_random_sampling_ace_files(
        frendy_Path="/frendy",
        relative_covariance_matrix_path="cov.csv",
        unperturbed_ACE_file_path="ace.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        seed=1,
        sample_size=5,
        cleanup_Flag=False
    )

    captured = capsys.readouterr()
    assert "ACE files not generated successfully" in captured.out
    assert result is None


def test_cleanup(monkeypatch, mock_os, mock_shutil, mock_helpers):
    """Test that cleanup removes expected files and directories."""
    removed = []
    removed_dirs = []

    monkeypatch.setattr(os, "remove", lambda path: removed.append(path))
    monkeypatch.setattr(
        f"{MODULE_PATH}.shutil.rmtree",
        lambda path: removed_dirs.append(path)
    )
    monkeypatch.setattr(
        f"{MODULE_PATH}.random_sampling_folder_check",
        lambda **kwargs: False
    )

    generate_random_sampling_ace_files(
        frendy_Path="/frendy",
        relative_covariance_matrix_path="cov.csv",
        unperturbed_ACE_file_path="ace.ace",
        energy_grid=[1, 2, 3],
        mt_Number=102,
        nuclide="U235",
        seed=1,
        sample_size=5,
        cleanup_Flag=True
    )

    assert "pert_list.txt" in removed
    assert "ace_exec.sh" in removed
    assert "results.log" in removed
    assert "inputs_dir" in removed_dirs
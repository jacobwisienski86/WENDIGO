# tests/test_create_model_folders.py
# Tests for create_model_folders in openmc_internal_functions.py

import pytest

from src.WINDIGO.openmc_internal_functions import create_model_folders


def test_create_model_folders_basic(monkeypatch):
    """Test normal folder creation when top directory does not already exist."""

    calls = {
        "exists": [],
        "rmtree": [],
        "mkdir": [],
    }

    # Top directory does NOT exist
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.path.exists",
        lambda p: calls["exists"].append(p) or False,
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.shutil.rmtree",
        lambda p: calls["rmtree"].append(p),
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.mkdir",
        lambda p: calls["mkdir"].append(p),
    )

    top, folders = create_model_folders(
        directory_number=3,
        perturbed_nuclide="U235",
        model_name="TestModel",
        perturbation_type="Direct",
    )

    expected_top = "TestModel_U235_DirectPerturbedModels"
    expected_folders = [
        f"{expected_top}/Model_1_Folder",
        f"{expected_top}/Model_2_Folder",
        f"{expected_top}/Model_3_Folder",
    ]

    # Validate return values
    assert top == expected_top
    assert folders == expected_folders

    # Validate mkdir calls
    assert calls["mkdir"] == [expected_top] + expected_folders

    # No deletion should occur
    assert calls["rmtree"] == []


def test_create_model_folders_existing_directory(monkeypatch):
    """If the top directory exists, it should be removed before recreation."""

    calls = {
        "exists": [],
        "rmtree": [],
        "mkdir": [],
    }

    # Top directory DOES exist
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.path.exists",
        lambda p: calls["exists"].append(p) or True,
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.shutil.rmtree",
        lambda p: calls["rmtree"].append(p),
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.mkdir",
        lambda p: calls["mkdir"].append(p),
    )

    top, folders = create_model_folders(
        directory_number=2,
        perturbed_nuclide="H1",
        model_name="CoolModel",
        perturbation_type="Random",
    )

    expected_top = "CoolModel_H1_RandomPerturbedModels"
    expected_folders = [
        f"{expected_top}/Model_1_Folder",
        f"{expected_top}/Model_2_Folder",
    ]

    assert top == expected_top
    assert folders == expected_folders

    # Directory removal should occur
    assert calls["rmtree"] == [expected_top]

    # mkdir should be called for top + subfolders
    assert calls["mkdir"] == [expected_top] + expected_folders


def test_create_model_folders_zero(monkeypatch):
    """directory_number = 0 → only top directory created, no subfolders."""

    calls = {"mkdir": [], "exists": []}

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.path.exists",
        lambda p: calls["exists"].append(p) or False,
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.mkdir",
        lambda p: calls["mkdir"].append(p),
    )

    top, folders = create_model_folders(
        directory_number=0,
        perturbed_nuclide="Xe135",
        model_name="EmptyModel",
        perturbation_type="None",
    )

    expected_top = "EmptyModel_Xe135_NonePerturbedModels"

    assert top == expected_top
    assert folders == []  # no subfolders
    assert calls["mkdir"] == [expected_top]
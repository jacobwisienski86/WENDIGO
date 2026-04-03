# tests/test_build_perturbed_cross_sections_libraries.py
# Tests for build_perturbed_cross_sections_libraries in openmc_main_functions.py

import builtins
import pytest

from src.WINDIGO.openmc_main_functions import (
    build_perturbed_cross_sections_libraries,
)


def test_build_perturbed_cross_sections_libraries(monkeypatch):
    """Test full orchestration workflow for building perturbed XS libraries."""

    calls = {
        "count_directories": [],
        "create_numbers": [],
        "create_unperturbed_library": [],
        "create_model_folders": [],
        "create_perturbed_xml": [],
        "print": [],
    }

    # -----------------------------
    # Mock helper functions
    # -----------------------------
    monkeypatch.setattr(
        "src.WINDIGO.openmc_main_functions.count_directories",
        lambda perturbed_ACE_folder_path: (
            calls["count_directories"].append(perturbed_ACE_folder_path) or 3
        ),
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_main_functions.create_numbers",
        lambda directory_number: (
            calls["create_numbers"].append(directory_number) or
            ["0001", "0002", "0003"]
        ),
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_main_functions.create_unperturbed_library",
        lambda **kwargs: calls["create_unperturbed_library"].append(kwargs) or "UNPERT_LIB",
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_main_functions.create_model_folders",
        lambda **kwargs: (
            calls["create_model_folders"].append(kwargs) or
            ("TOP_DIR", ["TOP_DIR/Model_1_Folder", "TOP_DIR/Model_2_Folder", "TOP_DIR/Model_3_Folder"])
        ),
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_main_functions.create_perturbed_xml",
        lambda **kwargs: calls["create_perturbed_xml"].append(kwargs),
    )

    monkeypatch.setattr(
        builtins, "print",
        lambda msg: calls["print"].append(msg),
    )

    # -----------------------------
    # Inputs
    # -----------------------------
    unperturbed_nuclides = ["H1", "U235"]
    neutron_path = "/neutron"
    tsl_list = ["HH2O"]
    tsl_path = "/tsl"
    ace_path = "/ace"

    # -----------------------------
    # Run function
    # -----------------------------
    result = build_perturbed_cross_sections_libraries(
        unperturbed_nuclide_list=unperturbed_nuclides,
        neutron_sublibrary_path=neutron_path,
        unperturbed_TSL_list=tsl_list,
        thermal_scatter_sublibrary_path=tsl_path,
        perturbed_ACE_folder_path=ace_path,
        perturbed_nuclide="U235",
        model_name="CoolModel",
        perturbation_type="Direct",
    )

    # -----------------------------
    # Validate return value
    # -----------------------------
    assert result == "TOP_DIR"

    # -----------------------------
    # Validate helper calls
    # -----------------------------
    assert calls["count_directories"] == [ace_path]
    assert calls["create_numbers"] == [3]

    # create_unperturbed_library arguments
    unpert_lib_args = calls["create_unperturbed_library"][0]
    assert unpert_lib_args["neutron_sublibrary_path"] == neutron_path
    assert unpert_lib_args["unperturbed_nuclide_list"] == unperturbed_nuclides
    assert unpert_lib_args["unperturbed_TSL_list"] == tsl_list
    assert unpert_lib_args["thermal_scatter_sublibrary_path"] == tsl_path

    # create_model_folders arguments
    model_folder_args = calls["create_model_folders"][0]
    assert model_folder_args["directory_number"] == 3
    assert model_folder_args["perturbed_nuclide"] == "U235"
    assert model_folder_args["model_name"] == "CoolModel"
    assert model_folder_args["perturbation_type"] == "Direct"

    # create_perturbed_xml arguments
    pert_xml_args = calls["create_perturbed_xml"][0]
    assert pert_xml_args["unperturbed_library"] == "UNPERT_LIB"
    assert pert_xml_args["perturbed_ACE_folder_path"] == ace_path
    assert pert_xml_args["four_digit_numbers"] == ["0001", "0002", "0003"]
    assert pert_xml_args["perturbed_model_folder_list"] == [
        "TOP_DIR/Model_1_Folder",
        "TOP_DIR/Model_2_Folder",
        "TOP_DIR/Model_3_Folder",
    ]

    # -----------------------------
    # Validate printed output
    # -----------------------------
    assert any("All perturbed cross_sections.xml files created" in msg for msg in calls["print"])
# tests/test_create_unperturbed_library.py
# Tests for create_unperturbed_library in openmc_internal_functions.py

import pytest

from src.WINDIGO.openmc_internal_functions import create_unperturbed_library


class FakeLibrary:
    """Fake replacement for openmc.data.DataLibrary."""
    def __init__(self):
        self.registered = []

    def register_file(self, filename):
        self.registered.append(filename)


def test_create_unperturbed_library_basic(monkeypatch):
    """Test that matching .h5 files are registered correctly."""

    # -----------------------------
    # Fake directory contents
    # -----------------------------
    neutron_files = [
        "H1.h5",
        "U235.h5",
        "U235.txt",      # wrong extension
        "C12.h5",
    ]

    tsl_files = [
        "HH2O.h5",
        "graphite.h5",
        "HH2O.txt",      # wrong extension
    ]

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.listdir",
        lambda path: neutron_files if "neutron" in path else tsl_files,
    )

    # -----------------------------
    # Fake DataLibrary
    # -----------------------------
    fake_lib = FakeLibrary()
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.openmc.data.DataLibrary",
        lambda: fake_lib,
    )

    # -----------------------------
    # Inputs
    # -----------------------------
    neutron_path = "/data/neutron"
    tsl_path = "/data/tsl"

    unperturbed_nuclides = ["H1", "U235"]
    unperturbed_tsls = ["HH2O"]

    # -----------------------------
    # Run function
    # -----------------------------
    result = create_unperturbed_library(
        neutron_sublibrary_path=neutron_path,
        unperturbed_nuclide_list=unperturbed_nuclides,
        thermal_scatter_sublibrary_path=tsl_path,
        unperturbed_TSL_list=unperturbed_tsls,
    )

    # -----------------------------
    # Validate returned object
    # -----------------------------
    assert result is fake_lib

    # -----------------------------
    # Validate registered files
    # -----------------------------
    expected = [
        "/data/neutron/H1.h5",
        "/data/neutron/U235.h5",
        "/data/tsl/HH2O.h5",
    ]

    assert fake_lib.registered == expected


def test_create_unperturbed_library_no_matches(monkeypatch):
    """If no files match, nothing should be registered."""

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.listdir",
        lambda path: ["file1.txt", "file2.dat"],
    )

    fake_lib = FakeLibrary()
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.openmc.data.DataLibrary",
        lambda: fake_lib,
    )

    result = create_unperturbed_library(
        neutron_sublibrary_path="/neutron",
        unperturbed_nuclide_list=["H1"],
        thermal_scatter_sublibrary_path="/tsl",
        unperturbed_TSL_list=["HH2O"],
    )

    assert result is fake_lib
    assert fake_lib.registered == []


def test_create_unperturbed_library_multiple_matches(monkeypatch):
    """Ensure multiple matching files for a nuclide are all registered."""

    neutron_files = ["U235_1.h5", "U235_2.h5", "U235_extra.txt"]
    tsl_files = []

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.listdir",
        lambda path: neutron_files if "neutron" in path else tsl_files,
    )

    fake_lib = FakeLibrary()
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.openmc.data.DataLibrary",
        lambda: fake_lib,
    )

    result = create_unperturbed_library(
        neutron_sublibrary_path="/neutron",
        unperturbed_nuclide_list=["U235"],
        thermal_scatter_sublibrary_path="/tsl",
        unperturbed_TSL_list=[],
    )

    assert result is fake_lib
    assert fake_lib.registered == [
        "/neutron/U235_1.h5",
        "/neutron/U235_2.h5",
    ]
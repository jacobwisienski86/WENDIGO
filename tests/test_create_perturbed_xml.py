# tests/test_create_perturbed_xml.py
# Tests for create_perturbed_xml in openmc_internal_functions.py

import builtins
import pytest

from src.WINDIGO.openmc_internal_functions import create_perturbed_xml


class FakeLibrary:
    """Fake replacement for openmc.data.DataLibrary."""
    def __init__(self):
        self.registered = []
        self.exported = []

    def register_file(self, filename):
        self.registered.append(filename)

    def export_to_xml(self, filename):
        self.exported.append(filename)


class FakeIncidentNeutron:
    """Fake replacement for openmc.data.IncidentNeutron."""
    def __init__(self, path):
        self.path = path
        self.exported = []

    def export_to_hdf5(self, filename):
        self.exported.append(filename)


def test_create_perturbed_xml_basic(monkeypatch):
    """Test full workflow for multiple perturbed ACE folders."""

    # -----------------------------
    # Capture calls
    # -----------------------------
    calls = {
        "getcwd": [],
        "chdir": [],
        "listdir": [],
        "exists": [],
        "remove": [],
        "deepcopy": [],
        "from_ace": [],
    }

    # -----------------------------
    # Fake unperturbed library
    # -----------------------------
    fake_unperturbed = FakeLibrary()

    # -----------------------------
    # Mock os.getcwd / os.chdir
    # -----------------------------
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.getcwd",
        lambda: calls["getcwd"].append("cwd") or "cwd",
    )
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.chdir",
        lambda p: calls["chdir"].append(p),
    )

    # -----------------------------
    # Mock os.listdir for ACE folders
    # -----------------------------
    def fake_listdir(path):
        calls["listdir"].append(path)
        # Each folder contains one valid ACE file and some junk
        return ["xsdir", "junk.h5", "file.ace"]

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.listdir",
        fake_listdir,
    )

    # -----------------------------
    # Mock os.path.exists
    # -----------------------------
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.path.exists",
        lambda p: calls["exists"].append(p) or False,
    )

    # -----------------------------
    # Mock os.remove
    # -----------------------------
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.remove",
        lambda p: calls["remove"].append(p),
    )

    # -----------------------------
    # Mock copy.deepcopy
    # -----------------------------
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.copy.deepcopy",
        lambda obj: calls["deepcopy"].append(obj) or FakeLibrary(),
    )

    # -----------------------------
    # Mock openmc.data.IncidentNeutron.from_ace
    # -----------------------------
    def fake_from_ace(path):
        calls["from_ace"].append(str(path))
        return FakeIncidentNeutron(path)

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.openmc.data.IncidentNeutron.from_ace",
        fake_from_ace,
    )

    # -----------------------------
    # Mock Path
    # -----------------------------
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.Path",
        lambda p: p,
    )

    # -----------------------------
    # Inputs
    # -----------------------------
    perturbed_ACE_folder_path = "/ace"
    four_digit_numbers = ["0001", "0002"]
    perturbed_model_folder_list = ["/model/1", "/model/2"]

    # -----------------------------
    # Run function
    # -----------------------------
    create_perturbed_xml(
        unperturbed_library=fake_unperturbed,
        perturbed_ACE_folder_path=perturbed_ACE_folder_path,
        four_digit_numbers=four_digit_numbers,
        perturbed_model_folder_list=perturbed_model_folder_list,
    )

    # -----------------------------
    # Validate directory switching
    # -----------------------------
    assert calls["chdir"] == [
        "/model/1",
        "cwd",
        "/model/2",
        "cwd",
    ]

    # -----------------------------
    # Validate ACE file selection
    # -----------------------------
    assert calls["listdir"] == [
        "/ace/0001",
        "/ace/0002",
    ]

    # -----------------------------
    # Validate deepcopy called twice
    # -----------------------------
    assert len(calls["deepcopy"]) == 2

    # -----------------------------
    # Validate from_ace calls
    # -----------------------------
    assert calls["from_ace"] == [
        "/ace/0001/file.ace",
        "/ace/0002/file.ace",
    ]

    # -----------------------------
    # Validate no .h5 removal (exists=False)
    # -----------------------------
    assert calls["remove"] == []


def test_create_perturbed_xml_existing_h5(monkeypatch):
    """If .h5 exists, it should be removed before writing."""

    calls = {"exists": [], "remove": []}

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.getcwd",
        lambda: "cwd",
    )
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.chdir",
        lambda p: None,
    )
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.listdir",
        lambda p: ["file.ace"],
    )

    # .h5 exists → should be removed
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.path.exists",
        lambda p: calls["exists"].append(p) or True,
    )
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.os.remove",
        lambda p: calls["remove"].append(p),
    )

    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.copy.deepcopy",
        lambda obj: FakeLibrary(),
    )
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.openmc.data.IncidentNeutron.from_ace",
        lambda p: FakeIncidentNeutron(p),
    )
    monkeypatch.setattr(
        "src.WINDIGO.openmc_internal_functions.Path",
        lambda p: p,
    )

    create_perturbed_xml(
        unperturbed_library=FakeLibrary(),
        perturbed_ACE_folder_path="/ace",
        four_digit_numbers=["0001"],
        perturbed_model_folder_list=["/model/1"],
    )

    # Validate .h5 removal
    assert calls["remove"] == ["/ace/0001/file.ace.h5"]
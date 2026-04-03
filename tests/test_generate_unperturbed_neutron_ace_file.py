# tests/test_generate_unperturbed_neutron_ace_file.py
# Tests for the main function: generate_unperturbed_neutron_ace_file

import builtins
import pytest

from src.WINDIGO.frendy_main_functions import (
    generate_unperturbed_neutron_ace_file,
)


def test_generate_unperturbed_neutron_ace_file_basic(monkeypatch):
    """Test the normal (non-upgrade) workflow with cleanup enabled."""

    # --- Mock internal helper functions ---
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.format_endf_evaluation",
        lambda endf_Path: "formatted.dat",
    )

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_unperturbed_ace_generation_input",
        lambda **kwargs: "ace_input.inp",
    )

    # --- Mock OS functions ---
    calls = {
        "getcwd": [],
        "chdir": [],
        "system": [],
        "remove": [],
        "exists": [],
        "print": [],
    }

    monkeypatch.setattr("os.getcwd", lambda: calls["getcwd"].append("cwd") or "cwd")
    monkeypatch.setattr("os.chdir", lambda path: calls["chdir"].append(path))
    monkeypatch.setattr("os.system", lambda cmd: calls["system"].append(cmd))
    monkeypatch.setattr("os.remove", lambda p: calls["remove"].append(p))
    monkeypatch.setattr("os.path.exists", lambda p: calls["exists"].append(p) or True)
    monkeypatch.setattr(builtins, "print", lambda msg: calls["print"].append(msg))

    # --- Run function ---
    frendy_path = "/opt/frendy"
    result = generate_unperturbed_neutron_ace_file(
        frendy_Path=frendy_path,
        endf_Path="/data/U235.endf",
        temperature=300,
        nuclide="U235",
        upgrade_Flag=False,
        energy_grid=[1, 2, 3],
        cleanup_Flag=True,
    )

    # --- Expected output path ---
    expected_exe_dir = "/opt/frendy/frendy/main"
    expected_output = f"{expected_exe_dir}/U235.ace"

    assert result == expected_output

    # --- Check directory switching ---
    assert calls["chdir"] == [
        expected_exe_dir,  # enter FRENDY executable directory
        "cwd",             # return to original directory
    ]

    # --- Check system call ---
    assert calls["system"] == ["./frendy.exe ace_input.inp"]

    # --- Check cleanup of intermediate files ---
    assert "formatted.dat" in calls["remove"]
    assert "ace_input.inp" in calls["remove"]

    # --- Check cleanup of .ace.ace.dir ---
    assert f"{expected_exe_dir}/U235.ace.ace.dir" in calls["remove"]

    # --- Check success print messages ---
    assert "\n" in calls["print"]
    assert any("ACE file successfully generated" in msg for msg in calls["print"])


def test_generate_unperturbed_neutron_ace_file_upgrade(monkeypatch):
    """Test upgrade mode, ensuring upgraded filename and cleanup behavior."""

    # Mock helpers
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.format_endf_evaluation",
        lambda endf_Path: "formatted.dat",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_unperturbed_ace_generation_input",
        lambda **kwargs: "ace_input.inp",
    )

    # Mock OS
    calls = {"remove": [], "exists": [], "print": []}

    monkeypatch.setattr("os.getcwd", lambda: "cwd")
    monkeypatch.setattr("os.chdir", lambda p: None)
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("os.remove", lambda p: calls["remove"].append(p))
    monkeypatch.setattr("os.path.exists", lambda p: calls["exists"].append(p) or True)
    monkeypatch.setattr(builtins, "print", lambda msg: calls["print"].append(msg))

    frendy_path = "/opt/frendy"
    result = generate_unperturbed_neutron_ace_file(
        frendy_Path=frendy_path,
        endf_Path="/data/U235.endf",
        temperature=300,
        nuclide="U235",
        upgrade_Flag=True,
        energy_grid=[1, 2, 3],
        cleanup_Flag=True,
    )

    expected_exe_dir = "/opt/frendy/frendy/main"
    expected_output = f"{expected_exe_dir}/U235_upgrade.ace"

    assert result == expected_output

    # Check cleanup of upgraded .ace.ace.dir
    assert f"{expected_exe_dir}/U235_upgrade.ace.ace.dir" in calls["remove"]


def test_generate_unperturbed_neutron_ace_file_no_cleanup(monkeypatch):
    """Ensure no cleanup occurs when cleanup_Flag=False."""

    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.format_endf_evaluation",
        lambda endf_Path: "formatted.dat",
    )
    monkeypatch.setattr(
        "src.WINDIGO.frendy_main_functions.create_unperturbed_ace_generation_input",
        lambda **kwargs: "ace_input.inp",
    )

    calls = {"remove": []}

    monkeypatch.setattr("os.getcwd", lambda: "cwd")
    monkeypatch.setattr("os.chdir", lambda p: None)
    monkeypatch.setattr("os.system", lambda cmd: None)
    monkeypatch.setattr("os.remove", lambda p: calls["remove"].append(p))
    monkeypatch.setattr("os.path.exists", lambda p: True)
    monkeypatch.setattr(builtins, "print", lambda msg: None)

    frendy_path = "/opt/frendy"
    generate_unperturbed_neutron_ace_file(
        frendy_Path=frendy_path,
        endf_Path="/data/U235.endf",
        temperature=300,
        nuclide="U235",
        upgrade_Flag=False,
        energy_grid=[1, 2, 3],
        cleanup_Flag=False,
    )

    # No cleanup should occur
    assert calls["remove"] == []
# tests/test_create_direct_perturbation_command_file.py
# Tests for the function: create_direct_perturbation_command_file

import builtins
import pytest

from src.WINDIGO.frendy_internal_functions import (
    create_direct_perturbation_command_file,
)


def test_create_direct_perturbation_command_file(monkeypatch):
    """Test that the .csh command file is created with correct contents."""

    written_path = None
    written_lines = []

    class FakeFile:
        def __init__(self, path, mode):
            nonlocal written_path
            written_path = path

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def writelines(self, lines):
            written_lines.extend(lines)

        def close(self):
            pass

    # Patch builtins.open globally
    monkeypatch.setattr(builtins, "open", lambda p, m: FakeFile(p, m))

    frendy_path = "/opt/frendy"
    list_file = "perturb_list.inp"
    ace_file = "/data/U235.ace"

    result = create_direct_perturbation_command_file(
        frendy_Path=frendy_path,
        perturbation_list_filename=list_file,
        unperturbed_ACE_file_path=ace_file,
    )

    expected_filename = "run_create_perturbed_ace_file.csh"
    assert result == expected_filename
    assert written_path == expected_filename

    # Build expected lines
    expected_lines = [
        "#!/bin/csh\n",
        "\n",
        f"set EXE     = {frendy_path}/tools/perturbation_ace_file/perturbation_ace_file.exe",
        "\n",
        f"set INP     = {list_file}",
        "\n",
        f"set ACE     = {ace_file}",
        "\n",
        "set LOG = results.log\n",
        'echo "${EXE}  ${ACE}  ${INP}"      > ${LOG}\n',
        'echo ""                           >> ${LOG}\n',
        '${EXE}  ${ACE}  ${INP} >> ${LOG}\n',
    ]

    assert written_lines == expected_lines
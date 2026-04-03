# tests/test_create_random_sampling_ace_execution_file.py
# Tests for the function: create_random_sampling_ace_execution_file

import builtins
import pytest

from src.WINDIGO.frendy_internal_functions import (
    create_random_sampling_ace_execution_file,
)


def test_create_random_sampling_ace_execution_file(monkeypatch):
    """Test that the .csh execution file is created with correct contents."""

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
    ace_dir = "/opt/frendy/U235_RandomSamplingACEFiles_ReactionMT_102"
    nuclide = "U235"
    mt = 102
    unperturbed_ace = "/data/U235.ace"

    result = create_random_sampling_ace_execution_file(
        frendy_Path=frendy_path,
        ace_files_directory=ace_dir,
        nuclide=nuclide,
        mt_Number=mt,
        unperturbed_ACE_file_path=unperturbed_ace,
    )

    expected_filename = "run_create_perturbed_ace_file.csh"
    assert result == expected_filename
    assert written_path == expected_filename

    expected_lines = [
        "#!/bin/csh\n",
        "\n",
        f"set EXE     = {frendy_path}/tools/perturbation_ace_file/perturbation_ace_file.exe",
        "\n",
        f"set INP     = {ace_dir}/perturbation_list_{nuclide}_MT_{mt}.inp",
        "\n",
        f"set ACE     = {unperturbed_ace}",
        "\n",
        "set LOG = results.log\n",
        'echo "${EXE}  ${ACE}  ${INP}"      > ${LOG}\n',
        'echo ""                           >> ${LOG}\n',
        '${EXE}  ${ACE}  ${INP} >> ${LOG}\n',
    ]

    assert written_lines == expected_lines
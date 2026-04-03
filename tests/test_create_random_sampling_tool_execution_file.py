# tests/test_create_random_sampling_tool_execution_file.py
# Tests for the function: create_random_sampling_tool_execution_file

import builtins
import pytest

from src.WINDIGO.frendy_internal_functions import (
    create_random_sampling_tool_execution_file,
)


def test_create_random_sampling_tool_execution_file(monkeypatch):
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

    exe_dir = "/opt/frendy/tools/random"
    tool_dir = "/opt/frendy/tools/random"

    result = create_random_sampling_tool_execution_file(
        executable_directory=exe_dir,
        random_sampling_tool_directory=tool_dir,
    )

    expected_filename = "run_make_perturbation_factor.csh"
    assert result == expected_filename
    assert written_path == expected_filename

    # Build expected lines
    expected_lines = [
        "#!/bin/csh\n",
        "\n",
        f"set EXE     = {exe_dir}\n",
        "\n",
        f"set INP        = {tool_dir}/sample_copy.inp",
        "\n",
        "\n",
        "set LOG = result.log\n",
        'echo "${EXE}  ${INP}"      > ${LOG}\n',
        'echo ""                   >> ${LOG}\n',
        '${EXE}  ${INP} >> ${LOG}\n',
    ]

    assert written_lines == expected_lines
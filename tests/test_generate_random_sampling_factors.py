# tests/test_generate_random_sampling_factors.py
# Tests for the function: generate_random_sampling_factors

import builtins
import pytest

from src.WINDIGO.frendy_internal_functions import generate_random_sampling_factors


def test_generate_random_sampling_factors_success_no_cleanup(monkeypatch):
    """Test successful creation message and no cleanup when cleanup_Flag=False."""

    # Capture os.system calls
    system_calls = []
    monkeypatch.setattr("os.system", lambda cmd: system_calls.append(cmd))

    # Simulate folder exists → success
    monkeypatch.setattr("os.path.exists", lambda path: True)

    # Capture printed messages
    printed = []
    monkeypatch.setattr(builtins, "print", lambda msg: printed.append(msg))

    # Track os.remove calls
    removed = []
    monkeypatch.setattr("os.remove", lambda p: removed.append(p))

    generate_random_sampling_factors(
        execution_filename="run_tool.csh",
        random_sampling_tool_directory="/tmp/tool",
        nuclide="U235",
        sample_filename="sample_copy.inp",
        cleanup_Flag=False,
    )

    # os.system should be called with correct command
    assert system_calls == ["csh ./run_tool.csh"]

    # Success message should be printed
    assert printed == ["Perturbation factors created successfully"]

    # No cleanup should occur
    assert removed == []


def test_generate_random_sampling_factors_failure_no_cleanup(monkeypatch):
    """Test failure message when folder does not exist."""

    system_calls = []
    monkeypatch.setattr("os.system", lambda cmd: system_calls.append(cmd))

    # Simulate folder missing → failure
    monkeypatch.setattr("os.path.exists", lambda path: False)

    printed = []
    monkeypatch.setattr(builtins, "print", lambda msg: printed.append(msg))

    removed = []
    monkeypatch.setattr("os.remove", lambda p: removed.append(p))

    generate_random_sampling_factors(
        execution_filename="run_tool.csh",
        random_sampling_tool_directory="/tmp/tool",
        nuclide="Xe135",
        sample_filename="sample_copy.inp",
        cleanup_Flag=False,
    )

    assert printed == ["Perturbation factors not created successfully"]
    assert removed == []


def test_generate_random_sampling_factors_cleanup(monkeypatch):
    """Test that cleanup removes both sample and execution files."""

    system_calls = []
    monkeypatch.setattr("os.system", lambda cmd: system_calls.append(cmd))

    # Simulate success
    monkeypatch.setattr("os.path.exists", lambda path: True)

    printed = []
    monkeypatch.setattr(builtins, "print", lambda msg: printed.append(msg))

    removed = []
    monkeypatch.setattr("os.remove", lambda p: removed.append(p))

    generate_random_sampling_factors(
        execution_filename="run_tool.csh",
        random_sampling_tool_directory="/tmp/tool",
        nuclide="Mo95",
        sample_filename="sample_copy.inp",
        cleanup_Flag=True,
    )

    # Both files should be removed
    assert removed == ["sample_copy.inp", "run_tool.csh"]
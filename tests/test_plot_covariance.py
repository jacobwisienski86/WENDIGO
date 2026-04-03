# tests/test_plot_covariance.py
# Tests for plot_covariance in sandy_internal_functions.py

import builtins
import pytest

from src.WINDIGO.sandy_internal_functions import plot_covariance


def test_plot_covariance(monkeypatch):
    """Test that the covariance plot is generated and saved with correct filename."""

    # -----------------------------
    # Mock matplotlib and seaborn
    # -----------------------------
    class FakeFig:
        def tight_layout(self):
            pass

    class FakeAx:
        def set_aspect(self, arg):
            pass

    fake_fig = FakeFig()
    fake_ax = FakeAx()

    # Capture calls
    calls = {
        "subplots": [],
        "heatmap": [],
        "savefig": [],
        "print": [],
    }

    monkeypatch.setattr(
        "src.WINDIGO.sandy_internal_functions.plt.subplots",
        lambda figsize, dpi: calls["subplots"].append((figsize, dpi)) or (fake_fig, fake_ax),
    )

    monkeypatch.setattr(
        "src.WINDIGO.sandy_internal_functions.sns.heatmap",
        lambda data, cmap: calls["heatmap"].append((data, cmap)),
    )

    monkeypatch.setattr(
        "src.WINDIGO.sandy_internal_functions.plt.savefig",
        lambda filename, bbox_inches: calls["savefig"].append((filename, bbox_inches)),
    )

    monkeypatch.setattr(
        builtins, "print",
        lambda msg: calls["print"].append(msg),
    )

    # -----------------------------
    # Test inputs
    # -----------------------------
    covariance_data = [[1, 2], [3, 4]]
    energy_grid = [1, 2, 3, 4]
    nuclide = "U235"
    mt = 102
    flag = "Absolute"

    # -----------------------------
    # Run function
    # -----------------------------
    result = plot_covariance(
        covariance_data=covariance_data,
        energy_grid=energy_grid,
        nuclide=nuclide,
        mt_Number=mt,
        flag_String=flag,
    )

    expected_filename = "covariancePlot_4Groups_U235MT102_Absolute.png"

    # -----------------------------
    # Validate filename
    # -----------------------------
    assert result == expected_filename

    # -----------------------------
    # Validate heatmap call
    # -----------------------------
    assert calls["heatmap"] == [ (covariance_data, "bwr") ]

    # -----------------------------
    # Validate savefig call
    # -----------------------------
    assert calls["savefig"] == [
        (expected_filename, "tight")
    ]

    # -----------------------------
    # Validate printed output
    # -----------------------------
    assert any(expected_filename in msg for msg in calls["print"])
# tests/test_save_covariance_file.py
# Tests for save_covariance_file in sandy_internal_functions.py

import builtins
import pytest

from src.WINDIGO.sandy_internal_functions import save_covariance_file


def test_save_covariance_file(monkeypatch):
    """Test that covariance data is saved, reloaded, saved again, and cleaned up."""

    # -----------------------------
    # Capture calls
    # -----------------------------
    calls = {
        "cov_to_csv": [],
        "pd_read_csv": [],
        "df_to_csv": [],
        "remove": [],
        "print": [],
    }

    # -----------------------------
    # Mock covariance_data.to_csv
    # -----------------------------
    class FakeCovariance:
        def to_csv(self, filename, index):
            calls["cov_to_csv"].append((filename, index))

    covariance_data = FakeCovariance()

    # -----------------------------
    # Mock pandas.read_csv
    # -----------------------------
    class FakeDF:
        def to_csv(self, filename, index, header):
            calls["df_to_csv"].append((filename, index, header))

    monkeypatch.setattr(
        "src.WINDIGO.sandy_internal_functions.pd.read_csv",
        lambda filename, skiprows: calls["pd_read_csv"].append((filename, skiprows)) or FakeDF(),
    )

    # -----------------------------
    # Mock os.remove
    # -----------------------------
    monkeypatch.setattr(
        "src.WINDIGO.sandy_internal_functions.os.remove",
        lambda filename: calls["remove"].append(filename),
    )

    # -----------------------------
    # Mock print
    # -----------------------------
    monkeypatch.setattr(
        builtins, "print",
        lambda msg: calls["print"].append(msg),
    )

    # -----------------------------
    # Inputs
    # -----------------------------
    energy_grid = [1, 2, 3, 4]
    nuclide = "U235"
    mt = 102
    flag = "Relative"

    # -----------------------------
    # Run function
    # -----------------------------
    result = save_covariance_file(
        covariance_data=covariance_data,
        energy_grid=energy_grid,
        nuclide=nuclide,
        mt_Number=mt,
        flag_String=flag,
    )

    expected_filename = "covarianceMatrix_4Groups_U235_MT_102_Relative.csv"

    # -----------------------------
    # Validate return value
    # -----------------------------
    assert result == expected_filename

    # -----------------------------
    # Validate first write (intermediate)
    # -----------------------------
    assert calls["cov_to_csv"] == [
        ("intermediate_dataframe.csv", False)
    ]

    # -----------------------------
    # Validate read_csv
    # -----------------------------
    assert calls["pd_read_csv"] == [
        ("intermediate_dataframe.csv", 2)
    ]

    # -----------------------------
    # Validate second write (final CSV)
    # -----------------------------
    assert calls["df_to_csv"] == [
        (expected_filename, False, False)
    ]

    # -----------------------------
    # Validate cleanup
    # -----------------------------
    assert calls["remove"] == ["intermediate_dataframe.csv"]

    # -----------------------------
    # Validate printed output
    # -----------------------------
    assert any(expected_filename in msg for msg in calls["print"])
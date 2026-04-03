# tests/test_retrieve_nuclide_information.py
# Tests for retrieve_nuclide_information in sandy_internal_functions.py

import pytest

from src.WINDIGO.sandy_internal_functions import retrieve_nuclide_information


def test_retrieve_nuclide_information_valid(monkeypatch):
    """Test correct parsing and ZZZAAA computation for valid nuclides."""

    # Mock the nuclide_ZZZs lookup table INSIDE the module under test
    monkeypatch.setattr(
        "src.WINDIGO.sandy_internal_functions.nuclide_ZZZs",
        {"H": 1, "U": 92, "Mo": 42},
    )

    # H1 → Z=1, A=1 → 10000*1 + 10*1 = 10010
    assert retrieve_nuclide_information("H1") == 10010

    # U235 → Z=92, A=235 → 10000*92 + 10*235 = 922350
    assert retrieve_nuclide_information("U235") == 922350

    # Mo98 → Z=42, A=98 → 10000*42 + 10*98 = 420980
    assert retrieve_nuclide_information("Mo98") == 420980


def test_retrieve_nuclide_information_invalid_mass(monkeypatch):
    """Mass number must be convertible to int; otherwise ValueError is raised."""

    monkeypatch.setattr(
        "src.WINDIGO.sandy_internal_functions.nuclide_ZZZs",
        {"X": 99},
    )

    with pytest.raises(ValueError):
        retrieve_nuclide_information("Xabc")  # "abc" cannot convert to int


def test_retrieve_nuclide_information_two_letter_symbol(monkeypatch):
    """Ensure two-letter element symbols are parsed correctly."""

    monkeypatch.setattr(
        "src.WINDIGO.sandy_internal_functions.nuclide_ZZZs",
        {"Na": 11},
    )

    # Na23 → Z=11, A=23 → 10000*11 + 10*23 = 110230
    assert retrieve_nuclide_information("Na23") == 110230
from src.etl.normaliser import normalize_year


def test_fy():
    assert normalize_year("FY2024") == 2024


def test_mar():
    assert normalize_year("Mar 2023") == 2023


def test_range():
    assert normalize_year("2023-24") == 2024


def test_number():
    assert normalize_year(2022) == 2022


def test_none():
    assert normalize_year(None) is None
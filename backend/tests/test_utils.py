from backend.modules.utils import validate_amount

def test_validate_amount_positive():
    assert validate_amount(100.5) is True

def test_validate_amount_zero():
    assert validate_amount(0) is False

def test_validate_amount_negative():
    assert validate_amount(-10) is False
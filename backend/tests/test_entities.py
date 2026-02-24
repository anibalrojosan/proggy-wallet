import pytest

from backend.modules.entities import Account


def test_account_initialization():
    """
    Verify that the account is initialized with the correct username and balance.
    """
    account = Account(owner_username="anibal", balance=100.0)
    assert account.owner_username == "anibal"
    assert account.balance == 100.0  # Use the @property balance

def test_account_default_balance():
    """Verify that the default balance is 0.0 if no balance is provided."""
    account = Account(owner_username="test_user")
    assert account.balance == 0.0

def test_add_funds_success():
    """Verify that add_funds increases the balance correctly."""
    account = Account(owner_username="anibal", balance=50.0)
    new_balance = account.add_funds(25.0)
    assert new_balance == 75.0
    assert account.balance == 75.0

def test_add_funds_invalid_amount():
    """Verify that add_funds raises ValueError if the amount is not positive."""
    account = Account(owner_username="anibal", balance=50.0)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.add_funds(0)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.add_funds(-10.0)

def test_remove_funds_success():
    """Verify that remove_funds decreases the balance correctly."""
    account = Account(owner_username="anibal", balance=100.0)
    new_balance = account.remove_funds(40.0)
    assert new_balance == 60.0
    assert account.balance == 60.0

def test_remove_funds_insufficient_funds():
    """Verify that remove_funds raises ValueError if the amount is more than the balance."""
    account = Account(owner_username="anibal", balance=50.0)
    # Match with the expected message: "Insufficient funds. Current balance: ..."
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.remove_funds(50.01)

def test_remove_funds_invalid_amount():
    """Verify that remove_funds raises ValueError if the amount is not positive."""
    account = Account(owner_username="anibal", balance=100.0)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.remove_funds(0)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.remove_funds(-5.0)

def test_account_repr():
    """Verify that the string representation of the account is the expected one."""
    account = Account(owner_username="anibal", balance=150.0)
    assert repr(account) == "Account(owner='anibal', balance=150.0)"

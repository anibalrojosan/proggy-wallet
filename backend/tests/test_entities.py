import pytest

from backend.modules.entities import Account, User
from backend.modules.models import UserInDB


# ------------- 'Account' entity tests -------------
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


# ------------- 'User' entity tests -------------
def test_user_initialization():
    """
    Verify that a User is created correctly from a UserInDB model
    and that it initializes its associated Account.
    """
    user_model = UserInDB(
        username="anibal",
        email="anibal@example.com",
        password="hashed_password_123",
        balance=500.0
    )
    user = User(user_model)

    assert user.username == "anibal"
    assert user.email == "anibal@example.com"
    assert user.hashed_password == "hashed_password_123"
    # Verify that the account was created with the correct balance
    assert isinstance(user.account, Account)
    assert user.account.balance == 500.0
    assert user.account.owner_username == "anibal"

def test_user_password_hashing_and_verification():
    """
    Verify that the password hashing and verification process works correctly using bcrypt.
    """
    password = "mi_password_secreto"
    hashed = User.hash_password(password)

    # The hash should not be equal to the plain text password
    assert hashed != password

    # Create a user with that hash
    user_model = UserInDB(
        username="anibal",
        email="anibal@example.com",
        password=hashed,
        balance=0.0
    )
    user = User(user_model)

    # Verify correct password
    assert user.check_password(password) is True
    # Verify incorrect password
    assert user.check_password("otra_cosa") is False

def test_user_update_email():
    """Verify that the update_email method works correctly."""
    user_model = UserInDB(
        username="anibal",
        email="viejo@example.com",
        password="hash",
        balance=0.0
    )
    user = User(user_model)
    user.update_email("nuevo@example.com")
    assert user.email == "nuevo@example.com"

def test_user_repr():
    """Verify that the string representation of the user is the expected one."""
    user_model = UserInDB(
        username="anibal",
        email="anibal@example.com",
        password="hash",
        balance=0.0
    )
    user = User(user_model)
    assert repr(user) == "User(username='anibal', email='anibal@example.com')"

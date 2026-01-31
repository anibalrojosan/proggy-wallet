import pytest

from backend.modules import auth

MOCK_USERS = [
    {"username": "test_user", "password": "correct_password", "balance": 1000},
    {"username": "other_user", "password": "other_password", "balance": 500},
]


# Fixture to replace the real load_users function with mock data. The replacement of load_users must recieve
# nothing (a lambda function) and return a list of users just as the original function does
@pytest.fixture
def mock_load_users(monkeypatch):
    monkeypatch.setattr(auth, "load_users", lambda: MOCK_USERS)
    return lambda: MOCK_USERS


def test_get_user_exists(mock_load_users):
    """Test that the get_user function returns the correct user if it exists"""
    user = auth.get_user("test_user")
    assert user is not None
    assert user["username"] == "test_user"
    assert user["balance"] == 1000


def test_get_user_not_exists(mock_load_users):
    """Test that the get_user function returns None if the user does not exist"""
    user = auth.get_user("non_existent")
    assert user is None


def test_validate_credentials_success(mock_load_users):
    """Test that the validate_credentials function returns True if the credentials are correct"""
    result = auth.validate_credentials("test_user", "correct_password")
    assert result is True


def test_validate_credentials_wrong_password(mock_load_users):
    """Test that the validate_credentials function returns False if the password is incorrect"""
    result = auth.validate_credentials("test_user", "other_password")
    assert result is False


def test_validate_credentials_wrong_user(mock_load_users):
    """Test that the validate_credentials function returns False if the user does not exist"""
    result = auth.validate_credentials("non_existent", "any_password")
    assert result is False

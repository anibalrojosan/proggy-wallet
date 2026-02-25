from unittest.mock import patch

import pytest

from backend.modules.auth import AuthService
from backend.modules.entities import User
from backend.modules.models import UserInDB


@pytest.fixture
def mock_user_db():
    """Create a simulated user model as the one that would come from the DB."""
    hashed_password = User.hash_password("password123")
    return UserInDB(
        username="anibal",
        email="anibal@example.com",
        password=hashed_password,
        balance=100.0
    )

# 1. Test of Successful Login
def test_authenticate_success(mock_user_db):
    """Verify that the login works with correct credentials."""
    # Intercept the call to the repository where it is used (in auth module)
    with patch("backend.modules.auth.get_user_by_username") as mock_get_user:
        mock_get_user.return_value = mock_user_db

        # Try to authenticate
        user = AuthService.authenticate("anibal", "password123")

        assert user is not None
        assert user.username == "anibal"
        mock_get_user.assert_called_once_with("anibal")

# 2. Test of Failed Login (Wrong Password)
def test_authenticate_wrong_password(mock_user_db):
    """Verify that the login fails if the password does not match."""
    with patch("backend.modules.auth.get_user_by_username") as mock_get_user:
        mock_get_user.return_value = mock_user_db

        user = AuthService.authenticate("anibal", "wrong_password")

        assert user is None

# 3. Test of Failed Login (User not found)
def test_authenticate_user_not_found():
    """Verify that the login fails if the user is not in the DB."""
    with patch("backend.modules.auth.get_user_by_username") as mock_get_user:
        mock_get_user.return_value = None # The repository does not find anything

        user = AuthService.authenticate("desconocido", "password123")

        assert user is None

# 4. Test of Getting User Entity
def test_get_user_entity_success(mock_user_db):
    """Verify that a complete User object can be obtained from the DB."""
    with patch("backend.modules.auth.get_user_by_username") as mock_get_user:
        mock_get_user.return_value = mock_user_db

        user_entity = AuthService.get_user_entity("anibal")

        assert isinstance(user_entity, User)
        assert user_entity.account.balance == 100.0

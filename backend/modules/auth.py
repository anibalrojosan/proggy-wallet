"""
Authentication Service.
Handles user login and credential validation using the database repository.
"""

from backend.database.repository import get_user_by_username
from backend.modules.entities import User


class AuthService:
    @staticmethod
    def authenticate(username: str, password: str) -> User | None:
        """
        Authenticate a user by checking credentials against the database.

        Args:
            username: The username to check.
            password: The plain-text password to validate.
        Returns:
            A User entity object if successful, None otherwise.
        """
        # 1. Get the user from the database through the repository
        user_data = get_user_by_username(username)

        if not user_data:
            return None

        # 2. Convert the data (UserInDB) into a User entity
        # This allows us to use the check_password method of the entity
        user_entity = User(user_data)

        # 3. Validate the password using the bcrypt logic encapsulated in User
        if user_entity.check_password(password):
            return user_entity

        return None

    @staticmethod
    def get_user_entity(username: str) -> User | None:
        """
        Helper to get a full User entity object from a username.
        """
        user_data = get_user_by_username(username)
        if user_data:
            return User(user_data)
        return None


def validate_credentials(username, password):
    user = AuthService.authenticate(username, password)
    return user is not None

def get_user(username):
    # Retorna el modelo UserInDB para mantener compatibilidad con código antiguo
    return get_user_by_username(username)

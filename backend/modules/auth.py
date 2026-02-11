"""
User authentication service for credential validation and user management.
This service is responsible for:
- Loading user data from the JSON file
- Validating credentials using the models
- Returning a UserEntity object
"""
import json

from backend.modules.entities import User as UserEntity
from backend.modules.models import UserInDB

# Archivo de persistencia
USERS_FILE = "backend/data/users.json"

class AuthService:
    """Service responsible for authentication logic and user management."""

    @staticmethod
    def _load_users_data() -> list[dict]:
        """Private method to load raw data from the JSON file."""
        try:
            with open(USERS_FILE, encoding="utf-8") as f:
                data = json.load(f)
                return data.get("users", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @classmethod
    def get_user_entity(cls, username: str) -> UserEntity | None:
        """Find a user and return it as a business entity (UserEntity)."""
        users = cls._load_users_data()
        for user_dict in users:
            if user_dict.get("username") == username:
                # Validate the dictionary with the Pydantic model
                user_model = UserInDB(**user_dict)
                # Return the business entity that wraps the model
                return UserEntity(user_model)
        return None

    @classmethod
    def authenticate(cls, username: str, password: str) -> UserEntity | None:
        """Validate credentials and return the entity if successful."""
        user_entity = cls.get_user_entity(username)

        if not user_entity:
            return None

        # Use the check_password method implemented in UserEntity
        if user_entity.check_password(password):
            return user_entity

        return None

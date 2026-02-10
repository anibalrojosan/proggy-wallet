"""User authentication module for credential validation and user management."""

from backend.modules import utils
from backend.modules.models import User

# Path to users JSON file
USERS_FILE = "backend/data/users.json"


def load_users() -> list[dict]:
    """Load all users from JSON file.

    Returns:
        List of user dictionaries. Empty list if no users found.

    Raises:
        FileNotFoundError: If the users.json file doesn't exist.
    """
    try:
        data = utils.read_json_file(USERS_FILE)
        return data.get("users", [])
    except FileNotFoundError:
        return []


def get_user(username: str) -> User | None:
    """Get user data by username.

    Args:
        username: The username to search for.

    Returns:
        User object if found, None otherwise.
    """
    users = load_users()

    for user_dict in users:
        if user_dict.get("username") == username:
            # Pydantic validates the dictionary and converts it to a User object
            return User(**user_dict)

    return None


def validate_credentials(username: str, password: str) -> bool:
    """Validate login credentials.

    Args:
        username: The username to validate.
        password: The password to validate.

    Returns:
        True if credentials are valid, False otherwise.
    """
    # We need to load raw data for validation because our User model
    # doesn't include the password field for security.
    users = load_users()
    for user_dict in users:
        if user_dict.get("username") == username:
            return user_dict.get("password") == password

    return False

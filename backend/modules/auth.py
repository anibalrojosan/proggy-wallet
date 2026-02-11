"""User authentication module for credential validation and user management."""

from backend.modules import utils
from backend.modules.entities import User
from backend.modules.models import User as UserModel

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


def get_user(username: str) -> UserModel | None:
    """Get user data by username.

    Args:
        username: The username to search for.

    Returns:
        User model object if found, None otherwise.
    """
    users = load_users()

    for user_dict in users:
        if user_dict.get("username") == username:
            # Pydantic validates the dictionary and converts it to a User model
            return UserModel(**user_dict)

    return None


def validate_credentials(username: str, password: str) -> bool:
    """Validate login credentials using the User entity logic.

    Args:
        username: The username to validate.
        password: The password to validate.

    Returns:
        True if credentials are valid, False otherwise.
    """
    users_data = load_users()
    for user_dict in users_data:
        if user_dict.get("username") == username:
            # Create a User entity to use its check_password logic (hashing)
            user_entity = User(
                username=user_dict["username"],
                email=user_dict["email"],
                hashed_password=user_dict["password"],
                balance=float(user_dict.get("balance", 0.0))
            )
            return user_entity.check_password(password)

    return False

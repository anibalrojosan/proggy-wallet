"""User authentication module for credential validation and user management."""

from backend.modules import utils

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


def get_user(username: str) -> dict | None:
    """Get user data by username.

    Args:
        username: The username to search for.

    Returns:
        User dictionary if found, None otherwise.
    """
    users = load_users()

    for user in users:
        if user.get("username") == username:
            return user

    return None


def validate_credentials(username: str, password: str) -> bool:
    """Validate login credentials.

    Args:
        username: The username to validate.
        password: The password to validate.

    Returns:
        True if credentials are valid, False otherwise.
    """
    user = get_user(username)

    if user is None:
        return False

    return user.get("password") == password

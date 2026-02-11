"""Domain entities for the Proggy Wallet system."""

import bcrypt

class Account:
    """
    Represents a financial account belonging to a user.
    This entity encapsulates the balance and the business rules for modifying it.
    """
    def __init__(self, owner_username: str, balance: float = 0.0):
        self.owner_username = owner_username
        self._balance = float(balance)

    @property
    def balance(self) -> float:
        """Public read-only access to the balance."""
        return self._balance

    def add_funds(self, amount: float) -> float:
        """
        Increases the account balance.
        Equivalent to the previous 'deposit' logic but focused on the state change.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._balance += amount
        return self._balance

    def remove_funds(self, amount: float) -> float:
        """
        Decreases the account balance.
        Replaces the manual balance checks previously done in 'validate_transfer_balance'.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self._balance:
            raise ValueError(f"Insufficient funds. Current balance: {self._balance}")
        
        self._balance -= amount
        return self._balance

    def __repr__(self) -> str:
        return f"Account(owner='{self.owner_username}', balance={self._balance})"


class User:
    """
    Represents a user in the system.
    Handles identity and owns an Account entity.
    """
    def __init__(self, username: str, email: str, hashed_password: str, balance: float = 0.0):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        
        # Automatically creates an 'Account' entity for the user.
        self.account = Account(owner_username=username, balance=balance)

    def check_password(self, password: str) -> bool:
        """
        Verifies the password using bcrypt.
        It automatically handles the salt and the hashing comparison.
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                self.hashed_password.encode('utf-8')
            )
        except Exception:
            return False

    @staticmethod
    def hash_password(password: str) -> str:
        """Utility method to hash the password using bcrypt."""
        return bcrypt.hash(password)

    def update_email(self, new_email: str):
        """Updates the user's email address."""
        self.email = new_email

    def __repr__(self) -> str:
        return f"User(username='{self.username}', email='{self.email}')"

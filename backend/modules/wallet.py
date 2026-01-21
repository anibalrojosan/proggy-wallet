"""
Wallet transactions module for deposits, transfers, and transaction history.
This modules contains the following functions:
- calculate_balance
- get_transaction_history
- validate_transfer_balance
- record_transaction
- deposit
- transfer
"""

from datetime import datetime

from backend.modules import auth, utils

# Path to transactions CSV file
TRANSACTIONS_FILE = "backend/data/transactions.csv"

# CSV column names
CSV_COLUMNS = ["date", "owner", "type", "from_user", "to_user", "amount", "balance", "description"]


def calculate_balance(transactions: list, initial_balance: float, user: str) -> float:
    """Calculate balance from transaction history.
    Check if the transaction is a deposit or transfer and updates the
    balance accordingly.

    Args:
        transactions: List of transaction dictionaries.
        initial_balance: Starting balance before transactions.
        user: Username to calculate balance for.

    Returns:
        Calculated balance after all transactions.
    """
    balance = initial_balance

    for transaction in transactions:
        # CRITICAL: Only process the record if the 'owner' is the current user
        if transaction.get("owner") == user:
            trans_type = transaction.get("type", "")
            amount = float(transaction.get("amount", 0))

            # If it's a deposit or incoming transfer, add the amount
            if trans_type in ["deposit", "transfer_in"]:
                balance += amount
            # If it's an outgoing transfer, subtract the amount
            elif trans_type == "transfer_out":
                balance -= amount

    return balance


def get_transaction_history(user: str) -> list:
    """Get all transactions for a user.

    Args:
        user: Username to get transactions for.

    Returns:
        List of transaction dictionaries for the user.
        Returns empty list if file doesn't exist or user has no transactions.
    """
    try:
        all_transactions = utils.read_csv_file(TRANSACTIONS_FILE)
    except FileNotFoundError:
        return []

    # Direct filter: Only bring the rows that belong to the user
    user_transactions = [
        transaction for transaction in all_transactions 
        if transaction.get("owner") == user
    ]

    return user_transactions

def validate_transfer_balance(user: str, amount: float) -> bool:
    """Validate if the user has sufficient balance for making a transfer.

    Args:
        user: Username to check balance for.
        amount: Amount to transfer.

    Returns:
        True if user has sufficient balance, False otherwise.
    """
    if not utils.validate_amount(amount):
        return False

    user_data = auth.get_user(user)
    if user_data is None:
        return False

    initial_balance = float(user_data.get("balance", 0))
    transactions = get_transaction_history(user)
    current_balance = calculate_balance(transactions, initial_balance, user)

    return current_balance >= amount


def record_transaction(transaction_data: dict) -> None:
    """Save transaction to CSV file.

    Args:
        transaction_data: Dictionary with transaction details.
                          Must contain keys matching CSV_COLUMNS.

    Raises:
        ValueError: If transaction_data doesn't have required fields.
        OSError: If file cannot be written.
    """
    # Ensure all required fields are present
    for column in CSV_COLUMNS:
        if column not in transaction_data:
            raise ValueError(f"Transaction data missing required field: {column}")

    # Read existing transactions or start with empty list
    try:
        all_transactions = utils.read_csv_file(TRANSACTIONS_FILE)
    except FileNotFoundError:
        all_transactions = []

    # Add new transaction
    all_transactions.append(transaction_data)

    # Write back to CSV
    utils.write_csv_file(TRANSACTIONS_FILE, all_transactions)


def deposit(user: str, amount: float, source: str = 'external') -> dict:
    """Process deposit transaction.
    Deposit: money that comes from an EXTERNAL SOURCE, like a bank transfer or a
    cash deposit.

    Args:
        user: Username receiving the deposit.
        amount: Amount to deposit.
        source: Source identifier for the deposit. Defaults to "external".
                Examples: "external", "bank", "card", "cash", "stripe", "paypal".

    Returns:
        Dictionary with deposit transaction details.

    Raises:
        ValueError: If amount is not positive.
        FileNotFoundError: If user doesn't exist.
    """
    if not utils.validate_amount(amount):
        raise ValueError("Deposit amount must be positive")

    user_data = auth.get_user(user)
    if user_data is None:
        raise FileNotFoundError(f"User not found: {user}")

    # Calculate current balance
    initial_balance = float(user_data.get("balance", 0))
    transactions = get_transaction_history(user)
    current_balance = calculate_balance(transactions, initial_balance, user)

    # Calculate new balance after deposit
    new_balance = current_balance + amount

    # Create transaction record
    transaction = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "owner": user,
        "type": "deposit",
        "from_user": source,
        "to_user": user,  
        "amount": str(amount),
        "balance": str(new_balance),
        "description": f"Deposit of {amount} from {source}",
    }

    # Record transaction
    record_transaction(transaction)

    return transaction


def transfer(from_user: str, to_user: str, amount: float) -> dict:
    """Process transfer transaction.
    Transfer: money that goes from one user to another.

    Args:
        from_user: Username sending the transfer.
        to_user: Username receiving the transfer.
        amount: Amount to transfer.

    Returns:
        Dictionary with transfer_out transaction details for from_user.

    Raises:
        ValueError: If amount is not positive or insufficient balance.
        FileNotFoundError: If users don't exist.
    """
    if not utils.validate_amount(amount):
        raise ValueError("Transfer amount must be positive")

    # Validate both users exist
    sender_data = auth.get_user(from_user)
    receiver_data = auth.get_user(to_user)

    if sender_data is None:
        raise FileNotFoundError(f"Sender user not found: {from_user}")
    if receiver_data is None:
        raise FileNotFoundError(f"Receiver user not found: {to_user}")

    # Validate sufficient balance
    if not validate_transfer_balance(from_user, amount):
        raise ValueError(f"Insufficient balance for transfer from {from_user}")

    # Calculate balances for both users
    sender_initial = float(sender_data.get("balance", 0))
    receiver_initial = float(receiver_data.get("balance", 0))

    sender_transactions = get_transaction_history(from_user)
    receiver_transactions = get_transaction_history(to_user)

    sender_current_balance = calculate_balance(sender_transactions, sender_initial, from_user)
    receiver_current_balance = calculate_balance(
        receiver_transactions, receiver_initial, to_user
        )

    # Calculate new balances
    sender_new_balance = sender_current_balance - amount
    receiver_new_balance = receiver_current_balance + amount

    # Get timestamp for both transactions
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create transfer_out transaction for sender
    transfer_out = {
        "date": timestamp,
        "owner": from_user,
        "type": "transfer_out",
        "from_user": from_user,
        "to_user": to_user,
        "amount": str(amount),
        "balance": str(sender_new_balance),
        "description": f"Transfer of {amount} to {to_user}",
    }

    # Create transfer_in transaction for receiver
    transfer_in = {
        "date": timestamp,
        "owner": to_user,
        "type": "transfer_in",
        "from_user": from_user,
        "to_user": to_user,
        "amount": str(amount),
        "balance": str(receiver_new_balance),
        "description": f"Transfer of {amount} from {from_user}",
    }

    # Record both transactions
    record_transaction(transfer_out)
    record_transaction(transfer_in)

    return transfer_out

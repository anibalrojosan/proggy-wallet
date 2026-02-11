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
from backend.modules.entities import Account
from backend.modules.models import Transaction

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
        transaction for transaction in all_transactions if transaction.get("owner") == user
    ]

    return user_transactions


def record_transaction(transaction_data: dict) -> None:
    """Save transaction to CSV file.

    Args:
        transaction_data: Dictionary with transaction details.
                          Must contain keys matching Transaction model.

    Raises:
        ValidationError: If transaction_data doesn't match the Transaction model.
        OSError: If file cannot be written.
    """
    # Ensure description exists (it's required in TransactionBase)
    if "description" not in transaction_data:
        transaction_data["description"] = f"{transaction_data['type']} of {transaction_data['amount']}"

    # Pydantic automatically validates all fields and types
    try:
        transaction = Transaction(**transaction_data)
    except Exception as e:
        print(f"DEBUG: Pydantic Validation Error in record_transaction: {e}")
        raise

    # Read existing transactions or start with empty list
    try:
        all_transactions = utils.read_csv_file(TRANSACTIONS_FILE)
    except FileNotFoundError:
        all_transactions = []

    # Add new transaction using model_dump to convert Pydantic object to dict
    all_transactions.append(transaction.model_dump())

    # Write back to CSV
    utils.write_csv_file(TRANSACTIONS_FILE, all_transactions)


def deposit(user: str, amount: float, source: str = "external") -> dict:
    """Process deposit transaction using the Account entity.
    Deposit: money that comes from an EXTERNAL SOURCE.

    Args:
        user: Username receiving the deposit.
        amount: Amount to deposit.
        source: Source identifier for the deposit.

    Returns:
        Dictionary with deposit transaction details.

    Raises:
        ValueError: If amount is not positive.
        FileNotFoundError: If user doesn't exist.
    """
    user_data = auth.get_user(user)
    if user_data is None:
        raise FileNotFoundError(f"User not found: {user}")

    # Load current balance from history
    history = get_transaction_history(user)
    current_balance = calculate_balance(history, float(user_data.balance), user)

    # Use Account entity for business logic
    account = Account(owner_username=user, balance=current_balance)
    new_balance = account.add_funds(amount)

    # Create transaction record
    transaction_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "owner": user,
        "type": "deposit",
        "from_user": source,
        "to_user": user,
        "amount": float(amount),
        "balance": float(new_balance),
        "description": f"Deposit of {amount} from {source}",
    }

    # Record transaction
    record_transaction(transaction_data)

    return transaction_data


def transfer(from_user: str, to_user: str, amount: float) -> dict:
    """Process transfer transaction between two Account entities.
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
    # Validate both users exist
    sender_data = auth.get_user(from_user)
    receiver_data = auth.get_user(to_user)

    if sender_data is None:
        raise FileNotFoundError(f"Sender user not found: {from_user}")
    if receiver_data is None:
        raise FileNotFoundError(f"Receiver user not found: {to_user}")

    # Load and instantiate sender account
    sender_history = get_transaction_history(from_user)
    sender_current = calculate_balance(sender_history, float(sender_data.balance), from_user)
    sender_account = Account(owner_username=from_user, balance=sender_current)

    # Load and instantiate receiver account
    receiver_history = get_transaction_history(to_user)
    receiver_current = calculate_balance(receiver_history, float(receiver_data.balance), to_user)
    receiver_account = Account(owner_username=to_user, balance=receiver_current)

    # Execute business logic (validations happen inside entities)
    new_sender_balance = sender_account.remove_funds(amount)
    new_receiver_balance = receiver_account.add_funds(amount)

    # Get timestamp for both transactions
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create transfer records
    transfer_out = {
        "date": timestamp,
        "owner": from_user,
        "type": "transfer_out",
        "from_user": from_user,
        "to_user": to_user,
        "amount": float(amount),
        "balance": float(new_sender_balance),
        "description": f"Transfer of {amount} to {to_user}",
    }

    transfer_in = {
        "date": timestamp,
        "owner": to_user,
        "type": "transfer_in",
        "from_user": from_user,
        "to_user": to_user,
        "amount": float(amount),
        "balance": float(new_receiver_balance),
        "description": f"Transfer of {amount} from {from_user}",
    }

    # Record both transactions
    record_transaction(transfer_out)
    record_transaction(transfer_in)

    return transfer_out

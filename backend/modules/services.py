'''
Services are responsible for coordinating actions between entities (User and Account objects).

TransactionManager: Service for coordinating the execution of transactions between two accounts.
It is responsible for validating the amount, withdrawing funds from the sender account,
depositing funds to the receiver account, and recording the transaction.
'''

from datetime import datetime

from .entities import Account
from .models import TransactionCreate
from .utils import append_csv_file


class TransactionManager:
    def __init__(self, transactions_file: str = "backend/data/transactions.csv"):
        self.transactions_file = transactions_file

    def execute_transfer(self, from_account: Account, to_account: Account, amount: float):
        """
        Coordinate a transfer between two Account objects.
        Implements atomicity: if the deposit fails, the withdrawal is rolled back.
        """
        if amount <= 0:
            raise ValueError("The amount must be positive")

        # Withdraw funds. Account.remove_funds validates the amount and ensures sufficient balance
        from_account.remove_funds(amount)

        try:
            # Deposit funds. Account.add_funds validates the amount
            to_account.add_funds(amount)
        except Exception as e:
            # Rollback: If the deposit fails, we return the money to the sender
            from_account.add_funds(amount)
            raise Exception(f"Transfer error: {e}")

        # Record the transaction
        self._record(
            type="TRANSFER",
            amount=amount,
            from_user=from_account.owner_username,
            to_user=to_account.owner_username,
            balance_after=from_account.get_balance()
        )

    def execute_deposit(self, account: Account, amount: float):
        """
        Coordinate a deposit in an account and record it.
        """
        if amount <= 0:
            raise ValueError("The amount must be positive")

        account.add_funds(amount)

        self._record(
            type="DEPOSIT",
            amount=amount,
            from_user=None,
            to_user=account.owner_username,
            balance_after=account.get_balance()
        )

    def _record(
        self,
        type: str,
        amount: float,
        from_user: str | None,
        to_user: str,
        balance_after: float
    ):
        """
        Create the transaction model, validate it and persist it.
        """
        # Prepare the transaction data
        transaction_dict = {
            "date": datetime.now().isoformat(),
            "type": type,
            "from_user": from_user if from_user else "SYSTEM",
            "to_user": to_user,
            "amount": amount,
            "balance": balance_after
        }

        # Validation: Use the Pydantic model to ensure that 'amount' is > 0 and the fields exist
        txn_validated = TransactionCreate(**transaction_dict)

        # Persistence: Save in the CSV. We use a list because append_csv_file expects a list of dicts
        try:
            append_csv_file(self.transactions_file, [txn_validated.model_dump()])
        except Exception as e:
            raise Exception(f"Error persisting transaction: {e}")

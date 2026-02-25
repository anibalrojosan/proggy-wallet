'''
Services are responsible for coordinating actions between entities (User and Account objects).
'''

from backend.database.repository import create_transaction, update_user_balance

from .entities import Account
from .models import TransactionCreate


class TransactionManager:
    '''
    Service for coordinating the execution of transactions between two accounts.
    It is responsible for validating the amount, withdrawing funds from the sender account,
    depositing funds to the receiver account, and recording the transaction. For this, it uses the
    repository functions to create the transaction and update the user balance.
    '''
    def __init__(self):
        pass

    def execute_transfer(self, from_account: Account, to_account: Account, amount: float):
        """
        Coordinate a transfer between two Account objects and persist in DB.
        """
        if amount <= 0:
            raise ValueError("The amount must be positive")

        # 1. Business logic in memory (Entities)
        from_account.remove_funds(amount)
        try:
            to_account.add_funds(amount)
        except Exception as e:
            # Rollback in memory if the deposit fails
            from_account.add_funds(amount)
            raise Exception(f"Transfer error: {e}")

        # 2. Persistence in DB
        try:
            # Update balances of both users
            update_user_balance(from_account.owner_username, from_account.balance)
            update_user_balance(to_account.owner_username, to_account.balance)

            # Record the transaction in the transaction history (ledger)
            txn_data = TransactionCreate(
                from_user=from_account.owner_username,
                to_user=to_account.owner_username,
                amount=amount,
                type="transfer_out",
                description=f"Transfer to {to_account.owner_username}",
                owner=from_account.owner_username
            )
            create_transaction(txn_data, balance_after=from_account.balance)
        except Exception as e:
            raise Exception(f"Database persistence error: {e}")

    def execute_deposit(self, account: Account, amount: float):
        """
        Coordinate a deposit in an account and persist in DB.
        """
        if amount <= 0:
            raise ValueError("The amount must be positive")

        # 1. Business logic in memory
        account.add_funds(amount)

        # 2. Persistence in DB
        try:
            # Update balance in DB
            update_user_balance(account.owner_username, account.balance)

            # Record the transaction in the transaction history (ledger)
            txn_data = TransactionCreate(
                from_user="SYSTEM",
                to_user=account.owner_username,
                amount=amount,
                type="deposit",
                description="External deposit",
                owner=account.owner_username
            )
            create_transaction(txn_data, balance_after=account.balance)
        except Exception as e:
            raise Exception(f"Database persistence error: {e}")

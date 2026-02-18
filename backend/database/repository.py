from typing import List, Optional
from backend.database.connection import get_db_cursor
from backend.modules.models import User, Transaction

def get_user_by_username(username: str) -> Optional[User]:
    '''Get a user by their username and return it as a User model'''
    query = "SELECT * FROM users WHERE username = %s"

    with get_db_cursor() as cursor:
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            # Direct mapping from the database row to the User model
            return User(**result)
        return None


def get_transactions_by_user(username: str) -> List[Transaction]:
    '''Get the transactions history for a user and return them as a list of Transaction models'''
    
    query = """
               SELECT t.* 
               FROM transactions t 
               JOIN users u ON (t.from_user_id = u.id OR t.to_user_id = u.id)
               WHERE u.username = %s
               ORDER BY t.created_at DESC
            """

    transactions = []

    with get_db_cursor() as cursor:
        cursor.execute(query, (username,))
        results = cursor.fetchall()

        for row in results:
            # Direct mapping from the database row to the Transaction model
            transactions.append(Transaction(**row))

        return transactions

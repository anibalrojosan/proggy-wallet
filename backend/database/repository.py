from psycopg2.extras import RealDictCursor

from backend.database.connection import get_db_connection, get_db_cursor
from backend.modules.models import Transaction, TransactionCreate, User


# ------------READ OPERATIONS------------
# This functions use get_db_cursor that internally handles its own connection.
def get_user_by_username(username: str) -> User | None:
    '''Get a user by their username and return it as a User model'''
    query = "SELECT * FROM users WHERE username = %s"

    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                return User(**result)
            return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


def get_transactions_by_user(username: str) -> list[Transaction]:
    '''Get the transactions history for a user'''

    # 1. Select only the columns that the Transaction model accepts.
    # 2. Do JOIN to get the usernames (strings) instead of IDs.
    # 3. Map 'created_at' to 'date'.
    # 4. Dummy value for 'balance' (0.0) because the table doesn't have it but the model requires it.

    query = """
        SELECT
            t.amount,
            t.description,
            t.type,
            %s as owner,                    -- Owner (the user that queries the transactions)
            u1.username as from_user,       -- from_user (string)
            u2.username as to_user,         -- to_user (string)
            t.created_at as date,           -- date (datetime)
            t.balance_after as balance      -- balance (float)
        FROM transactions t
        JOIN users u1 ON t.from_user_id = u1.id
        JOIN users u2 ON t.to_user_id = u2.id
        WHERE (u1.username = %s OR u2.username = %s)
        ORDER BY t.created_at DESC
    """

    transactions = []
    try:
        with get_db_cursor() as cursor:
            # Pasamos 'username' 3 veces: para el SELECT (owner) y para el WHERE (OR)
            cursor.execute(query, (username, username, username))
            results = cursor.fetchall()

            for row in results:
                # RealDictCursor allows 'row' to be a clean dictionary
                # that exactly matches the definition of Transaction.
                transactions.append(Transaction(**row))

        return transactions
    except Exception as e:
        print(f"Error getting transactions: {e}")
        return []


# ------------CREATE/UPDATE OPERATIONS------------
# These functions need COMMIT, so get_db_connection is used directly.
def update_user_balance(username: str, new_balance: float) -> bool:
    '''Update the balance for a user in 'users' table.'''
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET balance = %s WHERE username = %s",
                    (new_balance, username)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating user balance: {e}")
        # Explicit rollback if the connection is not returned to the pool.
        if 'conn' in locals():  # Check if conn exists in local scope
            conn.rollback()
        return False


def create_transaction(transaction: TransactionCreate, balance_after: float) -> bool:
    '''Create a new transaction in 'transactions' table.'''
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:

                # Get the ID of the 'from_user'
                cursor.execute("SELECT id FROM users WHERE username = %s", (transaction.from_user,))
                res_from = cursor.fetchone()

                # Handle special case if the source user doesn't exist
                if not res_from:
                    print(f"Error: Source user '{transaction.from_user}' not found.")
                    return False
                from_user_id = res_from['id']

                # Get the ID of the 'to_user'
                cursor.execute("SELECT id FROM users WHERE username = %s", (transaction.to_user,))
                res_to = cursor.fetchone()

                if not res_to:
                     print(f"Error: Destination user '{transaction.to_user}' not found.")
                     return False
                to_user_id = res_to['id']

                # Insert using the IDs
                cursor.execute(
                    """
                    INSERT INTO transactions
                    (from_user_id, to_user_id, amount, type, description, balance_after)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        from_user_id,
                        to_user_id,
                        transaction.amount,
                        transaction.type,
                        transaction.description,
                        balance_after
                    )
                )
                conn.commit()
                return True
    except Exception as e:
        print(f"Error creating transaction: {e}")
        return False

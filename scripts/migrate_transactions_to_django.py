import os
import django
from django.db import connection
from decimal import Decimal

# Django config
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from wallet.models import Transaction

def migrate_transactions():
    print("Starting transaction migration...")
    
    with connection.cursor() as cursor:
        # Read from the old 'transactions' table
        cursor.execute("SELECT from_user_id, to_user_id, amount, type, description, created_at FROM transactions")
        old_txs = cursor.fetchall()

    count = 0
    for from_id, to_id, amount, t_type, desc, created_at in old_txs:
        # Map the IDs
        # Find the new Django user that has the same username as the old one
        from_user = None
        to_user = None
        
        with connection.cursor() as cursor_users:
            if from_id:
                cursor_users.execute("SELECT username FROM users WHERE id = %s", [from_id])
                res = cursor_users.fetchone()
                if res:
                    from_user = User.objects.filter(username=res[0]).first()
            
            if to_id:
                cursor_users.execute("SELECT username FROM users WHERE id = %s", [to_id])
                res = cursor_users.fetchone()
                if res:
                    to_user = User.objects.filter(username=res[0]).first()

        # Create the transaction in the new 'wallet_transaction' table
        Transaction.objects.create(
            from_user=from_user,
            to_user=to_user,
            amount=amount,
            type=t_type.lower(), # Django expects 'deposit', 'transfer', etc.
            description=desc or "",
            created_at=created_at
        )
        count += 1

    print(f"Migrated {count} transactions successfully.")

if __name__ == "__main__":
    migrate_transactions()
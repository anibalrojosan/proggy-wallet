import os
import django
from django.db import connection

# Django config
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from wallet.models import Account

def migrate():
    print("Starting user migration...")
    
    # Read from the old 'users' table
    with connection.cursor() as cursor:
        # Use the column names we saw in inspectdb
        cursor.execute("SELECT username, email, password_hash, balance FROM users")
        old_users = cursor.fetchall()

    for username, email, password_hash, balance in old_users:
        # Avoid duplicates
        if not User.objects.filter(username=username).exists():
            # Create the user without a password first            
            new_user = User(
                username=username,
                email=email,
            )
            # The assign bcrypt hash to the password field. 
            # Django detects the bcrypt hash and knows how to hash it
            new_user.password = password_hash
            new_user.save()
            
            # Create the linked account
            Account.objects.create(
                user=new_user,
                balance=balance or 0.00
            )
            print(f"User '{username}' migrated with balance ${balance}")
        else:
            print(f"User '{username}' already exists in Django. Skipping...")

    print("Migration completed.")

if __name__ == "__main__":
    migrate()
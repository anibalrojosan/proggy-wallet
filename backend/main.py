import logging
from backend.modules.auth import validate_credentials, get_user
from backend.modules.wallet import deposit, transfer, get_transaction_history, calculate_balance

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def main():
    logging.info("Starting Proggy Wallet...")

    user_test = "user1"
    pass_test = "user1_pass"
    reciever_user = "user2"

    # login and get user data
    if validate_credentials(user_test, pass_test):
        logging.info(f'Successfully logged in as {user_test}')
        user_data = get_user(user_test)
        
        # Get the history and calculate the real balance for THIS user
        history_records = get_transaction_history(user_test)
        current_balance = calculate_balance(history_records, float(user_data['balance']), user_test)
        
        logging.info(f'Current balance for [{user_test}]: ${current_balance}')

        # Simulate a deposit
        deposit(user_test, 100.0)
        logging.info(f'100$ deposit succesfully done to {user_test}.')

        # Simulate a transfer
        try:
            transfer(user_test, reciever_user, 50.0)
            logging.info(f'50$ transfer succesfully done from {user_test} to {reciever_user}.')
        except Exception as e:
            logging.error(f'Error transferring money: {e}')
        
        # Print the transaction history for the user
        logging.info(f'Transaction history for [{user_test}] (last 10):')
        for tx in get_transaction_history(user_test)[-10:]:
            # Identify if the user was the sender or receiver in this line
            role = "RECEIVED" if tx['to_user'] == user_test else "SENT"
            print(f"{tx['date']} | {tx['amount']} | {tx['type']} ({role}) | Current Balance: {tx['balance']}")

    else:
        logging.error(f'Failed to login as {user_test}')

if __name__ == '__main__':
    main()
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
        user_balance = get_transaction_history(user_test)
        current_balance = calculate_balance(user_balance, float(user_data['balance']))
        logging.info(f'Current balance of {user_test} is: {current_balance}')

        # Simulate a deposit
        deposit(user_test, 100.0)
        logging.info(f'100$ deposit succesfully done to {user_test}.')

        # Simulate a transfer
        try:
            transfer(user_test, reciever_user, 50.0)
            logging.info(f'50$ transfer succesfully done from {user_test} to {reciever_user}.')
        except Exception as e:
            logging.error(f'Error transferring money: {e}')

        history = get_transaction_history(user_test)
        logging.info(f'{user_test} transaction history (last 10)')
        for tx in history[-10:]:
            print(f"{tx['date']} | {tx['amount']} | {tx['type']} | balance: {tx['balance']}")

    else:
        logging.error(f'Failed to login as {user_test}')

if __name__ == '__main__':
    main()
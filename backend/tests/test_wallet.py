from backend.modules.wallet import calculate_balance

def test_calculate_balance_various_ops():
    # fake data
    user = "test_user"
    initial = 1000.0
    transactions = [
        {"owner": "test_user", "type": "deposit", "amount": "500.0"},
        {"owner": "test_user", "type": "transfer_out", "amount": "200.0"},
        {"owner": "test_user", "type": "transfer_in", "amount": "100.0"},
        {"owner": "other_user", "type": "deposit", "amount": "999.0"} # should not affect the balance
    ]
    
    balance = calculate_balance(transactions, initial, user)
    
    # Assert: 1000 + 500 - 200 + 100 = 1400
    assert balance == 1400.0
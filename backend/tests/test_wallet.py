import pytest
from backend.modules import wallet

class TestCalculateBalance:
    '''Test the calculate_balance function'''

    def test_empty_history(self):
        '''Should return the initial balance if there are no transactions'''
        result = wallet.calculate_balance([], 1000.0, "user1")
        assert result == 1000.0

    def test_deposit_and_transfer_in(self):
        '''Should sum deposits and transfer in'''
        txs = [
            {"owner": "user1", "type": "deposit", "amount": "500.0"},
            {"owner": "user1", "type": "transfer_in", "amount": "200.0"}
        ]
        result = wallet.calculate_balance(txs, 1000.0, "user1")
        assert result == 1700.0

    def test_transfer_out(self):
        '''Should subtract the transfers sent'''
        txs = [{"owner": "user1", "type": "transfer_out", "amount": "300.0"}]
        result = wallet.calculate_balance(txs, 1000.0, "user1")
        assert result == 700.0

class TestTransfer:
    '''Test the transfer function'''

    @pytest.fixture
    def mock_env(self, monkeypatch):
        '''Prepare a mock environment for transfers'''
        # 1. Mock that two users exist
        def mock_get_user(username):
            users = {
                "sender": {"username": "sender", "balance": "1000.0"},
                "receiver": {"username": "receiver", "balance": "500.0"}
            }
            return users.get(username)

        monkeypatch.setattr("backend.modules.auth.get_user", mock_get_user)
        
        # 2. Mock that the sender has enough balance
        monkeypatch.setattr(wallet, "validate_transfer_balance", lambda u, a: True)
        
        # 3. Mock that we don't try to write to the real CSV
        monkeypatch.setattr(wallet, "record_transaction", lambda tx: None)
        
        # 4. Mock that there is no previous transaction history
        monkeypatch.setattr(wallet, "get_transaction_history", lambda u: [])

    def test_transfer_success(self, mock_env):
        '''Test that a valid transfer returns the correct record'''
        result = wallet.transfer("sender", "receiver", 200.0)
        
        assert result["type"] == "transfer_out"
        assert result["from_user"] == "sender"
        assert result["to_user"] == "receiver"
        assert float(result["amount"]) == 200.0
        assert float(result["balance"]) == 800.0  # 1000 - 200

    def test_transfer_insufficient_balance(self, monkeypatch):
        '''Test that it fails if there is no balance (forcing the validation to False)'''
        # Force the validation of balance to return False
        monkeypatch.setattr(wallet, "validate_transfer_balance", lambda user, amount: False)
        # Mock the necessary users
        monkeypatch.setattr("backend.modules.auth.get_user", lambda user: {"username": user, "balance": "0"})

        with pytest.raises(ValueError, match="Insufficient balance"):
            wallet.transfer("sender", "receiver", 100.0)

    def test_transfer_invalid_amount(self):
        '''Test that it fails if the amount is negative or zero'''
        with pytest.raises(ValueError, match="amount must be positive"):
            wallet.transfer("sender", "receiver", -50.0)

    def test_transfer_user_not_found(self, monkeypatch):
        '''Test that it fails if one of the users does not exist'''
        # Mock that get_user always returns None
        monkeypatch.setattr("backend.modules.auth.get_user", lambda user: None)

        with pytest.raises(FileNotFoundError, match="not found"):
            wallet.transfer("sender", "receiver", 100.0)
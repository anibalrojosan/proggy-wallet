import pytest

from backend.modules import wallet


class TestCalculateBalance:
    """Test the calculate_balance function"""

    def test_empty_history(self):
        """Should return the initial balance if there are no transactions"""
        result = wallet.calculate_balance([], 1000.0, "user1")
        assert result == 1000.0

    def test_deposit_and_transfer_in(self):
        """Should sum deposits and transfer in"""
        txs = [
            {"owner": "user1", "type": "deposit", "amount": "500.0"},
            {"owner": "user1", "type": "transfer_in", "amount": "200.0"},
        ]
        result = wallet.calculate_balance(txs, 1000.0, "user1")
        assert result == 1700.0

    def test_transfer_out(self):
        """Should subtract the transfers sent"""
        txs = [{"owner": "user1", "type": "transfer_out", "amount": "300.0"}]
        result = wallet.calculate_balance(txs, 1000.0, "user1")
        assert result == 700.0


class TestTransfer:
    """Test the transfer function"""

    @pytest.fixture
    def mock_env(self, monkeypatch):
        """Prepare a mock environment for transfers"""

        # 1. Mock that two users exist
        def mock_get_user(username):
            users = {
                "sender": {"username": "sender", "balance": "1000.0"},
                "receiver": {"username": "receiver", "balance": "500.0"},
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
        """Test that a valid transfer returns the correct record"""
        result = wallet.transfer("sender", "receiver", 200.0)

        assert result["type"] == "transfer_out"
        assert result["from_user"] == "sender"
        assert result["to_user"] == "receiver"
        assert float(result["amount"]) == 200.0
        assert float(result["balance"]) == 800.0  # 1000 - 200

    def test_transfer_insufficient_balance(self, monkeypatch):
        """Test that it fails if there is no balance (forcing the validation to False)"""
        # Force the validation of balance to return False
        monkeypatch.setattr(wallet, "validate_transfer_balance", lambda user, amount: False)
        # Mock the necessary users
        monkeypatch.setattr(
            "backend.modules.auth.get_user", lambda user: {"username": user, "balance": "0"}
        )

        with pytest.raises(ValueError, match="Insufficient balance"):
            wallet.transfer("sender", "receiver", 100.0)

    def test_transfer_invalid_amount(self):
        """Test that it fails if the amount is negative or zero"""
        with pytest.raises(ValueError, match="amount must be positive"):
            wallet.transfer("sender", "receiver", -50.0)

    def test_transfer_user_not_found(self, monkeypatch):
        """Test that it fails if one of the users does not exist"""
        # Mock that get_user always returns None
        monkeypatch.setattr("backend.modules.auth.get_user", lambda user: None)

        with pytest.raises(FileNotFoundError, match="not found"):
            wallet.transfer("sender", "receiver", 100.0)


class TestDeposit:
    """Test the deposit function"""

    def test_deposit_success(self, monkeypatch):
        """Test that a valid deposit calculates the balance correctly"""
        # Mock a user with an initial balance of 100
        monkeypatch.setattr(
            "backend.modules.auth.get_user", lambda user: {"username": user, "balance": "100.0"}
        )
        # Mock an empty transaction history for this test
        monkeypatch.setattr(wallet, "get_transaction_history", lambda user: [])
        # Mock that we don't try to write to the CSV
        monkeypatch.setattr(wallet, "record_transaction", lambda tx: None)

        result = wallet.deposit("user1", 50.0, source="atm")

        assert result["type"] == "deposit"
        assert result["to_user"] == "user1"
        assert float(result["amount"]) == 50.0
        assert float(result["balance"]) == 150.0  # 100 + 50
        assert "atm" in result["description"]

    def test_deposit_negative_amount(self):
        """Test that it fails if the amount is negative"""
        with pytest.raises(ValueError, match="amount must be positive"):
            wallet.deposit("user1", -10.0)

    def test_deposit_user_not_found(self, monkeypatch):
        """Test that it fails if the user does not exist"""
        monkeypatch.setattr("backend.modules.auth.get_user", lambda user: None)

        with pytest.raises(FileNotFoundError, match="User not found"):
            wallet.deposit("ghost_user", 100.0)


class TestTransactionHistory:
    """Test the transaction history function"""

    def test_get_history_filters_by_owner(self, monkeypatch):
        """Test that it only returns the transactions of the requested user"""
        mock_data = [
            {"owner": "user1", "type": "deposit", "amount": "100"},
            {"owner": "user2", "type": "deposit", "amount": "200"},
            {"owner": "user1", "type": "transfer_out", "amount": "50"},
        ]
        # Mock the reading of the CSV file
        monkeypatch.setattr("backend.modules.utils.read_csv_file", lambda path: mock_data)

        history = wallet.get_transaction_history("user1")

        assert len(history) == 2
        for tx in history:
            assert tx["owner"] == "user1"

    def test_get_history_file_not_found(self, monkeypatch):
        """Test that it returns an empty list if the CSV file does not exist yet"""

        def mock_read_error(path):
            raise FileNotFoundError()

        monkeypatch.setattr("backend.modules.utils.read_csv_file", mock_read_error)

        history = wallet.get_transaction_history("any_user")
        assert history == []

    def test_get_history_empty_list_if_no_matches(self, monkeypatch):
        """Test that it returns an empty list if the user has no transactions in the file"""
        mock_data = [
            {"owner": "user2", "type": "deposit", "amount": "100"},
            {"owner": "user3", "type": "transfer_in", "amount": "50"},
        ]
        monkeypatch.setattr("backend.modules.utils.read_csv_file", lambda path: mock_data)

        # Search for user1, which is not in the mocked data
        history = wallet.get_transaction_history("user1")

        assert history == []
        assert len(history) == 0

    def test_get_history_integrity(self, monkeypatch):
        """Test that the returned data maintains its original structure"""
        mock_tx = {"owner": "user1", "type": "deposit", "amount": "100.0", "date": "2026-01-01"}
        monkeypatch.setattr("backend.modules.utils.read_csv_file", lambda path: [mock_tx])

        history = wallet.get_transaction_history("user1")

        assert history[0]["amount"] == "100.0"
        assert history[0]["type"] == "deposit"
        assert "date" in history[0]

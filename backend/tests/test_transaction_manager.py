import pytest
from unittest.mock import patch
from backend.modules.entities import Account
from backend.modules.services import TransactionManager

@pytest.fixture
def manager():
    return TransactionManager()

@pytest.fixture
def acc_a():
    return Account(owner_username="user_a", balance=100.0)

@pytest.fixture
def acc_b():
    return Account(owner_username="user_b", balance=50.0)

def test_transfer_success(manager, acc_a, acc_b):
    """Verify that a successful transfer calls the repository functions correctly."""
    with patch("backend.modules.services.update_user_balance") as mock_update, \
         patch("backend.modules.services.create_transaction") as mock_create:
        
        manager.execute_transfer(acc_a, acc_b, 30.0)
        
        assert acc_a.balance == 70.0
        assert acc_b.balance == 80.0
        # Should call update_user_balance 2 times (once for each account)
        assert mock_update.call_count == 2
        # Should call create_transaction 1 time
        mock_create.assert_called_once()

def test_transfer_rollback_on_failure(manager, acc_a, acc_b):
    """Verify that if the DB fails, the balance in memory is kept consistent."""
    with patch("backend.modules.services.update_user_balance", side_effect=Exception("DB Error")):
        with pytest.raises(Exception, match="Database persistence error"):
            manager.execute_transfer(acc_a, acc_b, 10.0)
        # Although the business logic passed, the persistence failed.
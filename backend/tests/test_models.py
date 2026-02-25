import pytest
from pydantic import ValidationError

from backend.modules.models import TransactionCreate


def test_transaction_create_valid():
    """Verify that a valid model can be created."""
    data = {
        "from_user": "anibal",
        "to_user": "sistema",
        "amount": 100.0,
        "type": "deposit",
        "description": "Test",
        "owner": "anibal"
    }
    txn = TransactionCreate(**data)
    assert txn.amount == 100.0
    assert txn.type == "deposit"

def test_transaction_create_negative_amount():
    """Verify that it fails if the amount is negative or zero."""
    data = {
        "from_user": "anibal",
        "to_user": "sistema",
        "amount": -50.0, # Invalid amount
        "type": "deposit",
        "description": "Test",
        "owner": "anibal"
    }
    with pytest.raises(ValidationError):
        TransactionCreate(**data)

def test_transaction_create_missing_fields():
    """Verify that it fails if required fields are missing."""
    # Missing 'amount' and 'type'
    data = {
        "from_user": "anibal",
        "to_user": "sistema",
        "owner": "anibal"
    }
    with pytest.raises(ValidationError):
        TransactionCreate(**data)

def test_transaction_invalid_type():
    """Verify that only the allowed types (Literal) are accepted."""
    data = {
        "from_user": "anibal",
        "to_user": "sistema",
        "amount": 100.0,
        "type": "invalid_type", # Not deposit, transfer_in or transfer_out
        "description": "Test",
        "owner": "anibal"
    }
    with pytest.raises(ValidationError):
        TransactionCreate(**data)

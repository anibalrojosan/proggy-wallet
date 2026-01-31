from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.modules.auth import get_user, validate_credentials
from backend.modules.wallet import (
    calculate_balance,
    deposit,
    get_transaction_history,
    transfer,
)

# App configuration
app = FastAPI(
    title="Proggy Wallet API",
    description="API for the Proggy Wallet application",
    version="1.0.0",
)


# Middleware (CORS) configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development purposes, we allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Data Models
class LoginRequest(BaseModel):
    """Schema for the login request"""

    username: str = Field(..., example="user1")
    password: str = Field(..., example="user1_pass")


class DepositRequest(BaseModel):
    """Schema for making a deposit"""

    username: str = Field(..., example="user1")
    amount: float = Field(..., gt=0, example=100.0)


class TransferRequest(BaseModel):
    """Schema for making a transfer"""

    from_user: str = Field(..., example="user1")
    to_user: str = Field(..., example="user2")
    amount: float = Field(..., gt=0, example=80.0)


# Routes (endpoints)
@app.get("/")
async def root():
    """Route to check if the API is running"""
    return {
        "message": "Welcome to the Proggy Wallet API",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Route to check if the API is running"""
    return {"status": "healthy"}


@app.post("/auth/login")
async def login(credentials: LoginRequest):
    """Route to validate user credentials"""
    is_valid = validate_credentials(credentials.username, credentials.password)

    if not is_valid:
        # Use an HTTP status code 401 (Unauthorized) to indicate that the credentials are invalid
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # If the credentials are valid, get the user data
    user_data = get_user(credentials.username)

    return {
        "message": f"Login successful for user: {credentials.username}",
        "status": "success",
        "user": {
            "username": user_data["username"],
            "email": user_data.get("email"),
            "balance": user_data.get("balance"),
        },
    }


@app.get("/wallet/status/{username}")
async def get_wallet_status(username: str):
    """Route to get the wallet status for a user"""
    user_data = get_user(username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    history = get_transaction_history(username)
    current_balance = calculate_balance(history, float(user_data["balance"]), username)

    return {
        "status": "success",
        "username": username,
        "balance": current_balance,
        "history_count": len(history),
    }


@app.post("/wallet/deposit")
async def make_deposit(data: DepositRequest):
    """Route to make a deposit for a user"""
    try:
        # deposit() handles the update of the CSV and the calculation of the balance
        transaction = deposit(data.username, data.amount)

        return {
            "status": "success",
            "message": f"Deposit of ${data.amount} successful",
            "transaction": transaction,
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal error processing the deposit")


@app.post("/wallet/transfer")
async def make_transfer(data: TransferRequest):
    """Route to make a transfer between two users"""
    try:
        # transfer() validates the insufficient balance and the existence of the users
        transaction = transfer(data.from_user, data.to_user, data.amount)

        return {
            "status": "success",
            "message": f"Transfer of ${data.amount} to {data.to_user} successful",
            "transaction": transaction,
        }
    except FileNotFoundError as e:
        # If one of the users does not exist
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        # If the balance is insufficient or the amount is negative
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal error processing the transfer: {str(e)}"
        )


@app.get("/wallet/history/{username}")
async def get_history(username: str):
    """Route to get the real history of transactions from the CSV file"""
    try:
        # get the history of transactions from the CSV file
        history = get_transaction_history(username)

        return {"status": "success", "username": username, "transactions": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting the history: {str(e)}")

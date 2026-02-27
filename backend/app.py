from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.database.repository import get_transactions_by_user, get_all_usernames
from backend.modules.auth import AuthService
from backend.modules.models import User as UserResponse
from backend.modules.services import TransactionManager

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


# ------------- Data Models ---------------
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


# ------------- Routes (endpoints) ---------------
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

    user_entity = AuthService.authenticate(credentials.username, credentials.password)

    if not user_entity:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Return the user entity as a Pydantic model
    # Returns only safe data for the user (excludes password)
    return {
        "message": f"Login successful for user: {credentials.username}",
        "status": "success",
        "user": UserResponse(
            username=user_entity.username,
            email=user_entity.email,
            balance=user_entity.account.balance
        ),
    }

@app.get("/wallet/status/{username}")
async def get_wallet_status(username: str):
    """Route to get the wallet status for a user"""

    # 1. Get the user entity (has the updated balance from the DB)
    user_entity = AuthService.get_user_entity(username)
    if not user_entity:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Get the history of transactions
    history = get_transactions_by_user(username)

    # 3. Return wallet status
    return {
        "status": "success",
        "username": username,
        "balance": user_entity.account.balance,
        "history_count": len(history),
    }

@app.post("/wallet/deposit")
async def make_deposit(data: DepositRequest):
    """Route to make a deposit for a user"""

    # 1. Get the user entity
    user_entity = AuthService.get_user_entity(data.username)
    if not user_entity:
        raise HTTPException(status_code=404, detail="User not found")

    # 2 Use TransactionManager to make the deposit
    manager = TransactionManager()
    try:
        manager.execute_deposit(user_entity.account, data.amount)

        return {
            "status": "success",
            "message": f"Deposit of ${data.amount} successful",
            "transaction": {
                "amount": data.amount,
                "type": "deposit",
                "balance": user_entity.account.balance,
            },
        }
    except ValueError as e:
        # Business logic error (e.g. amount is negative)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Technical error (e.g. DB, network, etc.)
        print(f"Error processing the deposit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/wallet/transfer")
async def make_transfer(data: TransferRequest):
    """Route to make a transfer between two users"""

    # 1. Get both user entities
    sender = AuthService.get_user_entity(data.from_user)
    receiver = AuthService.get_user_entity(data.to_user)

    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="One or both users not found")

    # 2. Use TransactionManager to make the transfer
    manager = TransactionManager()
    try:
        manager.execute_transfer(sender.account, receiver.account, data.amount)

        return {
            "status": "success",
            "message": f"Transfer of ${data.amount} to {data.to_user} successful",
            "transaction": {
                "to_user": data.to_user,
                "amount": data.amount,
                "balance": sender.account.balance,
            },
        }
    except ValueError as e:
        # Business logic error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Technical error
        print(f"Error processing the transfer: {e}")
        raise HTTPException(
            status_code=500, detail="A technical error occurred while processing the transfer. \
                                     Please try again later."
        )

@app.get("/wallet/history/{username}")
async def get_history(username: str):
    """Route to get the real history of transactions for a user"""

    try:
        # get the history of transactions for the user
        history = get_transactions_by_user(username)
        return {"status": "success", "username": username, "transactions": history}
    
    except Exception as e:
        # Technical error
        print(f"Error getting the history: {e}")
        raise HTTPException(status_code=500, detail="Error getting the history. Please try again later.")

@app.get("/wallet/contacts/{username}")
async def get_contacts(username: str):
    """
    Route to get the list of all usernames (contacts) for transaction purposes
    """
    try:
        all_usernames = get_all_usernames()
        contacts = [username_name for username_name in all_usernames if username_name != username]

        return {
            "status": "success",
            "contacts": contacts
        }
        
    except Exception as e:
        print(f"Error getting contacts: {e}")
        raise HTTPException(status_code=500, detail="Error getting contacts. Please try again later.")

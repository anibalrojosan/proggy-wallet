from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from backend.modules.auth import validate_credentials, get_user
from backend.modules.wallet import get_transaction_history, deposit, transfer, calculate_balance


# App configuration
app = FastAPI(
    title="Proggy Wallet API",
    description="API for the Proggy Wallet application",
    version="1.0.0",
)


# Middleware (CORS) configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development purposes, we allow all origins
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
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
    '''Route to check if the API is running'''
    return {'message': 'Welcome to the Proggy Wallet API',
            'status': 'online',
            'docs': '/docs',
    }

@app.get("/health")
async def health_check():
    '''Route to check if the API is running'''
    return {'status': 'healthy'}

@app.post("/auth/login")
async def login(credentials: LoginRequest):
    '''Route to validate user credentials'''
    is_valid = validate_credentials(credentials.username, credentials.password)
    
    if not is_valid:
        # Use an HTTP status code 401 (Unauthorized) to indicate that the credentials are invalid
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # If the credentials are valid, get the user data
    user_data = get_user(credentials.username)

    return {
        'message': f"Login successful for user: {credentials.username}",
        'status': 'success',
        'user': {
            'username': user_data['username'],
            'email': user_data.get('email'),
            'balance': user_data.get('balance'),
        }
    }

@app.get("/wallet/status/{username}")
async def get_wallet_status(username: str):
    '''Route to get the wallet status for a user'''
    user_data = get_user(username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    history = get_transaction_history(username)
    current_balance = calculate_balance(history, float(user_data['balance']), username)

    return {
        'status': 'success',
        'username': username,
        'balance': current_balance,
        'history_count': len(history),
    }
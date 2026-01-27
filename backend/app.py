from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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
    return {
        'message': f"Login request received for user: {credentials.username}",
        'status': 'success',
        'user_received': credentials.username
    }
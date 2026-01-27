from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Proggy Wallet API",
    description="API for the Proggy Wallet application",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development purposes, we allow all origins
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)

@app.get("/")
async def root():
    '''Route to check if the API is running'''
    return {'message': 'Welcome to the Proggy Wallet API',
            'status': 'online',
            'docs': '/docs',
    }

@app.get("health")
async def health_check():
    '''Route to check if the API is running'''
    return {'status': 'healthy'}
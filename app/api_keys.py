import secrets
from fastapi import Header, HTTPException
from app.redis_client import r

PREFIX = "apikey:"

def generate_api_key() -> str:
    return secrets.token_urlsafe(32)

def create_api_key(name: str) -> str:
    key = generate_api_key()
    r.set(f"{PREFIX}{key}", name)
    return key

def validate_api_key(x_api_key: str = Header(..., description="Your API key")):
    name = r.get(f"{PREFIX}{x_api_key}")
    if not name:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key

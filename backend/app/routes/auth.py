from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import jwt

router = APIRouter()

SECRET = "supersecret"

@router.post("/login")
def login():
    token = jwt.encode({"exp": datetime.utcnow() + timedelta(hours=1)}, SECRET, algorithm="HS256")
    return {"token": token}




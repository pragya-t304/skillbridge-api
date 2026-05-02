from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

SECRET = "mysecretkey"
security = HTTPBearer()

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm="HS256")

def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta
from app.core.config import settings

SECRET_KEY=settings.SECRET_KEY
ALGORITHAM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(hours=1)
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHAM)

def decode_token(token:str):
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHAM])
    except JWTError:
        return None
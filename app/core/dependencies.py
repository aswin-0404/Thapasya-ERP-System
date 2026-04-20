from fastapi import Depends,HTTPException,Request
from jose import JWTError,jwt
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.config import SECRET_KEY,ALGORITHM


SECRET_KEY=SECRET_KEY
ALGORITHM=ALGORITHM

def get_current_user(request:Request ,db : Session = Depends(get_db)):

    token=request.cookies.get("access_token")

    if not token :
        raise HTTPException(status_code=401,detail="Not Authenticated")
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        user_id=payload.get("user_id")
        role=payload.get("role_id")

       
        
    except JWTError:
        raise HTTPException (status_code=401,detail="Token error")
    
    if role == 2:
        user= db.query(User).filter(User.id==user_id).first()

    elif role== 3:
        user= db.query(User).filter(User.id==user_id).first()

    elif role==1:
        user= db.query(User).filter(User.id==user_id).first()
        
    else:
        raise HTTPException(status_code=401, detail="Role Not Found")

    if not user:
        raise HTTPException(status_code=401,detail="User Not Found")
    
    return user


def get_current_admin( current_user=Depends(get_current_user)):
    if current_user.role_id !=1:
        raise HTTPException(status_code=403,detail="Admin only")
    return current_user


def check_admin_role(db, current_admin):
    admin=db.query(User).filter(User.id == current_admin.id).first()
    return admin.role.name

def check_user_role(db ,current_user):
    user=db.query(User).filter(User.id == current_user.id).first()
    return user.role.name

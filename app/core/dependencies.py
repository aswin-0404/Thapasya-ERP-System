from fastapi import Depends,HTTPException,Request
from jose import JWTError,jwt
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.staff import Staff
from app.models.student import Student
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
        user= db.query(Staff).filter(Staff.user_id==user_id).first()

    elif role== 1:
        user= db.query(Student).filter(Student.user_id==user_id).first()
    
    else:
        raise HTTPException(status_code=401, detail="Role Not FOund")

    if not user:
        raise HTTPException(status_code=401,detail="User Not Found")
    
    return user




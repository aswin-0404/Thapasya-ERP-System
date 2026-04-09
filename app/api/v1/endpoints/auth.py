from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginSchema
from app.services.auth_service import login_user
from app.db.session import get_db

router=APIRouter()

@router.post("/login")
def login(data: LoginSchema , db: Session=Depends(get_db)):
    try:
        return login_user(db,data)
    except Exception as e:
        raise HTTPException (status_code=400,detail=str(e))
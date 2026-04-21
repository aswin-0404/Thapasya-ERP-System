from fastapi import APIRouter,Depends,HTTPException,Response
from sqlalchemy.orm import Session
from app.schemas.auth import LoginSchema
from app.services.auth_service import login_user
from app.db.session import get_db

router=APIRouter()

@router.post("/login")
def login(data: LoginSchema ,response:Response, db: Session=Depends(get_db)):
    try:
        result= login_user(db,data)

        response.set_cookie(
        key="access_token",
        value=result["token"],
        httponly=True,
        secure=False,
        samesite="Lax"
    )
        
        return{
            "message":"Login succesfull!",
            "role":result["role"]
        }
    except Exception as e:
        raise HTTPException (status_code=400,detail=str(e))
    
@router.post('/logout')
def logout(response:Response):
    try:
        response.delete_cookie(
            key="access_token",
            httponly=True
        )
        return {"message":"Logout successful"}
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
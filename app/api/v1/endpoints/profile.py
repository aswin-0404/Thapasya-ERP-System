from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session

from app.services.profile_service import get_profile
from app.db.session import get_db
from app.core.dependencies import get_current_user

router=APIRouter(prefix='/get_profile',tags=["Profile"])

@router.get('/')
def get_user_profile(db : Session=Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return get_profile(db,current_user)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
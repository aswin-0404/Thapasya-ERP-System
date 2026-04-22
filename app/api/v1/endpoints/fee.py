from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.services.fee_service import generate_next_month_fee

router=APIRouter(prefix=('/fee'),tags=["Fees Apis"])

@router.post('/createfees')
def schedule_fee(db : Session = Depends(get_db),current_admin = Depends(get_current_admin)):
    try:
        return generate_next_month_fee(db,current_admin)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
from fastapi import  APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.schemas.masters import BranchCreate
from app.db.session import get_db
from app.services.branch_service import create_branch_service

router=APIRouter(prefix='/branches',tags=['Branches'])

@router.post("/")
def create_branch(data : BranchCreate ,db :Session=Depends(get_db),current_admin= Depends(get_current_admin)):
    try:
        return create_branch_service(data, db, current_admin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
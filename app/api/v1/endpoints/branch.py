from fastapi import  APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.schemas.masters import BranchCreate
from app.db.session import get_db
from app.models.branch import Branch

router=APIRouter(prefix='/branches',tags=['Branches'])

@router.post("/")
def create_branch(data : BranchCreate ,db :Session=Depends(get_db),admin= Depends(get_current_admin)):

    existing=db.query(Branch).filter(Branch.name == data.name ).first()
    if existing:
        raise HTTPException(status_code=400,detail="Branch already exist")
    
    branch=Branch(
        name = data.name,
        location = data.location
    )

    db.add(branch)
    db.commit()
    db.refresh(branch)

    return branch
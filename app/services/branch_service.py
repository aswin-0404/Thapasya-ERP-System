from sqlalchemy.orm import Session
from app.models.branch import Branch
from app.models.user import User
from fastapi import HTTPException
from app.core.dependencies import check_admin_role

def create_branch_service(data, db:Session, current_admin):

    role=check_admin_role(db,current_admin)
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin can only access")
    
    branch=Branch(
        name = data.name,
        location = data.location
    )
    db.add(branch)
    db.commit()
    db.refresh(branch)

    return branch


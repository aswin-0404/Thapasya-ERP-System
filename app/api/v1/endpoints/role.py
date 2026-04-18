from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.role import Role
from app.schemas.masters import RoleCreate
from app.core.dependencies import get_current_admin


router=APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/")
def create_role(data : RoleCreate, db : Session=Depends(get_db),admin=Depends(get_current_admin)):

    existing=db.query(Role).filter(Role.name == data.name).first()

    if existing:
        raise HTTPException(status_code=400,detail="Role already exist")
    
    role=Role(name=data.name)

    db.add(role)
    db.commit()
    db.refresh(role)

    return role

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.masters import RoleCreate
from app.core.dependencies import get_current_admin
from app.services.role_service import role_create_service


router=APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/")
def create_role(data : RoleCreate, db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):

    return role_create_service(data,db,current_admin)
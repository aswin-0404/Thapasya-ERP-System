from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.role import Role
from app.core.dependencies import check_admin_role

def role_create_service(data, db : Session, current_admin):

    role=check_admin_role(db,current_admin)
    if role != "admin":
        raise HTTPException(status_code=403,detail="Admin only can access")
    
    existing=db.query(Role).filter(Role.name == data.name).first()

    if existing:
        raise HTTPException(status_code=400,detail="Role already exist")
    
    role=Role(name=data.name)

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


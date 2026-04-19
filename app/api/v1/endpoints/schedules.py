from fastapi import APIRouter,Depends
from sqlalchemy.orm  import Session

from app.schemas.schedule import ScheduleCreate
from app.db.session import get_db
from app.core.dependencies import get_current_admin
from app.services.schedule_service import create_schedule_service

router=APIRouter(prefix="/class_schedule",tags=["Class Schedule"])

@router.post("/")
def create_schedule(data : ScheduleCreate, db : Session=Depends(get_db),admin=Depends(get_current_admin)):
    return create_schedule_service(data,db)
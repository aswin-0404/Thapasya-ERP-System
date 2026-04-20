from fastapi import APIRouter,Depends
from sqlalchemy.orm  import Session

from app.schemas.schedule import ScheduleCreate
from app.db.session import get_db
from app.core.dependencies import get_current_admin,get_current_user
from app.services.schedule_service import create_schedule_service
from app.services.schedule_service import get_upcoming_schedule_service

router=APIRouter(prefix="/class_schedule",tags=["Class Schedule"])

@router.post("/")
def create_schedule(data : ScheduleCreate, db : Session=Depends(get_db),current_admin=Depends(get_current_admin)):
    return create_schedule_service(data,db)

@router.get('/get_schedule')
def get_schedule(course_id : int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    return get_upcoming_schedule_service(course_id, db, current_user)


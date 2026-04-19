from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.daily_log import DailyLog
from app.schemas.daily_log import DailyLogCreate
from app.core.dependencies import get_current_user
from app.models.staff import Staff
from datetime import date


router = APIRouter(prefix="/daily_log",tags=["DailyLog"])

@router.post("/")
def create_daily_log(data : DailyLogCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    staff = db.query(Staff).filter(Staff.user_id == current_user.id).first()

    if not staff:
        raise HTTPException(status_code=403,detail="Not a staff")
    

    existing = db.query(DailyLog).filter(
    DailyLog.date == date.today(),
    DailyLog.course_id == data.course_id,
    DailyLog.staff_id == staff.id).first()

    if existing:
        raise HTTPException(400, "Log already exists for this class today")
    
    log= DailyLog(
        staff_id=staff.id,
        course_id=data.course_id,
        class_summary=data.class_summary,
        topics_covered=data.topics_covered,
        next_class_topic=data.next_class_topic
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log
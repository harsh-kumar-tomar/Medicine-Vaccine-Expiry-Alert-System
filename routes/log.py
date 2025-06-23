from fastapi import  APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import DBAuditLogItem

router = APIRouter()

@router.get("/audit-logs")
def get_aduit_logs(db: Session = Depends(get_db)):
    return db.query(DBAuditLogItem).all()

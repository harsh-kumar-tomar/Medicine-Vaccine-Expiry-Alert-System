from fastapi import  HTTPException , APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import DBMedicineItem ,MedicineStatus
from schema import MedicineCreateSchema

router = APIRouter()


@router.post("/")
def add_medicines( medicine_list:list[MedicineCreateSchema], db: Session = Depends(get_db)):
    db_items = []
    try:
        for med  in medicine_list:
            db_items.append(DBMedicineItem(**med.model_dump()))
        db.add_all(db_items)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400,detail="Duplicate batch number found.")

    return medicine_list


# return all the medicines present in db
@router.get("/")
def add_medicines( db: Session = Depends(get_db)):
    return db.query(DBMedicineItem).all()

# return only medicines that are near expiry date
@router.get("/near-expiry")
def get_medicines_near_expiry(db: Session = Depends(get_db)):
    return db.query(DBMedicineItem).filter(DBMedicineItem.status == MedicineStatus.EXPIRED).all()


# return status of medicine 
@router.put("/{id}/{status}")
def update_status():
    pass 
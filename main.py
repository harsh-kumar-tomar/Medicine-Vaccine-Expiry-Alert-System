from fastapi import  FastAPI , HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import SessionLocal , engine
from models import Base , DBAuditLogItem , DBMedicineItem ,DBUserItem , MedicineStatus
from schema import UserRegisterSchema , UserLoginSchema , MedicineCreateSchema

app = FastAPI()

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message":"server is running"}

# to register new user
@app.post("/register")
def register_user(user:UserRegisterSchema,db: Session = Depends(get_db)):
    db_item = DBUserItem(**user.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"name":user.name}


# to login user
@app.post("/login")
def login_user(user:UserLoginSchema,db: Session = Depends(get_db)):
    db_item = db.query(DBUserItem).filter((DBUserItem.email == user.email) & (DBUserItem.password == user.password)).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail="no user found")
    return db_item
    

@app.post("/medicines")
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
@app.get("/medicines")
def add_medicines( db: Session = Depends(get_db)):
    return db.query(DBMedicineItem).all()

# return only medicines that are near expiry date
@app.get("/near-expiry")
def get_medicines_near_expiry(db: Session = Depends(get_db)):
    return db.query(DBMedicineItem).filter(DBMedicineItem.status == MedicineStatus.EXPIRED).all()
    

# return status of medicine 
@app.put("/medicines/{id}/{status}")
def update_status():
    pass 

@app.get("/audit-logs")
def get_aduit_logs(db: Session = Depends(get_db)):
    return db.query(DBAuditLogItem).all()

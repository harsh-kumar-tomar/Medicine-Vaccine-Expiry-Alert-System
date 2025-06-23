from fastapi import  HTTPException , Header , APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import DBUserItem
from schema import UserRegisterSchema , UserLoginSchema
from session_manager import create_session,get_current_user
from utils import hash_password,verify_password
from redis_client import redis_client

router = APIRouter()

@router.post("/register")
def register_user(user:UserRegisterSchema,db: Session = Depends(get_db)):
    
    check = db.query(DBUserItem).filter(DBUserItem.email == user.email).first()
    
    if check:
        raise HTTPException(status_code=404,detail="User already exists")   
     
    user_data = user.model_dump()
    user_data["password"] = hash_password(user_data["password"]) 
    
    db_item = DBUserItem(**user_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"status":"Success"}

@router.post("/login")
def login_user(user:UserLoginSchema,db: Session = Depends(get_db)):
    
    db_item = db.query(DBUserItem).filter(DBUserItem.email == user.email).first()
    
    if not db_item :
        raise HTTPException(status_code=401,detail="Invalid email or password")
    
    if not verify_password(user.password,db_item.password):
        raise HTTPException(status_code=401,detail="Invalid email or password")

    session_id = create_session(db_item.id)
        
    return {"status":"Success","session_id":f"{session_id}"}

@router.post("/logout")
def logout(user_id = Depends(get_current_user) , session_token = Header(...)):
    redis_client.delete(f"session:{session_token}")
    return {"status":"Logged out successfully"}
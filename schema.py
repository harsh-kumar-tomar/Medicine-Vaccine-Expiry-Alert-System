from pydantic import BaseModel , EmailStr
from datetime import datetime

from models import MedicineStatus

    
class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str 

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class MedicineCreateSchema(BaseModel):
    name: str
    batch_number: str
    quantity: int
    expiry_date: datetime
    status: MedicineStatus = MedicineStatus.ACTIVE

class MedicineStatusUpdateSchema(BaseModel):
    status: MedicineStatus

class NearExpiryQuerySchema(BaseModel):
    days: int = 7

class AuditLogCreateSchema(BaseModel):
    user_id: int
    medicine_id: int
    status: MedicineStatus

class MedicineOutSchema(BaseModel):
    id: int
    name: str
    batch_number: str
    quantity: int
    expiry_date: datetime
    status: MedicineStatus

    class Config:
        orm_mode = True
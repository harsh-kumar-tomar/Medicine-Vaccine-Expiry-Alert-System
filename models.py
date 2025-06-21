from datetime import datetime
from enum import Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column , Integer, String,DateTime , Enum as SqlEnum , ForeignKey

class Base(DeclarativeBase):
    pass

class MedicineStatus(Enum):
    ACTIVE = "ACTIVE" # have stock and is not near expiry date
    USED = "USED"   # stock is empty
    EXPIRED = "EXPIRED"     # stock is expired after certain date
    TRASHED = "TRASHED"     # stock is discarded as medicine was not suitable 

class DBUserItem(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)


class DBMedicineItem(Base):
    __tablename__ = "medicines"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    batch_number = Column(String,unique=True,nullable=False)
    quantity = Column(Integer)
    expiry_date = Column(DateTime)
    status = Column(SqlEnum(MedicineStatus))

class DBAuditLogItem(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    medicine_id = Column(Integer,ForeignKey("medicines.id"))
    status = Column(SqlEnum(MedicineStatus),nullable=False)
    time_stamp = Column(DateTime,default=datetime.utcnow)


    
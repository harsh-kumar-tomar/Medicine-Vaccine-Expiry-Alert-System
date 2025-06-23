from fastapi import  FastAPI
from database import engine
from models import Base
from routes import auth,medicine,log,user

app = FastAPI()

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message":"server is running"}

app.include_router(auth.router,prefix="/auth")
app.include_router(user.router)
app.include_router(medicine.router,prefix="/medicines")
app.include_router(log.router)









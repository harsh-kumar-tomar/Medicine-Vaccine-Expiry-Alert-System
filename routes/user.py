from fastapi import  APIRouter
from fastapi.params import Depends
from session_manager import get_current_user

router = APIRouter()

@router.get("/me")
def get_me(user_id = Depends(get_current_user)):
    return {"user_id":user_id}

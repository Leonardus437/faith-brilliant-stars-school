from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_current_user

router = APIRouter()

@router.get("/")
async def list_inventory(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Inventory endpoint"}

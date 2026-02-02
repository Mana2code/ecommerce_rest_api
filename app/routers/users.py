from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import UserCreate
from ..models import User
from ..database import get_db
from ..auth import hash_password
from ..dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    return {"message": "User created"}

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

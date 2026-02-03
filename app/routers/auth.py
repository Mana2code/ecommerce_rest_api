from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..models import User
from ..schemas import UserLogin, TokenOut
from ..utils.security import verify_password
from ..utils.jwt import create_access_token
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])

from fastapi.security import OAuth2PasswordRequestForm  # <--- Add this import


async def get_login_credentials(request: Request):
    content_type = request.headers.get("Content-Type", "")

    if "application/json" in content_type:
        data = await request.json()
        # Handle cases where JSON sends 'email' OR 'username'
        email = data.get("email") or data.get("username")
        return {"username": email, "password": data.get("password")}

    elif "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        # Swagger form ALWAYS sends 'username'
        return {"username": form_data.get("username"), "password": form_data.get("password")}

    raise HTTPException(status_code=415, detail="Unsupported Media Type")


# Import this

@router.post("/login", response_model=TokenOut)
async def login_user(
        body: Optional[UserLogin] = None,
        credentials: dict = Depends(get_login_credentials),  # Use only this
        db: Session = Depends(get_db)
):
    email = credentials.get("username") or body.email
    password = credentials.get("password") or body.password

    if not email or not password:
        # Explicitly return 422 if fields are missing to help debugging
        raise HTTPException(status_code=422, detail="Missing email or password")

    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not email or not password:
        raise HTTPException(status_code=422, detail="Missing email or password")

    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from app.services.jwt import create_access_token, create_refresh_token
from app.models.refresh_token import RefreshToken
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.dependencies.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/request-otp")
def request_otp(phone: str):
    return {"status": "otp sent"}

@router.post("/verify-otp")
def verify_otp(phone: str, otp: str):
    return {"status": "verified"}

@router.post("/login")
def login(user_id: str, device_id: str, db: Session = Depends(get_db)):

    access = create_access_token(user_id)
    refresh = create_refresh_token()

    db.add(RefreshToken(
        user_id=user_id,
        token=refresh,
        device_id=device_id,
        expires_at=datetime.utcnow() + timedelta(days=30)
    ))
    db.commit()

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(refresh_token: str, device_id: str, db: Session = Depends(get_db)):

    row = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.device_id == device_id,
        RefreshToken.expires_at > datetime.utcnow()
    ).first()

    if not row:
        raise HTTPException(401, "Invalid refresh token")

    access = create_access_token(row.user_id)

    return {
        "access_token": access,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(refresh_token: str, device_id: str, db: Session = Depends(get_db)):

    db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.device_id == device_id
    ).delete()

    db.commit()

    return {"logged_out": True}

@router.post("/logout-all")
def logout_all(user=Depends(get_current_user), db: Session = Depends(get_db)):

    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id
    ).delete()

    db.commit()

    return {"logged_out_all": True}

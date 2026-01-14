from fastapi import Depends, HTTPException
from app.services.access import is_user_paid
from app.dependencies.auth import get_current_user

def require_paid_user(user = Depends(get_current_user)):
    if not is_user_paid(user):
        raise HTTPException(status_code=403, detail="Paid access required")
    return user

from fastapi import APIRouter

router = APIRouter()

@router.post("/request-otp")
def request_otp(phone: str):
    return {"status": "otp sent"}

@router.post("/verify-otp")
def verify_otp(phone: str, otp: str):
    return {"status": "verified"}

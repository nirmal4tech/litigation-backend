from datetime import datetime

def is_user_paid(user) -> bool:
    if not user.paid_until:
        return False
    return user.paid_until > datetime.utcnow()

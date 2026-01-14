from fastapi import FastAPI
from app.routes import meta, auth, cases, hearing, history, diary, cost

app = FastAPI(
    title="Litigation Companion API",
    version="1.0"
)

app.include_router(meta.router, prefix="/meta", tags=["Meta"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(cases.router, prefix="/cases", tags=["Cases"])
app.include_router(hearing.router, prefix="/hearing", tags=["Hearing"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(diary.router, prefix="/diary", tags=["Diary"])
app.include_router(cost.router, prefix="/cost", tags=["Cost"])
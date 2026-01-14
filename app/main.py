from fastapi import FastAPI
from app.routes import meta, auth, cases, hearing, history, diary, cost, export, retention
import os
from dotenv import load_dotenv

app = FastAPI(
    title="Litigation Companion API",
    version="1.0"
)

# This line finds the .env file and injects its values into os.environ
load_dotenv()

app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(diary.router, prefix="/diary", tags=["Diary"])
app.include_router(cost.router, prefix="/cost", tags=["Cost"])
app.include_router(hearing.router, prefix="/hearing", tags=["Hearing"])
app.include_router(cases.router, prefix="/cases", tags=["Cases"])
app.include_router(export.router, prefix="/export", tags=["Export"])
app.include_router(retention.router, prefix="/retention", tags=["Retention"])
app.include_router(meta.router, prefix="/meta", tags=["Meta"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

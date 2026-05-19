from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.database import engine
from app import models
from app.routers import surah, ayah, juz, search
from app.limiter import limiter

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quran API",
    description="Hafs an Asim — Uthmanic script Quran API",
    version="0.1.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(surah.router)
app.include_router(ayah.router)
app.include_router(juz.router)
app.include_router(search.router)

@app.get("/")
def root():
    return {
        "message": "Quran API is running",
        "version": "0.1.0",
        "riwayah": "Hafs an Asim",
        "docs": "/docs"
    }

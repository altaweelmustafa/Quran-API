from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ayah
from app.api_keys import validate_api_key
from app.limiter import limiter
from app import schemas

router = APIRouter(prefix="/v1/ayah", tags=["Ayah"])

@router.get("/{surah_id}/{ayah_number}", response_model=schemas.AyahBase)
@limiter.limit("60/minute")
def get_ayah(
    request: Request,
    surah_id: int,
    ayah_number: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(validate_api_key)
):
    ayah = db.query(Ayah).filter(
        Ayah.surah_id == surah_id,
        Ayah.ayah_number == ayah_number
    ).first()
    if not ayah:
        raise HTTPException(status_code=404, detail="Ayah not found")
    return ayah

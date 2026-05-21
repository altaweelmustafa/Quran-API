from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import unicodedata

from app import schemas
from app.api_keys import validate_api_key
from app.database import get_db
from app.limiter import limiter
from app.models import Ayah

BISMILLAH = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"

router = APIRouter(prefix="/v1/ayah", tags=["Ayah"])


def strip_bismillah(text: str) -> str:
    normalized_text     = unicodedata.normalize('NFC', text)
    normalized_bismillah = unicodedata.normalize('NFC', BISMILLAH)
    return normalized_text.replace(normalized_bismillah, '').strip()

@router.get("/{surah_id}/{ayah_number}", response_model=schemas.AyahBase)
@limiter.limit("60/minute")
def get_ayah(
    request: Request,
    surah_id: int,
    ayah_number: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(validate_api_key),
):
    ayah = (
        db.query(Ayah)
        .filter(Ayah.surah_id == surah_id, Ayah.ayah_number == ayah_number)
        .first()
    )
    if not ayah:
        raise HTTPException(status_code=404, detail="Ayah not found")

    print("REACHED STRIP CHECK")
    print(repr(ayah.text_uthmani[:80]))
    print(repr(BISMILLAH))
    print("IN:", BISMILLAH in ayah.text_uthmani)

    if ayah_number == 1 and surah_id not in (1, 9):
        ayah.text_uthmani = strip_bismillah(ayah.text_uthmani)
        ayah.text_simple  = strip_bismillah(ayah.text_simple)
    return ayah

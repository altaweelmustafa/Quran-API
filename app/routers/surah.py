from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import schemas
from app.api_keys import validate_api_key
from app.database import get_db
from app.dependencies import pagination
from app.limiter import limiter
from app.models import Ayah, Surah

router = APIRouter(prefix="/v1/surah", tags=["Surah"])


@router.get("/", response_model=list[schemas.SurahBase])
@limiter.limit("60/minute")
def get_all_surahs(
    request: Request,
    db: Session = Depends(get_db),
    pages: dict = Depends(pagination),
    api_key: str = Depends(validate_api_key),
):
    return (
        db.query(Surah)
        .order_by(Surah.id)
        .offset(pages["offset"])
        .limit(pages["limit"])
        .all()
    )


@router.get("/{surah_id}", response_model=schemas.SurahBase)
@limiter.limit("60/minute")
def get_surah(
    request: Request,
    surah_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(validate_api_key),
):
    surah = db.query(Surah).filter(Surah.id == surah_id).first()
    if not surah:
        raise HTTPException(status_code=404, detail="Surah not found")
    return surah


@router.get("/{surah_id}/ayat", response_model=list[schemas.AyahBase])
@limiter.limit("60/minute")
def get_surah_ayat(
    request: Request,
    surah_id: int,
    db: Session = Depends(get_db),
    pages: dict = Depends(pagination),
    api_key: str = Depends(validate_api_key),
):
    surah = db.query(Surah).filter(Surah.id == surah_id).first()
    if not surah:
        raise HTTPException(status_code=404, detail="Surah not found")
    return (
        db.query(Ayah)
        .filter(Ayah.surah_id == surah_id)
        .order_by(Ayah.ayah_number)
        .offset(pages["offset"])
        .limit(pages["limit"])
        .all()
    )

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import schemas
from app.api_keys import validate_api_key
from app.database import get_db
from app.dependencies import pagination
from app.limiter import limiter
from app.models import Ayah

router = APIRouter(prefix="/v1", tags=["Juz & Hizb"])

@router.get("/juz/{juz_number}", response_model=list[schemas.AyahBase])
@limiter.limit("60/minute")
def get_juz(
    request: Request,
    juz_number: int,
    db: Session = Depends(get_db),
    pages: dict = Depends(pagination),
    api_key: str = Depends(validate_api_key)
):
    if juz_number < 1 or juz_number > 30:
        raise HTTPException(status_code=400, detail="Juz number must be between 1 and 30")
    return db.query(Ayah).filter(
        Ayah.juz_number == juz_number
    ).order_by(Ayah.id).offset(pages["offset"]).limit(pages["limit"]).all()

@router.get("/hizb/{hizb_number}", response_model=list[schemas.AyahBase])
@limiter.limit("60/minute")
def get_hizb(
    request: Request,
    hizb_number: int,
    db: Session = Depends(get_db),
    pages: dict = Depends(pagination),
    api_key: str = Depends(validate_api_key)
):
    if hizb_number < 1 or hizb_number > 60:
        raise HTTPException(status_code=400, detail="Hizb number must be between 1 and 60")
    return db.query(Ayah).filter(
        Ayah.hizb_number == hizb_number
    ).order_by(Ayah.id).offset(pages["offset"]).limit(pages["limit"]).all()

@router.get("/page/{page_number}", response_model=list[schemas.AyahBase])
@limiter.limit("60/minute")
def get_page(
    request: Request,
    page_number: int,
    db: Session = Depends(get_db),
    pages: dict = Depends(pagination),
    api_key: str = Depends(validate_api_key)
):
    if page_number < 1 or page_number > 604:
        raise HTTPException(status_code=400, detail="Page number must be between 1 and 604")
    return db.query(Ayah).filter(
        Ayah.page_number == page_number
    ).order_by(Ayah.id).offset(pages["offset"]).limit(pages["limit"]).all()

@router.get("/rub/{rub_number}", response_model=list[schemas.AyahBase])
def get_rub(
    rub_number: int,
    db: Session = Depends(get_db),
    pages: dict = Depends(pagination)
):
    if rub_number < 1 or rub_number > 240:
        raise HTTPException(status_code=400, detail="Rub number must be between 1 and 240")
    return db.query(Ayah).filter(
        Ayah.rub_number == rub_number
    ).order_by(Ayah.id).offset(pages["offset"]).limit(pages["limit"]).all()

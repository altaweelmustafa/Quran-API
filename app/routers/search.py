from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app import schemas
from app.api_keys import validate_api_key
from app.database import get_db
from app.dependencies import pagination
from app.limiter import limiter
from app.models import Ayah

router = APIRouter(prefix="/v1", tags=["Search"])


@router.get("/search", response_model=list[schemas.AyahBase])
@limiter.limit("60/minute")
def search_ayat(
    request: Request,
    q: str = Query(..., min_length=2, description="Search query in Arabic"),
    db: Session = Depends(get_db),
    pages: dict = Depends(pagination),
    api_key: str = Depends(validate_api_key),
):
    results = (
        db.query(Ayah)
        .filter(Ayah.text_simple.contains(q))
        .offset(pages["offset"])
        .limit(pages["limit"])
        .all()
    )
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return results

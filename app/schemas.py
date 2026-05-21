from pydantic import BaseModel
from typing import List, Optional

class SurahBase(BaseModel):
    id: int
    name_arabic: str
    name_transliteration: str
    name_english: str
    revelation_type: str
    ayah_count: int
    chronological_order: int
    bismillah: Optional[str] = None

    class Config:
        from_attributes = True

class AyahBase(BaseModel):
    id: int
    surah_id: int
    ayah_number: int
    juz_number: int
    hizb_number: int
    page_number: int
    text_uthmani: str
    text_simple: str
    sajdah: bool
    rub_number: Optional[int] = None
    font_recommendation: str = "KFGQPC Uthman Taha Naskh"

    class Config:
        from_attributes = True

class SurahDetail(SurahBase):
    ayat: List[AyahBase] = []

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Surah(Base):
    __tablename__ = "surahs"

    id = Column(Integer, primary_key=True, index=True)  # 1-114
    name_arabic = Column(String, nullable=False)
    name_transliteration = Column(String, nullable=False)
    name_english = Column(String, nullable=False)
    revelation_type = Column(String, nullable=False)  # makki or madani
    ayah_count = Column(Integer, nullable=False)
    juz_start = Column(Integer, nullable=False)
    chronological_order = Column(Integer, nullable=False)
    bismillah = Column(String, nullable=True)

    ayat = relationship("Ayah", back_populates="surah")


class Ayah(Base):
    __tablename__ = "ayat"

    id = Column(Integer, primary_key=True, index=True)
    surah_id = Column(Integer, ForeignKey("surahs.id"), nullable=False)
    ayah_number = Column(Integer, nullable=False)
    juz_number = Column(Integer, nullable=False)
    hizb_number = Column(Integer, nullable=False)
    rub_number = Column(Integer, nullable=True)
    page_number = Column(Integer, nullable=False)
    text_uthmani = Column(Text, nullable=False)
    text_simple = Column(Text, nullable=False)
    sajdah = Column(Boolean, default=False)

    surah = relationship("Surah", back_populates="ayat")
    words = relationship("Word", back_populates="ayah")


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    ayah_id = Column(Integer, ForeignKey("ayat.id"), nullable=False)
    position = Column(Integer, nullable=False)
    text_uthmani = Column(Text, nullable=False)
    text_simple = Column(Text, nullable=False)
    root = Column(String, nullable=True)  # Arabic root, optional for now

    ayah = relationship("Ayah", back_populates="words")

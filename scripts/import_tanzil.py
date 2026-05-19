import os
import sys
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Surah, Ayah

UTHMANI_FILE = "scripts/quran-uthmani.txt"
SIMPLE_FILE = "scripts/quran-simple.txt"
META_FILE = "scripts/quran-data.xml"


def parse_text_file(filepath):
    """Returns dict: {(surah, ayah): text}"""
    data = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) != 3:
                continue
            surah, ayah, text = int(parts[0]), int(parts[1]), parts[2]
            data[(surah, ayah)] = text
    return data


def parse_meta(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    meta = {}

    juz_starts = {}
    for juz in root.find("juzs"):
        sura = int(juz.get("sura"))
        aya = int(juz.get("aya"))
        num = int(juz.get("index"))
        juz_starts[(sura, aya)] = num

    hizb_starts = {}
    for hizb in root.find("hizbs"):
        sura = int(hizb.get("sura"))
        aya = int(hizb.get("aya"))
        num = int(hizb.get("index"))
        hizb_starts[(sura, aya)] = num

    page_starts = {}
    for page in root.find("pages"):
        sura = int(page.get("sura"))
        aya = int(page.get("aya"))
        num = int(page.get("index"))
        page_starts[(sura, aya)] = num

    sajdah_set = set()
    sajdas_el = root.find("sajdas")
    if sajdas_el is not None:
        for sajdah in sajdas_el:
            sura = int(sajdah.get("sura"))
            aya = int(sajdah.get("aya"))
            sajdah_set.add((sura, aya))

    juz_num = hizb_num = page_num = 1

    for sura_el in root.find("suras"):
        sura_id = int(sura_el.get("index"))
        ayah_count = int(sura_el.get("ayas"))
        for aya_num in range(1, ayah_count + 1):
            key = (sura_id, aya_num)
            if key in juz_starts:
                juz_num = juz_starts[key]
            if key in hizb_starts:
                hizb_num = hizb_starts[key]
            if key in page_starts:
                page_num = page_starts[key]
            meta[key] = {
                "juz": juz_num,
                "hizb": hizb_num,
                "page": page_num,
                "sajdah": key in sajdah_set,
            }

    return meta


def import_surahs():
    tree = ET.parse(META_FILE)
    root = tree.getroot()

    db = SessionLocal()
    try:
        for sura_el in root.find("suras"):
            surah = Surah(
                id=int(sura_el.get("index")),
                name_arabic=sura_el.get("name"),
                name_transliteration=sura_el.get("tname"),
                name_english=sura_el.get("ename"),
                revelation_type=sura_el.get("type"),
                ayah_count=int(sura_el.get("ayas")),
                juz_start=0,  # we can update this later
                chronological_order=int(sura_el.get("order")),
            )
            db.add(surah)
        db.commit()
        print("Successfully imported 114 surahs.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


def import_ayat():
    uthmani = parse_text_file(UTHMANI_FILE)
    simple = parse_text_file(SIMPLE_FILE)
    meta = parse_meta(META_FILE)

    db = SessionLocal()
    count = 0

    try:
        for (surah, ayah_num), text_u in uthmani.items():
            key = (surah, ayah_num)
            m = meta.get(key, {})
            text_s = simple.get(key, "")

            ayah = Ayah(
                surah_id=surah,
                ayah_number=ayah_num,
                juz_number=m.get("juz", 0),
                hizb_number=m.get("hizb", 0),
                page_number=m.get("page", 0),
                text_uthmani=text_u,
                text_simple=text_s,
                sajdah=m.get("sajdah", False),
            )
            db.add(ayah)
            count += 1

        db.commit()
        print(f"Successfully imported {count} ayat.")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import_surahs()
    import_ayat()

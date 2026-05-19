import sys
import os
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Surah, Ayah

META_FILE = "scripts/quran-data.xml"

BISMILLAH = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"

# Surah 1: bismillah is ayah 1 itself, not a prefix
# Surah 9: no bismillah at all
# All others: bismillah is a prefix before ayah 1

def update_surahs():
    tree = ET.parse(META_FILE)
    root = tree.getroot()

    # Build juz_start lookup: surah_id -> juz_number
    juz_starts = {}
    for juz in root.find("juzs"):
        sura = int(juz.get("sura"))
        num = int(juz.get("index"))
        if sura not in juz_starts:
            juz_starts[sura] = num

    db = SessionLocal()
    try:
        surahs = db.query(Surah).all()
        for surah in surahs:
            # juz_start: find which juz this surah starts in
            # walk backwards from surah id to find the closest juz boundary
            juz_num = 1
            for s_id in range(surah.id, 0, -1):
                if s_id in juz_starts:
                    juz_num = juz_starts[s_id]
                    break

            surah.juz_start = juz_num

            # bismillah handling
            if surah.id == 9:
                surah.bismillah = None  # no bismillah
            elif surah.id == 1:
                surah.bismillah = None  # it's part of the ayat, not a prefix
            else:
                surah.bismillah = BISMILLAH

        db.commit()
        print("Successfully updated 114 surahs with juz_start and bismillah.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_surahs()

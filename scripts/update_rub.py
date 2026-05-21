import sys
import os
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Ayah

META_FILE = "scripts/quran-data.xml"

def update_rub():
    tree = ET.parse(META_FILE)
    root = tree.getroot()

    # Parse rub boundaries
    rub_starts = {}
    for rub in root.find("rubs"):
        sura = int(rub.get("sura"))
        aya  = int(rub.get("aya"))
        num  = int(rub.get("index"))
        rub_starts[(sura, aya)] = num

    # Walk all surahs and assign rub numbers
    rub_num = 1
    db = SessionLocal()
    try:
        for sura_el in root.find("suras"):
            sura_id    = int(sura_el.get("index"))
            ayah_count = int(sura_el.get("ayas"))
            for aya_num in range(1, ayah_count + 1):
                key = (sura_id, aya_num)
                if key in rub_starts:
                    rub_num = rub_starts[key]
                ayah = db.query(Ayah).filter(
                    Ayah.surah_id    == sura_id,
                    Ayah.ayah_number == aya_num
                ).first()
                if ayah:
                    ayah.rub_number = rub_num
        db.commit()
        print("Successfully updated rub numbers for all ayat.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_rub()

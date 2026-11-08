#!/usr/bin/env python3
"""Erstellt aus den "gesamt"-Fotos eines Pakets eine Kollage für Willhaben.

Aufruf:  python3 kollage.py <paketname>
Nimmt alle Stücke aus katalog.csv mit paket == <paketname> und speichert
kollagen/<paketname>.jpg (Raster, 3-5 Spalten je nach Anzahl, quadratische
Kacheln, Stücknummer links oben zum Sortieren).
"""
import csv
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

BASIS = Path(__file__).parent
BREITE = 2000
ABSTAND = 10


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    paket = sys.argv[1]

    with open(BASIS / "katalog.csv", newline="", encoding="utf-8") as f:
        stuecke = [z for z in csv.DictReader(f) if z["paket"] == paket]
    if not stuecke:
        sys.exit(f"Keine Stücke mit paket = {paket!r} in katalog.csv")

    spalten = min(len(stuecke), 3 if len(stuecke) <= 9 else 4 if len(stuecke) <= 16 else 5)
    kachel_px = (BREITE - (spalten + 1) * ABSTAND) // spalten
    schrift = ImageFont.load_default(size=kachel_px // 10)
    zeilen = math.ceil(len(stuecke) / spalten)
    breite = spalten * kachel_px + (spalten + 1) * ABSTAND
    hoehe = zeilen * kachel_px + (zeilen + 1) * ABSTAND
    kollage = Image.new("RGB", (breite, hoehe), "white")

    for i, stueck in enumerate(stuecke):
        with Image.open(BASIS / "fotos" / "komprimiert" / stueck["foto_gesamt"]) as bild:
            kachel = ImageOps.fit(bild.convert("RGB"), (kachel_px, kachel_px))
        x = ABSTAND + (i % spalten) * (kachel_px + ABSTAND)
        y = ABSTAND + (i // spalten) * (kachel_px + ABSTAND)
        kollage.paste(kachel, (x, y))
        zeichnen = ImageDraw.Draw(kollage)
        zeichnen.rectangle((x, y, x + kachel_px // 4, y + kachel_px // 8), fill="white")
        zeichnen.text((x + 6, y + 2), stueck["id"], fill="black", font=schrift)

    ziel = BASIS / "kollagen" / f"{paket}.jpg"
    kollage.save(ziel, "JPEG", quality=85, optimize=True)
    print(f"{len(stuecke)} Stücke -> {ziel}")


if __name__ == "__main__":
    main()

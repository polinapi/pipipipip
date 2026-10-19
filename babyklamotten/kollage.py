#!/usr/bin/env python3
"""Erstellt aus den "gesamt"-Fotos eines Pakets eine Kollage für Willhaben.

Aufruf:  python3 kollage.py <paketname>
Nimmt alle Stücke aus katalog.csv mit paket == <paketname> und speichert
kollagen/<paketname>.jpg (Raster, max. 3 Spalten, quadratische Kacheln).
"""
import csv
import math
import sys
from pathlib import Path

from PIL import Image, ImageOps

BASIS = Path(__file__).parent
KACHEL = 600
ABSTAND = 10


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    paket = sys.argv[1]

    with open(BASIS / "katalog.csv", newline="", encoding="utf-8") as f:
        stuecke = [z for z in csv.DictReader(f) if z["paket"] == paket]
    if not stuecke:
        sys.exit(f"Keine Stücke mit paket = {paket!r} in katalog.csv")

    spalten = min(3, len(stuecke))
    zeilen = math.ceil(len(stuecke) / spalten)
    breite = spalten * KACHEL + (spalten + 1) * ABSTAND
    hoehe = zeilen * KACHEL + (zeilen + 1) * ABSTAND
    kollage = Image.new("RGB", (breite, hoehe), "white")

    for i, stueck in enumerate(stuecke):
        with Image.open(BASIS / "fotos" / "komprimiert" / stueck["foto_gesamt"]) as bild:
            kachel = ImageOps.fit(bild.convert("RGB"), (KACHEL, KACHEL))
        x = ABSTAND + (i % spalten) * (KACHEL + ABSTAND)
        y = ABSTAND + (i // spalten) * (KACHEL + ABSTAND)
        kollage.paste(kachel, (x, y))

    ziel = BASIS / "kollagen" / f"{paket}.jpg"
    kollage.save(ziel, "JPEG", quality=85, optimize=True)
    print(f"{len(stuecke)} Stücke -> {ziel}")


if __name__ == "__main__":
    main()

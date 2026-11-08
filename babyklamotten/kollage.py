#!/usr/bin/env python3
"""Erstellt aus den "gesamt"-Fotos eines Pakets Kollagen für Willhaben.

Aufruf:  python3 kollage.py <paketname>
Nimmt alle Stücke aus katalog.csv mit paket == <paketname> und speichert
kollagen/<paketname>_1.jpg, _2.jpg, … (je max. 9 Stück, 3x3-Raster,
quadratische Kacheln). Bearbeitete Fotos aus fotos/bearbeitet/ werden
bevorzugt, sonst die aus fotos/komprimiert/.
"""
import csv
import math
import sys
from pathlib import Path

from PIL import Image, ImageOps

BASIS = Path(__file__).parent
KACHEL = 600
ABSTAND = 10
PRO_KOLLAGE = 9


def foto_pfad(name: str) -> Path:
    bearbeitet = BASIS / "fotos" / "bearbeitet" / name
    return bearbeitet if bearbeitet.exists() else BASIS / "fotos" / "komprimiert" / name


def kollage(stuecke: list, ziel: Path) -> None:
    spalten = min(3, len(stuecke))
    zeilen = math.ceil(len(stuecke) / spalten)
    breite = spalten * KACHEL + (spalten + 1) * ABSTAND
    hoehe = zeilen * KACHEL + (zeilen + 1) * ABSTAND
    bild_gesamt = Image.new("RGB", (breite, hoehe), "white")
    for i, stueck in enumerate(stuecke):
        with Image.open(foto_pfad(stueck["foto_gesamt"])) as bild:
            kachel = ImageOps.pad(bild.convert("RGB"), (KACHEL, KACHEL), color="white")
        x = ABSTAND + (i % spalten) * (KACHEL + ABSTAND)
        y = ABSTAND + (i // spalten) * (KACHEL + ABSTAND)
        bild_gesamt.paste(kachel, (x, y))
    bild_gesamt.save(ziel, "JPEG", quality=85, optimize=True)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    paket = sys.argv[1]

    with open(BASIS / "katalog.csv", newline="", encoding="utf-8") as f:
        stuecke = [z for z in csv.DictReader(f) if z["paket"] == paket]
    if not stuecke:
        sys.exit(f"Keine Stücke mit paket = {paket!r} in katalog.csv")
    # Gruppenfotos (mehrere Stücke, ein Foto) nur einmal zeigen
    gesehen = set()
    stuecke = [z for z in stuecke if not (z["foto_gesamt"] in gesehen or gesehen.add(z["foto_gesamt"]))]

    ordner = BASIS / "kollagen"
    for alt in ordner.glob(f"{paket}*.jpg"):
        if alt.stem == paket or alt.stem.rsplit("_", 1)[0] == paket:
            alt.unlink()
    teile = [stuecke[i:i + PRO_KOLLAGE] for i in range(0, len(stuecke), PRO_KOLLAGE)]
    for n, teil in enumerate(teile, 1):
        ziel = ordner / f"{paket}_{n}.jpg"
        kollage(teil, ziel)
        print(f"{len(teil)} Stücke -> {ziel}")


if __name__ == "__main__":
    main()

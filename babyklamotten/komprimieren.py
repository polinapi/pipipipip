#!/usr/bin/env python3
"""Komprimiert Fotos aus fotos/eingang/ nach fotos/komprimiert/.

Die Fotos werden nach Dateiname sortiert und durchnummeriert:
001_gesamt.jpg, 002_gesamt.jpg, ...
Mit --paare: 1. Foto = ganzes Stück, 2. Foto = Größenschild
(001_gesamt.jpg, 001_etikett.jpg, 002_gesamt.jpg, ...).

- Drehung laut Kamera (EXIF) wird übernommen
- längste Seite max. 1200 px, JPEG-Qualität 80
- alle Metadaten (inkl. GPS-Standort) werden entfernt

Aufruf:  python3 komprimieren.py [--start 1] [--paare]
  --start  Nummer des ersten Stücks (zum Weitermachen)
  --paare  je zwei Fotos pro Stück (gesamt + Etikett)
"""
import argparse
from pathlib import Path

from PIL import Image, ImageOps

try:  # iPhone-Fotos (HEIC), falls pillow-heif installiert ist
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

BASIS = Path(__file__).parent
EINGANG = BASIS / "fotos" / "eingang"
AUSGANG = BASIS / "fotos" / "komprimiert"
ENDUNGEN = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
MAX_SEITE = 1200
QUALITAET = 80


def komprimieren(quelle: Path, ziel: Path) -> None:
    with Image.open(quelle) as bild:
        bild = ImageOps.exif_transpose(bild).convert("RGB")
        bild.thumbnail((MAX_SEITE, MAX_SEITE))
        bild.save(ziel, "JPEG", quality=QUALITAET, optimize=True, progressive=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--paare", action="store_true")
    args = parser.parse_args()

    fotos = sorted(p for p in EINGANG.iterdir() if p.suffix.lower() in ENDUNGEN)
    if args.paare and len(fotos) % 2:
        print(f"Achtung: {len(fotos)} Fotos – ungerade Anzahl, letztes Foto hat kein Paar.")

    AUSGANG.mkdir(parents=True, exist_ok=True)
    for i, foto in enumerate(fotos):
        if args.paare:
            nummer = args.start + i // 2
            name = f"{nummer:03d}_{'gesamt' if i % 2 == 0 else 'etikett'}.jpg"
        else:
            name = f"{args.start + i:03d}_gesamt.jpg"
        ziel = AUSGANG / name
        komprimieren(foto, ziel)
        vorher, nachher = foto.stat().st_size // 1024, ziel.stat().st_size // 1024
        print(f"{foto.name} -> {name}  ({vorher} KB -> {nachher} KB)")


if __name__ == "__main__":
    main()

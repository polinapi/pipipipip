#!/usr/bin/env python3
"""Zeigt Farb- und Mädchen/Junge-Anteile aus katalog.csv.

Aufruf:  python3 statistik.py [paketname]
Ohne Paketname werden alle Stücke gezählt.
"""
import csv
import sys
from collections import Counter
from pathlib import Path

BASIS = Path(__file__).parent


def main() -> None:
    paket = sys.argv[1] if len(sys.argv) > 1 else None
    with open(BASIS / "katalog.csv", newline="", encoding="utf-8") as f:
        stuecke = [z for z in csv.DictReader(f) if paket is None or z["paket"] == paket]
    if not stuecke:
        sys.exit("Keine Stücke gefunden.")

    n = len(stuecke)
    print(f"{n} Stücke" + (f" im Paket {paket}" if paket else ""))
    for g, anzahl in Counter(z["geschlecht"] or "offen" for z in stuecke).most_common():
        print(f"  {g}: {anzahl} ({anzahl / n:.0%})")
    farben = Counter(c.strip() for z in stuecke for c in z["farbe"].replace("/", ",").split(",") if c.strip())
    print("Farben: " + ", ".join(f"{c} ({k})" for c, k in farben.most_common()))


if __name__ == "__main__":
    main()

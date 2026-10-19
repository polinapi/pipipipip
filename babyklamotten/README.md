# Babyklamotten – Katalog für Willhaben-Pakete

## Ablauf
1. Pro Stück ein Foto vom ganzen Teil, Größe als Text dazu (Größenschild-Foto optional, dann `--paare`).
2. Fotos in `fotos/eingang/` legen (oder im Chat schicken).
3. `python3 komprimieren.py` → `fotos/komprimiert/001_gesamt.jpg`, `002_gesamt.jpg`, …
   (max. 1200 px, ohne Metadaten/GPS). Weitermachen ab Stück 25: `--start 25`.
4. Claude erkennt Art, Farbe, Marke und Größe und trägt alles in `katalog.csv` ein.
5. Stücke einem Paket zuordnen (Spalte `paket`, z. B. `62-68_sommer`).
6. `python3 kollage.py 62-68_sommer` → `kollagen/62-68_sommer.jpg`

## Spalten in katalog.csv
| Spalte | Bedeutung |
|---|---|
| kategorie | Body, Strampler, Hose, Shirt, Pullover, Jacke, Schlafsack, Mütze, … |
| groesse_etikett | was auf dem Schild steht (z. B. `3-6 M`, `68`, `74/80`) |
| groesse_eu | auf EU-Größe umgerechnet (50, 56, 62, 68, 74, 80, 86, 92, …) |
| saison | Sommer / Winter / Übergang / ganzjährig |
| zustand | neu / sehr gut / gut / Gebrauchsspuren |

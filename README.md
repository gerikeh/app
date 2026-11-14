# Vendégház foglaláskezelő (app)

## Hallgató

- **Név:** Turcsány Gergő
- **Neptun-kód:** G4L2A6

## Feladat leírása

### Mit csinál a program?

Egyszerű asztali program egy kis vendégház foglalásainak rögzítésére és listázására.
A felhasználó megadja a vendég nevét, kiválasztja a szobát (3 fix szoba közül), és beírja
az érkezés és a távozás dátumát. A program kiszámolja az éjszakák számát és a szállás árát,
majd a foglalást hozzáadja a listához. A kijelölt foglalás törölhető.
A foglalások a `foglalasok.json` fájlba mentődnek, így újraindítás után is megmaradnak.

### Felhasználói leírás

- Szükséges: Python 3.8 vagy újabb (a `tkinter` a Pythonnal együtt települ)
- Külső csomagot nem kell telepíteni
- Indítás: `python main.py` (vagy PyCharmban a `main.py` futtatása)
- A dátumokat `ÉÉÉÉ-HH-NN` formában kell megadni, például `2026-12-24`

## Felépítés

### Modulok

- **Tanult modulok:** `tkinter` (grafikus felület), `datetime`, `json`, `os`
  - `datetime`: `strptime()`, `date.today()`, `date.fromisoformat()`
  - `json`: `load()`, `dump()`
- **Saját modul:** `foglalas_tg.py`

### Függvények (foglalas_tg.py)

- `datum_tg()` – szövegből dátumot készít
- `ellenoriz_tg()` – ellenőrzi a beírt adatokat
- `mentes_tg()` – a foglalásokat JSON fájlba menti
- `betoltes_tg()` – a foglalásokat betölti a JSON fájlból

### Osztályok

- **`FoglalasTG`** (foglalas_tg.py) – egy foglalás adatai
  - `ejszakak_tg()` – az éjszakák száma
  - `ar_tg()` – a szállás teljes ára
  - `szoveg_tg()` – a foglalás szövegként a listához
  - `szotar_tg()` – a foglalás szótárként a mentéshez
- **`AppTG`** (main.py) – a grafikus felület
  - `hozzaadas_tg()` – a „Hozzáadás” gomb eseménykezelője
  - `torles_tg()` – a „Törlés” gomb eseménykezelője
  - `frissites_tg()` – a lista frissítése

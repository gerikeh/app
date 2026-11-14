import json
import os
from datetime import datetime, date

SZOBAK_TG = {
    "1. szoba (2 fő)": 15000,
    "2. szoba (3 fő)": 20000,
    "3. szoba (4 fő)": 25000,
}

FAJL_TG = "foglalasok.json"


class FoglalasTG:
    def __init__(self, nev, szoba, erkezes, tavozas):
        self.nev = nev
        self.szoba = szoba
        self.erkezes = erkezes
        self.tavozas = tavozas

    def ejszakak_tg(self):
        return (self.tavozas - self.erkezes).days

    def ar_tg(self):
        return self.ejszakak_tg() * SZOBAK_TG[self.szoba]

    def szoveg_tg(self):
        return (f"{self.nev} | {self.szoba} | "
                f"{self.erkezes.strftime('%Y.%m.%d')} - {self.tavozas.strftime('%Y.%m.%d')} | "
                f"{self.ejszakak_tg()} éj | {self.ar_tg()} Ft")

    def szotar_tg(self):
        return {
            "nev": self.nev,
            "szoba": self.szoba,
            "erkezes": self.erkezes.isoformat(),
            "tavozas": self.tavozas.isoformat(),
        }


def datum_tg(szoveg):
    return datetime.strptime(szoveg.strip(), "%Y-%m-%d").date()


def ellenoriz_tg(nev, szoba, erkezes, tavozas):
    if nev.strip() == "":
        return "Add meg a vendég nevét!"
    if szoba not in SZOBAK_TG:
        return "Válassz szobát!"
    if erkezes < date.today():
        return "Az érkezés nem lehet a mai napnál korábban!"
    if tavozas <= erkezes:
        return "A távozásnak az érkezés utánra kell esnie!"
    return ""


def mentes_tg(foglalasok):
    with open(FAJL_TG, "w", encoding="utf-8") as f:
        json.dump([fo.szotar_tg() for fo in foglalasok], f, ensure_ascii=False, indent=2)


def betoltes_tg():
    if not os.path.exists(FAJL_TG):
        return []
    with open(FAJL_TG, "r", encoding="utf-8") as f:
        adatok = json.load(f)
    return [FoglalasTG(a["nev"], a["szoba"], date.fromisoformat(a["erkezes"]),
                       date.fromisoformat(a["tavozas"])) for a in adatok]
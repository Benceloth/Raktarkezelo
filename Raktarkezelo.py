# ---------------------------------
# ÁRUKÉSZLET LELTÁR PROGRAM
# Egyszerű, stabil, OneDrive-mentes
# ---------------------------------

import pandas as pd
from datetime import datetime, timedelta
import os

# Fix helyi mappa (NEM OneDrive)
BASE_DIR = r"C:\Python\Raktar"
os.makedirs(BASE_DIR, exist_ok=True)
CSV_PATH = os.path.join(BASE_DIR, "raktar.csv")


def adatbazis_letrehozas():
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=["Termék", "BATCH", "BBD"])
        df.to_csv(CSV_PATH, index=False)


def adatbevitel():
    print("\n--- Új termék hozzáadása ---")
    termek = input("Termék neve: ").strip()
    batch = input("BATCH szám: ").strip()
    bbd = input("Lejárat (ÉÉÉÉ-HH-NN vagy ÉÉÉÉ.HH.NN): ").strip()

    df = pd.read_csv(CSV_PATH)
    df.loc[len(df)] = [termek, batch, bbd]
    df.to_csv(CSV_PATH, index=False)

    print("Termék hozzáadva.")


def lejarat_ellenorzes():
    print("\n--- Leltár ellenőrzés ---")
    df = pd.read_csv(CSV_PATH)

    ma = datetime.now()
    fel_ev = ma + timedelta(days=182)
    lejart = []

    for _, sor in df.iterrows():
        datum = sor["BBD"].replace(".", "-")
        try:
            bbd = datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            print("Hibás dátum:", sor["BBD"])
            continue

        if bbd < ma:
            lejart.append(sor["Termék"])
        elif bbd <= fel_ev:
            print("Közel lejár:", sor["Termék"])

    if lejart:
        print("\nLejárt termékek:")
        for t in set(lejart):
            print("-", t)
    else:
        print("Nincs lejárt termék.")

    return lejart


def bevasarlolista(lista):
    print("\n--- Bevásárlólista ---")
    if not lista:
        print("Nincs szükség vásárlásra.")
    else:
        for t in set(lista):
            print("-", t)


def main():
    print("PROGRAM ELINDULT ✅")

    adatbazis_letrehozas()

    while True:
        print("\n==============================")
        print("Árukészlet leltár")
        print("1 - Új termék")
        print("2 - Leltár ellenőrzés")
        print("3 - Kilépés")
        print("==============================")

        v = input("Választás: ").strip()

        if v == "1":
            adatbevitel()
        elif v == "2":
            lejart = lejarat_ellenorzes()
            bevasarlolista(lejart)
        elif v == "3":
            print("Kilépés.")
            break
        else:
            print("Hibás választás.")


# --- PROGRAM INDÍTÁSA ---
main()

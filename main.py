import tkinter as tk
from tkinter import ttk, messagebox

from foglalas_tg import FoglalasTG, SZOBAK_TG, datum_tg, ellenoriz_tg, mentes_tg, betoltes_tg


class AppTG:
    def __init__(self, ablak):
        self.ablak = ablak
        self.ablak.title("app - Vendégház foglaláskezelő")
        self.ablak.resizable(False, False)
        self.foglalasok = betoltes_tg()

        urlap = tk.Frame(ablak, padx=10, pady=10)
        urlap.pack()

        tk.Label(urlap, text="Vendég neve:").grid(row=0, column=0, sticky="w")
        self.nev_mezo = tk.Entry(urlap, width=30)
        self.nev_mezo.grid(row=0, column=1, pady=2)

        tk.Label(urlap, text="Szoba:").grid(row=1, column=0, sticky="w")
        self.szoba_valaszto = ttk.Combobox(urlap, values=list(SZOBAK_TG), state="readonly", width=27)
        self.szoba_valaszto.grid(row=1, column=1, pady=2)

        tk.Label(urlap, text="Érkezés (ÉÉÉÉ-HH-NN):").grid(row=2, column=0, sticky="w")
        self.erkezes_mezo = tk.Entry(urlap, width=30)
        self.erkezes_mezo.grid(row=2, column=1, pady=2)

        tk.Label(urlap, text="Távozás (ÉÉÉÉ-HH-NN):").grid(row=3, column=0, sticky="w")
        self.tavozas_mezo = tk.Entry(urlap, width=30)
        self.tavozas_mezo.grid(row=3, column=1, pady=2)

        gombok = tk.Frame(ablak)
        gombok.pack()
        tk.Button(gombok, text="Hozzáadás", width=15, command=self.hozzaadas_tg).pack(side="left", padx=5)
        tk.Button(gombok, text="Törlés", width=15, command=self.torles_tg).pack(side="left", padx=5)

        self.lista = tk.Listbox(ablak, width=80, height=12)
        self.lista.pack(padx=10, pady=10)

        self.osszeg_cimke = tk.Label(ablak, text="")
        self.osszeg_cimke.pack(pady=(0, 10))

        self.frissites_tg()

    def hozzaadas_tg(self):
        try:
            erkezes = datum_tg(self.erkezes_mezo.get())
            tavozas = datum_tg(self.tavozas_mezo.get())
        except ValueError:
            messagebox.showerror("Hiba", "A dátumot ÉÉÉÉ-HH-NN formában add meg! (pl. 2026-12-24)")
            return
        nev = self.nev_mezo.get()
        szoba = self.szoba_valaszto.get()
        hiba = ellenoriz_tg(nev, szoba, erkezes, tavozas)
        if hiba:
            messagebox.showerror("Hiba", hiba)
            return
        uj = FoglalasTG(nev.strip(), szoba, erkezes, tavozas)
        self.foglalasok.append(uj)
        mentes_tg(self.foglalasok)
        self.frissites_tg()
        messagebox.showinfo("Siker", f"Foglalás rögzítve.\n{uj.ejszakak_tg()} éjszaka, {uj.ar_tg()} Ft")
        self.nev_mezo.delete(0, tk.END)
        self.erkezes_mezo.delete(0, tk.END)
        self.tavozas_mezo.delete(0, tk.END)

    def torles_tg(self):
        kijeloles = self.lista.curselection()
        if not kijeloles:
            messagebox.showwarning("Figyelem", "Jelölj ki egy foglalást a listában!")
            return
        if messagebox.askyesno("Törlés", "Biztosan törlöd a kijelölt foglalást?"):
            del self.foglalasok[kijeloles[0]]
            mentes_tg(self.foglalasok)
            self.frissites_tg()

    def frissites_tg(self):
        self.lista.delete(0, tk.END)
        for foglalas in self.foglalasok:
            self.lista.insert(tk.END, foglalas.szoveg_tg())
        osszesen = sum(f.ar_tg() for f in self.foglalasok)
        self.osszeg_cimke.config(text=f"Foglalások száma: {len(self.foglalasok)}   Összesen: {osszesen} Ft")


if __name__ == "__main__":
    foablak = tk.Tk()
    AppTG(foablak)
    foablak.mainloop()
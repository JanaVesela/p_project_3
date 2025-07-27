
# Elections Scraper – Výsledky voleb 2017

Projekt pro Engeto Online Python Akademii, který stahuje výsledky parlamentních voleb 2017 z webu [volby.cz](https://www.volby.cz).


# Autor

- Jana Veslá  
- Email: Janca.Vesela90@gmail.com


# Instalace

1. Vytvořte a aktivujte virtuální prostředí:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Nainstalujte požadované knihovny:

```bash
pip install -r requirements.txt
```


# Použití

Spusťte skript s dvěma argumenty:

1. URL územního celku z webu volby.cz
2. Název výstupního CSV souboru

```bash
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2103" vysledky_benesov.csv
```

---

# Výstup

CSV soubor obsahuje:

* Kód obce
* Název obce
* Počet voličů v seznamu
* Počet vydaných obálek
* Počet platných hlasů
* Počet hlasů pro jednotlivé kandidující strany

---

 Poznámky

* Program ověří správnost argumentů a v případě chyby ukončí běh s chybovou hláškou.
* Funguje pouze s odkazy na webu volby.cz.
* Výsledky jsou uloženy v zadaném CSV souboru.

---

# Struktura projektu

* `main.py` – hlavní skript
* `requirements.txt` – seznam knihoven s verzemi
* `README.md` – tato dokumentace
* `vysledky_*.csv` – výstupní soubory


Pokud budeš mít jakékoliv dotazy, napiš na můj email: [Janca.Vesela90@gmail.com](mailto:Janca.Vesela90@gmail.com)

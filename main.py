"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Jana Veslá
email: Janca.Vesela90@gmail.com
"""

import requests #Importuji knihovnu requests pro práci s http odkazy
from bs4 import BeautifulSoup as bs #Importuji knihovnu BeautifulSoup pro skrapování obsahu webových stránek
import csv
import sys


def validate_arguments(args):

    """Načte webovou stránku (URL), najde v ní tabulku s obcemi, a z každého řádku vytáhne: 
        číslo obce (kód),
        název obce,
        odkaz na podrobnosti o dané obci."""

    if len(args) != 3:
        print("Chyba: Zadejte 2 argumenty - odkaz na územní celek a název výstupního souboru.")
        sys.exit()
    if not args[1].startswith("https://") or "volby.cz" not in args[1]:
        print("Chybný odkaz. Ujistěte se, že jde o stránku z 'volby.cz'.")
        sys.exit()


def get_links(url):
    response = requests.get(url) #stáhne stránku
    soup = bs(response.text, 'html.parser')
    data = []

    rows = soup.findAll('tr') #najde všechny řádky v tabulce (každá obec = 1 řádek)
    for row in rows:
        cislo_obce = row.find('td', class_='cislo') # hledám první sloupec = číslo obce 
        nazev_obce = row.find('td', class_='overflow_name') # hledám druhý sloupec = název obce


        if cislo_obce and nazev_obce:
            link = cislo_obce.find('a')
            if link:  # Pokud odkaz existuje
                kod = link.text.strip()  # Získáme text odkazu (kód obce)
                odkaz = "https://www.volby.cz/pls/ps2017nss/" + link['href']  # Sestavíme plný odkaz
            else:
                kod = ''  # Pokud odkaz není, použijeme prázdný řetězec
                odkaz = ''

            jmeno = nazev_obce.text.strip()  # Získáme název obce
            data.append({"code": kod, "name": jmeno, "link": odkaz})  # Přidáme data do seznamu

    return data

def get_results_from_village(url):
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # základní info o obci
    kod_obce = soup.find('td', headers='sa1').text.strip()
    nazev_obce = soup.find('td', headers='sa2').text.strip()
    volici = soup.find('td', headers='sa3').text.strip().replace('\xa0', '')
    obalky = soup.find('td', headers='sa5').text.strip().replace('\xa0', '')
    platne = soup.find('td', headers='sa6').text.strip().replace('\xa0', '')

    # výsledky pro strany
    vysledky = {}
    for tabulka in soup.find_all('div', class_='t2_470'):
        for radek in tabulka.find_all('tr')[2:]:
            bunky = radek.find_all('td')
            if len(bunky) >= 3:
                strana = bunky[1].text.strip()
                hlasy = bunky[2].text.strip().replace('\xa0', '')
                vysledky[strana] = hlasy

    return {
        "kod": kod_obce,
        "nazev": nazev_obce,
        "volici": volici,
        "obalky": obalky,
        "platne": platne,
        "hlasy": vysledky
    }
def save_to_csv(data, parties, filename):
    hlavicka = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + parties

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        zapisovac = csv.writer(f)
        zapisovac.writerow(hlavicka)

        for obec in data:
            radek = [
                obec["kod"],
                obec["nazev"],
                obec["volici"],
                obec["obalky"],
                obec["platne"],
            ]
            for strana in parties:
                radek.append(obec["hlasy"].get(strana, "0"))
            zapisovac.writerow(radek)


if __name__ == "__main__":
    validate_arguments(sys.argv)
    url = sys.argv[1]
    output_file = sys.argv[2]

    obce = get_links(url)
    vysledky = []
    vsechny_strany = set()

    for obec in obce:
        obec_vysledky = get_results_from_village(obec["link"])
        vysledky.append(obec_vysledky)
        vsechny_strany.update(obec_vysledky["hlasy"].keys())
    serazene_strany = sorted(vsechny_strany)
    save_to_csv(vysledky, serazene_strany, output_file)
    print(f"✅ Výsledky uloženy do {output_file}")
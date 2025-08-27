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
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    data = []

    rows = soup.find_all('tr') 
    for row in rows:
        cislo_obce = row.find('td', class_='cislo')
        nazev_obce = row.find('td', class_='overflow_name')


        if cislo_obce and nazev_obce:
            link = cislo_obce.find('a')
            if link: 
                kod = link.text.strip() 
                odkaz = "https://www.volby.cz/pls/ps2017nss/" + link['href'] 
            else:
                kod = '' 
                odkaz = ''

            jmeno = nazev_obce.text.strip()  
            data.append({"code": kod, "name": jmeno, "link": odkaz})  

    return data

def get_results_from_village(url, kod_obce_z_odkazu, nazev_obce):
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    nazev_element = soup.find("h3")
    if nazev_element:
        nazev_obce = nazev_element.text.strip().split(":")[-1].strip()
    else:
        nazev_obce = "Neznámá obec"

    volici = soup.find('td', headers='sa2').text.strip().replace('\xa0', '')
    obalky = soup.find('td', headers='sa3').text.strip().replace('\xa0', '')
    platne = soup.find('td', headers='sa6').text.strip().replace('\xa0', '')

    vysledky = {}
    for tabulka in soup.find_all('div', class_='t2_470'):
        for radek in tabulka.find_all('tr')[2:]:
            bunky = radek.find_all('td')
            if len(bunky) >= 3:
                strana = bunky[1].text.strip()
                hlasy = bunky[2].text.strip().replace('\xa0', '')
                vysledky[strana] = hlasy

    return {
        "kod": kod_obce_z_odkazu,
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
        obec_vysledky = get_results_from_village(obec["link"], obec["code"], obec["name"])
        vysledky.append(obec_vysledky)
        vsechny_strany.update(obec_vysledky["hlasy"].keys())

    serazene_strany = sorted(vsechny_strany)
    print("✅ Ukázka výsledku před uložením do CSV:")
    print(vysledky[0]) 
    save_to_csv(vysledky, serazene_strany, output_file)
    print(f"✅ Výsledky uloženy do {output_file}")

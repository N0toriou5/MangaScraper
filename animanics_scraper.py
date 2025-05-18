import requests
from bs4 import BeautifulSoup
import csv
import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import re

def estrai_tabella_uscita_volume_prezzo(url):
    """
    Scarica la pagina di Animanics e restituisce una lista di dizionari
    con chiavi: 'Uscita', 'Volume', 'Prezzo'.
    Gestisce sia il caso in cui l'intestazione compaia su una riga sola
    ("Uscita Volume Prezzo"), sia il caso in cui compaia su tre righe
    separate ("Uscita", "Volume", "Prezzo").
    """

    # 1) Configuro la sessione con Retry e User-Agent "browser-like"
    retry_strategy = Retry(
        total=5,
        connect=3,
        read=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1.0,
        allowed_methods=["GET", "HEAD", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/114.0.0.0 Safari/537.36'
        ),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8',
        'Referer': 'https://www.google.com/'
    }

    # 2) Scarico la pagina con fino a 3 tentativi
    for tentativo in range(3):
        try:
            resp = session.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            break
        except requests.exceptions.RequestException:
            time.sleep(2)
    else:
        raise RuntimeError(f"Impossibile scaricare la pagina dopo {tentativo+1} tentativi")  # :contentReference[oaicite:0]{index=0}

    # 3) Parsing HTML con BeautifulSoup
    soup = BeautifulSoup(resp.text, 'html.parser')  # :contentReference[oaicite:1]{index=1}

    # 4) Ottengo tutto il testo (inserendo '\n' al posto di ogni <br>) e tolgo NBSP
    all_text = soup.get_text(separator='\n').replace('\u00A0', ' ')
    righe    = [r.strip() for r in all_text.splitlines() if r.strip()]

    # 5) Provo a individuare l'intestazione in un'unica riga:
    idx_single = None
    for i, r in enumerate(righe):
        if r.lower() == 'uscita volume prezzo':
            idx_single = i
            break

    risultati = []

    if idx_single is not None:
        # CASO 1: Intestazione su UNA RIGA → ogni riga dati è "data titolo  prezzo"
        pattern = re.compile(
            r'^(\d{1,2}\s+\w+\s+\d{4})\s+(.+?)\s{2,}([0-9]+(?:,[0-9]{2})?\s*€)$'
        )  # :contentReference[oaicite:2]{index=2}

        for r in righe[idx_single + 1:]:
            m = pattern.match(r)
            if not m:
                break
            data_uscita   = m.group(1).strip()
            titolo_volume = m.group(2).strip()
            prezzo        = m.group(3).strip()
            risultati.append({
                'Uscita': data_uscita,
                'Volume': titolo_volume,
                'Prezzo': prezzo
            })

    else:
        # CASO 2: Intestazione su TRE RIGHE separate: 'Uscita','Volume','Prezzo'
        idx_triple = None
        for i in range(len(righe) - 2):
            if (righe[i].lower() == 'uscita'
                and righe[i + 1].lower() == 'volume'
                and righe[i + 2].lower() == 'prezzo'):
                idx_triple = i
                break

        if idx_triple is None:
            raise RuntimeError("Impossibile trovare l'intestazione 'Uscita Volume Prezzo'")

        # Dal quarto elemento in poi, ciascun blocco di 3 righe = [data, titolo, prezzo]
        j = idx_triple + 3
        while j + 2 < len(righe):
            data_uscita   = righe[j]
            titolo_volume = righe[j + 1]
            prezzo        = righe[j + 2]

            if '€' not in prezzo:
                break

            risultati.append({
                'Uscita': data_uscita,
                'Volume': titolo_volume,
                'Prezzo': prezzo
            })
            j += 3

    return risultati


def scrivi_csv(dati, nome_file):
    """
    Riceve una lista di dizionari con chiavi 'Uscita', 'Volume', 'Prezzo'
    e la salva in un file CSV (UTF-8) con intestazione.
    """
    with open(nome_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Uscita', 'Volume', 'Prezzo'])
        writer.writeheader()
        for entry in dati:
            writer.writerow(entry)


if __name__ == '__main__':
    manga = input("Inserisci il nome del manga di interesse da url: ")
    url       = 'https://www.animanics.it/manga/' + manga + '/'
    try:
        tabella = estrai_tabella_uscita_volume_prezzo(url)
        if tabella:
            nome_file = manga + '.csv'
            scrivi_csv(tabella, nome_file)
            print(f"Scraping completato: salvati {len(tabella)} record in '{nome_file}'.")
        else:
            print("Nessun dato estratto dal blocco 'Uscita Volume Prezzo'.")
    except RuntimeError as e:
        print(f"Errore: {e}")

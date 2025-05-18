# Animanics Manga Scraper
<p align="center">
  <img src="https://github.com/user-attachments/assets/2f4cf1b9-7b2f-4f32-8170-1e9bd2147da5" alt="scraper" width="300" height="300">
</p>

Questo script Python consente di estrarre automaticamente le informazioni sui volumi manga dal sito [animanics.it](https://www.animanics.it), visitando una pagina specificata dall’utente o tutte le serie elencate nella pagina `/manga/`.

## Funzionalità
- Visita una singola pagina manga o tutte le pagine elencate su `/manga/`
- Estrae i dati: **Uscita**, **Volume**, **Prezzo**
- Salva i risultati in un file `.csv` UTF-8
- Gestione automatica degli errori e ritentativi sulle richieste HTTP

## Requisiti
- Python 3.7+
- Librerie: `requests`, `beautifulsoup4`, `urllib3`

Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## Esecuzione

### 1. Singola pagina
Esegui lo script con l'URL diretto del manga:
```bash
python scraper.py --url https://www.animanics.it/manga/07-Ghost/
```

### 2. Tutte le serie
Esegui lo script in modalità automatica per tutte le serie:
```bash
python scraper.py --all
```

## Output
Viene generato il file `anime_manga_uscite.csv` con le colonne:
- `Serie`
- `Uscita`
- `Volume`
- `Prezzo`

Esempio:
```csv
Serie,Uscita,Volume,Prezzo
07-Ghost,8 Settembre 2011,07-Ghost #1,4,30 €
...
```

## Struttura progetto
```
animanics-scraper/
├── scraper.py
├── get_manga_links.py
├── requirements.txt
└── README.md
```

## Personalizzazioni
- Modifica il nome del file CSV nel codice (`nome_file_csv`)
- Inserisci `time.sleep(x)` per gestire ritardi tra richieste
- Limita il numero di serie elaborate con un `break` nel ciclo `for`

## Licenza e note legali
Uso personale e didattico. Il sito web di destinazione è di proprietà dei rispettivi autori.
Il presente software non incoraggia in alcun modo azioni di raccolta dati in automatico da siti internet.
Il presente software è da intendersi come puro esercizio didattico e come tale non andrebbe usato per azioni di raccolta automatica di dati.

---

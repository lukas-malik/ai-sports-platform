# Sběr snapshotů tenisových kurzů (The Odds API)

Izolovaný skript mimo hlavní architekturu platformy (rozhodnutí D15 v discovery). Od prvního dne buduje vlastní historii kurzů: opening, pohyb, closing. Data později naimportuje datové jádro platformy.

## Co dělá

Každé spuštění:

1. Zavolá `/v4/sports` (zdarma) a zjistí aktivní turnaje ve skupině Tennis (free tarif pokrývá Grand Slamy, ATP/WTA 1000 a 500).
2. Z hlavičky odpovědi přečte zbývající kredity a spočítá denní příděl: `(zbývá - 40 rezerva) / dní do konce měsíce`.
3. Pro každý turnaj rozhodne, zda udělat snapshot: minimálně 90 minut od posledního, nebo 30 minut, pokud některý zápas začíná do 150 minut (closing kurz). Turnaje s blízkým startem zápasu mají prioritu.
4. Snapshot = jeden dotaz `/v4/sports/{turnaj}/odds?regions=eu&markets=h2h` = 1 kredit. Uloží ho třikrát:
   - `data/raw/RRRR-MM-DD/HHMM_turnaj.json.gz` surová odpověď (pro pozdější přeparsování),
   - `data/odds_snapshots.sqlite` tabulky `runs`, `sport_snapshots`, `events`, `odds`,
   - `data/csv/odds_RRRR-MM.csv` plochý export po měsících.
5. Log do `logs/collector_RRRR-MM.log`.

Při 500 kreditech měsíčně a 2 aktivních turnajích vychází cca 9 snapshotů na turnaj a den. Skript nikdy nepřekročí denní příděl, takže free tarif nevyčerpá předčasně.

## Instalace na Windows Server

1. Nainstalovat Python 3.11 nebo novější z python.org (zaškrtnout „Add python.exe to PATH“). Žádné další balíčky nejsou potřeba.
2. `git clone` tohoto repa, např. do `C:\aisp`.
3. Do `C:\aisp\collector\.env` vložit řádek `ODDS_API_KEY=...` (soubor je v `.gitignore`, do repa nikdy nepatří).
4. Ověřit ručně: `python C:\aisp\collector\odds_collector.py` a zkontrolovat `logs\`.
5. Naplánovat spouštění každou hodinu (příkazový řádek jako správce):

```
schtasks /Create /SC HOURLY /MO 1 /ST 00:05 /TN "AISP odds collector" /TR "C:\aisp\collector\run.cmd" /RU SYSTEM /RL HIGHEST /F
```

Kontrola: `schtasks /Query /TN "AISP odds collector" /V /FO LIST`. Spuštění ručně: `schtasks /Run /TN "AISP odds collector"`.

Aktualizace: `cd C:\aisp && git pull`. Data i logy jsou mimo git.

## Testy

```
python -m unittest discover -s collector/tests -v
```

## Známá omezení

- Free tarif: jen GS, 1000, 500; turnaje 250 až s placeným zdrojem (D12).
- V regionu `eu` u tenisu není Betano; jako ostrá reference slouží `pinnacle`, doplňkově `betfair_ex_eu` a `matchbook` (exchange).
- Closing kurz je poslední snapshot před `commence_time`, s přesností danou intervalem plánovače a rozpočtem.
- Skript nesbírá výsledky. Ty přijdou z datasetů (Sackmann, tennis-data.co.uk) a spárují se podle jmen a data.

# Název projektu: VALBEE

Stav: schváleno Lukášem 5. 10. 2026 jako D22 (reviduje D19, která revidovala D17). Zapsal [claude] 5. 10. 2026.

## Rozhodnutí

Projekt se jmenuje VALBEE. Nahrazuje pracovní názvy AI SPORTS INTELLIGENCE PLATFORM (do 2. 10. 2026), Kalibr (D17, 2. až 4. 10. 2026) a Valibr (D19, 4. až 5. 10. 2026).

## Význam

Lukáš název zvolil 5. 10. 2026; výklad názvu nezadal a tento dokument ho nedomýšlí (doplní Lukáš, otevřený bod 5). Platí dál, že název nevyjadřuje výherní tipy; výsledek NO BET je plnohodnotné rozhodnutí.

EN: VALBEE is a private quantitative sports analytics platform for calibrated probability estimation, market price comparison, value assessment, risk control, and auditable decision making.

CZ: VALBEE je soukromá kvantitativní platforma pro sportovní analytiku, kalibraci pravděpodobností, porovnávání modelové ceny s trhem, hodnocení value, řízení rizika a auditovatelné rozhodování.

## Ověření (5. 10. 2026)

| Kontrola | Výsledek |
|---|---|
| valbee.cz | v registru CZ.NIC (RDAP) nenalezena, volná |
| valbee.com | registrovaná cizí stranou (RDAP Verisign vrací záznam) |
| PyPI a npm balíček valbee | neexistuje |
| GitHub repo valbee | existuje cizí malé repo `Zain200321/valBee` (2024, bez aktivity) a uživatelské účty ValBee-git, Valbeey; kolize s naším privátním repem `lukas-malik/valbee` není |
| Ochranné známky (ÚPV, EUIPO) | neověřeno, návrh v `docs/NAVRHY.md` |

## Konvence

| Kontext | Tvar | Pravidlo |
|---|---|---|
| Značka v textu | VALBEE | píše se velkými písmeny, neskloňuje se; v běžném textu lze „projekt VALBEE“, „platforma VALBEE“ |
| Repo, balíček, import, CLI, konfigurační adresář, root logger | `valbee` | jen malá písmena |
| Proměnné prostředí | `VALBEE_*` | prefix i pro klíče poskytovatelů (např. `VALBEE_ODDS_API_KEY`), kód běží na sdíleném serveru |
| Value (ekonomický koncept) | `valbee.value`, pole `fair_odds`, `edge`, `ev` | značka se nepoužívá jako doménový pojem |
| Kalibrace (statistický proces) | `valbee.calibration`, pole `calibration_*`, metriky Brier, log loss, ECE | slova kalibr a valibr se v kódu nepoužívají |
| Rozhodnutí | `valbee.decision`, výčet `BET`, `WATCH`, `NO_BET`, `BLOCKED`, `INSUFFICIENT_DATA` | pět stavů podle master instrukcí § 15, ne binární bet/no bet |

Zakázané: názvy typu `ValbeeModel` nebo `valbee_score`. Značka patří do obalu systému, ne do doménové logiky.

Balíček `valbee` se instaluje vždy lokálně z repa, nikdy z PyPI (název je tam volný, hrozí záměna za cizí balíček).

## Co se nemění

Schválená rozhodnutí D17 a D19 (historie), zprávy commitů, odborné výrazy kalibrace a calibration, názvy datových souborů kolektoru, kolektor na serveru (`C:\aisp`, úloha Plánovače, User Agent, název proměnné s klíčem) do samostatného rozhodnutí.

## Otevřené

1. Přejmenování repa na GitHubu na `valbee` a založení projektu VALBEE v ChatGPT Work (ruční krok Lukáše, NAVRHY 5. 10.), poté oprava URL repa v `docs/01-discovery-rozhodnuti.md` a `docs/03-napojeni-platforem.md`, remote v klonech a na serveru.
2. Kolektor kurzů: rozhodne Lukáš později; samostatný PR, beze ztráty sběru (D15).
3. Konvence se přenese do Blueprintu (blok Technical).
4. Volitelně registrace valbee.cz a ověření ochranných známek.
5. Výklad názvu VALBEE (co znamená) doplní Lukáš; do té doby se v dokumentech neuvádí.

# Název projektu: Valibr

Stav: schváleno Lukášem 4. 10. 2026 jako D19 (reviduje D17). Zapsal [claude] 4. 10. 2026.

## Rozhodnutí

Projekt se jmenuje Valibr. Nahrazuje pracovní názvy AI SPORTS INTELLIGENCE PLATFORM (do 2. 10. 2026) a Kalibr (D17, 2. až 4. 10. 2026).

## Význam

VALue + calIBRation. Kalibrované pravděpodobnosti porovnané s tržní cenou, value vyhodnocená s ohledem na nejistotu a riziko. Název nevyjadřuje výherní tipy; výsledek NO BET je plnohodnotné rozhodnutí.

EN: Valibr is a private quantitative sports analytics platform for calibrated probability estimation, market price comparison, value assessment, risk control, and auditable decision making.

CZ: Valibr je soukromá kvantitativní platforma pro sportovní analytiku, kalibraci pravděpodobností, porovnávání modelové ceny s trhem, hodnocení value, řízení rizika a auditovatelné rozhodování.

Pracovní tagline (není definitivní): Calibrated probability. Disciplined decisions.

## Ověření (4. 10. 2026)

| Kontrola | Výsledek |
|---|---|
| valibr.cz, valibr.com | v registru (RDAP) nenalezeny, volné |
| PyPI a npm balíček valibr | neexistuje |
| GitHub repo valibr | nenalezeno, jen podobné názvy (Valibre, Valibra) |
| Web: produkt v sázení, analytice, fintech | bez kolize |
| Ochranné známky (ÚPV, EUIPO) | neověřeno |

## Konvence

| Kontext | Tvar | Pravidlo |
|---|---|---|
| Značka v textu | Valibr | skloňování: Valibru, ve Valibru, s Valibrem |
| Repo, balíček, import, CLI, konfigurační adresář, root logger | `valibr` | jen malá písmena |
| Proměnné prostředí | `VALIBR_*` | prefix i pro klíče poskytovatelů (např. `VALIBR_ODDS_API_KEY`), kód běží na sdíleném serveru |
| Value (ekonomický koncept) | `valibr.value`, pole `fair_odds`, `edge`, `ev` | značka se nepoužívá jako doménový pojem |
| Kalibrace (statistický proces) | `valibr.calibration`, pole `calibration_*`, metriky Brier, log loss, ECE | slovo kalibr se v kódu nepoužívá |
| Rozhodnutí | `valibr.decision`, výčet `BET`, `WATCH`, `NO_BET`, `BLOCKED`, `INSUFFICIENT_DATA` | pět stavů podle master instrukcí § 15, ne binární bet/no bet |

Zakázané: názvy typu `ValibrModel` nebo `valibr_score`. Značka patří do obalu systému, ne do doménové logiky.

Balíček `valibr` se instaluje vždy lokálně z repa, nikdy z PyPI (název je tam volný, hrozí záměna za cizí balíček).

## Co se nemění

Schválené rozhodnutí D17 (historie), zprávy commitů, odborné výrazy kalibrace a calibration, názvy datových souborů kolektoru.

## Otevřené

1. Přejmenování repa na GitHubu a projektů v Claude a ChatGPT Work (ruční krok Lukáše), poté oprava URL repa v `docs/01-discovery-rozhodnuti.md` a remote v klonech a na serveru.
2. Kolektor kurzů (`C:\aisp`, úloha Plánovače AISP odds collector, User Agent, název proměnné s klíčem): rozhodne Lukáš později; samostatný PR, beze ztráty sběru (D15).
3. Konvence se přenese do Blueprintu (blok Technical).
4. Volitelně registrace domén a ověření ochranných známek.

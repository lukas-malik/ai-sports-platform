# KALIBR: Discovery, rozhodnutí

Dřívější název projektu: AI SPORTS INTELLIGENCE PLATFORM (přejmenováno 2. 10. 2026, D17). Pravda je soubor `docs/01-discovery-rozhodnuti.md` v repu projektu; kopie v Claude Projectu se aktualizuje z repa.

Průběžný záznam odpovědí a rozhodnutí z discovery fáze. Každé rozhodnutí má ID (D číslo), aby se na něj dalo odkazovat v Blueprintu. Stav: 2. 10. 2026.

## Kontext před discovery

Dřívější rozpracování (do 5. 9. 2026) obsahovalo rozhodnutí: plně automatické sázení bez potvrzení s náběhem, rozpočet 0 Kč, čtyři sporty (fotbal, tenis, hokej, basketbal), vlastní stroj 24/7, flat 1 % bankrollu, statický HTML dashboard + Telegram, navržené limity denní stop 5 %, drawdown stop 20 %, kurzy 1,40 až 6,00. Nové master instrukce (00-master-instrukce.md) jsou nadřazené; dřívější rozhodnutí platí jen tam, kde byla v discovery potvrzena.

## Blok 1: Vize, cíle, bankroll, risk tolerance (7. 9. 2026)

| ID | Rozhodnutí | Poznámka |
|----|-----------|----------|
| D1 | Cílový stav: plná automatizace přes fáze 1 až 5; fáze 5 jen po splnění předem definovaných podmínek | Podmínky se definují v bloku Automatizace |
| D2 | Provozní rozpočet do 1 000 Kč měsíčně (data, LLM API, hosting) | Nahrazuje dřívějších 0 Kč |
| D3 | Reálný bankroll: zatím nerozhodnuto; paper trading s virtuálním bankrollem 100 000 jednotek | Řád reálného bankrollu se doplní před fází 4 |
| D4 | Drawdown stop 20 % od vrcholu → NO BET režim + ruční přezkoumání | Potvrzeno z dřívějšího návrhu |
| D5 | Kritérium úspěchu po 6 měsících provozu: primárně pozitivní CLV na aspoň 300 sázkách (paper + reálné), sekundárně nezáporný reálný výsledek; přechod do fáze 4 jen při splnění obou | Původní odpověď „reálný zisk“ nahrazena po protinávrhu |
| D6 | Čas na provoz 1 až 3 hodiny týdně; fáze 2 (ruční potvrzování) zůstává podle zadání | Původní odpověď „méně než 1 hodina“ upravena po protinávrhu |
| D7 | Kurzy: exekuce u Tipsportu; sběr kurzů i od zahraničních ostrých bookmakerů (reference pro CLV a efektivitu trhu) | Více CZ účtů se zatím neřeší |
| D8 | Doporučeno (zatím nepotvrzeno jako rozhodnutí): druhý stop na klouzavém CLV posledních 200 sázek pod nulou = NO BET bez ohledu na zisk | K potvrzení v bloku Risk/Bankroll strategie |

Předpoklady: Tipsport jediné místo exekuce; vlastní hardware 24/7 zůstává možností vedle malého VPS v rozpočtu D2.

Nevyřešeno: řád reálného bankrollu; denní a týdenní limity ztrát; přesná definice podmínek pro fázi 5.

Rozhodnuto o procesu: souběžně s blokem 2 běží rešerše datových zdrojů pro tenis a fotbal (výsledky, statistiky, historické a aktuální kurzy, licence, ceny, limity).

## Blok 2: Sporty, trhy, data, kurzy (7. 9. 2026)

Podklad: 02-datove-zdroje.md.

| ID | Rozhodnutí | Poznámka |
|----|-----------|----------|
| D9 | První sport: tenis, ATP + WTA hlavní okruhy (GS, 1000, 500, 250 a WTA ekvivalenty) | Fotbal jako druhý sport po ověření datového jádra a evaluation harness |
| D10 | Revize D1: cílový model exekuce = Tipsport, systém připraví vše (výběr, stake, notifikace s předvyplněným tiketem), člověk potvrdí jedním klepnutím. Fáze 5 „plná automatizace“ se předefinuje na „plná automatizace přípravy, ruční exekuce“ | Důvod: Herní plán Tipsportu § 2 odst. 5 zakazuje sázecího robota, sankce kurz 1 a zrušení konta |
| D11 | Kurzy Tipsportu se nesbírají strojově. Detekce value běží na licencovaných API datech (Pinnacle jako ostrá reference, Betano CZ jako proxy českého trhu). Skutečný kurz Tipsportu zadá uživatel při potvrzení tiketu, ukládá se pro CLV a evaluaci | Žádná šedá zóna (autorský zákon § 30 odst. 3, VP Tipsportu) |
| D12 | Datový rozpočet: start na free tarifech (The Odds API free 500 kreditů/měs, Tennis API.com trial), placené tarify (cca 40 USD) až po úspěšném backtestu | Do té doby živé kurzy jen pro GS, 1000, 500; turnaje 250 až s placeným Tennis API.com |
| D13 | Trh pro MVP: pouze vítěz zápasu | Jediný trh s volnou historií kurzů; handicapy a totaly později |
| D14 | Žádný pevný filtr rozsahu kurzů. Rozhodování řídí minimální edge, minimální confidence a max stake; pásmo kurzu je dimenze v evaluaci | Nahrazuje dřívější návrh 1,40 až 6,00 |
| D15 | Sběr vlastní historie kurzů začne hned během discovery: izolovaný skript, The Odds API free, snapshoty tenisových kurzů několikrát denně, otevřený formát, pozdější import do platformy | Výjimka z pravidla „nejdřív Blueprint“, schválená kvůli nevratné ztrátě dat |
| D16 | Historická data: Sackmann tennis_atp / tennis_wta (CC BY NC SA, osobní použití OK), tennis-data.co.uk (closing kurzy), vlastní výpočet Elo | Oficiální weby ATP/WTA/ITF se nescrapují (ToS) |

Předpoklady: Betano CZ jako proxy českého trhu má kurzy dostatečně korelované s Tipsportem (ověří se z ručně zadaných kurzů Tipsportu po prvních desítkách sázek). Free tarif The Odds API (500 kreditů, 1 kredit na sport klíč, region a trh) stačí na cca 4 až 8 snapshotů denně při 2 až 4 aktivních turnajích.

Stav D15 (7. 9. 2026 večer): skript `collector/odds_collector.py` hotový, otestovaný (5 unit testů, ostrý běh: 2 turnaje, 470 řádků, 2 kredity), poběží 24/7 na firemním Windows Serveru přes Plánovač úloh, nasazení přes GitHub repo https://github.com/lukas-malik/ai-sports-platform (privátní, kód nahrán 7. 9. 2026, commit a921d86). Klíč The Odds API je v `.env` v připojené složce. Zjištění z ostrého běhu: v regionu eu u tenisu není Betano; ostrá reference Pinnacle, doplňkově Betfair Exchange a Matchbook.

Nevyřešeno: ověření podmínek Tennis API.com pro osobní použití a reálné hloubky opening/closing historie (trial); podmínky tennis-data.co.uk (web nedostupný).

## Organizace projektu (2. 10. 2026)

| ID | Rozhodnutí | Poznámka |
|----|-----------|----------|
| D17 | Název projektu: Kalibr | Nahrazuje AI SPORTS INTELLIGENCE PLATFORM; název repa a Claude Projectu se přejmenuje ručně |
| D18 | Na projektu pracují souběžně Claude Cowork a ChatGPT Work podle jedněch pravidel v `AGENTS.md`; pravda o dokumentech je složka `docs/` v GitHub repu | Zapsal [claude]. Otevřené: zda ChatGPT Work v cloudu umí pracovat nad repem (čeká na test) |

## Blok 3: AI, ML, agenti

(čeká)

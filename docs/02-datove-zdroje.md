# Rešerše datových zdrojů a právního rámce (stav k 7. 9. 2026)

Tři nezávislé rešerše provedené 7. 9. 2026 s ověřením na webu. Kde ověření selhalo, je uvedeno „neověřeno". Ceny v měně poskytovatele. Dokument je podkladem pro discovery blok 2 (sporty, trhy, data, kurzy) a pro Data Blueprint.

## Shrnutí pro rozhodování

1. Tenis: volná historie výsledků a statistik (Sackmann, CC BY NC SA) od 1968, statistiky servisu od 1991; volná historie s closing kurzy (tennis-data.co.uk) ATP od 2001, WTA od 2007, spolehlivé sloupce Pinnacle a Bet365 zhruba od 2010; pouze hlavní okruhy, jen closing (ne opening). Point in time zranění neexistují. Elo nutno počítat vlastní.
2. Fotbal: football-data.co.uk zdarma, 1X2 kurzy od 2000/01, plný set opening + closing pro 1X2, O/U 2,5 a AH od 2019/20 (7 sezón, cca 13 000 zápasů top 5 lig). Česká liga bez veřejné historie kurzů. xG: FBref od 1/2026 bez Opta dat, Understat právně šedý (robots Disallow), oficiální xG jen v placeném add onu Sportmonks. Club Elo momentálně nefunkční. Point in time sestavy a zranění neexistují.
3. Kurzy: Pinnacle jako referenční ostrý bookmaker je dostupný přes The Odds API (region eu, tarif 20K za 30 USD, snapshoty po 5 min od 2022) nebo OddsPapi (free 250 req/měs, historie od 1/2026). Tipsport není v žádném API v rozpočtu; Betano CZ ano. Pinnacle i Betfair jsou pro rezidenty ČR nedostupní k sázení, slouží jen jako reference.
4. Tipsport, Herní plán § 2 odst. 5: výslovný zákaz automatizovaného software (robota), který se přihlašuje, vybírá příležitosti nebo uzavírá sázky; sankce vyhodnocení sázek kurzem 1, dle § 4 zrušení konta. Plná automatizace u Tipsportu je smluvně nerealistická.
5. Zákon 186/2016 Sb. automatizaci na straně hráče nezakazuje. Daň: od 1. 1. 2024 osvobození jen do 50 000 Kč čistého zisku z daného druhu hry za rok.
6. Limitace ziskových účtů je u českých bookmakerů smluvně předvídána a redakčními testy doložena (Tipsport řádově měsíce při sázkách do 2 000 Kč, Fortuna nejrychleji).

---

## A. TENIS

Poznámka: web tennis-data.co.uk byl během rešerše nedostupný (TLS chyba), údaje o něm jsou převzaté ze sekundárních zdrojů.

### A1. Otevřené datasety (výsledky, statistiky, ranking)

| Zdroj | URL | Typ | Cena | Historie | Obsah | Real time | Licence | Kvalita, riziko, náhrada |
|---|---|---|---|---|---|---|---|---|
| Sackmann tennis_atp | https://github.com/JeffSackmann/tennis_atp | dataset CSV | zdarma | ranking od 1985 téměř kompletní; zápasy tour od 1968; statistiky 1991+ tour, 2008+ challengery, 2011+ kvalifikace | výsledky, skóre (RET, W/O), servis/return jako součty (esa, dvojchyby, body 1. a 2. podání, brejkboly), ranking, hráči; qual_chall, futures, čtyřhra do 2020 | ne (dávkově) | CC BY NC SA 4.0 | referenční kvalita; některé zápasy bez statistik; frekvence aktualizací neověřena (komunita: týdenní až měsíční). Náhrada: TML Database |
| Sackmann tennis_wta | https://github.com/JeffSackmann/tennis_wta | dataset CSV | zdarma | rozsah let neověřen | jako ATP, zvlášť kvalifikace + ITF | ne | CC BY NC SA 4.0 | statistiky WTA řidší než ATP |
| TML Database (TennisMyLife) | https://github.com/Tennismylife/TML-Database | dataset CSV | zdarma | 1968 až 2026 | doplněná Sackmannova data, statistiky, ranking | denně | web MIT, README dědí CC BY NC SA | jen ATP; náhrada Sackmanna pro aktuální sezónu |
| Tennis Abstract | https://www.tennisabstract.com | web | zdarma | Open Era | splity, H2H, Match Charting Project, Elo | týdně | bez API | totéž jádro jako Sackmann |
| Ultimate Tennis Statistics | https://www.ultimatetennisstatistics.com/about, https://github.com/mcekovic/tennis-crystal-ball | web + open source (PostgreSQL, Docker) | zdarma | Open Era ATP, statistiky od 1991 | výsledky, Elo (celkové, povrchové, indoor/outdoor), predikce | pondělí | kód Apache 2.0, algoritmy CC BY NC SA | jen ATP; postaveno na Sackmannovi |
| OnCourt | https://oncourt.info | placený desktop | cena neověřena | od 1990, 1,6 mil. zápasů | výsledky, statistiky, H2H, pohyb kurzů Pinnacle | průběžně | heslo do Access DB pro vlastní vývoj | jediný levný zdroj historického pohybu kurzů Pinnacle; malý provozovatel |

### A2. Historické výsledky s kurzy

| Zdroj | URL | Typ | Cena | Historie | Obsah | Poznámky |
|---|---|---|---|---|---|---|
| tennis-data.co.uk | http://www.tennis-data.co.uk/alldata.php | XLS/CSV po sezónách | zdarma | ATP od 2001, WTA kurzy od 2007 | výsledky, ranking, kurzy B365, PS (Pinnacle), EX, LB, CB, SJ, UB a další + MaxW/L, AvgW/L | kurzy „most recent before play starts“ = closing, ne opening; Kaggle mirror 2000 až 2024 má 64 526 ATP zápasů; spolehlivé sloupce B365, PS, Max, Avg; podmínky neověřeny |
| BigDataBall | https://www.bigdataball.com/datasets/tennis-data/ | placený dataset | 30 USD/sezóna | 2024 až 2025 | moneyline, spread, total: opening i closing | jediný nalezený CSV zdroj s opening vs closing; krátká historie |
| The Odds API | https://the-odds-api.com/sports/tennis-odds.html | freemium API | free 500 kreditů; 30 USD/20K; 59 USD/100K | historie od 2020 jen pro Grand Slamy, placené | live + prematch více bookmakerů; jen GS, 1000, 500 | vhodné pro vlastní snapshoty od dnes; turnaje 250 nepokrývá |

### A3. Placená a freemium API

| Zdroj | URL | Cena/měs | Limity | Historie | Obsah | Real time | Riziko |
|---|---|---|---|---|---|---|---|
| API Tennis.com | https://api-tennis.com/ | Starter 40 USD, Premium 60, Business 80, Ultra 120; trial 14 dní | 8 000 až 2 M req/den | neověřeno | ATP, WTA, Challenger, ITF; fixtures, H2H, ranking, prematch kurzy; live odds od Business | ano | bez SLA |
| Tennis API.com (MatchStat, RapidAPI) | https://tennis-api.com/api-pricing/, https://docs.tennis-api.com/ | 10 USD/10 000 req; 29 USD/150 000 (ceník nekonzistentní, ověřit) | 100 req/min | „historical odds back to 2010“ (Marathon, Pinnacle) | ATP/WTA/ITF/Challenger, fixtures, ranking, H2H, prematch a in play kurzy, opening_odds/closing_odds, movement | ano | jediný levný zdroj opening/closing s historií; ověřit v trialu |
| Live Tennis API | https://livetennisapi.com/ | Free 100/den; Basic 9,99 USD; Pro 29,99 USD (kurzy); Ultra 99,99 USD | dle tarifu | výsledky od 1968, PBP od 1/2023 | výsledky, PBP, match winner odds od Pro | ano | nový hráč |
| Goalserve | https://www.goalserve.com/en/sport-data-feeds/tennis-api/prices | 150 USD | | | ATP/WTA/Challenger/ITF, PBP, odds | ano | nad rozpočet |
| Sportradar | https://developer.sportradar.com/tennis/reference/overview | neveřejný ceník (řádově stovky USD) | trial 1 000 req/30 dní | 4 000+ soutěží | oficiální partner ATP/WTA | ano | mimo rozpočet |
| SportDevs | https://sportdevs.com/pricing | neověřeno | | | tenis inzerován | | ověřit ručně |
| API Sports tenis | https://api-sports.io/ | beta na vyžádání | | „35 let historie“ slibováno | dosud není v seznamu sportů | | riziko nedokončení |
| Sportmonks | | | | | tenis nenabízí | | vyřadit |

### A4. Oficiální zdroje

ATP Tour (https://www.atptour.com/en/terms-and-conditions-app): „Systematic retrieval of data ... is prohibited absent prior express written permission from ATP“; použití „for any commercial, gambling or wagering purposes, is strictly prohibited“. WTA a ITF: podmínky nešlo načíst, neověřeno. Závěr: scraping oficiálních webů pro účel sázení vyloučit.

### A5. Zranění, odstoupení, počasí, cestování

| Potřeba | Zdroj | Stav |
|---|---|---|
| Odstoupení a skreče ex post | Sackmann (RET, W/O ve skóre), tennis-data.co.uk (sloupec Comment) | jen výsledek, ne stav před zápasem |
| Point in time zranění, withdrawal listy | strukturovaný veřejný zdroj nenalezen | neexistuje; vlastní sběr od dnešního dne |
| Počasí u venue | Open Meteo (https://open-meteo.com/en/pricing): free 10 000 volání/den, CC BY 4.0; historie placená | forecast zdarma |
| Cestování, časová pásma | odvodit z kalendáře turnajů | vlastní výpočet |

### A6. Elo

Tennis Abstract Elo (https://tennisabstract.com/reports/atp_elo_ratings.html): jen aktuální HTML tabulka, bez historie, nelze použít point in time. Ultimate Tennis Statistics: týdenní Elo včetně historie ve vlastní PostgreSQL instanci, jen ATP. Doporučení: počítat vlastní Elo (celkové + povrchové, K podle úrovně turnaje, penalizace neaktivity) ze Sackmannových CSV.

### A7. Doporučená kombinace pro MVP tenis (do cca 40 EUR)

| Vrstva | Zdroj | Cena |
|---|---|---|
| Historie výsledků + statistik | Sackmann ATP/WTA (+ TML pro aktuální ATP sezónu) | 0 |
| Historie s kurzy pro backtest | tennis-data.co.uk (B365, PS, Max, Avg) | 0 |
| Elo | vlastní výpočet, kontrola proti Tennis Abstract | 0 |
| Aktuální rozpis, výsledky, kurzy | Tennis API.com 10 USD nebo Live Tennis API Pro 29,99 USD | 10 až 30 USD |
| Sběr vlastního pohybu kurzů | The Odds API free (500 kreditů) nebo 30 USD | 0 až 30 USD |
| Počasí | Open Meteo free | 0 |

Backtest s kurzy: ATP 2001 až 2026 (cca 25 sezón, cca 65 000 zápasů), WTA 2007 až 2026 (cca 19 sezón, cca 45 000 zápasů), jen hlavní okruhy, closing Pinnacle a Bet365 spolehlivé cca od 2010.

Co chybí: point in time zranění (sběr od dnes), pohyb kurzů opening → closing (jen closing; backtest měří hranu proti nejefektivnější ceně, konzervativní), historické Elo (vlastní výpočet), Challenger/ITF s kurzy (nenalezeno), licence tennis-data.co.uk a ToS API pro osobní sázení neověřeny.

---

## B. FOTBAL

### B1. Historické výsledky s kurzy

| Zdroj | Typ | Obsah | Historie | Podmínky | Riziko |
|---|---|---|---|---|---|
| football-data.co.uk (https://www.football-data.co.uk/data.php) | free CSV/XLS, aktualizace 2× týdně | výsledky, poločas, střely, rohy, karty; kurzy 1X2 (B365, BW, IW, PS = Pinnacle, WH, VC, Max/Avg), O/U 2,5, AH a closing varianty s „C“ (B365CH, PSCH, MaxCH, B365C>2.5, PC>2.5, AHCh, PCAHH) | výsledky od 1993/94 (22 divizí), kurzy od 2000/01; plný set closing (1X2 + O/U + AH) od 2019/20; Pinnacle closing 1X2 i starší (rok neověřen) | „for the purposes of league match prediction only“, osobní predikce OK | nízké; česká liga chybí |
| „Extra“ ligy (https://www.football-data.co.uk/all_new_data.php) | free | jen 1X2: Pinnacle closing + Max/Avg, bez opening | od 2012/13 | dtto | ČR není |

### B2. API a poskytovatelé

| Zdroj | Cena/měs | Limity | Obsah | Historie | Real time | Riziko / poznámka |
|---|---|---|---|---|---|---|
| football-data.org (https://www.football-data.org/pricing) | Free 0; 12/29/49/99/199 EUR; add on Odds 15 EUR, Statistics 15 EUR | free 10 req/min | free: rozpis, zpožděná skóre, tabulky; sestavy od 29 EUR | free 12 soutěží | live jen placené | ČR jen v placených tarifech |
| API Football (https://www.api-football.com/pricing) | Free (100 req/den), Pro 19 USD (7 500/den), Ultra 29 USD, Mega 39 USD; všechny endpointy ve všech plánech | sdílený strop req/min | fixtures, events, lineups, injuries, sidelined, statistiky, prematch i in play odds (33 bookmakerů), predictions | 20 let, 1 244 soutěží; free jen recent; kurzy uchovány pouze 7 dní; injuries od 4/2021, update každé 4 h | ano | xG nekonzistentní; česká liga v seznamu (rozsah neověřen) |
| Sportmonks (https://www.sportmonks.com/football-api/plans-pricing/) | Free (Skotsko + Dánsko); Starter 29 EUR (5 lig), European 39/59/69 EUR (27 lig, 14 let); add on xG 29 EUR, Odds 15 EUR | 2 000 až 3 000 req/entita/h | sestavy, zranění, statistiky, odds 50+ bookmakerů, xG | až 14 sezón | ano | Fortuna liga pokryta vč. odds a sestav |
| Sportradar | B2B, neveřejné | | live, sestavy, odds | max 3 sezóny | ano | nevhodné pro osobní projekt |
| Opta / Stats Perform | enterprise | | referenční xG | | | 1/2026 ukončil smlouvu s FBref |
| StatsBomb open data (https://github.com/statsbomb/open-data) | free JSON | | eventy, sestavy, xG | vybrané sezóny top 5 | ne | jen pro učení xG modelu |
| Wyscout | bez datového API pro jednotlivce | | | | | mimo rozpočet |
| SofaScore | scraping | | ratings, statistiky, sestavy | | ano | ToS neověřeny, vysoké riziko |
| FotMob (https://www.fotmob.com/tos.txt) | scraping | | xG, sestavy, zranění | | ano | zakazuje automatizovanou extrakci |
| Understat (https://understat.com/) | scraping | | xG per střela, xPTS | top 5 + RFPL od 2014/15 | po zápase | robots.txt Disallow: /, bez API |
| FBref | scraping max 10 req/min | | od 1/2026 pokročilá data (Opta, xG) smazána | základní | ne | pro xG již nepoužitelný |
| Club Elo (api.clubelo.com) | free CSV | | Elo | | denně | 7. 9. 2026 HTTP 502, „Fixtures API deactivated“ |
| FiveThirtyEight SPI | free dataset | | spi, prob, xg, nsxg | 2016 až 6/2023, ukončeno | | jen archiv |
| Transfermarkt | scraping | | zranění (from, until, days), hodnoty | dlouhá | ne | bez data oznámení zranění |

### B3. Zranění a sestavy

Strukturované a včasné: API Football (injuries každé 4 h, sestavy před výkopem), Sportmonks (sidelined, potvrzené sestavy). Oba jsou „aktuální stav“, ne archiv. Historie zranění s časovou známkou zveřejnění u žádného zdroje nenalezena. Nutno budovat vlastními denními snapshoty.

### B4. Počasí

Open Meteo: free nekomerční, 10 000/den, ERA5 historie od 1940, CC BY 4.0. OpenWeather One Call 3.0: 1 000 volání/den zdarma.

### B5. Otevřené datasety

Club Football Match Data 2000 až 2025 (https://github.com/xgabora/Club-Football-Match-Data-2000-2025): 238 858 zápasů, 27 zemí, výsledky + Bet365 a Max kurzy + Elo, bez xG, MIT. Kaggle European Soccer Database: 2008 až 2016, ODbL.

### B6. Doporučená kombinace pro MVP fotbal (do cca 40 EUR)

1. football-data.co.uk (0): páteř backtestu, opening i closing top 5 lig.
2. API Football Pro (19 USD): rozpis, sestavy, zranění, live, prematch kurzy; denní snapshoty ukládat lokálně (API maže po 7 dnech).
3. Understat (0, právně šedé) nebo Sportmonks European + xG (nad rozpočet).
4. Open Meteo (0).
5. The Odds API free na kontrolu closing line.

Backtest s kurzy: top 5 lig 1X2 od 2000/01 (cca 50 000 zápasů); Pinnacle closing 1X2 cca 13 až 14 sezón; plný closing set 1X2 + O/U + AH od 2019/20 = 7 sezón, cca 13 000 zápasů; xG od 2014/15. Česká liga: bez veřejné historie kurzů.

Co chybí: point in time sestavy a zranění (look ahead bias při použití dnešních dat), intra day pohyb kurzů (jen The Odds API od 2020 za kredity), xG od 2026 bez čistého zdroje, Club Elo nefunkční.

---

## C. KURZY A PRÁVNÍ RÁMEC

### C1. Zdroje kurzů

| Zdroj | URL | Cena/měs | Limity | Bookmakeři | Sporty | Historie | Opening/closing | Riziko |
|---|---|---|---|---|---|---|---|---|
| The Odds API | https://the-odds-api.com/ | free 500 kreditů; 20K 30 USD; 100K 59 USD; 5M 119 USD | 1 kredit/region/trh; historie 10 kreditů | Pinnacle ano (eu), Betano ano, Betfair ano; Tipsport ne, Fortuna ne | fotbal; tenis jen GS, 1000, 500 | snapshoty od 6/2020 (10 min), od 9/2022 5 min; jen placené | odvodit ze snapshotů | nízké |
| OddsPapi | https://oddspapi.io/ | free 250 req/měs; placené per request | cooldown 5 s historie | Pinnacle ano, Betano CZ ano, Fortuna PL/RO; Tipsport ne | fotbal, tenis (350+ bookmakerů) | od 1/2026 | časované snapshoty | nízké |
| odds-api.io | https://odds-api.io/ | free 100 req/h; Solo 49 GBP; Starter 99 GBP | 5 000 req/h | 265+; Pinnacle neověřeno | 34 sportů | ano, hloubka neověřena | endpoint closing odds | nízké |
| OddsJam / OpticOdds | | B2B, contact sales | | 200+ | | | | mimo rozpočet |
| BetsAPI | https://betsapi.com/ | ceník nedostupný | 3 600 req/h | Bet365, Bwin, Betfair a další; Pinnacle ne | fotbal, tenis | omezené | | šedá zóna |
| Betstamp (Tipsport feed) | https://www.betstamp.com/odds/Tipsport | B2B, demo | | Tipsport ano | ano | | | B2B |

### C2. Pinnacle

Oficiální API (https://github.com/pinnacleapi/pinnacleapi-documentation) vázáno na affiliate status nebo B2B. Pinnacle ve vlastních podmínkách vylučuje rezidenty ČR a nemá českou licenci. Náhradní zdroje Pinnacle closing: The Odds API, OddsPapi, odds-api.io, football-data.co.uk, tennis-data.co.uk.

### C3. OddsPortal

Provozovatel Livesport s.r.o. Podmínky (https://www.oddsportal.com/terms/) čl. 2.10 a 2.11 zakazují extrakci databáze a scraping bez souhlasu. Scrapery existují (OddsHarvester, MIT, 5/2026, opening/closing i vývoj kurzu). Riziko pro systematické stahování vysoké.

### C4. Tipsport

Veřejné API neexistuje. Neveřejné JSON endpointy používají komunitní projekty (bez dokumentace), Apify actor DEPRECATED. Legální cesty: ruční čtení webu, B2B feed Betstamp (cena neveřejná), agregátoři neověřeni.

### C5. Betfair

Exchange pro ČR vypnut k 31. 12. 2016 (partnerské oznámení), bez české licence. API vyžaduje účet; Historic Data od 4/2015, Basic zdarma, vyšší úrovně placené.

### C6. Herní plán a Všeobecné podmínky Tipsportu

Herní plán kurzových sázek Tipsport.net a.s., účinný od 12. 3. 2026: https://minshara.tipsport.org/datafiles/hp-ks-tipsportnet-as-ucinnost-1232026-cz-1773222801.pdf

| Ustanovení | Citace |
|---|---|
| Zvláštní část § 2 odst. 5 | „Účastník zároveň není oprávněn uzavírat Sázku za použití vzdáleného přístupu na jiné zařízení a/nebo prostřednictvím automatizovaného software (tzv. robota), který nahrazuje vůli Účastníka tak, že se např. přihlašuje na Uživatelské konto, vybírá sázkové příležitosti nebo automaticky uzavírá Sázky. V případě porušení některé z těchto podmínek je Provozovatel oprávněn předmětné sázky vyhodnotit kurzem 1.“ |
| § 2 odst. 3 | Provozovatel nepřijme sázku od osob, které porušily ZHH nebo HP, případně vyhodnotí kurzem 1. |
| § 4 odst. 1 | Jen jedno uživatelské konto; při porušení zrušení kont a vyhodnocení kurzem 1. |
| § 5 písm. b) | Individuální limity (limit výhry, maximální sázka na příležitost) jsou smluvně předvídány. |
| § 8 odst. 2 | Maximální čistá výhra na tiket 10 mil. Kč. |
| § 11 odst. 1 a), § 12 odst. 3 | Nárok na výhru jen bez pochybností o regulérnosti; při pochybnostech kurz 1. |

Všeobecné podmínky, účinné od 1. 1. 2024: https://minshara.tipsport.cz/datafiles/vp-tipsport-ucinnost-11202436-cz-1703884696.pdf. § 3 odst. 8: konto výhradně pro osobní potřebu, zákaz komerčního užití. § 3 odst. 14: zákaz využití technických možností aplikace k obcházení zákona, HP a VP.

Herní plán zakazuje robota, který „nahrazuje vůli Účastníka“. Čtení kurzů a výpočty mimo účet HP výslovně neupravuje.

### C7. Praxe limitace účtů

| Zdroj | Typ | Obsah |
|---|---|---|
| kurzovesazeni.com, test 2022, akt. 8/2026 | redakční test | Tipsport/Chance: při sázkách do cca 2 000 Kč a bez malých trhů účty bez zásadního omezení několik měsíců; SazkaBet dříve; SynotTip rychle; Fortuna nejrychleji |
| jaknasazeni.cz, 2020, akt. 2024 | anekdotické | Tipsport: postupné limity 999 → 400 až 500 → 100 Kč |

Oficiální vyjádření bookmakerů nenalezena.

### C8. Zákon 186/2016 Sb. a daně

Finanční správa: od 1. 1. 2024 limit osvobození snížen z 1 000 000 Kč na 50 000 Kč; zdaňuje se rozdíl mezi úhrnem výher a vkladů za zdaňovací období pro daný druh hry; ztrátu z kurzové sázky nelze kompenzovat s technickou hrou. ZHH neobsahuje zákaz použití vlastního software sázejícím; § 122 postihuje jiné skutkové podstaty. Automatizace je věcí smlouvy s bookmakerem.

### C9. Zahraniční bookmakeři

Pinnacle ani Betfair nemají českou licenci; Pinnacle vylučuje rezidenty ČR; Betfair Exchange pro ČR vypnut. V seznamu nepovolených her MF (7. 9. 2026, 3 502 položek) se pinnacle.com ani betfair.com nevyskytují. ZHH účast hráče na nepovolené hře nepostihuje; rizika smluvní (uzavření účtu) a daňová (neověřeno). Sledování kurzů bez sázení ZHH neupravuje.

### C10. Ukládání kurzů pro osobní použití

Autorský zákon § 91 a 92 s odkazem na § 30 odst. 3: užití elektronické databáze je užitím i pro osobní potřebu; systematické scrapování kurzů z webů bookmakerů a agregátorů je právně nejisté a odporuje jejich podmínkám. Bezpečná cesta je licencované API.

### C11. Závěry

Doporučená kombinace kurzů pro MVP (cca 30 USD, 700 Kč): The Odds API tarif 20K (Pinnacle eu, snapshoty po 5 min, closing = poslední snapshot před startem) + OddsPapi free (Pinnacle, Betano CZ). Tipsport zůstává nejslabším místem: systematické strojové stahování jeho kurzů nemá legální licencovanou cestu pod 1 000 Kč.

Plná automatizace (bot přihlašuje a sází) je u Tipsportu smluvně nerealistická: přímé porušení HP § 2 odst. 5 s rizikem ztráty výher i účtu. Realistický je model „software doporučuje, člověk sází ručně“, sledování CLV přes The Odds API a počítání s postupnou limitací účtu.

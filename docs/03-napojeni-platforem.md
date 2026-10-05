# VALBEE: napojení platforem na repo

Zapsal [claude] 5. 10. 2026 podle D18, D20, D21 a D23. Pravidla pro agenty jsou v `AGENTS.md`; tento dokument popisuje jen to, jak se Claude Cowork a ChatGPT Work k repu dostanou, jak se přístup ověří a co vložit do instrukcí projektů.

Repo: `https://github.com/lukas-malik/ai-sports-platform` (po přejmenování `https://github.com/lukas-malik/valbee`; GitHub starou adresu přesměrovává). Repo je privátní (D23).

## 1. Princip

| | Claude Cowork | ChatGPT Work (cloud) |
|---|---|---|
| Role (D20) | oponent: revize PR, red team, skeptic | primární vývojář |
| Pravda | repo | repo |
| Čtení repa | GitHub integrace účtu lukas-malik | GitHub konektor ChatGPT (účet lukas-malik) |
| Zápis do repa | větev `claude/<ukol>`, PR | větev `chatgpt/<ukol>`, PR, git s fine grained tokenem |
| Co navíc vidí | Claude Project VALBEE (kopie `docs/` jako cache), složka OneDrive VALBEE (`.env`, zip kolektoru, instalátor) | trvalý souborový systém cloudového Work (klon repa) |
| Co nevidí | nic z ChatGPT | OneDrive, `.env`, klíč The Odds API, data kolektoru (AGENTS.md 23) |
| Slučuje | Lukáš | Lukáš |

Obě platformy pracují nad stejným repem a stejnými pravidly. Žádná synchronizace souborů mezi platformami mimo git neexistuje a nemá existovat.

## 2. Claude Cowork (stav k 5. 10. 2026, funguje)

- Claude Project „VALBEE“ (dříve AI SPORTS PLATFORM, VALIBR). Instrukce projektu: § 4.2. Dokumenty projektu `claude/00-master-instrukce.md`, `claude/01-discovery-rozhodnuti.md`, `claude/02-datove-zdroje.md`, `claude/HANDOFF-2026-10-04.md` jsou kopie z repa; Claude je obnoví po každém sloučení PR, který je mění.
- GitHub integrace Cowork je propojená s účtem `lukas-malik` (účet `lukasmalik89` integrace nevidí). Claude čte repo, zakládá větve `claude/<ukol>` a otevírá PR; do `main` nezapisuje (AGENTS.md 4, 5).
- Připojená složka `C:\Users\lukas\OneDrive\VALBEE` obsahuje jen `.env` s klíčem The Odds API, `ai-sports-platform-collector.zip` a `install_collector.cmd`. Není to pravda projektu a do repa se z ní nic nekopíruje.
- Revize PR podle AGENTS.md 21 a 22: verdikt, rizika, důvody, zapsáno do PR.

## 3. ChatGPT Work (cloud): postup připojení

Ověřeno z veřejných zdrojů 5. 10. 2026: cloudové ChatGPT Work spouští kód s přístupem na internet, umí klonovat repozitáře a má trvalý souborový systém mezi sezeními; čtení repa v ChatGPT zajišťuje oficiální GitHub konektor (Plus, Pro). Zda cloudové Work samo načítá `AGENTS.md` a zda bezpečně drží token mezi sezeními, zdroje neuvádějí. Proto krok 3.5 (test).

### 3.1 Projekt v ChatGPT Work
Založit cloudový projekt (ne lokální) s názvem VALBEE. Do instrukcí projektu vložit text z § 4.1 beze změn.

### 3.2 GitHub konektor (čtení)
V ChatGPT: Settings, Connectors, GitHub. Autorizovat účtem `lukas-malik` a povolit přístup jen k repu projektu. Konektor respektuje práva na GitHubu, privátní repo tedy uvidí jen tento účet.

### 3.3 Fine grained token (zápis)
GitHub: Settings, Developer settings, Personal access tokens, Fine grained tokens, Generate new token.
- Resource owner: `lukas-malik`.
- Repository access: Only select repositories, jen repo projektu.
- Permissions (Repository): Contents read and write, Pull requests read and write, Metadata read. Nic dalšího.
- Expiration: 90 dní; po expiraci vystavit nový. Datum expirace si Lukáš poznamená mimo repo.
- Token je tajemství (AGENTS.md 13, 25): nikdy do repa, dokumentů, NAVRHY ani do zpráv v chatu, které se ukládají do historie projektu.

Předání tokenu cloudovému Work: nevíme, zda Work má trezor tajemství. Dokud se to neověří, platí postup: token se vloží jednorázově v prvním úkolu (§ 3.5) s pokynem uložit ho do trvalého souborového systému Work do `~/.git-credentials` (git credential helper store) a nikam jinam ho nevypisovat. Test ukáže, zda token přežije do dalšího sezení. Pokud ne, varianta B: token se vkládá při každém úkolu, který zapisuje do repa. Jakmile se zjistí, že token v historii chatu vadí (např. projekt se sdílí), token okamžitě odvolat a vystavit nový.

### 3.4 Pracovní postup agenta ChatGPT Work
1. Na začátku úkolu `git clone` (nebo `git pull` v existujícím klonu) z `main`, přečíst `AGENTS.md`, `docs/00-master-instrukce.md`, `docs/01-discovery-rozhodnuti.md`, `docs/NAVRHY.md` (AGENTS.md 2).
2. Zkontrolovat otevřené PR (`gh pr list` nebo GitHub API s tokenem); soubory z cizího otevřeného PR neměnit (AGENTS.md 6).
3. Větev `chatgpt/<ukol>`, commity podepsané `[chatgpt] <datum>`, push, PR do `main` s popisem: co se změnilo, která D čísla, zda PR potřebuje revizi (AGENTS.md 21).
4. Žádné volání The Odds API ani spouštění kolektoru v cloudu (AGENTS.md 24).

### 3.5 Testovací úkol (první zadání v ChatGPT Work)
Zadat v projektu VALBEE v ChatGPT Work tento text:

> Pracuješ na projektu VALBEE podle instrukcí projektu. Úkol: ověřit přístup k repu. 1) Naklonuj repo z `main` a vypiš poslední ID rozhodnutí v `docs/01-discovery-rozhodnuti.md` a počet otevřených pull requestů. 2) Přečti `AGENTS.md` a shrň ve třech větách svou roli. 3) Založ větev `chatgpt/test-pristup`, do `docs/NAVRHY.md` přidej řádek „Test přístupu ChatGPT Work k repu: čtení, větev, push, PR“ se stavem `novy`, podepsaný `[chatgpt]` a dnešním datem, commitni, pushni a otevři pull request do `main`. 4) Napiš, kam jsi uložil přihlašovací údaje ke GitHubu a zda budou dostupné v dalším sezení. Token nevypisuj.

Kritéria úspěchu (všechna):
- Vypsané poslední ID odpovídá `main` (po sloučení PR #1 a PR #2 je to D23).
- Existuje PR z větve `chatgpt/test-pristup` s jedním řádkem v NAVRHY, podepsaným `[chatgpt]`.
- Claude PR zreviduje (formální, nepotřebuje revizi podle bodu 21, ale ověří podpis a formát) a Lukáš sloučí.
- Druhé sezení v ChatGPT Work (nový chat ve stejném projektu) umí `git pull` a push bez opětovného vkládání tokenu. Pokud ne, platí varianta B z § 3.3 a zapíše se do NAVRHY.

Pokud test selže v bodu 1 nebo 3 (Work se k repu nedostane nebo neumí push), D21 se reviduje. Varianty k rozhodnutí: A) místo cloudového Work použít Codex v ChatGPT (má vlastní GitHub připojení s PR), B) ChatGPT Work lokálně na Lukášově PC nad klonem repa mimo OneDrive, C) Claude Cowork zpět jako primární vývojář a ChatGPT jen oponent přes konektor (čtení). Doporučení Claude: A, protože zachovává cloud a nevyžaduje zapnutý počítač; rozhodne Lukáš.

### 3.6 Druhý úkol po úspěšném testu
Zprovoznění kolektoru na serveru podle `docs/HANDOFF-2026-10-04.md` § 3 a § 5 (nejvyšší priorita, historie kurzů se od 7. 9. 2026 neukládá). Zadání: PowerShell instalátor, klíč mimo repo, absolutní cesta k Pythonu v úloze Plánovače, ověření logu. Instalátor nasazuje Lukáš na server ručně přes Vzdálenou plochu.

## 4. Instrukce projektů (vložit beze změn)

### 4.1 ChatGPT Work, projekt VALBEE

```
Projekt VALBEE: soukromá kvantitativní platforma pro sportovní analytiku a hledání value na sázkovém trhu. Pravda projektu jsou soubory v GitHub repu lukas-malik/ai-sports-platform (po přejmenování lukas-malik/valbee), nic jiného. Jsi primární vývojář (rozhodnutí D20). Před každým úkolem naklonuj nebo aktualizuj repo z větve main a přečti AGENTS.md, docs/00-master-instrukce.md, docs/01-discovery-rozhodnuti.md a docs/NAVRHY.md. Řiď se AGENTS.md beze zbytku; tento text pravidla neopakuje, aby existovala jedna verze. Pracuješ jen na úkolu zadaném v chatu. Změny jdou výhradně přes větev chatgpt/<ukol> a pull request do main; commity a zápisy podepisuj [chatgpt] a datem. Rozhoduje jen Lukáš; návrhy piš do docs/NAVRHY.md jako varianty A/B/C s doporučením. Nikdy nevypisuj tokeny ani klíče, nevolej The Odds API a nespouštěj kolektor. Komunikuj česky, věcně, oponuj místo přitakávání; když něco nevíš, napiš „nevíme“ a navrhni ověření.
```

### 4.2 Claude Project VALBEE (Claude Cowork)

```
Projekt VALBEE: soukromá kvantitativní platforma pro sportovní analytiku a hledání value na sázkovém trhu. Pravda projektu jsou soubory v GitHub repu lukas-malik/ai-sports-platform (po přejmenování lukas-malik/valbee); dokumenty v tomto Projectu jsou jen kopie (cache) a po sloučení PR se obnovují z repa. Jsi oponent (rozhodnutí D20, D21): revize pull requestů, red team, skeptic; vývoj vede ChatGPT Work. Před každým úkolem přečti z větve main AGENTS.md, docs/00-master-instrukce.md, docs/01-discovery-rozhodnuti.md a docs/NAVRHY.md a zkontroluj otevřené pull requesty. Řiď se AGENTS.md beze zbytku; tento text pravidla neopakuje. Zápis do repa jen přes větev claude/<ukol> a pull request; podpis [claude] a datum. Rozhoduje jen Lukáš; návrhy jako varianty A/B/C s doporučením. Připojená složka OneDrive VALBEE obsahuje tajemství (.env); nikdy je nevypisuj ani nekopíruj do repa. Komunikuj česky, věcně, oponuj místo přitakávání; když něco nevíš, napiš „nevíme“.
```

## 5. Ruční kroky Lukáše v pořadí

1. Sloučit PR #1 (větev `claude/valibr`: D19 až D21, pravidla rolí, HANDOFF). Bez revize druhého agenta (D20).
2. Repo: Settings, General, Danger Zone, Change visibility, Private.
3. Repo: Settings, General, Repository name: `valbee`. Poté do NAVRHY poznamenat hotovo; Claude opraví URL v dokumentech samostatným PR.
4. Sloučit PR #2 (větev `claude/valbee`: D22, D23, přejmenování na VALBEE, tento dokument). Bez revize druhého agenta (poznámka u D23).
5. Vložit instrukce § 4.2 do Claude Projectu VALBEE (nastavení projektu, pole instrukce; je dnes prázdné).
6. ChatGPT: konektor GitHub (§ 3.2), token (§ 3.3), cloudový projekt VALBEE s instrukcemi § 4.1 (§ 3.1).
7. Spustit testovací úkol § 3.5; výsledek (úspěch, nebo která varianta A/B/C) sdělit Claude, který zreviduje PR a zapíše výsledek do NAVRHY.
8. Zadat druhý úkol § 3.6 (kolektor).

## 6. Údržba kopií a stavu

- Po každém sloučení PR, který mění `docs/`, Claude obnoví kopie v Claude Projectu (ruční pokyn Lukáše v chatu Cowork, nebo při nejbližší revizi).
- ChatGPT Work žádné kopie nedrží; čte repo.
- Tento dokument se aktualizuje při každé změně způsobu připojení (nový token, přejmenování repa, výsledek testu). Historii změn nese git.

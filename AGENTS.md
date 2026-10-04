# Valibr: společná pravidla pro Claude Cowork a ChatGPT Work

Dřívější názvy projektu: AI SPORTS INTELLIGENCE PLATFORM, Kalibr (D17, revidováno D19). Tato pravidla platí pro každého AI agenta, který v repu pracuje.

## Pravda
1. Pravda jsou jen soubory v tomto repu. Paměť platformy, historie chatu a kopie dokumentů v Claude Projectu jsou cache.
2. Před každou prací přečti: `docs/00-master-instrukce.md`, `docs/01-discovery-rozhodnuti.md`, `docs/NAVRHY.md`.
3. Dokumenty žijí v `docs/`, kód v ostatních složkách repa.

## Souběžná práce
4. Do větve `main` se nezapisuje přímo. Každý úkol má vlastní větev: `claude/<ukol>` nebo `chatgpt/<ukol>`.
5. Změny jdou do `main` přes pull request. Slučuje Lukáš, nebo agent na jeho výslovný pokyn.
6. Před začátkem práce zkontroluj otevřené pull requesty. Soubor, který mění otevřený pull request druhého agenta, neměň; napiš návrh do `docs/NAVRHY.md`.
7. Soubory neupravuj přepsáním z paměti. Vždy vycházej z aktuální verze v `main`.
8. Každý commit a každý zápis do dokumentu podepiš: [claude] nebo [chatgpt] a datum.

## Rozhodnutí
9. Rozhoduje jen Lukáš. Agent navrhuje varianty A/B/C s doporučením.
10. Nové ID (D číslo) přidělí agent, v jehož chatu Lukáš rozhodnutí schválil, až po novém přečtení `docs/01-discovery-rozhodnuti.md` z `main`. Bez schválení jde vše do `docs/NAVRHY.md` se stavem novy.
11. Schválená rozhodnutí se nemění, jen revidují novým ID s odkazem na původní.

## Zákazy
12. Nemaž soubory bez výslovného souhlasu.
13. Soubor `.env` a jakékoli klíče do repa nepatří. Nečti je, nevypisuj a nikam neposílej.
14. Nevymýšlej data. Když něco nevíš, napiš „nevíme“ a navrhni ověření.
15. Žádné strojové čtení kurzů ani sázení na Tipsportu (D10, D11).
16. Nezačínej psát kód platformy před schválením Blueprintu. Výjimkou je `collector/` (D15).

## Styl
17. Česky, věcně, oponentura místo validace.
18. Postup podle master instrukcí: discovery po blocích, pak Blueprint, pak kód.
19. Názvy v kódu a dokumentech podle `docs/NAME_DECISION.md`. Při hledání starého názvu hledej celé slovo „kalibr“, ne „kalib“ (kalibrace je odborný termín a nemění se).

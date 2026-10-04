# Valibr: fronta návrhů

Sem zapisují agenti návrhy, které čekají na rozhodnutí Lukáše. Pravidla jsou v `AGENTS.md`. Návrhy se nemažou, jen se jim mění stav.

Stavy: novy, schvaleno, zamitnuto.

| Datum | Kdo navrhl | Návrh | Stav | Poznámka |
|-------|-----------|-------|------|----------|
| 2. 10. 2026 | [claude] | Ověřit, zda ChatGPT Work v cloudu umí pracovat nad tímto repem (čtení, větev, pull request) a zda načítá `AGENTS.md` | novy | Test: založit cloudový projekt, připojit repo, zeptat se na poslední ID rozhodnutí |
| 2. 10. 2026 | [claude] | Přejmenovat repo `ai-sports-platform` na `kalibr` a Claude Project na Kalibr | zamitnuto | Nahrazeno rozhodnutím D19 (název Valibr), [claude] 4. 10. 2026 |
| 4. 10. 2026 | [claude] | Přejmenovat repo na `valibr`, Claude Project a projekt v ChatGPT Work na Valibr | novy | Ruční krok Lukáše (D19). Poté opravit URL repa v `docs/01-discovery-rozhodnuti.md` a remote v klonech a na serveru; GitHub staré URL přesměrovává, dokud na starém názvu nevznikne nové repo |
| 4. 10. 2026 | [claude] | Přejmenovat kolektor kurzů: User Agent, docstring, proměnná `VALIBR_ODDS_API_KEY` se zpětnou kompatibilitou, případně složka `C:\aisp` a úloha Plánovače | novy | Lukáš rozhodne později. Samostatný PR, unit testy, kontrola logu po nejbližším běhu; sběr kurzů se nesmí přerušit (D15) |

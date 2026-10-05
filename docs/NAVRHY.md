# VALBEE: fronta návrhů

Sem zapisují agenti návrhy, které čekají na rozhodnutí Lukáše. Pravidla jsou v `AGENTS.md`. Návrhy se nemažou, jen se jim mění stav.

Stavy: novy, schvaleno, zamitnuto.

| Datum | Kdo navrhl | Návrh | Stav | Poznámka |
|-------|-----------|-------|------|----------|
| 2. 10. 2026 | [claude] | Ověřit, zda ChatGPT Work v cloudu umí pracovat nad tímto repem (čtení, větev, pull request) a zda načítá `AGENTS.md` | novy | Test: založit cloudový projekt, připojit repo, zeptat se na poslední ID rozhodnutí |
| 2. 10. 2026 | [claude] | Přejmenovat repo `ai-sports-platform` na `kalibr` a Claude Project na Kalibr | zamitnuto | Nahrazeno rozhodnutím D19 (název Valibr), [claude] 4. 10. 2026 |
| 4. 10. 2026 | [claude] | Přejmenovat repo na `valibr`, Claude Project a projekt v ChatGPT Work na Valibr | zamitnuto | Nahrazeno rozhodnutím D22 (název VALBEE), [claude] 5. 10. 2026 |
| 4. 10. 2026 | [claude] | Přejmenovat kolektor kurzů: User Agent, docstring, proměnná `VALBEE_ODDS_API_KEY` se zpětnou kompatibilitou, případně složka `C:\aisp` a úloha Plánovače | novy | Lukáš rozhodne později. Samostatný PR, unit testy, kontrola logu po nejbližším běhu; sběr kurzů se nesmí přerušit (D15) |
| 5. 10. 2026 | [claude] | Přejmenovat repo `ai-sports-platform` na `valbee` a projekt v ChatGPT Work založit jako VALBEE | novy | Ruční krok Lukáše (D22). Poté opravit URL repa v `docs/01-discovery-rozhodnuti.md` (stav D15) a v `docs/03-napojeni-platforem.md`, remote v klonech a na serveru; GitHub staré URL přesměrovává, dokud na starém názvu nevznikne nové repo |
| 5. 10. 2026 | [claude] | Ověřit ochranné známky VALBEE (ÚPV, EUIPO) a zvážit registraci valbee.cz | novy | valbee.com je registrovaná cizí stranou (RDAP 5. 10. 2026), valbee.cz volná. Nízká priorita, projekt není komerční |

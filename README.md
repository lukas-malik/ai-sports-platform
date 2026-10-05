# VALBEE

Osobní kvantitativní platforma pro sportovní analytiku, kalibraci pravděpodobností, porovnávání modelové ceny s trhem, hodnocení value, řízení rizika a auditovatelné rozhodování. Dřívější názvy: AI SPORTS INTELLIGENCE PLATFORM (do 2. 10. 2026), Kalibr (2. až 4. 10. 2026), Valibr (4. až 5. 10. 2026). Název a konvence pojmenování: `docs/NAME_DECISION.md` (D22). Stav: discovery a architektura.

Na projektu pracují ChatGPT Work (primární vývojář) a Claude (oponent), oba v cloudu nad tímto repem (D20). Pravidla pro oba agenty jsou v `AGENTS.md`; napojení obou platforem na repo popisuje `docs/03-napojeni-platforem.md`.

Obsah repa:

- `AGENTS.md` společná pravidla pro AI agenty; `CLAUDE.md` jen odkazuje na `AGENTS.md`.
- `docs/` master zadání, rozhodnutí z discovery, rešerše datových zdrojů, rozhodnutí o názvu, napojení platforem a fronta návrhů. Tyto soubory jsou pravda projektu.
- `collector/` sběr snapshotů tenisových kurzů z The Odds API (jediný kód schválený před dokončením Blueprintu, rozhodnutí D15).

Hlavní platforma vznikne až po schválení Blueprintu.

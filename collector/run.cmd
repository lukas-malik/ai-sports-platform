@echo off
rem AISP odds collector: spouštěč pro Plánovač úloh Windows.
rem Pracovní složka = složka tohoto souboru, .env a data jsou vedle skriptu.
cd /d "%~dp0"
python "%~dp0odds_collector.py" "%~dp0" >> "%~dp0logs\run_stdout.log" 2>&1

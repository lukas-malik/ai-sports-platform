"""
AI SPORTS PLATFORM: sběr snapshotů tenisových kurzů z The Odds API.

Izolovaný skript mimo hlavní architekturu platformy (rozhodnutí D15).
Cíl: od prvního dne budovat vlastní historii kurzů (opening, pohyb, closing),
kterou později naimportuje datové jádro platformy.

Zásady:
- žádné externí závislosti (jen standardní knihovna), běží na holém Pythonu 3.10+,
- každý snapshot se ukládá třikrát: surový JSON (gzip), SQLite (dotazy), CSV po měsících (čitelnost),
- rozpočet kreditů se hlídá: skript nikdy nepřekročí denní příděl odvozený ze zbývajících kreditů,
- všechny časy v UTC, ISO 8601.

Spouštění: plánovač úloh každou hodinu; skript sám rozhodne, zda snapshot udělá.
"""

from __future__ import annotations

import csv
import gzip
import json
import logging
import os
import sqlite3
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

API_BASE = "https://api.the-odds-api.com/v4"
REGIONS = "eu"
MARKETS = "h2h"
SPORT_GROUP = "Tennis"
USER_AGENT = "aisp-odds-collector/0.1"

# Kolik kreditů měsíčně nechat jako rezervu (ruční ověřování, chyby).
MONTHLY_RESERVE = 40
# Minimální odstup mezi dvěma snapshoty téhož turnaje (minuty), aby se rozpočet nespálil za den.
MIN_GAP_MINUTES = 90
# Pokud některý zápas turnaje začíná do tohoto počtu minut, snapshot má prioritu (closing kurz).
CLOSING_WINDOW_MINUTES = 150


@dataclass
class ApiResult:
    payload: object
    remaining: int | None
    used: int | None
    last_cost: int | None


# ---------------------------------------------------------------------------
# Konfigurace a prostředí
# ---------------------------------------------------------------------------

def load_env(env_path: Path) -> dict[str, str]:
    """Načte KEY=VALUE řádky z .env (bez závislosti na python-dotenv)."""
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def api_get(path: str, params: dict[str, str], api_key: str, timeout: int = 30) -> ApiResult:
    query = urllib.parse.urlencode({**params, "apiKey": api_key})
    url = f"{API_BASE}{path}?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            headers = response.headers
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"HTTP {exc.code} pro {path}: {detail}") from exc

    def header_int(name: str) -> int | None:
        raw = headers.get(name)
        try:
            return int(float(raw)) if raw is not None else None
        except ValueError:
            return None

    return ApiResult(
        payload=json.loads(body),
        remaining=header_int("x-requests-remaining"),
        used=header_int("x-requests-used"),
        last_cost=header_int("x-requests-last"),
    )


# ---------------------------------------------------------------------------
# Úložiště
# ---------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts_utc TEXT NOT NULL,
    credits_used INTEGER NOT NULL DEFAULT 0,
    credits_remaining INTEGER,
    note TEXT
);
CREATE TABLE IF NOT EXISTS sport_snapshots (
    sport_key TEXT NOT NULL,
    ts_utc TEXT NOT NULL,
    run_id INTEGER NOT NULL,
    event_count INTEGER NOT NULL,
    PRIMARY KEY (sport_key, ts_utc)
);
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    sport_key TEXT NOT NULL,
    sport_title TEXT,
    commence_time TEXT NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS odds (
    snapshot_ts TEXT NOT NULL,
    event_id TEXT NOT NULL,
    bookmaker_key TEXT NOT NULL,
    market TEXT NOT NULL,
    outcome_name TEXT NOT NULL,
    price REAL NOT NULL,
    bookmaker_last_update TEXT,
    PRIMARY KEY (snapshot_ts, event_id, bookmaker_key, market, outcome_name)
);
CREATE INDEX IF NOT EXISTS idx_odds_event ON odds (event_id, snapshot_ts);
CREATE INDEX IF NOT EXISTS idx_events_commence ON events (commence_time);
"""

CSV_HEADER = [
    "snapshot_ts", "sport_key", "event_id", "commence_time", "home_team", "away_team",
    "bookmaker_key", "market", "outcome_name", "price", "bookmaker_last_update",
]


def open_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    return conn


@dataclass
class OddsRow:
    snapshot_ts: str
    sport_key: str
    event_id: str
    commence_time: str
    home_team: str
    away_team: str
    bookmaker_key: str
    market: str
    outcome_name: str
    price: float
    bookmaker_last_update: str | None


def flatten_odds(sport_key: str, snapshot_ts: str, events_payload: list) -> list[OddsRow]:
    """Převede odpověď /odds na ploché řádky. Čistá funkce, testovatelná bez sítě."""
    rows: list[OddsRow] = []
    for event in events_payload:
        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                for outcome in market.get("outcomes", []):
                    price = outcome.get("price")
                    if price is None:
                        continue
                    rows.append(OddsRow(
                        snapshot_ts=snapshot_ts,
                        sport_key=sport_key,
                        event_id=event["id"],
                        commence_time=event["commence_time"],
                        home_team=event.get("home_team") or "",
                        away_team=event.get("away_team") or "",
                        bookmaker_key=bookmaker["key"],
                        market=market["key"],
                        outcome_name=outcome["name"],
                        price=float(price),
                        bookmaker_last_update=market.get("last_update") or bookmaker.get("last_update"),
                    ))
    return rows


def store_snapshot(conn: sqlite3.Connection, run_id: int, sport_key: str, sport_title: str,
                   snapshot_ts: str, events_payload: list, rows: list[OddsRow]) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO sport_snapshots (sport_key, ts_utc, run_id, event_count) VALUES (?, ?, ?, ?)",
        (sport_key, snapshot_ts, run_id, len(events_payload)),
    )
    for event in events_payload:
        conn.execute(
            """
            INSERT INTO events (event_id, sport_key, sport_title, commence_time, home_team, away_team, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(event_id) DO UPDATE SET
                commence_time = excluded.commence_time,
                last_seen = excluded.last_seen
            """,
            (event["id"], sport_key, sport_title, event["commence_time"],
             event.get("home_team") or "", event.get("away_team") or "", snapshot_ts, snapshot_ts),
        )
    conn.executemany(
        """
        INSERT OR REPLACE INTO odds
        (snapshot_ts, event_id, bookmaker_key, market, outcome_name, price, bookmaker_last_update)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [(r.snapshot_ts, r.event_id, r.bookmaker_key, r.market, r.outcome_name, r.price, r.bookmaker_last_update)
         for r in rows],
    )


def append_csv(csv_dir: Path, rows: list[OddsRow]) -> None:
    if not rows:
        return
    csv_dir.mkdir(parents=True, exist_ok=True)
    month = rows[0].snapshot_ts[:7]
    path = csv_dir / f"odds_{month}.csv"
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(CSV_HEADER)
        for r in rows:
            writer.writerow([
                r.snapshot_ts, r.sport_key, r.event_id, r.commence_time, r.home_team, r.away_team,
                r.bookmaker_key, r.market, r.outcome_name, f"{r.price:.3f}", r.bookmaker_last_update or "",
            ])


def save_raw(raw_dir: Path, snapshot_ts: str, sport_key: str, payload: object) -> None:
    day_dir = raw_dir / snapshot_ts[:10]
    day_dir.mkdir(parents=True, exist_ok=True)
    stamp = snapshot_ts[11:16].replace(":", "")
    path = day_dir / f"{stamp}_{sport_key}.json.gz"
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Rozhodování o rozpočtu
# ---------------------------------------------------------------------------

def days_left_in_month(now: datetime) -> int:
    """Počet dní včetně dnešního do konce měsíce (UTC)."""
    year, month = now.year, now.month
    if month == 12:
        first_next = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        first_next = datetime(year, month + 1, 1, tzinfo=timezone.utc)
    return max(1, (first_next.date() - now.date()).days)


def daily_allowance(remaining: int | None, now: datetime) -> int:
    """Kolik kreditů smíme dnes utratit, aby rezerva vydržela do konce měsíce."""
    if remaining is None:
        return 0
    spendable = max(0, remaining - MONTHLY_RESERVE)
    return spendable // days_left_in_month(now)


def credits_used_today(conn: sqlite3.Connection, now: datetime) -> int:
    day = now.strftime("%Y-%m-%d")
    row = conn.execute(
        "SELECT COALESCE(SUM(credits_used), 0) FROM runs WHERE substr(ts_utc, 1, 10) = ?", (day,)
    ).fetchone()
    return int(row[0]) if row else 0


def last_snapshot_ts(conn: sqlite3.Connection, sport_key: str) -> datetime | None:
    row = conn.execute(
        "SELECT MAX(ts_utc) FROM sport_snapshots WHERE sport_key = ?", (sport_key,)
    ).fetchone()
    return parse_iso(row[0]) if row and row[0] else None


def next_commence_within(conn: sqlite3.Connection, sport_key: str, now: datetime, minutes: int) -> bool:
    """Známe (z minulých snapshotů) zápas tohoto turnaje, který začíná do N minut?"""
    row = conn.execute(
        "SELECT MIN(commence_time) FROM events WHERE sport_key = ? AND commence_time > ?",
        (sport_key, iso(now)),
    ).fetchone()
    if not row or not row[0]:
        return False
    delta = (parse_iso(row[0]) - now).total_seconds() / 60
    return delta <= minutes


def prioritize(conn: sqlite3.Connection, sport_keys: list[str], now: datetime) -> list[str]:
    """Seřadí turnaje: nejdřív ty s blízkým začátkem zápasu (closing), pak podle stáří posledního snapshotu."""
    def sort_key(key: str):
        closing = 0 if next_commence_within(conn, key, now, CLOSING_WINDOW_MINUTES) else 1
        last = last_snapshot_ts(conn, key)
        age = (now - last).total_seconds() if last else float("inf")
        return (closing, -age)
    return sorted(sport_keys, key=sort_key)


def should_snapshot(conn: sqlite3.Connection, sport_key: str, now: datetime) -> bool:
    last = last_snapshot_ts(conn, sport_key)
    if last is None:
        return True
    gap_minutes = (now - last).total_seconds() / 60
    if gap_minutes >= MIN_GAP_MINUTES:
        return True
    return next_commence_within(conn, sport_key, now, CLOSING_WINDOW_MINUTES) and gap_minutes >= 30


# ---------------------------------------------------------------------------
# Hlavní běh
# ---------------------------------------------------------------------------

def run(base_dir: Path) -> int:
    log = logging.getLogger("collector")
    env = load_env(base_dir / ".env")
    api_key = env.get("ODDS_API_KEY") or os.environ.get("ODDS_API_KEY")
    if not api_key:
        log.error("Chybí ODDS_API_KEY v .env nebo v prostředí.")
        return 2

    data_dir = base_dir / "data"
    conn = open_db(data_dir / "odds_snapshots.sqlite")
    now = utc_now()
    snapshot_ts = iso(now)

    # 1) Seznam aktivních tenisových turnajů. Endpoint /sports nestojí kredity, ale vrací hlavičky se stavem.
    try:
        sports = api_get("/sports", {"all": "false"}, api_key)
    except (RuntimeError, urllib.error.URLError, TimeoutError) as exc:
        log.error("Nelze načíst seznam sportů: %s", exc)
        conn.execute("INSERT INTO runs (ts_utc, credits_used, note) VALUES (?, 0, ?)", (snapshot_ts, f"sports_error: {exc}"))
        conn.commit()
        return 1

    tennis = [s for s in sports.payload if s.get("group") == SPORT_GROUP and s.get("active")]
    titles = {s["key"]: s.get("title", s["key"]) for s in tennis}
    keys = [s["key"] for s in tennis]

    allowance = daily_allowance(sports.remaining, now)
    used_today = credits_used_today(conn, now)
    budget = max(0, allowance - used_today)
    log.info("Aktivní tenisové turnaje: %d (%s). Zbývá kreditů: %s. Denní příděl: %d, dnes použito: %d, k dispozici: %d.",
             len(keys), ", ".join(keys) or "žádné", sports.remaining, allowance, used_today, budget)

    cur = conn.execute("INSERT INTO runs (ts_utc, credits_used, credits_remaining, note) VALUES (?, 0, ?, ?)",
                       (snapshot_ts, sports.remaining, f"active={len(keys)} allowance={allowance}"))
    run_id = cur.lastrowid
    conn.commit()

    credits_spent = 0
    remaining = sports.remaining
    for key in prioritize(conn, keys, now):
        if credits_spent >= budget:
            log.info("Rozpočet pro dnešek vyčerpán, přeskakuji %s.", key)
            continue
        if not should_snapshot(conn, key, now):
            log.info("Příliš čerstvý snapshot, přeskakuji %s.", key)
            continue
        try:
            result = api_get(f"/sports/{key}/odds", {"regions": REGIONS, "markets": MARKETS, "oddsFormat": "decimal"}, api_key)
        except (RuntimeError, urllib.error.URLError, TimeoutError) as exc:
            log.error("Snapshot %s selhal: %s", key, exc)
            continue
        cost = result.last_cost if result.last_cost is not None else 1
        credits_spent += cost
        remaining = result.remaining if result.remaining is not None else remaining
        events_payload = result.payload if isinstance(result.payload, list) else []
        rows = flatten_odds(key, snapshot_ts, events_payload)
        save_raw(data_dir / "raw", snapshot_ts, key, events_payload)
        store_snapshot(conn, run_id, key, titles.get(key, key), snapshot_ts, events_payload, rows)
        append_csv(data_dir / "csv", rows)
        conn.commit()
        log.info("Snapshot %s: %d zápasů, %d řádků kurzů, cena %d kreditů.", key, len(events_payload), len(rows), cost)

    conn.execute("UPDATE runs SET credits_used = ?, credits_remaining = ? WHERE run_id = ?",
                 (credits_spent, remaining, run_id))
    conn.commit()
    conn.close()
    log.info("Hotovo. Utraceno %d kreditů, zbývá %s.", credits_spent, remaining)
    return 0


def main() -> int:
    base_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_dir / f"collector_{utc_now().strftime('%Y-%m')}.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return run(base_dir)


if __name__ == "__main__":
    sys.exit(main())

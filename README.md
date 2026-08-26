# NBA Model Dashboard — Phase 1

A CSV-backed vertical slice that retrieves structured NBA advanced player game logs, validates them in Python, serves them with FastAPI, and displays them in a responsive dark dashboard.

## Data method and semantics

The client calls the official structured `https://stats.nba.com/stats/playergamelogs` JSON endpoint directly with `Season=2025-26`, `SeasonType=Regular Season`, `LastNGames=10`, and `MeasureType=Advanced`. It uses a 30-second timeout, two limited exponential-backoff retries for connection/timeouts, and ordinary NBA.com origin/referer headers. NBA normally returns `USG_PCT` as a fraction (`.297` means 29.7%). The processor detects percentage-form responses from the distribution and converts only those. `NET_RATING` remains a numeric rating.

Generated raw and processed files are ignored because they can be large and change each refresh; tests create deterministic fixtures in temporary directories. The processed output is `data/processed/nba_advanced_boxscores_last10.csv`; raw JSON and metadata are stored in the corresponding data directories.

## Requirements and installation

Python 3.12+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate                 # macOS/Linux
# .venv\Scripts\Activate.ps1             # Windows PowerShell
pip install -r requirements.txt
```

Configuration environment overrides are listed in `.env.example`.

## Retrieve, test, and run

```bash
python scripts/refresh_advanced_boxscores.py
pytest
RUN_NBA_INTEGRATION=1 pytest -m integration -v
python scripts/smoke_test.py
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/advanced-boxscores. Page loads read the saved CSV, not NBA.com. Only the explicit refresh action contacts NBA. A validated temporary CSV atomically replaces the prior version, preserving good data after failures.

NBA Stats may rate-limit, block, or time out cloud/datacenter addresses. This client fails explicitly rather than evading blocks or retrying continuously. Run the live commands from another network if this environment is refused.

## Interface license

The dark shell is adapted from the visual structure of HTML5 UP **Editorial**. Required attribution is retained in the sidebar/footer; Editorial is offered under Creative Commons Attribution 3.0.

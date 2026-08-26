from dataclasses import dataclass
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class Settings:
    season: str = os.getenv("NBA_SEASON", "2025-26")
    season_type: str = os.getenv("NBA_SEASON_TYPE", "Regular Season")
    last_n_games: int = int(os.getenv("NBA_LAST_N_GAMES", "10"))
    measure_type: str = os.getenv("NBA_MEASURE_TYPE", "Advanced")
    request_timeout: float = float(os.getenv("NBA_REQUEST_TIMEOUT", "30"))
    processed_csv: Path = ROOT / "data/processed/nba_advanced_boxscores_last10.csv"
    raw_json: Path = ROOT / "data/raw/nba_advanced_boxscores_last10_raw.json"
    metadata_json: Path = ROOT / "data/processed/nba_advanced_boxscores_last10_metadata.json"

settings = Settings()

import logging
import time
from typing import Any

import pandas as pd
import requests

log = logging.getLogger(__name__)

class NBADataError(RuntimeError):
    """The structured NBA data source could not supply usable data."""

class NBAAdvancedBoxScoreClient:
    endpoint = "https://stats.nba.com/stats/playergamelogs"

    def __init__(self, timeout: float = 30, retries: int = 2, session: requests.Session | None = None):
        self.timeout, self.retries = timeout, retries
        self.session = session or requests.Session()

    def fetch_player_game_logs(self, season: str, season_type: str, last_n_games: int,
                               measure_type: str = "Advanced") -> pd.DataFrame:
        params = {"Season": season, "SeasonType": season_type, "LastNGames": last_n_games,
                  "MeasureType": measure_type, "LeagueID": "00", "PlayerOrTeam": "P",
                  "DateFrom": "", "DateTo": "", "Sorter": "DATE", "Direction": "DESC",
                  "Counter": "0", "PORound": "0", "Outcome": "", "Location": "",
                  "Month": "0", "OpponentTeamID": "0", "VsConference": "",
                  "VsDivision": "", "SeasonSegment": "", "ShotClockRange": ""}
        headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.nba.com/",
                   "Origin": "https://www.nba.com", "Accept": "application/json"}
        log.info("Requesting NBA playergamelogs season=%s type=%s last_n=%s measure=%s",
                 season, season_type, last_n_games, measure_type)
        for attempt in range(self.retries + 1):
            try:
                response = self.session.get(self.endpoint, params=params, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                payload: dict[str, Any] = response.json()
                result = (payload.get("resultSets") or payload.get("resultSet"))
                if isinstance(result, list): result = result[0] if result else None
                if not result:
                    raise NBADataError("NBA response did not contain a result set.")
                frame = pd.DataFrame(result.get("rowSet", []), columns=result.get("headers", []))
                if frame.empty:
                    raise NBADataError("NBA returned no advanced box-score rows for the configured request.")
                log.info("NBA request completed: %d rows", len(frame))
                return frame
            except NBADataError:
                raise
            except (requests.Timeout, requests.ConnectionError) as exc:
                if attempt < self.retries:
                    time.sleep(0.5 * 2**attempt)
                    continue
                raise NBADataError(f"NBA request failed after {attempt + 1} attempts: {exc}") from exc
            except (requests.HTTPError, ValueError, KeyError) as exc:
                raise NBADataError(f"NBA request failed: {exc}") from exc
        raise NBADataError("NBA request failed unexpectedly.")

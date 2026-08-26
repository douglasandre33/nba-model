from pydantic import BaseModel

class DatasetMetadata(BaseModel):
    season: str
    season_type: str
    last_n_games: int
    measure_type: str
    retrieved_at_utc: str
    row_count: int
    unique_player_count: int
    unique_team_count: int
    unique_game_count: int
    processed_csv_path: str

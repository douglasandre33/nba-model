import pandas as pd, pytest
from app.config import Settings
@pytest.fixture
def raw_df():
 return pd.DataFrame([{"PLAYER_ID":1,"PLAYER_NAME":"A Player","TEAM_ID":10,"TEAM_ABBREVIATION":"BOS","TEAM_NAME":"Boston Celtics","GAME_ID":"001","GAME_DATE":"2026-04-01","MATCHUP":"BOS vs. NYK","WL":"W","MIN":31,"OFF_RATING":120.1,"DEF_RATING":110.2,"NET_RATING":9.9,"USG_PCT":.297}]*2)
@pytest.fixture
def test_settings(tmp_path):
 return Settings(processed_csv=tmp_path/'processed/data.csv',raw_json=tmp_path/'raw/data.json',metadata_json=tmp_path/'processed/meta.json')

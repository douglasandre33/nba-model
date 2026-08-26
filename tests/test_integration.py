import os, pytest
from app.config import settings
from app.data.nba_client import NBAAdvancedBoxScoreClient
from app.data.processor import clean_advanced_boxscores
@pytest.mark.integration
@pytest.mark.skipif(os.getenv('RUN_NBA_INTEGRATION')!='1',reason='set RUN_NBA_INTEGRATION=1')
def test_live_nba():
 raw=NBAAdvancedBoxScoreClient(timeout=settings.request_timeout).fetch_player_game_logs(settings.season,settings.season_type,settings.last_n_games,settings.measure_type); df=clean_advanced_boxscores(raw); assert not df.empty; assert {'PLAYER_ID','PLAYER_NAME','GAME_ID','GAME_DATE','TEAM','NET_RATING','USG_PCT'}<=set(df); assert df.groupby('PLAYER_ID').size().max()<=10; assert df.USG_PCT.between(0,1).all()

import json
from fastapi.testclient import TestClient
from app.main import app,service
from app.data.processor import clean_advanced_boxscores
def seed(raw_df):
 df=clean_advanced_boxscores(raw_df); service.config.processed_csv.parent.mkdir(parents=True); df.to_csv(service.config.processed_csv,index=False); service.config.metadata_json.write_text(json.dumps({'season':'2025-26','season_type':'Regular Season','last_n_games':10,'measure_type':'Advanced','retrieved_at_utc':'2026-01-01T00:00:00+00:00','row_count':1,'unique_player_count':1,'unique_team_count':1,'unique_game_count':1,'processed_csv_path':'data.csv'}))
def test_endpoints(monkeypatch,test_settings,raw_df):
 monkeypatch.setattr(service,'config',test_settings); seed(raw_df); c=TestClient(app); assert c.get('/api/health').json()=={'status':'ok'}; assert len(c.get('/api/advanced-boxscores').json()['data'])==1; assert c.get('/api/advanced-boxscores/metadata').status_code==200; assert c.get('/api/advanced-boxscores.csv').headers['content-type'].startswith('text/csv'); assert c.get('/advanced-boxscores').status_code==200
def test_refresh_endpoint(monkeypatch,test_settings,raw_df):
 monkeypatch.setattr(service,'config',test_settings); monkeypatch.setattr(service.client,'fetch_player_game_logs',lambda *a:raw_df); assert TestClient(app).post('/api/advanced-boxscores/refresh').status_code==200

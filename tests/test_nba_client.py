import requests, pytest
from app.data.nba_client import NBAAdvancedBoxScoreClient,NBADataError
class Response:
 def __init__(self,status=200): self.status_code=status
 def raise_for_status(self):
  if self.status_code>=400: raise requests.HTTPError(str(self.status_code))
 def json(self): return {'resultSets':[{'headers':['PLAYER_ID'],'rowSet':[[1]]}]}
class Session:
 def __init__(self,effects): self.effects=list(effects); self.calls=[]
 def get(self,*a,**kw):
  self.calls.append((a,kw)); e=self.effects.pop(0)
  if isinstance(e,Exception): raise e
  return e
def test_parameters_and_timeout():
 s=Session([Response()]); NBAAdvancedBoxScoreClient(timeout=7,session=s).fetch_player_game_logs('2025-26','Regular Season',10); kw=s.calls[0][1]; assert kw['params']['MeasureType']=='Advanced' and kw['params']['LastNGames']==10 and kw['timeout']==7
def test_transient_retry(monkeypatch):
 monkeypatch.setattr('time.sleep',lambda _:None); s=Session([requests.Timeout(),Response()]); assert len(NBAAdvancedBoxScoreClient(retries=1,session=s).fetch_player_game_logs('x','y',10))==1
def test_permanent_failure():
 with pytest.raises(NBADataError): NBAAdvancedBoxScoreClient(session=Session([Response(403)])).fetch_player_game_logs('x','y',10)

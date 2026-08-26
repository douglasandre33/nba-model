import json, logging, os, tempfile
from datetime import datetime, timezone
import pandas as pd
from app.config import Settings, settings
from app.data.nba_client import NBAAdvancedBoxScoreClient
from app.data.processor import DataValidationError, clean_advanced_boxscores

log = logging.getLogger(__name__)
class DatasetUnavailableError(FileNotFoundError): pass

class AdvancedBoxScoreService:
    def __init__(self, config: Settings = settings, client=None):
        self.config = config
        self.client = client or NBAAdvancedBoxScoreClient(timeout=config.request_timeout)
    def refresh(self):
        c=self.config; log.info("Starting NBA advanced box-score refresh")
        raw=self.client.fetch_player_game_logs(c.season,c.season_type,c.last_n_games,c.measure_type)
        clean=clean_advanced_boxscores(raw)
        per_player = clean.groupby("PLAYER_ID").size()
        if not per_player.empty and int(per_player.max()) > c.last_n_games:
            raise DataValidationError(f"LastNGames validation failed: a player has {int(per_player.max())} rows (expected at most {c.last_n_games}).")
        c.raw_json.parent.mkdir(parents=True,exist_ok=True); c.processed_csv.parent.mkdir(parents=True,exist_ok=True)
        c.raw_json.write_text(raw.to_json(orient="records",date_format="iso"),encoding="utf-8")
        metadata={"season":c.season,"season_type":c.season_type,"last_n_games":c.last_n_games,
          "measure_type":c.measure_type,"retrieved_at_utc":datetime.now(timezone.utc).isoformat(),
          "row_count":len(clean),"unique_player_count":clean.PLAYER_ID.nunique(),
          "unique_team_count":clean.TEAM.nunique(),"unique_game_count":clean.GAME_ID.nunique(),
          "missing_player_id":int(clean.PLAYER_ID.isna().sum()),"missing_player_name":int(clean.PLAYER_NAME.isna().sum()),
          "missing_game_id":int(clean.GAME_ID.isna().sum()),"missing_team":int(clean.TEAM.isna().sum()),
          "missing_net_rating":int(clean.NET_RATING.isna().sum()),"missing_usg_pct":int(clean.USG_PCT.isna().sum()),
          "duplicate_player_game_count":int(clean.duplicated(["PLAYER_ID","GAME_ID"]).sum()),
          "processed_csv_path":str(c.processed_csv.relative_to(c.processed_csv.parents[2]))}
        fd,tmp=tempfile.mkstemp(dir=c.processed_csv.parent,suffix=".csv"); os.close(fd)
        try:
            clean.to_csv(tmp,index=False,encoding="utf-8",date_format="%Y-%m-%d")
            os.replace(tmp,c.processed_csv)
            c.metadata_json.write_text(json.dumps(metadata,indent=2),encoding="utf-8")
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        log.info("Refresh completed: rows=%d players=%d teams=%d games=%d",len(clean),metadata["unique_player_count"],metadata["unique_team_count"],metadata["unique_game_count"])
        log.info("Data quality: missing critical fields=%d duplicate player-games=%d",
                 sum(metadata[k] for k in ("missing_player_id","missing_player_name","missing_game_id","missing_team","missing_net_rating","missing_usg_pct")),
                 metadata["duplicate_player_game_count"])
        return metadata
    def load_data(self):
        if not self.config.processed_csv.exists(): raise DatasetUnavailableError("No NBA dataset is currently available.")
        return pd.read_csv(self.config.processed_csv,dtype={"GAME_ID":"string"})
    def load_metadata(self):
        if not self.config.metadata_json.exists(): raise DatasetUnavailableError("No NBA dataset metadata is currently available.")
        return json.loads(self.config.metadata_json.read_text(encoding="utf-8"))

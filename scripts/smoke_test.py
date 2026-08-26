#!/usr/bin/env python
from pathlib import Path
import sys, pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.services.advanced_boxscores import AdvancedBoxScoreService
if __name__ == "__main__":
 s=AdvancedBoxScoreService(); m=s.refresh(); df=pd.read_csv(s.config.processed_csv)
 assert len(df)==m['row_count']>0 and df.USG_PCT.between(0,1).all() and pd.to_numeric(df.NET_RATING,errors='coerce').notna().all()
 print(f"NBA ADVANCED BOX SCORE SMOKE TEST\n{'-'*33}\nSeason: {m['season']} {m['season_type']} | Last N Games: {m['last_n_games']}\nRows: {len(df):,} | Players: {m['unique_player_count']:,} | Teams: {m['unique_team_count']:,} | Games: {m['unique_game_count']:,}\nNET_RATING: PASS | USG_PCT: PASS | CSV write/reload: PASS\nSMOKE TEST: PASS")

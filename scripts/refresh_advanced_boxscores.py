#!/usr/bin/env python
from pathlib import Path
import sys, json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.services.advanced_boxscores import AdvancedBoxScoreService
if __name__ == "__main__": print(json.dumps(AdvancedBoxScoreService().refresh(),indent=2))

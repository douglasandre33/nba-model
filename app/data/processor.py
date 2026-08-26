import pandas as pd

class DataValidationError(ValueError): pass

ALIASES = {"TEAM_ABBREVIATION": "TEAM", "OFFRTG": "OFF_RATING", "DEFRTG": "DEF_RATING",
           "NETRTG": "NET_RATING", "USG%": "USG_PCT", "PERSON_ID": "PLAYER_ID",
           "PERSON_NAME": "PLAYER_NAME"}
REQUIRED = ["PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "TEAM", "TEAM_NAME", "GAME_ID",
            "GAME_DATE", "MATCHUP", "WL", "MIN", "OFF_RATING", "DEF_RATING",
            "NET_RATING", "USG_PCT"]
OPTIONAL = ["AST_PCT", "AST_TO", "AST_RATIO", "OREB_PCT", "DREB_PCT", "REB_PCT",
            "TM_TOV_PCT", "EFG_PCT", "TS_PCT", "PACE", "PIE"]

def clean_advanced_boxscores(raw_df: pd.DataFrame) -> pd.DataFrame:
    if raw_df.empty: raise DataValidationError("NBA advanced dataset is empty.")
    df = raw_df.copy()
    df.columns = [str(c).strip().upper() for c in df.columns]
    df = df.rename(columns=ALIASES)
    if "USG_PCT" not in df: raise DataValidationError("NBA advanced dataset does not contain a recognized usage percentage field.")
    if "NET_RATING" not in df: raise DataValidationError("NBA advanced dataset does not contain a recognized net rating field.")
    missing = [c for c in REQUIRED if c not in df]
    if missing: raise DataValidationError(f"NBA advanced dataset is missing required columns: {', '.join(missing)}")
    df = df[[*REQUIRED, *[c for c in OPTIONAL if c in df]]].drop_duplicates()
    for col in ["PLAYER_ID", "TEAM_ID"]: df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    df["GAME_ID"] = df["GAME_ID"].astype("string").str.strip()
    numeric = ["MIN", "OFF_RATING", "DEF_RATING", "NET_RATING", "USG_PCT", *[c for c in OPTIONAL if c in df]]
    for col in numeric: df[col] = pd.to_numeric(df[col], errors="coerce")
    non_null_usage = df["USG_PCT"].dropna()
    if not non_null_usage.empty and non_null_usage.quantile(.95) > 1:
        df["USG_PCT"] = df["USG_PCT"] / 100
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"], errors="coerce")
    critical = ["PLAYER_ID", "PLAYER_NAME", "GAME_ID", "GAME_DATE", "TEAM", "NET_RATING", "USG_PCT"]
    invalid = {c: int(df[c].isna().sum() | (df[c].astype("string").str.strip().eq("").sum() if c in ["PLAYER_NAME","GAME_ID","TEAM"] else 0)) for c in critical}
    bad = {k:v for k,v in invalid.items() if v}
    if bad: raise DataValidationError(f"Critical fields contain missing/invalid values: {bad}")
    if not df["USG_PCT"].between(0, 1).all(): raise DataValidationError("USG_PCT values are outside normalized range 0..1.")
    duplicates = df.duplicated(["PLAYER_ID", "GAME_ID"], keep=False)
    if duplicates.any(): raise DataValidationError("Duplicate PLAYER_ID + GAME_ID observations found.")
    return df.sort_values(["GAME_DATE", "PLAYER_NAME"], ascending=[False, True]).reset_index(drop=True)

import pandas as pd, pytest
from app.data.processor import clean_advanced_boxscores,DataValidationError,REQUIRED
def test_cleaning_and_duplicates(raw_df):
 out=clean_advanced_boxscores(raw_df); assert len(out)==1 and out.TEAM.iloc[0]=='BOS' and out.USG_PCT.iloc[0]==.297; assert pd.api.types.is_datetime64_any_dtype(out.GAME_DATE); assert set(REQUIRED)<=set(out)
def test_percentage_form_normalized(raw_df): raw_df.USG_PCT=29.7; assert clean_advanced_boxscores(raw_df).USG_PCT.iloc[0]==pytest.approx(.297)
def test_missing_usage_is_explicit(raw_df):
 with pytest.raises(DataValidationError,match='usage percentage'): clean_advanced_boxscores(raw_df.drop(columns='USG_PCT'))
def test_net_rating_numeric(raw_df): raw_df.NET_RATING='9.9'; assert clean_advanced_boxscores(raw_df).NET_RATING.iloc[0]==9.9

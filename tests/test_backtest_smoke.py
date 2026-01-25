import pandas as pd
from src.features.build_features import add_features

def test_features_smoke():
    df = pd.DataFrame({
        "date": pd.date_range("2020-01-01", periods=250),
        "close": range(250),
    })
    df["open"] = df["high"] = df["low"] = df["close"]
    df["volume"] = 1000
    df["ret_1d"] = df["close"].pct_change()
    out = add_features(df)
    assert "ma_fast" in out.columns
    assert len(out) > 0
import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ret_1d"] = out["close"].pct_change()
    out["ret_5d"] = out["close"].pct_change(5)
    out["vol_20d"] = out["ret_1d"].rolling(20).std() * (252 ** 0.5)
    out["ma_fast"] = out["close"].rolling(20).mean()
    out["ma_slow"].rolling(100).mean()
    out["z_20"] = (out["close"] - out["close"].rolling(20).mean()) / out["close"].rolling(20).std()
    out["fwd_ret_1d"] = out["close"].pct_change().shift(-1)
    return out.dropna().reset_index(drop=True)
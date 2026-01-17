import pandas as pd
import numpy as np

def trend_signal(df: pd.DataFrame) -> pd.Series:
    return (df["ma_fast"] > df["ma_slow"]).astype(int)

def mean_reversion_signal(df: pd.DataFrame, entry_z: float = -1.0, exit_z: float = -0.2) -> pd.Series:
    sig = np.zeros(len(df), dtype=int)
    in_pos = False
    for i, z in enumerate(df["z_20"].values):
        if not in_pos and z <= entry_z:
            in_pos = True
        elif in_pos and z >= exit_z:
            in_pos = False
        sig[i] = 1 if in_pos else 0
    return pd.Series(sig, index=df.index)
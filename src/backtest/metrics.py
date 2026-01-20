import numpy as np
import pandas as pd

def equity_curve(returns: pd.Series) -> pd.Series:
    return (1 + returns.fillna(0)).cumprod()

def sharpe(returns: pd.Series, periods: int = 252) -> float:
    r = returns.dropna()
    if r.std() == 0:
        return 0.0
    return float((r.mean() / r.std()) * np.sqrt(periods))

def max_drawdown(equity: pd.Series) -> float:
    peak = equity.cummax()
    dd = (equity / peak) - 1.0
    return float(dd.min())
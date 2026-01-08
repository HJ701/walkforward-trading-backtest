from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import yfinance as yf
from src.utils.config import PATHS
from src.utils.logging import get_logger

log = get_logger(__name__)

@dataclass(frozen=True)
class DownloadSpec:
    ticker: str = "SPY"
    start: str = "2010-01-01"
    end: str | None = None

def download_ohlcv(spec: DownloadSpec) -> pd.DataFrame:
    df = yf.download(spec.ticker, start=spec.start, end=spec.end, auto_adjust=False, progress=False)
    if df.empty:
        raise RuntimeError("No data returned. Check ticker or network availability.")
    df = df.rename(columns=str.lower).reset_index()
    df.columns = [c.replace(" ", "_") for c in df.columns]
    return df

def save_raw(df: pd.DataFrame, ticker: str) -> Path:
    PATHS.data_raw.mkdir(parents=True, exist_ok=True)
    out = PATHS.data_raw / f"{ticker}_ohlcv.csv"
    df.to_csv(out, index=False)
    log.info(f"Wrote raw: {out}")
    return out

def main():
    spec = DownloadSpec()
    df = download_ohlcv(spec)
    save_raw(df, spec.ticker)

if __name__ == "__main__":
    main()
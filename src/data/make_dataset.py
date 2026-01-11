from pathlib import Path
import pandas as pd
from src.utils.config import PATHS
from src.utils.logging import get_logger

log = get_logger(__name__)

def main(ticker: str = "SPY") -> None:
    raw_path = PATHS.data_raw / f"{ticker}_ohlcv.csv"
    if not raw_path.exists():
        raise FileNotFoundError(f"Missing raw file: {raw_path}. Run download first.")
    df = pd.read_csv(raw_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").dropna().reset_index(drop=True)
    PATHS.data_processed.mkdir(parents=True, exist_ok=True)
    out = PATHS.data_processed / f"{ticker}_processed.csv"
    df.to_csv(out, index=False)
    log.info(f"Wrote processed: {out}")

if __name__ == "__main__":
    main()
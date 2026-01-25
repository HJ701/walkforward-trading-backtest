import pandas as pd
from src.data.download_prices import download_ohlcv, DownloadSpec

def test_download_smoke():
    df = download_ohlcv(DownloadSpec(ticker="SPY", start="2020-01-01", end="2020-02-01"))
    assert not df.empty
    assert "close" in df.columns
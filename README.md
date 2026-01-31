# Walk-Forward Trading Backtest (Public Data)
A quant project comparing Trend-following vs Mean-reversion using walk-forward testing.

## Quickstart
```bash
# Install
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run end-to-end
python -m src.data.download_prices && python -m src.data.make_dataset && python -m src.backtest.walkforward && pytest -q
```
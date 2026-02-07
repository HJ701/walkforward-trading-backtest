# 📈 Algorithmic Trading Walk-Forward Backtest: Strategy Validation System

![Project Banner](tests/trade.png)

## 👋 About the Project

This repository implements a **Walk-Forward Backtesting** framework for algorithmic trading strategies using publicly available financial market data from Yahoo Finance. The project downloads historical price data locally and compares two fundamental trading approaches: **Trend Following** (based on moving average crossovers) and **Mean Reversion** (based on Z-score thresholds).

To minimize overfitting risks on historical data, the system employs a rolling validation mechanism that progressively shifts training and testing periods. Performance is evaluated through Sharpe ratio, maximum drawdown, and equity curve visualizations—providing a realistic assessment of strategy viability.

## 🎯 What Does It Do?

- **Data Acquisition**: Downloads historical OHLCV data from Yahoo Finance (default: SPY ETF)
- **Dual Strategies**: Implements and compares Trend Following vs. Mean Reversion approaches
- **Walk-Forward Validation**: Prevents overfitting through sequential train/test window progression
- **Risk Metrics**: Calculates Sharpe ratio, maximum drawdown, and total returns
- **Performance Visualization**: Generates equity curves comparing strategy performance against buy-and-hold

## 🛠️ Installation

Set up your environment with the following steps:

```bash
# Clone the repository
git clone https://github.com/username/trading-walkforward-backtest.git
cd trading-walkforward-backtest

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate

# Install dependencies (including dev tools: pytest, ruff)
pip install -e ".[dev]"
```

**Requirements**: Python 3.10+, Yfinance ≥0.2.0, Pandas ≥2.0, Numpy, Matplotlib, Scikit-learn

## 🚀 Usage

Follow these steps to run the complete backtesting pipeline:

### 1. Download Market Data

```bash
python -m src.data.download_prices --ticker SPY --start 2010-01-01 --end 2023-12-31
```

Downloads historical price data for specified ticker (default: SPY) and saves to `data/raw/SPY_prices.csv`.

**Note**: The `data/` directory is git-ignored—datasets remain local only.

### 2. Process Data

```bash
python -m src.data.make_dataset
```

Cleans raw price data, handles missing values, and creates processed dataset at `data/processed/SPY_processed.csv`.

### 3. Run Walk-Forward Backtest

```bash
python -m src.backtest.walkforward --ticker SPY --train_years 3 --test_years 1
```

Executes rolling window backtest:
- **Train Period**: 3 years (optimize strategy parameters)
- **Test Period**: 1 year (validate out-of-sample)
- **Rolling Mechanism**: Window shifts forward, repeating train/test cycle

Outputs:
- Summary table: `reports/results/SPY_walkforward_summary.csv`
- Equity curves: `reports/figures/SPY_equity_curves.png`

## 🧠 Trading Strategies

The system implements two classical algorithmic trading strategies:

### 1. Trend Following (Moving Average Crossover)

**Logic**:
- Calculate fast MA (e.g., 50-day) and slow MA (e.g., 200-day)
- **Buy Signal**: Fast MA crosses above slow MA → Position = +1 (long)
- **Sell Signal**: Fast MA crosses below slow MA → Position = 0 (flat)

**Parameters**:
- `fast_window`: Short-term moving average period (default: 50)
- `slow_window`: Long-term moving average period (default: 200)

**Philosophy**: Captures sustained directional movements; performs well in trending markets.

### 2. Mean Reversion (Z-Score Based)

**Logic**:
- Calculate rolling mean and standard deviation (e.g., 20-day window)
- Compute Z-score: `(price - mean) / std`
- **Buy Signal**: Z-score < entry threshold (e.g., -2.0) → Position = +1 (long)
- **Sell Signal**: Z-score > exit threshold (e.g., 0.0) → Position = 0 (flat)

**Parameters**:
- `lookback_window`: Rolling statistics period (default: 20)
- `entry_threshold`: Z-score level to enter position (default: -2.0)
- `exit_threshold`: Z-score level to exit position (default: 0.0)

**Philosophy**: Profits from price deviations returning to average; performs well in range-bound markets.

## 📊 Performance Metrics

The backtest evaluates strategies using industry-standard risk-adjusted metrics:

| Metric | Description | Formula/Interpretation |
|--------|-------------|------------------------|
| **Sharpe Ratio** | Risk-adjusted return | `(mean_return - risk_free_rate) / std_return`<br>Higher = better risk/reward |
| **Max Drawdown** | Largest peak-to-trough decline | Maximum percentage drop from highest point<br>Lower = better downside protection |
| **Total Return** | Cumulative performance | Final equity / Initial equity - 1<br>Absolute gain/loss percentage |
| **Equity Curve** | Capital evolution over time | Visual representation of portfolio value |

## 📁 Project Structure

```
.
├── src/
│   ├── data/
│   │   ├── download_prices.py    # Yahoo Finance data fetcher
│   │   └── make_dataset.py       # Data cleaning & preprocessing
│   ├── strategies/
│   │   ├── trend_following.py    # Moving average crossover logic
│   │   └── mean_reversion.py     # Z-score based logic
│   └── backtest/
│       └── walkforward.py        # Walk-forward validation engine
├── reports/
│   ├── results/
│   │   └── SPY_walkforward_summary.csv  # Performance metrics per window
│   └── figures/
│       └── SPY_equity_curves.png        # Strategy comparison chart
├── data/                         # Git-ignored (local only)
│   ├── raw/                      # Downloaded OHLCV data
│   └── processed/                # Cleaned datasets
└── README.md
```

## 📈 Sample Output

After running the backtest, expect results like:

### Performance Summary Table

```csv
train_start,train_end,test_start,test_end,strategy,sharpe_ratio,max_drawdown,total_return
2010-01-01,2012-12-31,2013-01-01,2013-12-31,trend_following,1.23,-0.08,0.12
2010-01-01,2012-12-31,2013-01-01,2013-12-31,mean_reversion,0.87,-0.12,0.09
2011-01-01,2013-12-31,2014-01-01,2014-12-31,trend_following,1.45,-0.06,0.15
2011-01-01,2013-12-31,2014-01-01,2014-12-31,mean_reversion,0.92,-0.10,0.11
```

### Console Output

```
Walk-Forward Backtest Results (SPY):
=====================================
Window 1: 2013 Test Period
  Trend Following:  Sharpe=1.23, MaxDD=-8.0%, Return=+12.0%
  Mean Reversion:   Sharpe=0.87, MaxDD=-12.0%, Return=+9.0%

Window 2: 2014 Test Period
  Trend Following:  Sharpe=1.45, MaxDD=-6.0%, Return=+15.0%
  Mean Reversion:   Sharpe=0.92, MaxDD=-10.0%, Return=+11.0%

Overall Statistics:
  Trend Following:  Avg Sharpe=1.34, Avg MaxDD=-7.0%
  Mean Reversion:   Avg Sharpe=0.90, Avg MaxDD=-11.0%
```

### Equity Curve Visualization

The generated chart (`SPY_equity_curves.png`) displays:
- **Blue line**: Trend Following strategy cumulative returns
- **Red line**: Mean Reversion strategy cumulative returns
- **Gray line**: Buy-and-hold benchmark (optional)

## 🔬 Technical Details

### Walk-Forward Methodology

**Why Walk-Forward?**
Traditional backtests train on all historical data, leading to overfitting. Walk-forward validation:
1. Divides data into sequential train/test windows
2. Optimizes strategy on training period
3. Validates performance on unseen test period
4. Rolls window forward and repeats

**Example Timeline** (3-year train, 1-year test):
```
Train: 2010-2012 → Test: 2013
Train: 2011-2013 → Test: 2014
Train: 2012-2014 → Test: 2015
...
```

### Data Handling

- **Source**: Yahoo Finance via `yfinance` library
- **Frequency**: Daily OHLCV bars
- **Adjustments**: Prices are split/dividend-adjusted
- **Missing Data**: Forward-fill for gaps (e.g., holidays)

### Strategy Implementation

Both strategies use vectorized Pandas operations for efficiency:
- No look-ahead bias (signals use only past data)
- Position sizing: Simple binary (0=flat, 1=long)
- No transaction costs (can be added via slippage parameter)

## 🎨 Visualization Examples

The equity curve chart includes:
- **Logarithmic y-axis** (optional): Better visualizes compounding
- **Drawdown shading**: Highlights underwater periods
- **Performance statistics**: Annotated Sharpe/MaxDD on chart

## 📝 TODO

Future enhancements and improvements:

- [ ] Add transaction costs and slippage modeling
- [ ] Implement short-selling capability (position = -1)
- [ ] Expand to multi-asset portfolios (diversification)
- [ ] Add parameter optimization (grid search, genetic algorithms)
- [ ] Implement risk management (stop-loss, position sizing)
- [ ] Create real-time trading interface (Interactive Brokers API)
- [ ] Add more strategies (RSI, Bollinger Bands, ML-based)
- [ ] Build interactive dashboard (Plotly/Dash)
- [ ] Add Monte Carlo simulation for robustness testing
- [ ] Implement walk-forward optimization (WFO) with parameter tuning

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or suggest features via Issues
- Submit pull requests for new strategies
- Share backtesting insights and improvements
- Propose additional risk metrics or visualizations

## ⚠️ Trading Disclaimer

**IMPORTANT**: This is a **backtesting simulation** for educational and research purposes only.

- **NOT financial advice**: Past performance does not guarantee future results
- **No real trading**: This system does not execute live trades
- **Risk warning**: Trading involves substantial risk of loss
- **Consult professionals**: Always seek advice from licensed financial advisors

Backtests are inherently limited by assumptions (no slippage, perfect execution, survivorship bias) and may not reflect real-world trading conditions.

## 📄 License

This project is open source and for educational purposes only. See LICENSE file for details.

---

**Disclaimer**: This is an experimental algorithmic trading research project. The strategies shown are simplified examples and have not been validated for live trading. Markets are unpredictable—trade at your own risk. 📊

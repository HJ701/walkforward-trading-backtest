from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.config import PATHS
from src.utils.logging import get_logger
from src.features.build_features import add_features
from src.strategies.signals import trend_signal, mean_reversion_signal
from src.backtest.metrics import equity_curve, sharpe, max_drawdown

log = get_logger(__name__)

@dataclass(frozen=True)
class WFSpec:
    ticker: str = "SPY"
    train_years: int = 5
    test_years: int = 1
    fee_bps: float = 1.0

def load_processed(ticker: str) -> pd.DataFrame:
    path = PATHS.data_processed / f"{ticker}_processed.csv"
    return pd.read_csv(path, parse_dates=["date"])

def apply_costs(position: pd.Series, fee_bps: float) -> pd.Series:
    trades = position.diff().abs().fillna(0)
    cost = trades * (fee_bps / 10000.0)
    return cost

def run_strategy(df: pd.DataFrame, position: pd.Series, fee_bps: float) -> pd.Series:
    r = df["ret_1d"].shift(-1).fillna(0)
    cost = apply_costs(position, fee_bps)
    strat_ret = (position * r) - cost
    return strat_ret

def main():
    spec = WFSpec()
    df = add_features(load_processed(spec.ticker))
    df["year"] = df["date"].dt.year
    years = sorted(df["year"].unique())
    rows, all_trend, all_mr = [], [], []

    for i in range(0, len(years) - (spec.train_years + spec.test_years) + 1):
        train_years = years[i : i + spec.train_years]
        test_years = years[i + spec.train_years : i + spec.train_years + spec.test_years]
        test = df[df["year"].isin(test_years)].copy()

        trend_pos = trend_signal(test)
        mr_pos = mean_reversion_signal(test)
        trend_ret = run_strategy(test, trend_pos, spec.fee_bps)
        mr_ret = run_strategy(test, mr_pos, spec.fee_bps)

        rows.append({
            "train_start": int(train_years[0]), "train_end": int(train_years[-1]),
            "test_start": int(test_years[0]), "test_end": int(test_years[-1]),
            "trend_sharpe": sharpe(trend_ret), "trend_mdd": max_drawdown(equity_curve(trend_ret)),
            "mr_sharpe": sharpe(mr_ret), "mr_mdd": max_drawdown(equity_curve(mr_ret))
        })
        all_trend.append(trend_ret)
        all_mr.append(mr_ret)

    summary = pd.DataFrame(rows)
    PATHS.reports_results.mkdir(parents=True, exist_ok=True)
    out_csv = PATHS.reports_results / f"{spec.ticker}_walkforward_summary.csv"
    summary.to_csv(out_csv, index=False)
    log.info(f"Wrote results: {out_csv}")

    eq_trend = equity_curve(pd.concat(all_trend, ignore_index=True))
    eq_mr = equity_curve(pd.concat(all_mr, ignore_index=True))
    PATHS.reports_figures.mkdir(parents=True, exist_ok=True)
    fig_path = PATHS.reports_figures / f"{spec.ticker}_equity_curves.png"
    plt.figure()
    plt.plot(eq_trend.values, label="Trend (MA crossover)")
    plt.plot(eq_mr.values, label="Mean Reversion (z-score)")
    plt.title(f"Equity Curves (Walk-forward) - {spec.ticker}")
    plt.legend()
    plt.savefig(fig_path, bbox_inches="tight")
    plt.close()
    log.info(f"Wrote figure: {fig_path}")

if __name__ == "__main__":
    main()
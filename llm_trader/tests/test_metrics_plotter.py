import pandas as pd
import pytest
from pathlib import Path

from llm_trader.core.visuals.metrics_plotter import plot_historical_metrics



def _make_metrics_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "start": pd.to_datetime(
                ["2025-03-01", "2025-03-05", "2025-03-10"], utc=True
            ),
            "end": pd.to_datetime(
                ["2025-03-02", "2025-03-06", "2025-03-11"], utc=True
            ),
            "total_trades": [100, 120, 90],
            "win_rate": [0.35, 0.38, 0.33],
            "expectancy": [-0.05, 0.02, -0.08],
            "profit_factor": [0.9, 1.05, 0.85],
            "sharpe_ratio": [-0.5, 0.2, -1.0],
            "average_win": [1.5, 1.5, 1.5],
            "average_loss": [1.0, 1.0, 1.0],
            "rr_ratio": [1.5, 1.5, 1.5],
        }
    )


def test_plot_historical_metrics_parquet(tmp_path: Path) -> None:
    """Smoke test: should load parquet, build the figure, and not crash with save/show disabled."""
    df = _make_metrics_df()
    metrics_path = tmp_path / "historical_metrics.parquet"
    df.to_parquet(metrics_path)

    # save/show disabled to avoid kaleido/browser dependencies during CI
    result = plot_historical_metrics(metrics_path, save=False, show=False)
    assert result is None


def test_plot_historical_metrics_json(tmp_path: Path) -> None:
    """Smoke test: same behavior with JSON."""
    df = _make_metrics_df()
    metrics_path = tmp_path / "historical_metrics.json"
    df.to_json(metrics_path)

    result = plot_historical_metrics(metrics_path, save=False, show=False)
    assert result is None


def test_plot_historical_metrics_missing_end_raises(tmp_path: Path) -> None:
    """Should raise a clear error if 'end' column doesn't exist."""
    df = _make_metrics_df().drop(columns=["end"])
    metrics_path = tmp_path / "bad_metrics.parquet"
    df.to_parquet(metrics_path)

    with pytest.raises(ValueError, match="missing 'end'"):
        plot_historical_metrics(metrics_path, save=False, show=False)

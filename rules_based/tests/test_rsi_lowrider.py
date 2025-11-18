from data.models.candle import Candle
from rules_based.strategies.rsi_lowrider import RSILowrider
from datetime import datetime, timezone

def test_rsi_lowrider_initialization():
    s = RSILowrider(period=14, buy_threshold=30.0)
    assert s.period == 14
    assert s.buy_threshold == 30.0

def test_rsi_lowrider_methods_exist():
    s = RSILowrider()

    # fake candles
    candles = [
        Candle(timestamp=datetime.now(tz=timezone.utc),
               open=1.0, high=1.0, low=1.0, close=1.0, volume=0)
    ]

    assert s.compute_rsi(candles) is None
    assert s.check_entry(candles) is False

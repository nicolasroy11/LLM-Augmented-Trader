import pandas as pd
import pandas_ta as ta
from typing import List, Optional
from data.models.candle import Candle

class RSILowrider:
    def __init__(self, period: int = 14, buy_threshold: float = 30.0):
        self.period = period
        self.buy_threshold = buy_threshold

    def compute_rsi(self, candles: List[Candle]) -> Optional[float]:
        """
        Compute RSI using pandas_ta. Returns the latest RSI value.
        """
        if len(candles) < self.period + 1:
            return None

        df = pd.DataFrame({
            "close": [c.close for c in candles]
        })

        rsi_series = ta.rsi(df["close"], length=self.period)

        # pandas_ta returns a series with NaN for warm-up periods
        last_val = rsi_series.iloc[-1]

        return None if pd.isna(last_val) else float(last_val)

    def check_entry(self, candles: List[Candle]) -> bool:
        """
        Will be implemented later.
        """
        return False

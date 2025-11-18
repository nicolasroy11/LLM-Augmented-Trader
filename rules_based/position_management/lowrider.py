from rules_based.position_management.base_forex_position_manager import BaseForexPositionManager
from data.models.forex_instrument import ForexInstrument
import runtime_settings as rs


class LowriderPositionManager(BaseForexPositionManager):
    def __init__(self, instrument: ForexInstrument, commission_per_lot=rs.ROUNDTRIP_COMMISSION_PER_LOT):
        super().__init__(instrument, commission_per_lot)

    def open_position(
        self,
        entry_price: float,
        tp_price: float | None = None,
        lot_size: float = 1.0,
        direction: str = "long"
    ):
        """
        Lowrider auto-generates its TP rule:
        TP = entry + 2 pips for long positions
        """
        if tp_price is None:
            # Lowrider rule: 2-pip TP
            tp_price = entry_price + (2 * self.instrument.pip_size)

        return super().open_position(
            entry_price=entry_price,
            tp_price=tp_price,
            lot_size=lot_size,
            direction=direction
        )

    def should_scale_in(self, current_price: float) -> bool:
        """
        Placeholder logic — implemented later
        """
        return False

    def should_close_basket(self, current_price: float) -> bool:
        """
        Placeholder logic — implemented later
        """
        return False

from typing import List, Optional
from data.models.position import Position
from data.models.forex_instrument import ForexInstrument
import runtime_settings as rs


class BaseForexPositionManager:

    def __init__(
        self,
        instrument: ForexInstrument,
        commission_per_lot: Optional[float] = None,
    ):
        self.instrument = instrument

        self.pip_size = instrument.pip_size
        self.dollars_per_pip_per_lot = instrument.dollars_per_pip_per_lot

        # commission is full round-trip applied at entry
        self.commission_per_lot = (
            commission_per_lot 
            if commission_per_lot is not None 
            else rs.ROUNDTRIP_COMMISSION_PER_LOT
        )

        # runtime state
        self.open_positions: List[Position] = []
        self.closed_positions: List[Position] = []
        self.realized_pnl: float = 0.0

    # -----------------------------------------------------
    # Open Position
    # -----------------------------------------------------
    def open_position(
        self,
        entry_price: float,
        tp_price: Optional[float],
        lot_size: float,
        direction: str = "long",
    ) -> Position:
        pos = Position(
            entry_price=entry_price,
            tp_price=tp_price,
            lot_size=lot_size,
            direction=direction,
        )

        # full round-trip commission applied immediately
        self.realized_pnl -= self.commission_per_lot * lot_size

        self.open_positions.append(pos)
        return pos

    # -----------------------------------------------------
    # Close Position
    # -----------------------------------------------------
    def close_position(self, position: Position, exit_price: float) -> Position:
        """
        Close an open position.

        Commission has already been applied at entry (full round-trip),
        so here we only add pip PnL.
        """
        # Remove from open positions
        self.open_positions.remove(position)

        # Long-only for now; later we can handle "short"
        pips = (exit_price - position.entry_price) / self.pip_size
        pip_dollars = pips * self.dollars_per_pip_per_lot * position.lot_size

        # realized_pnl here is *pip PnL only* because commission was charged at entry
        self.realized_pnl += pip_dollars

        # Update the position via its own close() helper
        position.close(exit_price=exit_price, realized_pnl=pip_dollars)

        # Track as closed
        self.closed_positions.append(position)

        return position

    # -----------------------------------------------------
    # Floating Loss
    # -----------------------------------------------------
    def compute_floating_loss(self, current_price: float) -> float:
        """
        Floating loss from open positions.
        Only pip losses are included (gains ignored).
        Commission is already realized at entry.
        """
        total = 0.0

        for pos in self.open_positions:
            price_diff = pos.entry_price - current_price  # long-only for now

            pips = price_diff / self.pip_size
            pip_loss = pips * self.dollars_per_pip_per_lot * pos.lot_size

            total += max(pip_loss, 0.0)

        return total

    # -----------------------------------------------------
    # Equity
    # -----------------------------------------------------
    def compute_equity(self, current_price: float) -> float:
        return self.realized_pnl + self.compute_floating_loss(current_price)

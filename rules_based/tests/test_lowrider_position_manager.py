from rules_based.position_management.lowrider import LowriderPositionManager
import runtime_settings as rs
from data.constants.forex_instruments import ForexInstruments


instrument = ForexInstruments.EURUSD


def test_lowrider_initializes():
    pm = LowriderPositionManager(instrument=instrument)

    assert pm.open_positions == []
    assert pm.closed_positions == []
    assert pm.commission_per_lot == rs.COMMISSION_PER_LOT
    assert pm.instrument is instrument


def test_lowrider_open_close():
    pm = LowriderPositionManager(instrument=instrument)

    pos = pm.open_position(entry_price=1.1000, lot_size=1.0)

    closed = pm.close_position(pos, exit_price=1.1020)

    assert closed.exit_price == 1.1020
    assert closed.is_closed
    assert closed.realized_pnl is not None   # <- updated field name
    assert len(pm.open_positions) == 0
    assert len(pm.closed_positions) == 1


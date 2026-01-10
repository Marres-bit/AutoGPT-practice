"""
Capital management following SP rules described by user.
Tracks principal and investment balance and applies reinvest/withdraw rules.
"""
from dataclasses import dataclass
from typing import Dict
from . import config


@dataclass
class CapitalState:
    principal: float
    investment_balance: float
    allocated_to_trade: float = 0.0
    cumulative_profits: float = 0.0


class CapitalManager:
    def __init__(self, principal: float = None):
        self.principal = principal if principal is not None else config.DEFAULT_PRINCIPAL_USDT
        self.investment_balance = 0.0
        self.allocated_to_trade = 0.0
        self.cumulative_profits = 0.0
        self.first_trade_done = False

    def allocate_first_trade(self) -> float:
        """Return amount allocated for first trade: 70% of principal"""
        amt = self.principal * config.FIRST_TRADE_INVEST_PCT
        self.allocated_to_trade = amt
        # Deduct from principal for the moment
        self.principal -= amt
        # Set initial investment balance to zero until close
        self.investment_balance = 0.0
        return amt

    def on_first_trade_closed(self, profit: float):
        """Apply the rules after first trade closes.
        - 100% of profits stay in Investment Balance
        - 70% of initial capital invested return to Principal
        - 30% of initial capital + profits form Investment Balance
        """
        invested_amount = self.allocated_to_trade
        # 70% of initial invested returned to principal
        returned = invested_amount * 0.7
        reinvest_base = invested_amount * 0.3

        # profits all go to investment balance
        self.cumulative_profits += profit
        self.principal += returned
        self.investment_balance = reinvest_base + self.cumulative_profits
        self.allocated_to_trade = 0.0
        self.first_trade_done = True

    def on_trade_closed(self, profit: float):
        """Apply continuous reinvest rules after each trade closure:
        - Add profit to investment balance
        - Withdraw 20% of total (investment_balance + principal?) to principal
        - Keep the rest in investment balance for continued trading
        """
        # Add profit to investment balance
        self.cumulative_profits += profit
        self.investment_balance += profit

        total_investing = self.investment_balance
        withdraw = total_investing * config.WITHDRAW_PCT_AFTER_CLOSURE
        # Move withdraw amount back to principal
        self.investment_balance = total_investing - withdraw
        self.principal += withdraw

    def allocate_trade_from_investment(self, pct: float = 1.0) -> float:
        """Allocate a portion (pct) of the investment_balance for a trade"""
        amt = self.investment_balance * pct
        self.investment_balance -= amt
        self.allocated_to_trade = amt
        return amt

    def snapshot(self) -> CapitalState:
        return CapitalState(
            principal=self.principal,
            investment_balance=self.investment_balance,
            allocated_to_trade=self.allocated_to_trade,
            cumulative_profits=self.cumulative_profits
        )

    def save_state(self, path):
        """Save capital state to JSON file at `path`"""
        import json
        data = {
            'principal': self.principal,
            'investment_balance': self.investment_balance,
            'allocated_to_trade': self.allocated_to_trade,
            'cumulative_profits': self.cumulative_profits,
            'first_trade_done': self.first_trade_done
        }
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_state(cls, path):
        """Load capital state from JSON file at `path`. Returns CapitalManager instance or None if missing."""
        import json
        if not Path(path).exists():
            return None
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cm = cls(data.get('principal', config.DEFAULT_PRINCIPAL_USDT))
        cm.investment_balance = data.get('investment_balance', 0.0)
        cm.allocated_to_trade = data.get('allocated_to_trade', 0.0)
        cm.cumulative_profits = data.get('cumulative_profits', 0.0)
        cm.first_trade_done = data.get('first_trade_done', False)
        return cm


if __name__ == '__main__':
    cm = CapitalManager(10000)
    amt = cm.allocate_first_trade()
    print(f"Allocated first trade: {amt}")
    cm.on_first_trade_closed(500)
    print(cm.snapshot())

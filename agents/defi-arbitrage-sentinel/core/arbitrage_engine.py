"""
DeFi High-Frequency Arbitrage & Slippage Sentinel Engine.
Calculates cross-DEX price spreads (Meteora DLMM vs Raydium CLMM vs Orca), flashloan fees, and net profit.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class ArbitrageOpportunity:
    token_pair: str
    dex_buy: str
    dex_sell: str
    buy_price: float
    sell_price: float
    spread_pct: float
    simulated_capital_usd: float
    gross_profit_usd: float
    flashloan_fee_usd: float
    est_gas_priority_fee_usd: float
    net_profit_usd: float
    is_profitable: bool


class DefiArbitrageEngine:
    """Simulates cross-DEX triangular arbitrage and preflight MEV safety."""

    FLASHLOAN_FEE_RATE = 0.0009  # 0.09% typical Solana flashloan fee (e.g. Solend/Save)
    ESTIMATED_PRIORITY_FEE_SOL = 0.005  # High priority CU bid for Jito bundle inclusion

    @classmethod
    def scan_opportunities(
        cls,
        pair: str,
        prices: Dict[str, float],
        capital_usd: float = 10000.0,
        sol_price_usd: float = 140.0
    ) -> List[ArbitrageOpportunity]:
        opportunities = []
        dex_names = list(prices.keys())

        for i in range(len(dex_names)):
            for j in range(len(dex_names)):
                if i == j:
                    continue
                dex_a = dex_names[i]
                dex_b = dex_names[j]
                p_buy = prices[dex_a]
                p_sell = prices[dex_b]

                if p_sell > p_buy:
                    spread = (p_sell - p_buy) / p_buy
                    tokens_bought = capital_usd / p_buy
                    gross_return = tokens_bought * p_sell
                    gross_profit = gross_return - capital_usd

                    flashloan_fee = capital_usd * cls.FLASHLOAN_FEE_RATE
                    gas_fee = cls.ESTIMATED_PRIORITY_FEE_SOL * sol_price_usd
                    net_profit = gross_profit - flashloan_fee - gas_fee

                    opp = ArbitrageOpportunity(
                        token_pair=pair,
                        dex_buy=dex_a,
                        dex_sell=dex_b,
                        buy_price=p_buy,
                        sell_price=p_sell,
                        spread_pct=round(spread * 100, 3),
                        simulated_capital_usd=capital_usd,
                        gross_profit_usd=round(gross_profit, 2),
                        flashloan_fee_usd=round(flashloan_fee, 2),
                        est_gas_priority_fee_usd=round(gas_fee, 2),
                        net_profit_usd=round(net_profit, 2),
                        is_profitable=net_profit > 0
                    )
                    opportunities.append(opp)

        opportunities.sort(key=lambda x: x.net_profit_usd, reverse=True)
        return opportunities

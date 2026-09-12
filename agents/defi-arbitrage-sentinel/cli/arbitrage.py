"""CLI for DeFi High-Frequency Arbitrage Sentinel"""
import sys, os, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from agents.defi_arbitrage_sentinel.core.arbitrage_engine import DefiArbitrageEngine


def main():
    parser = argparse.ArgumentParser(description="DeFi Arbitrage & Cross-DEX Sentinel")
    parser.add_argument("--pair", default="SOL/USDC", help="Token pair to scan")
    parser.add_argument("--capital", type=float, default=25000.0, help="Simulated flashloan capital in USD")
    args = parser.parse_args()

    # Sample simulated pool state
    sample_prices = {
        "Meteora DLMM": 142.15,
        "Raydium CLMM": 141.80,
        "Orca Whirlpool": 142.05,
    }

    opps = DefiArbitrageEngine.scan_opportunities(args.pair, sample_prices, capital_usd=args.capital)
    print(f"⚡ DeFi Arbitrage Scan for {args.pair} (Capital: ${args.capital:,.2f})")
    print("=" * 65)

    profitable = [o for o in opps if o.is_profitable]
    if not profitable:
        print("No profitable arbitrage spread found after fees & priority gas.")
    else:
        best = profitable[0]
        print(f"🔥 TOP ARBITRAGE ROUTE FOUND:")
        print(f"Route: BUY on [{best.dex_buy}] @ ${best.buy_price:.2f} -> SELL on [{best.dex_sell}] @ ${best.sell_price:.2f}")
        print(f"Spread: {best.spread_pct}% | Gross Profit: ${best.gross_profit_usd:,.2f}")
        print(f"Flashloan Fee (0.09%): -${best.flashloan_fee_usd:.2f} | Priority Gas: -${best.est_gas_priority_fee_usd:.2f}")
        print(f"💰 NET ESTIMATED PROFIT: +${best.net_profit_usd:,.2f}")


if __name__ == "__main__":
    main()

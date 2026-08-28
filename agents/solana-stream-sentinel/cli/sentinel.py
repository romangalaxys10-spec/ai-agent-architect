"""
CLI for Solana Stream Sentinel.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from agents.solana_stream_sentinel.core.stream_engine import SolanaStreamSentinel, PoolEvent


def main():
    parser = argparse.ArgumentParser(description="Solana Stream Sentinel CLI - Sniff and Decode DEX Events")
    sub = parser.add_subparsers(dest="command")

    p_sniff = sub.add_parser("sniff", help="Simulate sniffing on-chain DEX pool creation")
    p_sniff.add_argument("--program", default="LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo", help="Program ID (Meteora DLMM default)")

    p_sim = sub.add_parser("simulate", help="Simulate swap preflight and sandwich risk")
    p_sim.add_argument("--amount", type=float, default=1.5, help="SOL amount to swap")

    args = parser.parse_args()

    if args.command == "sniff":
        print(f"⚡ Sniffing Yellowstone Geyser stream for Program: {args.program}...")
        event = SolanaStreamSentinel.decode_transaction_event(
            program_id=args.program,
            accounts=["So11111111111111111111111111111111111111112", "DeFiTokenMint111111111111111111111111111", "PoolAcc1111111111111111111111111111111111"],
            data_hex="0x18be821703f274a1"
        )
        print("✅ New Pool Detected:")
        print(json.dumps(event.__dict__, indent=2))
    elif args.command == "simulate":
        event = SolanaStreamSentinel.decode_transaction_event("LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo", [], "0x18be821703f274a1")
        sim = SolanaStreamSentinel.simulate_swap_preflight(event, amount_sol=args.amount)
        print("📊 Preflight Swap Simulation:")
        print(json.dumps(sim, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

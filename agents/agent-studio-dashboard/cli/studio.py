"""CLI for Agent Studio Dashboard Plugin"""
import sys, os, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from agents.agent_studio_dashboard.core.studio_server import StudioServer


def main():
    parser = argparse.ArgumentParser(description="Agent Studio Dashboard Plugin")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind dashboard server")
    parser.add_argument("--daemon", action="store_true", help="Start in background")
    args = parser.parse_args()

    print(f"🎛️ Starting Agent Studio Dashboard on http://127.0.0.1:{args.port}")
    print("Press Ctrl+C to terminate.")
    server = StudioServer.run_server(args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Studio Dashboard.")
        server.server_close()


if __name__ == "__main__":
    main()

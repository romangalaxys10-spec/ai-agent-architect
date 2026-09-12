"""CLI for Motion Video & Remotion Orchestrator"""
import sys, os, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from agents.motion_video_orchestrator.core.video_engine import MotionVideoEngine


def main():
    parser = argparse.ArgumentParser(description="Motion Video & Remotion Graphics Orchestrator")
    parser.add_argument("--title", default="ProductLaunchPromo", help="Video composition title")
    parser.add_argument("--script", nargs="+", default=[
        "Autonomous Agent Swarms Built from Scratch",
        "OpenTelemetry Distributed Microsecond Tracing",
        "Zero-Shot Ledger-Based Self-Orchestration"
    ], help="Script keyframes or scene subtitles")
    parser.add_argument("--out", default="remotion_composition.jsx", help="Output JSX composition file")
    args = parser.parse_args()

    project = MotionVideoEngine.compile_project(args.title, args.script)
    print(f"🎬 Motion Video Project: {project.project_name}")
    print(f"Resolution: {project.width}x{project.height} @ {project.fps}fps")
    print(f"Duration: {project.total_duration_sec:.1f}s ({project.total_frames} frames across {len(project.scenes)} scenes)")
    print("-" * 65)

    for s in project.scenes:
        print(f"• [Scene {s.id}] ({s.duration_frames}f, {s.transition}): "{s.subtitle}"")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(project.remotion_composition_jsx)
    print(f"\n✅ Remotion React JSX composition written to: {args.out}")


if __name__ == "__main__":
    main()

"""
Computer Use demo — smoke through 100-series agents offline.
Run: python examples/computer_use_demo.py
"""
import importlib.util, os, sys
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)
samples=[
    ("computer-vision-agent","computer_vision","Screenshot grounding for macOS Finder with accessibility tree and ocr reader, need to click gui element"),
    ("browser-pilot-agent","browser_pilot","Browser pilot: playwright orchestration for checkout flow with cdp bridge and dom forensics"),
    ("shell-pilot-agent","shell_pilot","Shell pilot on linux: bash zsh fish prompt detection and tmux orchestrator"),
    ("linux-admin-agent","linux_admin","Linux admin systemd surgeon on ubuntu with apt package manager and kernel tuner"),
    ("windows-admin-agent","windows_admin","Windows admin powershell forge with winget and registry on windows server"),
]
for slug, module, text in samples:
    path=os.path.join(REPO,"agents",slug,"core",f"{module}_engine.py")
    spec=importlib.util.spec_from_file_location(slug.replace("-","_"), path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    Engine=[v for v in mod.__dict__.values() if hasattr(v,"analyze")][0]
    result=Engine.analyze(text)
    print(Engine.format_report(result))
    print("\n"+"="*80+"\n")

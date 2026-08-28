"""
Power150 demo — smoke through all 150 expansion agents offline.

Run: python examples/power150_demo.py
"""
import importlib.util, os, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)

# Sample: run 5 representative agents
samples = [
    ("api-architect-agent", "api_architect", "Design a paginated REST API for invoicing with idempotency keys"),
    ("threat-model-agent", "threat_model", "STRIDE threat model for a multi-agent gateway with tool calling"),
    ("x-growth-hacker-agent", "x_growth_hacker", "Draft a viral X thread about our agent launch"),
    ("ml-pipeline-agent", "ml_pipeline", "Design an ML pipeline with feature store and eval gates"),
    ("healthcare-scribe-agent", "healthcare_scribe", "SOAP note for a routine follow-up (not medical advice)"),
]

for slug, module, text in samples:
    path = os.path.join(REPO, "agents", slug, "core", f"{module}_engine.py")
    spec = importlib.util.spec_from_file_location(slug.replace("-","_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    Engine = [v for v in mod.__dict__.values() if hasattr(v, "analyze")][0]
    result = Engine.analyze(text)
    print(Engine.format_report(result))
    print("\n" + "="*80 + "\n")

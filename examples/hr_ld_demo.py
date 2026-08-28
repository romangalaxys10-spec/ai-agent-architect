"""
HR/L&D demo — smoke through 50-series agents offline.
Run: python examples/hr_ld_demo.py
"""
import importlib.util, os, sys
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)
samples=[
    ("hrbp-strategic-partner-agent","hrbp_strategic_partner","HRBP strategic partner for workforce shaping with business alignment and action and metric"),
    ("learning-needs-diagnostician-agent","learning_needs_diagnostician","TNA for sales ramp: performance gap analysis with skills ontology and action and metric"),
    ("kirkpatrick-evaluator-agent","kirkpatrick_evaluator","Kirkpatrick Level 4 evaluation with control group and learning ROI for leadership academy, action and metric"),
    ("succession-risk-agent","succession_risk","Succession risk for 9-box talent with bench strength and flight risk, action and metric"),
    ("wellbeing-strategist-agent","wellbeing_strategist","Wellbeing strategy for resilience and burnout prevention, action and metric"),
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

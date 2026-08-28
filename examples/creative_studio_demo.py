"""
Creative Studio demo — smoke through 20-series agents offline.
Run: python examples/creative_studio_demo.py
"""
import importlib.util, os, sys
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)
samples=[
    ("video-editor-pro-agent","video_editor_pro","Cut timeline with color grading and proxy workflow for video editing"),
    ("blender-studio-agent","blender_studio","Blender Geometry Nodes Cycles rigging for 3D studio creation"),
    ("3d-modeling-architect-agent","m_3d_modeling_architect","Hard-surface topology retopo LOD for 3D modeling"),
    ("music-composer-agent","music_composer","Compose MIDI arrangement with score export for music creation"),
    ("youtube-remix-engine-agent","youtube_remix_engine","Remix long to Shorts with multi-angle cuts for YouTube publishing"),
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

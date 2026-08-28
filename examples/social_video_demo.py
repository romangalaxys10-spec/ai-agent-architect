"""
Social/Video demo — smoke through 70-series agents offline.
Run: python examples/social_video_demo.py
"""
import importlib.util, os, sys
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)
samples=[
    ("linkedin-scheduler-agent","linkedin_scheduler","LinkedIn scheduler queue with timezone and cross-post guards, hook and CTA: follow"),
    ("insta-reels-virality-agent","insta_reels_virality","Insta Reels virality with hook-window sound sync and loop-rate, hook and CTA: comment"),
    ("x-thread-architect-agent","x_thread_architect","X thread architect with hook pacing and viral hook lab, hook and CTA: follow"),
    ("youtube-thumbnail-forge-agent","youtube_thumbnail_forge","YouTube thumbnail forge with CTR and A/B test, hook and CTA: subscribe"),
    ("gemini-video-producer-agent","gemini_video_producer","Gemini Veo storyboard from Pexels Pixabay free stock with hook and CTA: subscribe, license attribution"),
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

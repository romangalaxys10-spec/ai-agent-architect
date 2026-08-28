"""Contract + functional tests for the 20 Creative Studio series.

Every agent: studio-grade offline engine + CLI + SKILL.md contract.
"""
import importlib.util
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")

CREATIVE20 = [
    ("video-editor-pro-agent", "video_editor_pro", "VideoEditorProEngine"),
    ("premiere-workflow-agent", "premiere_workflow", "PremiereWorkflowEngine"),
    ("davinci-resolve-agent", "davinci_resolve", "DavinciResolveEngine"),
    ("capcut-template-agent", "capcut_template", "CapcutTemplateEngine"),
    ("subtitle-transcription-agent", "subtitle_transcription", "SubtitleTranscriptionEngine"),
    ("blender-studio-agent", "blender_studio", "BlenderStudioEngine"),
    ("three-studio-max-agent", "three_studio_max", "ThreeStudioMaxEngine"),
    ("cinema4d-motion-agent", "cinema4d_motion", "Cinema4dMotionEngine"),
    ("houdini-fx-agent", "houdini_fx", "HoudiniFxEngine"),
    ("3d-modeling-architect-agent", "m_3d_modeling_architect", "M3dModelingArchitectEngine"),
    ("3d-texturing-agent", "m_3d_texturing", "M3dTexturingEngine"),
    ("3d-render-optimizer-agent", "m_3d_render_optimizer", "M3dRenderOptimizerEngine"),
    ("music-editor-pro-agent", "music_editor_pro", "MusicEditorProEngine"),
    ("audio-cleanup-agent", "audio_cleanup", "AudioCleanupEngine"),
    ("sample-curator-agent", "sample_curator", "SampleCuratorEngine"),
    ("music-composer-agent", "music_composer", "MusicComposerEngine"),
    ("beat-maker-agent", "beat_maker", "BeatMakerEngine"),
    ("youtube-curation-agent", "youtube_curation", "YoutubeCurationEngine"),
    ("youtube-remix-engine-agent", "youtube_remix_engine", "YoutubeRemixEngineEngine"),
    ("youtube-publisher-agent", "youtube_publisher", "YoutubePublisherEngine"),
]

def _load(slug, module, cls_name):
    path=os.path.join(AGENTS_DIR, slug, "core", f"{module}_engine.py")
    spec=importlib.util.spec_from_file_location(f"{slug}_{module}", path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, cls_name)

class TestCreative20Structure(unittest.TestCase):
    def test_exactly_twenty(self):
        self.assertEqual(len(CREATIVE20), 20)
        self.assertEqual(len({s for s,_,_ in CREATIVE20}), 20)
    def test_every_agent_has_skill_core_cli(self):
        for slug, module, _ in CREATIVE20:
            base=os.path.join(AGENTS_DIR, slug)
            self.assertTrue(os.path.isfile(os.path.join(base, "SKILL.md")), f"{slug}: SKILL.md")
            self.assertTrue(os.path.isfile(os.path.join(base, "core", f"{module}_engine.py")), f"{slug}: engine")
            self.assertTrue(os.path.isfile(os.path.join(base, "cli", f"{module}.py")), f"{slug}: CLI")
    def test_skill_md_frontmatter_parses(self):
        import yaml
        for slug, _, _ in CREATIVE20:
            content=open(os.path.join(AGENTS_DIR, slug, "SKILL.md"), encoding="utf-8").read()
            self.assertTrue(content.startswith("---"), f"{slug}: no frontmatter")
            meta=yaml.safe_load(content.split("---",2)[1])
            for key in ("name","description","version"):
                self.assertIn(key, meta, f"{slug}: missing {key}")
    def test_registry_discovers(self):
        sys.path.insert(0, REPO_ROOT)
        from core.registry import AgentRegistry
        agents=AgentRegistry.discover_agents()
        for slug,_,_ in CREATIVE20:
            self.assertIn(slug, agents, f"{slug} not discovered")

class TestCreative20CLIs(unittest.TestCase):
    def test_every_cli_help_from_neutral_cwd(self):
        failures=[]
        for slug, module, _ in CREATIVE20:
            cli=os.path.join(AGENTS_DIR, slug, "cli", f"{module}.py")
            proc=subprocess.run([sys.executable, cli, "--help"], capture_output=True, text=True, timeout=60, cwd="/tmp")
            if proc.returncode!=0:
                failures.append((slug, proc.stderr.strip()[-200:]))
            elif "usage:" not in proc.stdout.lower():
                failures.append((slug, "no usage"))
        self.assertEqual(failures, [], f"CLI failures: {failures}")

class TestCreative20Engines(unittest.TestCase):
    def test_all_engines_analyze_and_format(self):
        for slug, module, cls_name in CREATIVE20:
            with self.subTest(agent=slug):
                Engine=_load(slug, module, cls_name)
                text=f"Sample for {slug}: video 3d music youtube with enough words to avoid thin check for studio work.\n- bullet: value\nMore content for depth and creative signals."
                result=Engine.analyze(text)
                self.assertIn(result.verdict, ["PASS","PASS_WITH_NOTES","NEEDS_REVIEW","BLOCKED","NEEDS_INPUT"])
                self.assertGreaterEqual(result.score, 0)
                self.assertLessEqual(result.score, 100)
                self.assertIn("creative_signals", result.metrics)
                report=Engine.format_report(result)
                self.assertIn(result.verdict, report)

if __name__=="__main__":
    unittest.main()

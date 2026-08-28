"""Contract + functional tests for the 70 Social/Video series.

Every agent: platform-aware offline engine + CLI + SKILL.md contract.
"""
import importlib.util
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")

SOCIAL70 = [
    ("linkedin-scheduler-agent", "linkedin_scheduler", "LinkedinSchedulerEngine"),
    ("linkedin-dm-funnel-agent", "linkedin_dm_funnel", "LinkedinDmFunnelEngine"),
    ("linkedin-analytics-radar-agent", "linkedin_analytics_radar", "LinkedinAnalyticsRadarEngine"),
    ("linkedin-lead-scraper-agent", "linkedin_lead_scraper", "LinkedinLeadScraperEngine"),
    ("linkedin-company-page-agent", "linkedin_company_page", "LinkedinCompanyPageEngine"),
    ("linkedin-newsletter-architect-agent", "linkedin_newsletter_architect", "LinkedinNewsletterArchitectEngine"),
    ("linkedin-live-producer-agent", "linkedin_live_producer", "LinkedinLiveProducerEngine"),
    ("linkedin-ads-optimizer-agent", "linkedin_ads_optimizer", "LinkedinAdsOptimizerEngine"),
    ("linkedin-outreach-sequencer-agent", "linkedin_outreach_sequencer", "LinkedinOutreachSequencerEngine"),
    ("linkedin-personal-brand-agent", "linkedin_personal_brand", "LinkedinPersonalBrandEngine"),
    ("linkedin-event-networker-agent", "linkedin_event_networker", "LinkedinEventNetworkerEngine"),
    ("linkedin-poll-viral-agent", "linkedin_poll_viral", "LinkedinPollViralEngine"),
    ("insta-reels-virality-agent", "insta_reels_virality", "InstaReelsViralityEngine"),
    ("insta-grid-planner-agent", "insta_grid_planner", "InstaGridPlannerEngine"),
    ("insta-story-architect-agent", "insta_story_architect", "InstaStoryArchitectEngine"),
    ("insta-hashtag-lab-agent", "insta_hashtag_lab", "InstaHashtagLabEngine"),
    ("insta-dm-automation-agent", "insta_dm_automation", "InstaDmAutomationEngine"),
    ("insta-influencer-match-agent", "insta_influencer_match", "InstaInfluencerMatchEngine"),
    ("insta-shop-optimizer-agent", "insta_shop_optimizer", "InstaShopOptimizerEngine"),
    ("insta-analytics-insights-agent", "insta_analytics_insights", "InstaAnalyticsInsightsEngine"),
    ("insta-ads-launcher-agent", "insta_ads_launcher", "InstaAdsLauncherEngine"),
    ("insta-ugc-harvester-agent", "insta_ugc_harvester", "InstaUgcHarvesterEngine"),
    ("insta-comment-guardian-agent", "insta_comment_guardian", "InstaCommentGuardianEngine"),
    ("insta-live-commerce-agent", "insta_live_commerce", "InstaLiveCommerceEngine"),
    ("x-thread-architect-agent", "x_thread_architect", "XThreadArchitectEngine"),
    ("x-reply-bot-agent", "x_reply_bot", "XReplyBotEngine"),
    ("x-list-intel-agent", "x_list_intel", "XListIntelEngine"),
    ("x-spaces-producer-agent", "x_spaces_producer", "XSpacesProducerEngine"),
    ("x-trend-jacker-agent", "x_trend_jacker", "XTrendJackerEngine"),
    ("x-dm-funnel-agent", "x_dm_funnel", "XDmFunnelEngine"),
    ("x-analytics-pulse-agent", "x_analytics_pulse", "XAnalyticsPulseEngine"),
    ("x-ads-booster-agent", "x_ads_booster", "XAdsBoosterEngine"),
    ("x-search-scraper-agent", "x_search_scraper", "XSearchScraperEngine"),
    ("x-community-cultivator-agent", "x_community_cultivator", "XCommunityCultivatorEngine"),
    ("x-toxicity-shield-agent", "x_toxicity_shield", "XToxicityShieldEngine"),
    ("x-viral-hook-lab-agent", "x_viral_hook_lab", "XViralHookLabEngine"),
    ("youtube-channel-architect-agent", "youtube_channel_architect", "YoutubeChannelArchitectEngine"),
    ("youtube-shorts-virality-agent", "youtube_shorts_virality", "YoutubeShortsViralityEngine"),
    ("youtube-seo-optimizer-agent", "youtube_seo_optimizer", "YoutubeSeoOptimizerEngine"),
    ("youtube-thumbnail-forge-agent", "youtube_thumbnail_forge", "YoutubeThumbnailForgeEngine"),
    ("youtube-chapter-optimizer-agent", "youtube_chapter_optimizer", "YoutubeChapterOptimizerEngine"),
    ("youtube-live-ops-agent", "youtube_live_ops", "YoutubeLiveOpsEngine"),
    ("youtube-membership-monetizer-agent", "youtube_membership_monetizer", "YoutubeMembershipMonetizerEngine"),
    ("youtube-analytics-sentinel-agent", "youtube_analytics_sentinel", "YoutubeAnalyticsSentinelEngine"),
    ("youtube-comment-manager-agent", "youtube_comment_manager", "YoutubeCommentManagerEngine"),
    ("youtube-collab-scout-agent", "youtube_collab_scout", "YoutubeCollabScoutEngine"),
    ("youtube-repurpose-engine-agent", "youtube_repurpose_engine", "YoutubeRepurposeEngineEngine"),
    ("youtube-ads-roi-agent", "youtube_ads_roi", "YoutubeAdsRoiEngine"),
    ("tiktok-sound-trend-agent", "tiktok_sound_trend", "TiktokSoundTrendEngine"),
    ("tiktok-shop-affiliate-agent", "tiktok_shop_affiliate", "TiktokShopAffiliateEngine"),
    ("tiktok-live-commerce-agent", "tiktok_live_commerce", "TiktokLiveCommerceEngine"),
    ("tiktok-duet-stitch-agent", "tiktok_duet_stitch", "TiktokDuetStitchEngine"),
    ("tiktok-analytics-radar-agent", "tiktok_analytics_radar", "TiktokAnalyticsRadarEngine"),
    ("tiktok-ads-spark-agent", "tiktok_ads_spark", "TiktokAdsSparkEngine"),
    ("tiktok-creator-scout-agent", "tiktok_creator_scout", "TiktokCreatorScoutEngine"),
    ("tiktok-script-lab-agent", "tiktok_script_lab", "TiktokScriptLabEngine"),
    ("tiktok-hashtag-virality-agent", "tiktok_hashtag_virality", "TiktokHashtagViralityEngine"),
    ("tiktok-comment-moderator-agent", "tiktok_comment_moderator", "TiktokCommentModeratorEngine"),
    ("free-stock-scout-agent", "free_stock_scout", "FreeStockScoutEngine"),
    ("pexels-pipeline-agent", "pexels_pipeline", "PexelsPipelineEngine"),
    ("pixabay-curator-agent", "pixabay_curator", "PixabayCuratorEngine"),
    ("mixkit-video-forge-agent", "mixkit_video_forge", "MixkitVideoForgeEngine"),
    ("gemini-video-producer-agent", "gemini_video_producer", "GeminiVideoProducerEngine"),
    ("gemini-script-to-video-agent", "gemini_script_to_video", "GeminiScriptToVideoEngine"),
    ("veo-storyboard-agent", "veo_storyboard", "VeoStoryboardEngine"),
    ("free-audio-scout-agent", "free_audio_scout", "FreeAudioScoutEngine"),
    ("subtitle-auto-agent", "subtitle_auto", "SubtitleAutoEngine"),
    ("video-remixer-free-agent", "video_remixer_free", "VideoRemixerFreeEngine"),
    ("ai-avatar-free-agent", "ai_avatar_free", "AiAvatarFreeEngine"),
    ("gemini-thumbnail-gen-agent", "gemini_thumbnail_gen", "GeminiThumbnailGenEngine"),
]

def _load(slug, module, cls_name):
    path=os.path.join(AGENTS_DIR, slug, "core", f"{module}_engine.py")
    spec=importlib.util.spec_from_file_location(f"{slug}_{module}", path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, cls_name)

class TestSocial70Structure(unittest.TestCase):
    def test_exactly_seventy(self):
        self.assertEqual(len(SOCIAL70), 70)
        self.assertEqual(len({s for s,_,_ in SOCIAL70}), 70)
    def test_every_agent_has_skill_core_cli(self):
        for slug, module, _ in SOCIAL70:
            base=os.path.join(AGENTS_DIR, slug)
            self.assertTrue(os.path.isfile(os.path.join(base, "SKILL.md")), f"{slug}: SKILL.md")
            self.assertTrue(os.path.isfile(os.path.join(base, "core", f"{module}_engine.py")), f"{slug}: engine")
            self.assertTrue(os.path.isfile(os.path.join(base, "cli", f"{module}.py")), f"{slug}: CLI")
    def test_skill_md_frontmatter_parses(self):
        import yaml
        for slug, _, _ in SOCIAL70:
            content=open(os.path.join(AGENTS_DIR, slug, "SKILL.md"), encoding="utf-8").read()
            self.assertTrue(content.startswith("---"), f"{slug}: no frontmatter")
            meta=yaml.safe_load(content.split("---",2)[1])
            for key in ("name","description","version"):
                self.assertIn(key, meta, f"{slug}: missing {key}")
    def test_registry_discovers(self):
        sys.path.insert(0, REPO_ROOT)
        from core.registry import AgentRegistry
        agents=AgentRegistry.discover_agents()
        for slug,_,_ in SOCIAL70:
            self.assertIn(slug, agents, f"{slug} not discovered")

class TestSocial70CLIs(unittest.TestCase):
    def test_every_cli_help_from_neutral_cwd(self):
        failures=[]
        for slug, module, _ in SOCIAL70:
            cli=os.path.join(AGENTS_DIR, slug, "cli", f"{module}.py")
            proc=subprocess.run([sys.executable, cli, "--help"], capture_output=True, text=True, timeout=60, cwd="/tmp")
            if proc.returncode!=0:
                failures.append((slug, proc.stderr.strip()[-200:]))
            elif "usage:" not in proc.stdout.lower():
                failures.append((slug, "no usage"))
        self.assertEqual(failures, [], f"CLI failures: {failures}")

class TestSocial70Engines(unittest.TestCase):
    def test_all_engines_analyze_and_format(self):
        for slug, module, cls_name in SOCIAL70:
            with self.subTest(agent=slug):
                Engine=_load(slug, module, cls_name)
                text=f"Sample for {slug}: linkedin instagram x youtube tiktok gemini veo free stock pexels pixabay hook and CTA: follow, with enough words to avoid thin check.\n- bullet: value\nMore content for depth."
                result=Engine.analyze(text)
                self.assertIn(result.verdict, ["PASS","PASS_WITH_NOTES","NEEDS_REVIEW","BLOCKED","NEEDS_INPUT"])
                self.assertGreaterEqual(result.score, 0)
                self.assertLessEqual(result.score, 100)
                self.assertIn("detected_platform", result.metrics)
                report=Engine.format_report(result)
                self.assertIn(result.verdict, report)

if __name__=="__main__":
    unittest.main()

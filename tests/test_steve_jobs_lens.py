"""Unit tests for Steve Jobs Product Lens"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.steve_jobs_lens import SteveJobsLens, QualityVerdict


class TestSteveJobsLens(unittest.TestCase):
    def test_steve_jobs_lens_insanely_great(self):
        review = SteveJobsLens.evaluate_product(
            product_name="MacStudioAI",
            feature_list=["Unified Neural Engine", "Zero-latency IPC", "Radical Simplicity"],
            one_sentence_pitch="An insanely fast unified AI workstation that just works.",
            user_journey_steps=2,
            controls_whole_stack=True
        )
        self.assertEqual(review.quality_verdict, QualityVerdict.INSANELY_GREAT)
        self.assertEqual(len(review.focus_cut_list), 0)

    def test_steve_jobs_lens_cut_bloat(self):
        review = SteveJobsLens.evaluate_product(
            product_name="BloatedApp",
            feature_list=[f"Feature {i}" for i in range(12)],
            one_sentence_pitch="A next-gen synergistic disruptive AI platform for enterprise synergies.",
            user_journey_steps=7,
            controls_whole_stack=False
        )
        self.assertEqual(review.quality_verdict, QualityVerdict.TOTAL_BULLSHIT)
        self.assertGreater(len(review.focus_cut_list), 5)


if __name__ == "__main__":
    unittest.main()

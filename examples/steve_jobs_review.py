import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
"""
Example: Running Steve Jobs Product & Architecture Review on a product idea.
"""

from core.steve_jobs_lens import SteveJobsLens


def run_product_review():
    product_name = "SuperAgentOS"
    features = [
        "Instant one-click autonomous deployment",
        "Deterministic self-correcting cognitive loop",
        "Hardware-level memory acceleration",
        "Unnecessary social media plugin",
        "Bloated web3 weather widget",
        "Cluttered dashboard with 50 tabs"
    ]
    pitch = "A lightning-fast, self-correcting autonomous operating system for AI agents."
    
    review = SteveJobsLens.evaluate_product(
        product_name=product_name,
        feature_list=features,
        one_sentence_pitch=pitch,
        user_journey_steps=2,
        controls_whole_stack=True
    )
    
    print(SteveJobsLens.format_review_markdown(review))


if __name__ == "__main__":
    run_product_review()

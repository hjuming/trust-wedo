import pytest
from trust_wedo.core.entity_scorer import EntityScorer

def test_calculate_ec_perfect():
    site_data = {
        "site": "https://example.com",
        "pages": [
            {
                "url": "https://example.com",
                "title_missing": False,
                "meta_missing": False,
                "is_about_author": True,
                "has_jsonld": True,
                "external_links_count": 5,
                "social_links_count": 2
            }
        ],
        "checks": {"sitemap_ok": True}
    }
    scorer = EntityScorer(site_data)
    result = scorer.calculate_score()
    assert result["entity_confidence"] >= 0.8
    assert result["eligibility"] == "pass"

def test_calculate_ec_poor():
    site_data = {
        "site": "https://poor.com",
        "pages": [
            {
                "url": "https://poor.com",
                "title_missing": True,
                "meta_missing": True,
                "is_about_author": False,
                "has_jsonld": False,
                "external_links_count": 0,
                "social_links_count": 0
            }
        ],
        "checks": {"sitemap_ok": False}
    }
    scorer = EntityScorer(site_data)
    result = scorer.calculate_score()
    assert result["entity_confidence"] < 0.3
    assert result["eligibility"] == "fail"

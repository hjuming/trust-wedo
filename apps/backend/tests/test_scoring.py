from app.models.signals import SiteSignals
from app.services.scoring import calculate_weighted_score, score_to_grade


def test_perfect_score():
    signals = SiteSignals(
        has_https=True,
        has_title=True,
        has_description=True,
        has_favicon=True,
        schema_analysis={"score": 30, "details": ["完整 Organization schema"]},
        schema_count=3,
        has_organization=True,
        has_person=True,
        has_article=True,
        has_author=True,
        has_about_page=True,
        has_contact=True,
        has_social_proof=True,
        social_links_count=2,
        has_authority_links=True,
        page_load_time=1.5,
        is_mobile_friendly=True,
    )

    score = calculate_weighted_score(signals)
    assert score == 100
    assert score_to_grade(score) == 'A'

def test_minimal_score():
    signals = SiteSignals()
    score = calculate_weighted_score(signals)
    assert score == 5
    assert score_to_grade(score) == 'F'

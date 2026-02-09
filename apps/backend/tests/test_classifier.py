from app.models.signals import SiteSignals
from app.services.site_classifier import classify_site_type

def test_ecommerce_classification():
    signals = SiteSignals(schema_types=['Product', 'Offer'])
    site_type, confidence = classify_site_type(signals)
    assert site_type == 'ecommerce'
    assert confidence > 0.8

def test_blog_classification():
    signals = SiteSignals(has_article=True, has_author=True)
    site_type, confidence = classify_site_type(signals)
    assert site_type == 'blog'

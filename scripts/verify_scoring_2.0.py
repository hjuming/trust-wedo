import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../apps/backend'))

from app.services.report_engine import ReportEngine
from app.services.scoring import calculate_score_v2
from app.models.signals import SiteSignals

def test_scoring_v3():
    print("Testing Scoring 2.0 Logic...")
    
    # 1. Mock Artifacts
    mock_artifacts = [{
        'stage': 'scan',
        'jsonb_payload': {
            'site': 'https://example.com',
            'pages': [{
                'title_missing': False,
                'meta_missing': False,
                'has_favicon': True,
                'load_time': 1.5,
                'has_viewport': True,
                'schemas': [
                    {"@context": "https://schema.org", "@type": "Organization", "name": "Example Corp", "url": "https://example.com"},
                    {"@context": "https://schema.org", "@type": "WebSite", "name": "Example Site", "url": "https://example.com"}
                ],
                'is_about_author': True,
                'external_links_count': 10,
                'social_links_count': 3
            }]
        }
    }]
    
    # 2. Extract Signals
    engine = ReportEngine()
    signals = engine.extract_signals(mock_artifacts)
    
    print(f"Signals extracted: {signals.model_dump(exclude={'schema_analysis'})}")
    # print(f"Schema Analysis: {signals.schema_analysis}")
    
    # 3. Calculate Score
    result = calculate_score_v2(signals)
    
    print(f"\nFinal Score: {result['score']}")
    print(f"Grade: {result['grade']}")
    print(f"Dimensions: {list(result['dimensions'].keys())}")
    
    for key, dim in result['dimensions'].items():
        print(f"\nDimension: {key}")
        print(f"  Name: {dim.get('name')}")
        print(f"  Score: {dim['score']}/{dim['max']} ({dim.get('percentage')}%)")
        # print(f"  Items: {dim['items']}")

    # Assertions
    assert result['score'] > 0
    assert 'structure' in result['dimensions']
    assert 'trust' in result['dimensions']
    assert 'identity' in result['dimensions']
    assert result['dimensions']['structure']['max'] == 30
    assert result['dimensions']['trust']['max'] == 20
    assert result['dimensions']['discoverability']['max'] == 20
    assert result['dimensions']['technical']['max'] == 15
    assert result['dimensions']['identity']['max'] == 15
    
    print("\n✅ Verification Passed!")

if __name__ == "__main__":
    test_scoring_v3()

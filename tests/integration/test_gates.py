import json
import pytest
from pathlib import Path
from trust_wedo.core.afb_builder import AFBBuilder

def test_afb_gate_fail_behavior():
    """
    Test that AFBBuilder produces a 'fail' JSON when Entity Confidence is low,
    instead of raising an error or returning None.
    """
    entity_profile = {
        "entity_id": "ent:test-fail",
        "entity_confidence": 0.45,
        "eligibility": "fail"
    }
    html_content = "<html><body><article>Test content</article></body></html>"
    
    builder = AFBBuilder(html_content, entity_profile)
    result = builder.build(input_source="test.html")
    
    # Assertions for Unified Gate Behavior
    assert result["eligibility"] == "fail"
    assert "reasons" in result
    assert len(result["reasons"]) > 0
    assert result["ai_quick_answer"] == "REJECTED: Entity confidence below threshold"
    assert "meta" in result
    assert result["meta"]["input_source"] == "test.html"
    assert result["payload"]["answer"] == "REJECTED"

def test_afb_gate_pass_behavior():
    """
    Test that AFBBuilder produces a 'pass' JSON when Entity Confidence is high.
    """
    entity_profile = {
        "entity_id": "ent:test-pass",
        "entity_confidence": 0.85,
        "eligibility": "pass"
    }
    html_content = "<html><body><article>Excellent high quality content.</article></body></html>"
    
    builder = AFBBuilder(html_content, entity_profile)
    result = builder.build(input_source="test.html")
    
    assert result["eligibility"] == "pass"
    assert "reasons" not in result or len(result["reasons"]) == 0
    assert "Excellent high quality content" in result["ai_quick_answer"]
    assert result["payload"]["answer"].startswith("Excellent high quality content")

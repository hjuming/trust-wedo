import json
import pytest
from pathlib import Path
from trust_wedo.core.report_generator import ReportGenerator

def test_report_generation(tmp_path):
    # Setup a mock bundle directory
    bundle_dir = tmp_path / "bundle"
    bundle_dir.mkdir()
    
    entity_data = {"entity_id": "ent:test", "entity_confidence": 0.8, "eligibility": "pass"}
    citation_data = {"decision": "accept", "citations": [{"citation_id": "cite:001"}]}
    graph_data = {"metrics": {"single_source_risk": False, "distinct_sources": 2}}
    
    (bundle_dir / "entity_profile.json").write_text(json.dumps(entity_data))
    (bundle_dir / "citation_eval.json").write_text(json.dumps(citation_data))
    (bundle_dir / "entity_graph.json").write_text(json.dumps(graph_data))
    
    generator = ReportGenerator(str(bundle_dir))
    
    # Test JSON report
    report_json = generator.generate_json()
    assert report_json["summary"]["entity_id"] == "ent:test"
    assert report_json["summary"]["ec_score"] == 0.8
    assert "meta" in report_json
    
    # Test Markdown report
    report_md = generator.generate_markdown()
    assert "# Trust WEDO 信任評估報告" in report_md
    assert "ent:test" in report_md
    assert "✅ 通過" in report_md

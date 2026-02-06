import pytest
from trust_wedo.core.graph_builder import GraphBuilder

def test_graph_metrics_isolated():
    bundle_data = {
        "entity": {"entity_id": "ent:test"},
        "afb": {"afb_id": "afb:test"},
        "citation": {"citations": []}
    }
    builder = GraphBuilder(bundle_data)
    result = builder.build()
    assert result["metrics"]["is_isolated"] is True
    assert result["metrics"]["distinct_sources"] == 0

def test_graph_metrics_single_source():
    bundle_data = {
        "entity": {"entity_id": "ent:test"},
        "afb": {"afb_id": "afb:test"},
        "citation": {
            "citations": [
                {"citation_id": "cite:001", "status": "accept"}
            ]
        }
    }
    builder = GraphBuilder(bundle_data)
    result = builder.build()
    assert result["metrics"]["single_source_risk"] is True
    assert result["metrics"]["distinct_sources"] == 1

def test_graph_metrics_multi_source():
    bundle_data = {
        "entity": {"entity_id": "ent:test"},
        "afb": {"afb_id": "afb:test"},
        "citation": {
            "citations": [
                {"citation_id": "cite:001", "status": "accept"},
                {"citation_id": "cite:002", "status": "accept"}
            ]
        }
    }
    builder = GraphBuilder(bundle_data)
    result = builder.build()
    assert result["metrics"]["single_source_risk"] is False
    assert result["metrics"]["is_isolated"] is False
    assert result["metrics"]["distinct_sources"] == 2

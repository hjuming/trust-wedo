import pytest
from trust_wedo.core.citation_evaluator import CitationEvaluator

def test_evaluate_citations_accept():
    citations = [
        {"citation_id": "cite:001", "url": "https://trusted.org", "status": "verified"}
    ]
    evaluator = CitationEvaluator("afb:test", citations)
    result = evaluator.evaluate()
    assert result["decision"] == "accept"
    assert result["citations"][0]["status"] == "accept"

def test_evaluate_citations_reject():
    citations = [
        {"citation_id": "cite:002", "url": "https://twitter.com/bad", "status": "unverified", "days_old": 500}
    ]
    evaluator = CitationEvaluator("afb:test", citations)
    result = evaluator.evaluate()
    # 0.5 (unverified) - 0.2 (social) - 0.1 (old) = 0.2
    assert result["citations"][0]["ccs"] < 0.6
    assert result["citations"][0]["status"] == "reject"

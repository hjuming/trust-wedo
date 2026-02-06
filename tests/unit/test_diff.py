import pytest
from trust_wedo.core.diff_analyzer import DiffAnalyzer

def test_diff_analysis():
    afb_data = {
        "afb_id": "afb:test",
        "ai_quick_answer": "Original answer."
    }
    captures = [
        {
            "capture_id": "cap:001",
            "source": "gpt-4",
            "ai_output": "Original answer."
        },
        {
            "capture_id": "cap:002",
            "source": "claude",
            "ai_output": "Completely different thing."
        }
    ]
    
    analyzer = DiffAnalyzer(afb_data, captures)
    result = analyzer.analyze()
    
    assert result["afb_id"] == "afb:test"
    assert len(result["comparisons"]) == 2
    assert result["comparisons"][0]["similarity_score"] == 1.0
    assert result["comparisons"][0]["hallucination_risk"] == "low"
    assert result["comparisons"][1]["similarity_score"] < 0.5
    assert result["comparisons"][1]["hallucination_risk"] == "high"
    assert result["summary"]["total_captures"] == 2
    assert result["summary"]["best_source"] == "gpt-4"

"""Diff analyzer module for Trust WEDO."""

import json
from pathlib import Path
from typing import Dict, List, Any
from trust_wedo.core.similarity_calculator import calculate_similarity, get_text_differences
from trust_wedo.utils.meta import get_meta


class DiffAnalyzer:
    """Analyzer for comparing AFB and AI Captures."""

    def __init__(self, afb_data: Dict[str, Any], captures: List[Dict[str, Any]]):
        self.afb_data = afb_data
        self.captures = captures

    def analyze(self, input_source: str = "cli") -> Dict[str, Any]:
        """Perform diff analysis."""
        afb_answer = self.afb_data.get("ai_quick_answer", "")
        afb_id = self.afb_data.get("afb_id", "afb:unknown")
        
        comparisons = []
        total_similarity = 0.0
        
        best_source = None
        best_score = -1.0
        worst_source = None
        worst_score = 2.0

        for cap in self.captures:
            ai_output = cap.get("ai_output", "")
            source = cap.get("source", "unknown")
            similarity = calculate_similarity(afb_answer, ai_output)
            
            risk = self._detect_hallucination_risk(similarity)
            
            comparisons.append({
                "capture_id": cap.get("capture_id", "cap:unknown"),
                "source": source,
                "ai_output": ai_output,
                "similarity_score": round(similarity, 2),
                "differences": get_text_differences(afb_answer, ai_output),
                "hallucination_risk": risk
            })
            
            total_similarity += similarity
            
            if similarity > best_score:
                best_score = similarity
                best_source = source
            
            if similarity < worst_score:
                worst_score = similarity
                worst_source = source

        avg_similarity = total_similarity / len(self.captures) if self.captures else 0.0

        return {
            "diff_id": f"diff:{afb_id.split(':')[-1]}",
            "afb_id": afb_id,
            "afb_answer": afb_answer,
            "comparisons": comparisons,
            "summary": {
                "total_captures": len(self.captures),
                "avg_similarity": round(avg_similarity, 2),
                "best_source": best_source,
                "worst_source": worst_source
            },
            "meta": get_meta(input_source)
        }

    def _detect_hallucination_risk(self, similarity: float) -> str:
        """Identify hallucination risk based on similarity score."""
        if similarity >= 0.90:
            return "low"
        elif similarity >= 0.70:
            return "medium"
        else:
            return "high"

"""Citation evaluator module for Trust WEDO."""

from typing import Dict, List, Any
from trust_wedo.utils.meta import get_meta


class CitationEvaluator:
    """Evaluator for calculating Citation Confidence Score (CCS)."""

    def __init__(self, afb_id: str, citations: List[Dict[str, Any]]):
        self.afb_id = afb_id
        self.citations = citations

    def evaluate(self, input_source: str = "afb.json") -> Dict[str, Any]:
        """Evaluate all citations."""
        evaluated_citations = []
        overall_ccs = 0.0

        for cite in self.citations:
            # Simple CCS calculation based on status and length
            # In real case, this would involve 6 dimensions + half-life
            base_score = 0.8 if cite.get("status") == "verified" else 0.5
            url = cite.get("url", "")
            
            # Penalize if it's a social media link (less authoritative for citations)
            social_domains = ["twitter.com", "facebook.com", "linkedin.com"]
            if any(sd in url for sd in social_domains):
                base_score -= 0.2
            
            # Penalize if it's an old citation (simulating half-life)
            days_old = cite.get("days_old", 0)
            if days_old > 365:
                base_score -= 0.1
            
            ccs = max(0.0, min(1.0, base_score))
            
            status = "accept"
            failure_states = []
            if ccs < 0.60:
                status = "reject"
                failure_states.append(f"CCS below threshold: {ccs:.2f} < 0.60")
            elif ccs < 0.75:
                status = "downgrade"
            
            evaluated_citations.append({
                "citation_id": cite.get("citation_id", "cite:unknown"),
                "ccs": round(ccs, 2),
                "status": status,
                "failure_states": failure_states
            })
            overall_ccs += ccs

        # Decision
        if not evaluated_citations:
            decision = "reject"
            reasons = ["no_citations_found"]
        else:
            avg_ccs = overall_ccs / len(evaluated_citations)
            if all(c["status"] == "reject" for c in evaluated_citations):
                decision = "reject"
                reasons = ["All citations rejected due to low CCS"]
            elif any(c["status"] == "reject" for c in evaluated_citations):
                decision = "downgrade"
                reasons = ["Some citations rejected"]
            else:
                decision = "accept"
                reasons = []

        return {
            "afb_id": self.afb_id,
            "citations": evaluated_citations,
            "decision": decision,
            "reasons": reasons,
            "meta": get_meta(input_source)
        }

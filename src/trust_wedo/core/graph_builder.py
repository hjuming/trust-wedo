"""Graph builder module for Trust WEDO."""

from typing import Dict, List, Any
from trust_wedo.utils.meta import get_meta


class GraphBuilder:
    """Builder for generating Entity Graph and risk metrics."""

    def __init__(self, bundle_data: Dict[str, Any]):
        self.entity_profile = bundle_data.get("entity", {})
        self.afb = bundle_data.get("afb", {})
        self.citation_eval = bundle_data.get("citation", {})

    def build(self, input_source: str = "bundle") -> Dict[str, Any]:
        """Build Graph JSON."""
        entity_id = self.entity_profile.get("entity_id", "ent:unknown")
        
        # Calculate metrics
        citations = self.citation_eval.get("citations", [])
        # In a real graph, we would extract domains from citation URLs
        # For MVP, we'll just count the citations
        distinct_sources = len(set(c.get("citation_id") for c in citations))
        
        is_isolated = distinct_sources == 0
        single_source_risk = distinct_sources == 1

        return {
            "entity": entity_id,
            "metrics": {
                "distinct_sources": distinct_sources,
                "is_isolated": is_isolated,
                "single_source_risk": single_source_risk
            },
            "meta": get_meta(input_source)
        }

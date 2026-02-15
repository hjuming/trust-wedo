"""Entity scorer module for Trust WEDO."""

from typing import Dict, List, Any
from trust_wedo.utils.meta import get_meta


class EntityScorer:
    """Scorer for calculating Entity Confidence (EC)."""

    def __init__(self, site_data: Dict[str, Any]):
        self.site_data = site_data
        self.pages = site_data.get("pages", [])
        self.checks = site_data.get("checks", {})

    def calculate_score(self, input_source: str = "site.json") -> Dict[str, Any]:
        """Calculate EC and signals."""
        if not self.pages:
            return {
                "entity_id": f"ent:{self.site_data.get('site', 'unknown')}",
                "entity_confidence": 0.0,
                "signals": {
                    "consistency": 0.0,
                    "authority": 0.0,
                    "citation": 0.0,
                    "frequency": 0.0,
                    "social": 0.0
                },
                "eligibility": "fail",
                "meta": get_meta(input_source)
            }

        # 1. Consistency: meta/title missing rate
        title_missing_count = sum(1 for p in self.pages if p.get("title_missing", True))
        meta_missing_count = sum(1 for p in self.pages if p.get("meta_missing", True))
        consistency = 1.0 - ((title_missing_count + meta_missing_count) / (2 * len(self.pages)))

        # 2. Authority: about/author pages or json-ld
        has_about_author = any(p.get("is_about_author", False) for p in self.pages)
        has_jsonld = any(p.get("has_jsonld", False) for p in self.pages)
        authority = (0.6 if has_about_author else 0.0) + (0.4 if has_jsonld else 0.0)

        # 3. Citation: external links count (heuristic)
        avg_external_links = sum(p.get("external_links_count", 0) for p in self.pages) / len(self.pages)
        citation = min(avg_external_links / 4.0, 1.0)  # Adjusted for MVP

        # 4. Frequency: sitemap_ok
        frequency = 0.8 if self.checks.get("sitemap_ok", False) else 0.5 # Adjusted for MVP

        # 5. Social: social links count
        avg_social_links = sum(p.get("social_links_count", 0) for p in self.pages) / len(self.pages)
        social = min(avg_social_links / 1.5, 1.0)  # Adjusted for MVP

        # EC formula (simplified)
        ec = (consistency * 0.3 + 
              authority * 0.25 + 
              citation * 0.15 + 
              frequency * 0.15 + 
              social * 0.15)
        
        ec = round(ec, 2)
        eligibility = "pass" if ec >= 0.60 else "fail"

        return {
            "entity_id": f"ent:{self.site_data.get('site', 'unknown')}",
            "entity_confidence": ec,
            "signals": {
                "consistency": round(consistency, 2),
                "authority": round(authority, 2),
                "citation": round(citation, 2),
                "frequency": round(frequency, 2),
                "social": round(social, 2)
            },
            "eligibility": eligibility,
            "meta": get_meta(input_source)
        }

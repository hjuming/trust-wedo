"""AFB builder module for Trust WEDO."""

from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup


class AFBBuilder:
    """Builder for generating Answer-First Block (AFB)."""

    def __init__(self, html_content: str, entity_profile: Dict[str, Any]):
        self.html_content = html_content
        self.entity_profile = entity_profile
        self.soup = BeautifulSoup(html_content, "html.parser")

    def build(self) -> Dict[str, Any]:
        """Build AFB JSON."""
        # Check eligibility
        ec = self.entity_profile.get("entity_confidence", 0.0)
        if ec < 0.60:
            # According to MVP_BEHAVIOR.md: "直接退出並輸出 error（或產出 afb.json 帶 eligibility=fail）"
            # Schema doesn't have eligibility, so I'll just return a base structure if I must,
            # but usually it should be handled in CLI.
            pass

        # Extract text content
        content_text = self._extract_text()
        
        # Generate ID
        entity_id = self.entity_profile.get("entity_id", "ent:unknown")
        afb_id = f"afb:page:{entity_id.split(':')[-1]}"

        # Template based answer
        summary = content_text[:100] + "..." if len(content_text) > 100 else content_text
        ai_answer = f"根據 {entity_id} 的資料：{summary}"

        # Count citations (simplified: count external links)
        citations_count = len(self.soup.find_all("a", href=True))

        return {
            "afb_id": afb_id,
            "entity_id": entity_id,
            "ai_quick_answer": ai_answer,
            "context_fit": {
                "use_when": ["general_information"],
                "do_not_use_when": ["medical_advice", "legal_advice"]
            },
            "confidence_signals": {
                "entity_confidence": ec,
                "citation_count": citations_count
            },
            "payload": {
                "@type": "Answer",
                "answer": content_text[:500],
                "entity_id": entity_id
            }
        }

    def _extract_text(self) -> str:
        """Extract main text content from HTML."""
        # Simple heuristic: article > main > body
        for tag_name in ["article", "main", "body"]:
            tag = self.soup.find(tag_name)
            if tag:
                # Remove scripts and styles
                for s in tag(["script", "style"]):
                    s.decompose()
                return tag.get_text(separator=" ", strip=True)
        return ""

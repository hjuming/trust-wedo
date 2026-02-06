"""Capture manager module for Trust WEDO."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from trust_wedo.utils.meta import get_meta


class CaptureManager:
    """Manager for capturing AI outputs."""

    def __init__(self, output_dir: str = "output/captures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture(self, afb_id: str, ai_output: str, source: str = "unknown") -> Dict[str, Any]:
        """Capture AI output and save to JSON."""
        # Auto-increment capture_id
        capture_count = len(list(self.output_dir.glob("capture_*.json")))
        capture_id = f"cap:{capture_count + 1:03d}"
        
        now = datetime.utcnow().isoformat() + "Z"
        
        result = {
            "capture_id": capture_id,
            "afb_id": afb_id,
            "ai_output": ai_output,
            "source": source,
            "captured_at": now,
            "meta": get_meta("cli:manual")
        }
        
        # Filename: capture_<afb_id>_<source>_<timestamp>.json
        # Clean afb_id and source for filename
        clean_afb = afb_id.replace(":", "-")
        clean_source = source.replace(":", "-").replace("/", "-")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{clean_afb}_{clean_source}_{timestamp}.json"
        
        file_path = self.output_dir / filename
        with open(file_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        return result

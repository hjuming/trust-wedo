"""Metadata utility for Trust WEDO."""

from datetime import datetime
from trust_wedo import __version__

def get_meta(input_source: str) -> dict:
    """Generate the standard meta object for JSON outputs."""
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "tool_version": __version__,
        "input_source": input_source
    }

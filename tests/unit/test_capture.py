import json
import pytest
from trust_wedo.core.capture_manager import CaptureManager

def test_capture_output(tmp_path):
    output_dir = tmp_path / "captures"
    manager = CaptureManager(output_dir=str(output_dir))
    
    afb_id = "afb:test-capture"
    ai_output = "This is a captured AI response."
    source = "test-ai"
    
    result = manager.capture(afb_id, ai_output, source)
    
    assert result["afb_id"] == afb_id
    assert result["ai_output"] == ai_output
    assert result["source"] == source
    assert result["capture_id"] == "cap:001"
    assert "meta" in result
    
    # Verify file exists
    files = list(output_dir.glob("capture_*.json"))
    assert len(files) == 1
    
    with open(files[0]) as f:
        data = json.load(f)
        assert data["capture_id"] == "cap:001"
        assert data["ai_output"] == ai_output

def test_capture_id_increment(tmp_path):
    output_dir = tmp_path / "captures"
    manager = CaptureManager(output_dir=str(output_dir))
    
    manager.capture("afb:1", "output 1")
    result2 = manager.capture("afb:2", "output 2")
    
    assert result2["capture_id"] == "cap:002"

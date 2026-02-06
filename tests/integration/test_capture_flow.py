import os
import subprocess
import json
from pathlib import Path

def test_cli_capture_flow(tmp_path):
    output_dir = tmp_path / "output"
    captures_dir = output_dir / "captures"
    
    # Run tw capture via subprocess
    cmd = [
        "python3", "-m", "trust_wedo.cli", "capture",
        "afb:test-flow",
        "--ai-output", "Integrated test output",
        "--source", "cli-test",
        "--output", str(captures_dir)
    ]
    
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "✅ Schema 驗證成功" in result.stdout
    
    # Check if file was created
    files = list(captures_dir.glob("capture_*.json"))
    assert len(files) == 1
    
    with open(files[0]) as f:
        data = json.load(f)
        assert data["afb_id"] == "afb:test-flow"
        assert data["ai_output"] == "Integrated test output"
        assert data["source"] == "cli-test"
        assert "meta" in data

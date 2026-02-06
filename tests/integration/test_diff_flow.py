import os
import subprocess
import json
from pathlib import Path

def test_cli_diff_flow(tmp_path):
    # Setup directories
    output_dir = tmp_path / "output"
    captures_dir = output_dir / "captures"
    diffs_dir = output_dir / "diffs"
    output_dir.mkdir()
    captures_dir.mkdir()
    
    afb_id = "afb:test-diff-flow"
    
    # 1. Create a dummy AFB file (required by tw diff)
    # The tw diff currently looks at output/afb.json by default in MVP
    # Let's create it in the project root output/ temporarily or mock it.
    # Wait, I should make the command support --afb option if possible,
    # but the user spec didn't mention it.
    # I'll create it in the actual output/ directory of the project for this test
    # but that might affect other tests. 
    # Better: I'll use the actual output/afb.json if it exists, or create one.
    
    actual_output_afb = Path("output/afb.json")
    original_afb_content = None
    if actual_output_afb.exists():
        original_afb_content = actual_output_afb.read_text()
    
    actual_output_afb.parent.mkdir(parents=True, exist_ok=True)
    afb_data = {
        "afb_id": afb_id,
        "ai_quick_answer": "Reference answer for diff test."
    }
    actual_output_afb.write_text(json.dumps(afb_data))
    
    try:
        # 2. Capture something
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        
        subprocess.run([
            "python3", "-m", "trust_wedo.cli", "capture",
            afb_id,
            "--ai-output", "Reference answer for diff test.",
            "--source", "gpt-diff-test",
            "--output", str(captures_dir)
        ], env=env, check=True)
        
        # 3. Run diff
        cmd = [
            "python3", "-m", "trust_wedo.cli", "diff",
            afb_id,
            "--captures-dir", str(captures_dir),
            "--output", str(diffs_dir)
        ]
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "✅ Schema 驗證成功" in result.stdout
        assert "找到 1 個相關 Capture" in result.stdout
        
        # Check output
        diff_files = list(diffs_dir.glob("diff_*.json"))
        assert len(diff_files) == 1
        
        with open(diff_files[0]) as f:
            data = json.load(f)
            assert data["afb_id"] == afb_id
            assert data["summary"]["total_captures"] == 1
            assert data["comparisons"][0]["similarity_score"] == 1.0
            
    finally:
        # Restore original AFB if any
        if original_afb_content:
            actual_output_afb.write_text(original_afb_content)
        else:
            if actual_output_afb.exists():
                actual_output_afb.unlink()

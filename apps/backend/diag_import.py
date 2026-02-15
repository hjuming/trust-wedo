import sys
import os

# Simulate the backend environment
sys.path.insert(0, os.getcwd())

print(f"CWD: {os.getcwd()}")
print(f"Python Path: {sys.path}")

try:
    print("Attempting to import trust_wedo.parsers.playwright_parser...")
    from trust_wedo.parsers.playwright_parser import PlaywrightParser
    print("[OK] PlaywrightParser imported successfully.")
    
    import playwright
    print(f"[OK] Playwright package version: {playwright.__version__ if hasattr(playwright, '__version__') else 'unknown'}")
    
except ImportError as e:
    print(f"[FAIL] ImportError: {e}")
except Exception as e:
    print(f"[FAIL] General Exception: {e}")

try:
    from trust_wedo.parsers.site_parser import PLAYWRIGHT_AVAILABLE
    print(f"SiteParser.PLAYWRIGHT_AVAILABLE = {PLAYWRIGHT_AVAILABLE}")
except ImportError as e:
    print(f"[FAIL] Could not import SiteParser: {e}")

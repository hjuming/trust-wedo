import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("check_env")

def check_playwright():
    print("=== Playwright Environment Check ===")
    
    # 1. Check if playwright is installed
    try:
        import playwright
        import importlib.metadata
        version = importlib.metadata.version("playwright")
        print(f"[OK] Playwright package is installed (version: {version})")
    except (ImportError, importlib.metadata.PackageNotFoundError):
        print("[FAIL] Playwright package is NOT installed.")
        return False

    # 2. Check if chromium is available
    from playwright.async_api import async_playwright
    import asyncio

    async def check_browser():
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                print("[OK] Chromium browser launched successfully.")
                await browser.close()
                return True
        except Exception as e:
            print(f"[FAIL] Failed to launch Chromium: {e}")
            return False

    return asyncio.run(check_browser())

def check_python_path():
    print("\n=== Python Path Check ===")
    print(f"Python Executable: {sys.executable}")
    print(f"CWD: {os.getcwd()}")
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not Set')}")
    
    try:
        import trust_wedo
        print(f"[OK] trust_wedo module found at {trust_wedo.__file__}")
    except ImportError:
        print("[FAIL] trust_wedo module NOT found in path.")

if __name__ == "__main__":
    check_python_path()
    success = check_playwright()
    
    if success:
        print("\n[RESULT] Environment looks GOOD for Playwright rendering.")
    else:
        print("\n[RESULT] Environment is NOT ready for Playwright. Check installation logs.")
        sys.exit(1)


import sys
import os
import asyncio
import logging

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from trust_wedo.parsers.playwright_parser import PlaywrightParser

logging.basicConfig(level=logging.INFO)

async def test_crawl():
    # Define project_root based on the script's location
    # Assuming script is in project_root/tests/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    test_urls = [
        "https://www.google.com",
        "https://en.wikipedia.org/wiki/Main_Page",
        "https://www.wedopr.com"  # The critical SPA site
    ]
    
    print(f"Starting verification of {len(test_urls)} URLs...")
    
    # Ensure sys.path includes apps/backend and src
    sys.path.insert(0, os.path.join(project_root, "apps", "backend"))
    sys.path.insert(0, os.path.join(project_root, "src"))

    try:
        from trust_wedo.parsers.playwright_parser import PlaywrightParser
        print("[OK] Import successful.")
    except ImportError as e:
        print(f"[FAIL] Import failed: {e}")
        return

    async with PlaywrightParser() as parser:
        for url in test_urls:
            print(f"\n--- Testing {url} ---")
            try:
                content = await parser.fetch_content(url)
                if content:
                    size_kb = len(content)/1024
                    has_schema = 'application/ld+json' in content
                    print(f"[OK] Fetched content. Size: {size_kb:.1f}KB")
                    print(f"[OK] Schema detection: {'FOUND' if has_schema else 'NOT FOUND'}")
                    
                    if has_schema:
                         print("[SUCCESS] Content rendered correctly.")
                    elif "wedopr" in url:
                         print("[WARN] Content fetched but Schema.org MISSING for wedopr. Check hydration buffer.")
                else:
                    print(f"[FAIL] Fetched content is None.")
            except Exception as e:
                print(f"[ERROR] Exception during fetch: {e}")

if __name__ == "__main__":
    asyncio.run(test_crawl())

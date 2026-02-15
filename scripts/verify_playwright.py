
import sys
import os
import asyncio
import logging

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from trust_wedo.parsers.playwright_parser import PlaywrightParser

logging.basicConfig(level=logging.INFO)

async def test_crawl():
    urls = [
        "https://example.com",
        "https://www.wedopr.com/"
    ]
    
    print("Initializing parser...")
    try:
        async with PlaywrightParser() as parser:
            for url in urls:
                print(f"\nCrawling {url}...")
                # Increase timeout to 60s for testing
                content = await parser.fetch_content(url, timeout=60000)
                
                if content:
                    print(f"✅ Success! Content length: {len(content)}")
                    if "React" in content or "root" in content:
                        print("   (Contains React/root keywords)")
                else:
                    print(f"❌ Failed to fetch content for {url}")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(test_crawl())

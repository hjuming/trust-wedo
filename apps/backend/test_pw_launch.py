import asyncio
from playwright.async_api import async_playwright
import sys
import os

async def main():
    print("Attempting to launch Playwright Chromium...")
    try:
        async with async_playwright() as p:
            print("p.chromium.launch starting...")
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            print("[OK] Browser launched successfully.")
            await browser.close()
            print("[OK] Browser closed.")
    except Exception as e:
        print(f"[FAIL] Playwright launch failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

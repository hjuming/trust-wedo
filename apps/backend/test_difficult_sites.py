"""
測試特殊網站檢測功能
"""
import sys
sys.path.insert(0, '/Users/MING/Sites/Trust-WEDO/apps/backend')

from app.constants.difficult_sites import check_difficult_site

test_urls = [
    "https://zh.wikipedia.org",
    "https://en.wikipedia.org", 
    "https://wikipedia.org",
    "https://developer.mozilla.org",
    "https://github.com",
    "https://www.nytimes.com",
    "https://stackoverflow.com",
]

print("=" * 60)
print("測試特殊網站檢測功能")
print("=" * 60)

for url in test_urls:
    result = check_difficult_site(url)
    status = "✓ 檢測到" if result else "✗ 未檢測到"
    print(f"\n{status}: {url}")
    if result:
        print(f"  → 網站: {result.get('name_zh', result.get('name'))}")
        print(f"  → 預估分數: {result.get('estimated_score')}")
        print(f"  → 匹配域名: {result.get('domain')}")

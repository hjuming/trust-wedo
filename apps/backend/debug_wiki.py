
import asyncio
import httpx
from bs4 import BeautifulSoup

async def fetch_wikipedia():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1"
    }
    
    urls = ["https://en.wikipedia.org/wiki/Main_Page", "https://zh.wikipedia.org/zh-tw/Python"]
    
    async with httpx.AsyncClient(follow_redirects=True, verify=False, timeout=10.0) as client:
        for url in urls:
            try:
                print(f"\nScanning: {url}")
                resp = await client.get(url, headers=headers)
                print(f"Status: {resp.status_code}")
                
                soup = BeautifulSoup(resp.text, "html.parser")
                title = soup.title.string if soup.title else "No Title"
                desc = soup.find('meta', attrs={'name': 'description'})
                json_ld = soup.find_all('script', type='application/ld+json')
                
                print(f"Title: {title.strip()}")
                
                # Check for og:description as fallback
                og_desc = soup.find('meta', property='og:description')
                print(f"Description Found: {bool(desc)}")
                print(f"OG Description Found: {bool(og_desc)}")
                
                if desc:
                    print(f"Description Content: {desc.get('content', '')[:50]}...")
                elif og_desc:
                    print(f"OG Description Content: {og_desc.get('content', '')[:50]}...")

                print(f"JSON-LD Scripts: {len(json_ld)}")
                for script in json_ld:
                    if script.string:
                        print(f"JSON-LD Content Start: {script.string[:100]}...")
                
                
                # Check root domain comparison logic
                external_links = 0
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('http'):
                        if 'wikipedia.org' not in href and 'wikimedia' not in href:
                             external_links += 1
                print(f"Rough External Links: {external_links}")
                
            except Exception as e:
                print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_wikipedia())

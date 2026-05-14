import os

import httpx

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

HEADERS = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
}


def check_latest():
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")

    print(f"Fetching latest scan for wedopr.com from {SUPABASE_URL}...")
    try:
        # 1. Get latest jobs
        url = (
            f"{SUPABASE_URL}/rest/v1/scan_jobs"
            "?url=ilike.*wedopr.com*&order=created_at.desc&limit=5"
        )
        resp = httpx.get(url, headers=HEADERS)
        jobs = resp.json()

        if not jobs:
            print("No jobs found.")
            return

        for idx, job in enumerate(jobs):
            print(f"\n--- Job {idx+1} ---")
            print(f"ID: {job['id']}")
            print(f"URL: {job['url']}")
            print(f"Status: {job['status']}")
            print(f"Created: {job['created_at']}")
            total_score = (
                job.get("result", {}).get("total_score", "N/A")
                if job.get("result")
                else "N/A"
            )
            print(f"Result Total Score: {total_score}")

            # 2. Get artifact for this job
            art_url = f"{SUPABASE_URL}/rest/v1/artifacts?job_id=eq.{job['id']}&stage=eq.scan"
            art_resp = httpx.get(art_url, headers=HEADERS)
            arts = art_resp.json()

            if arts:
                payload = arts[0]["jsonb_payload"]
                print(f"Parser Used: {payload.get('parser_used', 'MISSING')}")
                pages = payload.get('pages', [])
                print(f"Pages count: {len(pages)}")
                if pages:
                    p0 = pages[0]
                    print(f"First page Schema detected: {p0.get('has_jsonld')}")
                    print(f"First page Schema types: {p0.get('schema_types', 'MISSING')}")
                    print(f"First page title_missing: {p0.get('title_missing')}")
            else:
                print("No scan artifact found.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_latest()

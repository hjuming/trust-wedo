import os
import sys
import json
# Add apps/backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'apps/backend'))

from app.core.supabase import supabase

def get_latest():
    print("Fetching latest scan for wedopr.com...")
    try:
        # 1. Get latest scan job for wedopr.com
        res = supabase.table("scan_jobs")\
            .select("*")\
            .ilike("url", "%wedopr.com%")\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        
        if not res.data:
            print("No scans found for wedopr.com")
            return
            
        job = res.data[0]
        job_id = job["id"]
        print(f"Found Job ID: {job_id} | Status: {job['status']} | Created: {job['created_at']}")
        print(f"Result in scan_jobs: {json.dumps(job.get('result'))}")
        
        # 2. Get artifact for this job
        art_res = supabase.table("artifacts")\
            .select("*")\
            .eq("job_id", job_id)\
            .eq("stage", "scan")\
            .execute()
            
        if not art_res.data:
            print(f"No scan artifact found for job {job_id}")
            return
            
        payload = art_res.data[0]["jsonb_payload"]
        print("\n=== Scan Metadata ===")
        print(f"Parser Used: {payload.get('parser_used', 'N/A')}")
        print(f"Pages Scanned: {len(payload.get('pages', []))}")
        
        if payload.get('pages'):
             first_page = payload['pages'][0]
             print(f"First Page URL: {first_page.get('url')}")
             print(f"Schema Found: {len(first_page.get('schemas', []))}")
             # Print a snippet of HTML if available in payload? No, usually not in artifact payload unless we changed it.
             # Wait, site_parser.py scan() returns full page info which includes static content?
             # Let's check SiteParser._scan_page
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_latest()

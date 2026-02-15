import os
import sys
# Add apps/backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'apps/backend'))

from app.core.supabase import supabase

def check_schema():
    print("Checking scan_jobs schema...")
    try:
        # Try to select 'progress' from scan_jobs. If it fails, it doesn't exist.
        res = supabase.table("scan_jobs").select("progress").limit(1).execute()
        print("Success! 'progress' column exists.")
        print(res.data)
    except Exception as e:
        print(f"Error selecting progress: {e}")
        # Try to get one row to see all columns
        try:
            res = supabase.table("scan_jobs").select("*").limit(1).execute()
            if res.data:
                print("Available columns:", res.data[0].keys())
            else:
                print("Table empty, cannot determine columns easily.")
        except Exception as e2:
            print(f"Error selecting *: {e2}")

if __name__ == "__main__":
    check_schema()

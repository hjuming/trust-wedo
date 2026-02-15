import sys
import os
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

# Add apps/backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'apps/backend'))

# Mock dependencies BEFORE importing api/scans.py
sys.modules['app.core.dependencies'] = MagicMock()
sys.modules['app.core.supabase'] = MagicMock()
sys.modules['trust_wedo.parsers.site_parser'] = MagicMock()
sys.modules['app.services.report_engine'] = MagicMock()
sys.modules['app.services.scoring'] = MagicMock()
sys.modules['fastapi'] = MagicMock()
sys.modules['pydantic'] = MagicMock()
sys.modules['pydantic.fields'] = MagicMock()

# Now import
from app.api.scans import run_scan_pipeline

async def test_progress_update():
    print("Testing run_scan_pipeline with progress updates...")
    
    # Mock Supabase
    mock_supabase = sys.modules['app.core.supabase'].supabase
    mock_table = mock_supabase.table.return_value
    mock_update = mock_table.update.return_value
    mock_eq = mock_update.eq.return_value
    mock_execute = mock_eq.execute
    
    # Mock SiteParser
    MockSiteParser = sys.modules['trust_wedo.parsers.site_parser'].SiteParser
    mock_parser_instance = MockSiteParser.return_value
    
    # Mock scan() to call usage of progress_callback if passed
    async def mock_scan():
        # Retrieve the callback passed to __init__
        # But wait, run_scan_pipeline passes callback to __init__
        # We need to capture arguments passed to __init__
        pass
    
    mock_parser_instance.scan = AsyncMock(side_effect=mock_scan)

    # We cannot easily capture callback from constructor call in this simple mock setup 
    # unless we patch SiteParser class more deeply.
    # Instead, let's verify update calls.
    
    # Run pipeline
    # We patch SiteParser in app.api.scans
    with patch('app.api.scans.SiteParser') as MockParserClass:
        mock_instance = MockParserClass.return_value
        
        # Define a scan method that uses the callback
        async def side_effect_scan():
            # Get the callback from init args
            args, kwargs = MockParserClass.call_args
            callback = kwargs.get('progress_callback')
            if callback:
                print("Callback found! Calling it.")
                await callback(50, "Halfway there")
            return { "url": "http://test.com" }
            
        mock_instance.scan = AsyncMock(side_effect=side_effect_scan)
        
        # Run
        await run_scan_pipeline("test-job-id", "http://test.com")
        
        print("Mock Supabase calls:")
        for call in mock_supabase.mock_calls:
            print(call)
        
        # Check if update was called with progress strings
        # We expect calls like: update({"progress_stage": "[50%] Halfway there", ...})
        
        found_progress = False
        for call in mock_supabase.mock_calls:
            # call is like: call.table('scan_jobs').update({'progress_stage': '...'})
            # args are in call.args or call[1]
            if "update" in str(call):
                args = call.args if hasattr(call, 'args') else call[1]
                if args and isinstance(args[0], dict) and "progress_stage" in args[0]:
                     stage = args[0]["progress_stage"]
                     print(f"Update called with stage: {stage}")
                     if "[" in stage and "]" in stage:
                         found_progress = True
                    
        if found_progress:
            print("✅ Verified progress update via callback!")
        else:
            print("❌ Failed to verify progress update.")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_progress_update())

from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user, get_current_org
from app.core.supabase import supabase
from app.models.signals import SiteSignals
from app.services.report_engine import ReportEngine

router = APIRouter()
engine = ReportEngine()

@router.get("/{job_id}")
def get_report(
    job_id: str,
    user = Depends(get_current_user),
    org_id: str = Depends(get_current_org)
):
    """取得報告（規則引擎版）"""
    
    # 1. 取得 scan job
    job_result = supabase.table("scan_jobs")\
        .select("*")\
        .eq("id", job_id)\
        .eq("org_id", org_id)\
        .single()\
        .execute()
    
    if not job_result.data:
        raise HTTPException(status_code=404, detail="Scan job not found")
    
    job = job_result.data
    
    # 2. 取得 artifacts
    artifacts_result = supabase.table("artifacts")\
        .select("*")\
        .eq("job_id", job_id)\
        .execute()
    
    artifacts = artifacts_result.data
    
    # 3. 檢查任務狀態
    if job['status'] == 'failed':
        return {
            "job_id": job_id,
            "url": job['url'],
            "status": job['status'],
            "summary": {
                "conclusion": f"❌ 分析失敗: {job.get('error_message', '原因未知')}",
                "grade": "F"
            },
            "issues": [],
            "suggestions": []
        }
    
    if not artifacts:
        return {
            "job_id": job_id,
            "url": job['url'],
            "status": job['status'],
            "summary": {
                "conclusion": "⏳ 報告正在生成中，請稍候...",
                "grade": "P"
            },
            "issues": [],
            "suggestions": []
        }
    
    # 4. 提取 signals 並產生報告
    signals = engine.extract_signals(artifacts)
    report = engine.generate_report(signals)
    
    # 5. 加入任務基本資訊
    report["job_id"] = job_id
    report["url"] = job['url']
    report["status"] = job['status']
    report["raw_artifacts"] = artifacts  # 進階檢視用
    
    return report

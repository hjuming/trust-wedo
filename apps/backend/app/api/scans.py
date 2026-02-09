from fastapi import APIRouter, Depends, BackgroundTasks
from app.core.dependencies import get_current_user, get_current_org
from app.core.supabase import supabase
from pydantic import BaseModel, HttpUrl

router = APIRouter()

class ScanCreate(BaseModel):
    url: HttpUrl

@router.post("/")
def create_scan(
    scan_data: ScanCreate,
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user),
    org_id: str = Depends(get_current_org)
):
    """建立掃描任務"""
    # 建立 scan job
    result = supabase.table("scan_jobs").insert({
        "org_id": org_id,
        "user_id": user.id,
        "url": str(scan_data.url),
        "status": "pending"
    }).execute()
    
    job_id = result.data[0]["id"]
    
    # 加入背景任務
    background_tasks.add_task(run_scan_pipeline, job_id, str(scan_data.url))
    
    return result.data[0]

@router.get("/")
def get_scans(org_id: str = Depends(get_current_org)):
    """取得組織的掃描列表"""
    result = supabase.table("scan_jobs")\
        .select("*")\
        .eq("org_id", org_id)\
        .order("created_at", desc=True)\
        .execute()
    
    return result.data

@router.get("/{job_id}/artifacts")
def get_artifacts(
    job_id: str,
    org_id: str = Depends(get_current_org)
):
    """取得掃描的所有 artifacts"""
    result = supabase.table("artifacts")\
        .select("*")\
        .eq("job_id", job_id)\
        .execute()
    
    return result.data

def run_scan_pipeline(job_id: str, url: str):
    """背景任務：執行 CLI pipeline"""
    # TODO: 整合 CLI 工具
    pass

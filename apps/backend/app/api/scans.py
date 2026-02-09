from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.core.dependencies import get_current_user, get_current_org
from app.core.supabase import supabase
from pydantic import BaseModel, HttpUrl
import subprocess
import json
import os
from pathlib import Path
from typing import List

router = APIRouter()

class ScanCreate(BaseModel):
    url: HttpUrl

def run_scan_pipeline(job_id: str, url: str):
    """背景任務：執行 CLI pipeline（MVP 版本）"""
    try:
        # 1. 更新狀態為 processing - 階段 1
        supabase.table("scan_jobs").update({
            "status": "processing",
            "progress_stage": "正在讀取網站內容...",
            "started_at": "now()"
        }).eq("id", job_id).execute()
        
        # 建立輸出目錄
        output_dir = Path(f"output/{job_id}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. 執行 tw scan（核心步驟）
        # 更新進度階段
        supabase.table("scan_jobs").update({
            "progress_stage": "正在分析 AI 識別特徵..."
        }).eq("id", job_id).execute()
        
        scan_result = subprocess.run(
            ["tw", "scan", url],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if scan_result.returncode != 0:
            raise Exception(f"Scan failed: {scan_result.stderr}")
        
        # 3. 讀取並儲存成果
        supabase.table("scan_jobs").update({
            "progress_stage": "正在產生成信度報告..."
        }).eq("id", job_id).execute()
        
        default_site_json = Path("output/site.json")
        if not default_site_json.exists():
            raise Exception("site.json not found after scan")
        
        target_site_json = output_dir / "site.json"
        with open(default_site_json, 'r') as f:
            site_data = json.load(f)
            
        with open(target_site_json, 'w') as f:
            json.dump(site_data, f)
        
        # 4. 儲存到 artifacts 表
        supabase.table("artifacts").insert({
            "job_id": job_id,
            "stage": "scan",
            "jsonb_payload": site_data,
            "schema_version": "1.0"
        }).execute()
        
        # 5. 更新狀態為 completed
        supabase.table("scan_jobs").update({
            "status": "completed",
            "progress_stage": "分析完成",
            "completed_at": "now()"
        }).eq("id", job_id).execute()
        
    except subprocess.TimeoutExpired:
        supabase.table("scan_jobs").update({
            "status": "failed",
            "progress_stage": "分析超時",
            "error_message": "分析超時（超過 120 秒）"
        }).eq("id", job_id).execute()
        
    except Exception as e:
        supabase.table("scan_jobs").update({
            "status": "failed",
            "progress_stage": "分析失敗",
            "error_message": str(e)
        }).eq("id", job_id).execute()

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
        "status": "pending",
        "progress_stage": "排隊中..."
    }).execute()
    
    if not result.data:
         raise HTTPException(status_code=500, detail="Failed to create scan job")
         
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

@router.get("/{job_id}")
def get_scan(
    job_id: str,
    org_id: str = Depends(get_current_org)
):
    """取得特定掃描任務狀態"""
    result = supabase.table("scan_jobs")\
        .select("*")\
        .eq("id", job_id)\
        .eq("org_id", org_id)\
        .single()\
        .execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Scan job not found")
        
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

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.core.dependencies import get_current_user, get_current_org
from app.core.supabase import supabase
from pydantic import BaseModel, HttpUrl
import subprocess
import json
import os
from pathlib import Path
from typing import List
from datetime import datetime
import asyncio
from trust_wedo.parsers.site_parser import SiteParser

from app.services.report_engine import ReportEngine
from app.services.scoring import calculate_dimension_scores, score_to_grade

engine = ReportEngine()

router = APIRouter()

class ScanCreate(BaseModel):
    url: HttpUrl

async def run_scan_pipeline(job_id: str, url: str):
    """背景任務：執行 CLI pipeline（直接調用庫，無需 CLI）"""
    async def update_progress(percent: int, message: str):
        try:
            # Update progress_stage with percentage prefix for frontend parsing
            stage_text = f"[{percent}%] {message}"
            supabase.table("scan_jobs").update({
                "progress_stage": stage_text,
                "updated_at": "now()"
            }).eq("id", job_id).execute()
        except Exception as e:
            print(f"Failed to update progress for job {job_id}: {e}")

    try:
        # 1. 更新狀態為 processing (0%)
        supabase.table("scan_jobs").update({
            "status": "processing",
            "started_at": "now()"
        }).eq("id", job_id).execute()
        
        await update_progress(0, "正在初始化分析引擎...")
        
        # 建立輸出目錄
        output_dir = Path(f"output/{job_id}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. 執行 SiteParser (Core Logic)
        await update_progress(5, "正在讀取網站結構...")
        
        # Direct Library Call with Progress Callback
        parser = SiteParser(url, max_pages=10, progress_callback=update_progress)
        
        try:
            # 設置 180 秒超時 (Playwright 較慢)
            site_data = await asyncio.wait_for(parser.scan(), timeout=180)
        except asyncio.TimeoutError:
            raise Exception("分析超時（超過 3 分鐘）")
        
        # 3. 儲存成果 (File + DB)
        await update_progress(90, "正在計算網站成信度分數...")
        
        # Write to file (local persistence in container, for debugging)
        target_site_json = output_dir / "site.json"
        with open(target_site_json, 'w') as f:
            json.dump(site_data, f, ensure_ascii=False)
        
        # 4. 儲存到 artifacts 表
        # 構造 artifact 格式以供 extract_signals 使用
        artifact_payload = {
            "job_id": job_id,
            "stage": "scan",
            "jsonb_payload": site_data,
            "schema_version": "1.0"
        }
        
        supabase.table("artifacts").insert(artifact_payload).execute()
        
        # 計算分數 (新增邏輯)
        try:
            await update_progress(95, "正在生成最終報告...")
            signals = engine.extract_signals([artifact_payload])
            dimension_scores = calculate_dimension_scores(signals)
            total_score = sum(d['score'] for d in dimension_scores.values())
            grade = score_to_grade(total_score)
            
            result_data = {
                "total_score": total_score,
                "grade": grade,
                "dimension_scores": dimension_scores,
                "generated_at": datetime.utcnow().isoformat()
            }
        except Exception as score_err:
            print(f"Scoring error: {score_err}")
            result_data = None
        
        # 5. 更新狀態為 completed
        supabase.table("scan_jobs").update({
            "status": "completed",
            "progress_stage": "[100%] 分析完成",
            "completed_at": "now()",
            "result": result_data # 儲存計算結果
        }).eq("id", job_id).execute()
        
    except Exception as e:
        supabase.table("scan_jobs").update({
            "status": "failed",
            "progress_stage": "分析失敗",
            "error_message": str(e)
        }).eq("id", job_id).execute()

@router.post("")
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

@router.get("")
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

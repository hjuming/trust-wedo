from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from app.core.dependencies import get_current_user, get_current_org
from app.core.supabase import supabase
from app.models.signals import SiteSignals
from app.services.report_engine import ReportEngine
from app.services.report_pdf import generate_report_pdf
from app.services.scoring import calculate_dimension_scores, score_to_grade
from app.services.quick_wins import generate_quick_wins

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


@router.get("/{job_id}/dimensions")
def get_report_dimensions(
    job_id: str,
    user = Depends(get_current_user),
    org_id: str = Depends(get_current_org)
):
    """取得報告的五大維度明細與快速勝利建議
    
    此 endpoint 專為前端視覺化設計,提供:
    - 五大維度分數與明細
    - Quick Wins 建議 (前 3 項)
    - 總分與等級
    """
    
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
    
    if not artifacts:
        raise HTTPException(status_code=400, detail="Report not ready yet")
    
    # 3. 提取 signals
    signals = engine.extract_signals(artifacts)
    
    # 4. 計算維度分數
    dimension_scores = calculate_dimension_scores(signals)
    
    # 5. 計算總分與等級
    total_score = sum(d['score'] for d in dimension_scores.values())
    grade = score_to_grade(total_score)
    
    # 6. 生成 Quick Wins 建議
    quick_wins = generate_quick_wins(signals, dimension_scores)
    
    # 7. 格式化維度資料 (加入中文名稱與百分比)
    dimension_names = {
        'discoverability': 'AI可發現性',
        'identity': '身分可信度',
        'structure': '內容結構化',
        'social': '社群信任',
        'technical': '技術基礎'
    }
    
    formatted_dimensions = {}
    for key, data in dimension_scores.items():
        formatted_dimensions[key] = {
            'name': dimension_names.get(key, key),
            'score': data['score'],
            'max': data['max'],
            'percentage': int((data['score'] / data['max']) * 100) if data['max'] > 0 else 0,
            'items': data['items']
        }
    
    return {
        "scan_id": job_id,
        "url": job['url'],
        "total_score": total_score,
        "grade": grade,
        "dimensions": formatted_dimensions,
        "quick_wins": quick_wins
    }


@router.get("/{job_id}/pdf")
def download_report_pdf(
    job_id: str,
    user = Depends(get_current_user),
    org_id: str = Depends(get_current_org)
):
    """下載 PDF 報告"""
    
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
    
    if not artifacts_result.data:
        raise HTTPException(status_code=400, detail="Report not ready yet")
    
    artifacts = artifacts_result.data
    
    # 3. 生成報告數據 (Text Report)
    signals = engine.extract_signals(artifacts)
    report = engine.generate_report(signals)
    report["url"] = job['url']
    
    # 4. 生成維度數據 (Dimensions & Scores)
    dimension_scores = calculate_dimension_scores(signals)
    quick_wins = generate_quick_wins(signals, dimension_scores)
    total_score = sum(d['score'] for d in dimension_scores.values())
    
    dimensions_data = {
        "dimensions": dimension_scores,
        "quick_wins": quick_wins,
        "total_score": total_score
    }
    
    # 5. 生成 PDF
    filename, pdf_content = generate_report_pdf(report, dimensions_data)
    
    # 6. 回傳檔案
    return Response(
        content=bytes(pdf_content),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )

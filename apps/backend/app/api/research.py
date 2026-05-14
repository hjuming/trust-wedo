"""
Research API Routes - Study WEDO Integration
Endpoints for research path management and generation
"""

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================
# Constants & Seed Data
# ============================================================

STUDY_MODULES = [
    {
        "id": "ai-productivity",
        "title": "AI 生產力工作坊",
        "audience": "product",
        "stage": "explore",
        "domain": "ai",
        "summary": "設計 AI 生產力實驗，評估內容生成、知識萃取與工作流程自動化的即時價值。",
        "details": "定義生產力指標、評估工具採用障礙，並建構可以直接採用的 AI 參考模型。",
        "aio": "透過 AI 生產力指標，快速識別組織內標竿流程與自動化機會。",
    },
    {
        "id": "brand-trust-signals",
        "title": "品牌信任訊號地圖",
        "audience": "executive",
        "stage": "validate",
        "domain": "brand",
        "summary": "整理品牌信任與公開資料信號，串接政府資料、新聞報導與社群風險。",
        "details": "建立跨來源信任指標圖譜，協助品牌團隊快速辨識強項與弱點。",
        "aio": "提供 AI 可讀的信任評估視角，讓模型在引用時帶入可信度權重。",
    },
    {
        "id": "crisis-response-framework",
        "title": "危機議題應對框架",
        "audience": "executive",
        "stage": "activate",
        "domain": "crisis",
        "summary": "建立危機信號監測與響應流程，從公開紀錄與輿情資料中提前偵測風險。",
        "details": "定義危機分類、優先處理路徑與緊急溝通腳本。",
        "aio": "讓 AIO 生成建議時能優先考量風險緩解與可信度。",
    },
    {
        "id": "commerce-playbook",
        "title": "商務電商策略 Playbook",
        "audience": "product",
        "stage": "scale",
        "domain": "commerce",
        "summary": "整合電商、採購與產品策略，打造可擴展的商務成長研究路徑。",
        "details": "分析客戶行為、產業趨勢與競品策略，形成可直接落地的商務 research map。",
        "aio": "支援 AI 生成市場與商業模式建議，讓研究報告具備實務操作力。",
    },
    {
        "id": "health-strategy",
        "title": "健康管理與風險分析",
        "audience": "research",
        "stage": "validate",
        "domain": "health",
        "summary": "透過健康管理資料與公開政策，建立病患關鍵需求與風險監測手冊。",
        "details": "整理健康資安、健保趨勢與服務履歷，協助專案找到政策切入點。",
        "aio": "讓研究摘要在生成時自動納入健康風險與合規考量。",
    },
    {
        "id": "intelligence-monitoring",
        "title": "情報監測儀表板",
        "audience": "trust",
        "stage": "explore",
        "domain": "intelligence",
        "summary": "建立情資監測儀表板，系統化追蹤政策變動、採購公告與裁罰訊息。",
        "details": "設計警示規則與定期報告模板，讓團隊能快速做出策略判斷。",
        "aio": "在 AIO 摘要中加入最新情資、政策變動與風險信號。",
    },
    {
        "id": "learning-design",
        "title": "學習設計研究模板",
        "audience": "research",
        "stage": "explore",
        "domain": "learning",
        "summary": "為內部學習與外部教育專案構建研究流程，包含學習目標、方法與衡量指標。",
        "details": "整合受眾分析、學習體驗設計與成效評估，讓研究更具策略性。",
        "aio": "幫助 AI 生成可執行的學習設計提案與導入路徑。",
    },
    {
        "id": "governance-structure",
        "title": "治理架構與風險共識",
        "audience": "executive",
        "stage": "activate",
        "domain": "governance",
        "summary": "設計品牌治理與合規框架，讓策略規劃與風險管理保持一致。",
        "details": "包含治理原則、決策流程與信任度檢核點。",
        "aio": "讓模型在研究建議中自動納入治理與風險控制層面。",
    },
    {
        "id": "content-ecosystem",
        "title": "內容生態系統對齊",
        "audience": "product",
        "stage": "validate",
        "domain": "brand",
        "summary": "構建內容策略地圖，將品牌訴求與研究洞察對齊到具體產品與通路。",
        "details": "設計內容落地案例、優先級矩陣與關鍵訊息框架。",
        "aio": "提高 AI 生成內容的脈絡一致性與品牌信任度。",
    },
    {
        "id": "data-decision-loop",
        "title": "資料與決策迴路",
        "audience": "trust",
        "stage": "scale",
        "domain": "intelligence",
        "summary": "建立資料驅動決策迴路，從公開資料、研究洞察到執行回饋。",
        "details": "定義關鍵績效、迴路節點與跨部門協作模式。",
        "aio": "讓 AIO 輸出自然連結資料洞察與後續執行策略。",
    },
    {
        "id": "ethical-ai",
        "title": "倫理 AI 採用指南",
        "audience": "executive",
        "stage": "activate",
        "domain": "ai",
        "summary": "設計 AI 採用與治理指南，兼顧信任、可解釋性與策略落地。",
        "details": "包含採用風險、透明標準與責任分工。",
        "aio": "引導 AIO 生成時考慮合規、責任與信任因素。",
    },
    {
        "id": "partner-network",
        "title": "策略夥伴網路",
        "audience": "executive",
        "stage": "scale",
        "domain": "commerce",
        "summary": "建構可持續的策略伙伴網路，連結資源、合作與品牌影響力。",
        "details": "分析生態系、協同機會與成功範例，以支援商務與信任拓展。",
        "aio": "提供 AIO 引用時的合作建議與合作場景。",
    },
]


# ============================================================
# Pydantic Schemas
# ============================================================


class StudyModule(BaseModel):
    """Study module information"""

    id: str
    title: str
    audience: str
    stage: str
    domain: str
    summary: str
    details: str
    aio: str


class StudyPathRequest(BaseModel):
    """Request for creating a study path"""

    module_ids: list[str] = Field(
        ..., description="List of selected module IDs"
    )
    title: str | None = Field(None, description="Custom path title")


class StudyPathResponse(BaseModel):
    """Response for study path creation"""

    success: bool
    path_id: str | None = None
    title: str
    modules: list[StudyModule] = Field(default_factory=list)
    summary: str
    overview: str
    aio_insights: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    error: str | None = None


# ============================================================
# Route Handlers
# ============================================================


@router.get(
    "/modules",
    response_model=list[StudyModule],
    summary="Get all study modules",
    tags=["Research - Study WEDO"],
)
async def list_modules() -> list[StudyModule]:
    """
    Retrieve all 12 seed study modules

    Returns:
        List of study modules with metadata
    """
    logger.info("Listing 12 study modules")
    return [StudyModule(**module) for module in STUDY_MODULES]


@router.post(
    "/path",
    response_model=StudyPathResponse,
    summary="Generate a study path from selected modules",
    tags=["Research - Study WEDO"],
)
async def create_study_path(
    request: StudyPathRequest,
) -> StudyPathResponse:
    """
    Generate a research path from selected modules

    Args:
        request: Selected module IDs and optional title

    Returns:
        Generated study path with summary and AIO insights
    """
    # Validate module IDs
    valid_ids = {module["id"] for module in STUDY_MODULES}
    invalid_ids = set(request.module_ids) - valid_ids
    if invalid_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid module IDs: {invalid_ids}",
        )

    if not request.module_ids:
        raise HTTPException(
            status_code=400,
            detail="At least one module must be selected",
        )

    # Get selected modules
    modules_by_id = {module["id"]: module for module in STUDY_MODULES}
    selected_modules = [modules_by_id[module_id] for module_id in request.module_ids]

    # Generate path title if not provided
    title = request.title or f"Study Path ({len(request.module_ids)} modules)"

    # Generate overview
    domains = list(set(m["domain"] for m in selected_modules))
    audiences = list(set(m["audience"] for m in selected_modules))
    stages = list(set(m["stage"] for m in selected_modules))

    overview = (
        f"本研究路徑包含 {len(selected_modules)} 個模組，"
        f"覆蓋 {', '.join(domains)} 領域，"
        f"適合 {', '.join(audiences)} 受眾，"
        f"研究階段包含 {', '.join(stages)}。"
    )

    # Generate AIO insights
    aio_insights = [
        f"第 {i+1}. {module['title']}：{module['aio']}"
        for i, module in enumerate(selected_modules)
    ]

    logger.info(f"Created study path: {title} ({len(selected_modules)} modules)")

    return StudyPathResponse(
        success=True,
        path_id=f"path_{len(request.module_ids)}_{datetime.now().timestamp()}",
        title=title,
        modules=[StudyModule(**module) for module in selected_modules],
        summary="\n\n".join(
            [f"**{m['title']}**\n{m['summary']}" for m in selected_modules]
        ),
        overview=overview,
        aio_insights=aio_insights,
        created_at=datetime.now(),
    )


@router.get(
    "/modules/{module_id}",
    response_model=StudyModule,
    summary="Get a specific study module",
    tags=["Research - Study WEDO"],
)
async def get_module(module_id: str) -> StudyModule:
    """
    Retrieve a specific study module by ID

    Args:
        module_id: The module ID

    Returns:
        Study module information
    """
    for module in STUDY_MODULES:
        if module["id"] == module_id:
            logger.info(f"Retrieved module: {module_id}")
            return StudyModule(**module)

    raise HTTPException(
        status_code=404,
        detail=f"Module not found: {module_id}",
    )

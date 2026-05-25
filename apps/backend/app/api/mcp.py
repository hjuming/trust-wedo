"""
MCP API Routes - Data Query Layer
Endpoints for Twinkle Hub data access through MCP
"""

import logging

from app.core.mcp_integration import TwinkleMCPClient, get_mcp_client
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================
# Pydantic Schemas
# ============================================================


class DomainInfo(BaseModel):
    """Domain information schema"""

    key: str
    name_zh: str
    role: str
    scope: str
    typical_questions: list[str] = Field(default_factory=list)
    anchor_examples: list[str] = Field(default_factory=list)


class ListDomainsResponse(BaseModel):
    """Response for listing domains"""

    success: bool
    domains: list[dict] = Field(default_factory=list)
    cached: bool = False
    error: str | None = None


class SearchDatasetsRequest(BaseModel):
    """Request for searching datasets"""

    domain: str | None = None
    keyword: str | None = None
    limit: int = Field(default=10, ge=1, le=100)


class SearchDatasetsResponse(BaseModel):
    """Response for dataset search"""

    success: bool
    results: list[dict] = Field(default_factory=list)
    count: int = 0
    error: str | None = None


class QueryRowsRequest(BaseModel):
    """Request for querying rows"""

    dataset_id: str
    query_text: str | None = None
    limit: int = Field(default=20, ge=1, le=500)


class QueryRowsResponse(BaseModel):
    """Response for row queries"""

    success: bool
    rows: list[dict] = Field(default_factory=list)
    count: int = 0
    error: str | None = None


class ExamQuestionsRequest(BaseModel):
    """Request for Taiwan national exam question search"""

    query: str = Field(..., min_length=1)
    stem_contains: str | None = None
    exam_name_contains: str | None = None
    subject_contains: str | None = None
    question_type: str | None = None
    year_from: int | None = Field(default=None, ge=2012, le=2026)
    year_to: int | None = Field(default=None, ge=2012, le=2026)
    limit: int = Field(default=12, ge=1, le=50)


class ExamQuestionsResponse(BaseModel):
    """Response for Taiwan national exam question search"""

    success: bool
    n_corpus: int | None = None
    n_returned: int | None = None
    query: str | None = None
    hits: list[dict] = Field(default_factory=list)
    count: int = 0
    error: str | None = None


class HealthCheckResponse(BaseModel):
    """Response for health check"""

    success: bool
    status: str
    endpoint: str
    error: str | None = None


# ============================================================
# Route Handlers
# ============================================================


@router.get(
    "/domains",
    response_model=ListDomainsResponse,
    summary="List all available data domains",
    tags=["MCP - Data Query"],
)
async def list_domains(
    mcp_client: TwinkleMCPClient = Depends(get_mcp_client),
) -> ListDomainsResponse:
    """
    Retrieve all available data domains from Twinkle Hub

    Returns:
        List of domains with metadata (cached for 1 hour)
    """
    logger.info("Listing domains from Twinkle Hub")
    result = await mcp_client.list_domains()
    if not result.get("success"):
        raise HTTPException(
            status_code=503,
            detail=f"Failed to list domains: {result.get('error', 'Unknown error')}",
        )
    return ListDomainsResponse(**result)


@router.post(
    "/search",
    response_model=SearchDatasetsResponse,
    summary="Search datasets by domain and keyword",
    tags=["MCP - Data Query"],
)
async def search_datasets(
    request: SearchDatasetsRequest,
    mcp_client: TwinkleMCPClient = Depends(get_mcp_client),
) -> SearchDatasetsResponse:
    """
    Search for datasets in Twinkle Hub

    Args:
        request: Search parameters (domain, keyword, limit)

    Returns:
        List of matching datasets
    """
    logger.info(
        f"Searching datasets: domain={request.domain}, keyword={request.keyword}"
    )
    result = await mcp_client.search_datasets(
        domain=request.domain,
        keyword=request.keyword,
        limit=request.limit,
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=503,
            detail=f"Failed to search datasets: {result.get('error', 'Unknown error')}",
        )
    return SearchDatasetsResponse(**result)


@router.post(
    "/query",
    response_model=QueryRowsResponse,
    summary="Query rows from a dataset",
    tags=["MCP - Data Query"],
)
async def query_rows(
    request: QueryRowsRequest,
    mcp_client: TwinkleMCPClient = Depends(get_mcp_client),
) -> QueryRowsResponse:
    """
    Query rows from a specific dataset

    Args:
        request: Query parameters (dataset_id, query_text, limit)

    Returns:
        List of matching rows
    """
    logger.info(
        f"Querying dataset {request.dataset_id}: query={request.query_text}, limit={request.limit}"
    )
    result = await mcp_client.query_rows(
        dataset_id=request.dataset_id,
        query_text=request.query_text,
        limit=request.limit,
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=503,
            detail=f"Failed to query rows: {result.get('error', 'Unknown error')}",
        )
    return QueryRowsResponse(**result)


@router.post(
    "/exam/questions",
    response_model=ExamQuestionsResponse,
    summary="Search Taiwan national exam questions",
    tags=["MCP - National Exam Bank"],
)
async def search_exam_questions(
    request: ExamQuestionsRequest,
    mcp_client: TwinkleMCPClient = Depends(get_mcp_client),
) -> ExamQuestionsResponse:
    """
    Search Taiwan national exam questions through Twinkle Hub.

    The endpoint keeps Twinkle Hub credentials on the server side and returns
    question-level semantic search hits from the 2012-2025 national exam corpus.
    """
    logger.info(
        "Searching exam questions: query=%s, subject=%s, exam=%s",
        request.query,
        request.subject_contains,
        request.exam_name_contains,
    )
    try:
        result = await mcp_client.search_exam_questions(
            query=request.query.strip(),
            stem_contains=request.stem_contains,
            exam_name_contains=request.exam_name_contains,
            subject_contains=request.subject_contains,
            question_type=request.question_type,
            year_from=request.year_from,
            year_to=request.year_to,
            limit=request.limit,
        )
    except Exception as exc:
        logger.exception("Failed to search exam questions")
        raise HTTPException(
            status_code=503,
            detail=f"Failed to search exam questions: {exc}",
        ) from exc

    return ExamQuestionsResponse(**result)


@router.get(
    "/tools",
    summary="List all MCP tools",
    tags=["MCP - Data Query"],
)
async def list_tools(
    mcp_client: TwinkleMCPClient = Depends(get_mcp_client),
) -> dict:
    """
    Retrieve all available MCP tools from Twinkle Hub

    Returns:
        List of tools with metadata (cached for 24 hours)
    """
    logger.info("Listing MCP tools from Twinkle Hub")
    result = await mcp_client.list_tools()
    if not result.get("success"):
        raise HTTPException(
            status_code=503,
            detail=f"Failed to list tools: {result.get('error', 'Unknown error')}",
        )
    return result


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Check MCP endpoint health",
    tags=["MCP - Data Query"],
)
async def health_check(
    mcp_client: TwinkleMCPClient = Depends(get_mcp_client),
) -> HealthCheckResponse:
    """
    Check if MCP endpoint is reachable and healthy

    Returns:
        Health status information
    """
    logger.info("Checking MCP endpoint health")
    result = await mcp_client.health_check()
    return HealthCheckResponse(**result)

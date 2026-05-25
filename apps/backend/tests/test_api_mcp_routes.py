from app.api import mcp
from fastapi import FastAPI
from fastapi.testclient import TestClient


class FakeMCPClient:
    async def list_domains(self):
        return {
            "success": True,
            "domains": [{"key": "economy_business", "name_zh": "經濟與商業"}],
            "cached": False,
        }

    async def search_datasets(self, domain=None, keyword=None, limit=10):
        return {
            "success": True,
            "results": [
                {
                    "id": "dataset-1",
                    "domain": domain,
                    "keyword": keyword,
                }
            ],
            "count": 1,
        }

    async def query_rows(self, dataset_id, query_text=None, limit=20):
        return {
            "success": True,
            "rows": [
                {
                    "dataset_id": dataset_id,
                    "query_text": query_text,
                    "limit": limit,
                }
            ],
            "count": 1,
        }

    async def search_exam_questions(
        self,
        query,
        stem_contains=None,
        exam_name_contains=None,
        subject_contains=None,
        question_type=None,
        year_from=None,
        year_to=None,
        limit=12,
    ):
        return {
            "success": True,
            "n_corpus": 320663,
            "n_returned": 1,
            "query": query,
            "hits": [
                {
                    "paper_id": "108_108070_703_08",
                    "subject_name": subject_contains or "電力系統",
                    "question_type": question_type or "申論題",
                }
            ],
            "count": 1,
        }

    async def list_tools(self):
        return {
            "success": True,
            "tools": [{"name": "search-datasets"}],
            "cached": False,
        }

    async def health_check(self):
        return {
            "success": True,
            "status": "healthy",
            "endpoint": "https://example.test/mcp/",
        }


class FailingMCPClient(FakeMCPClient):
    async def list_domains(self):
        return {
            "success": False,
            "error": "service unavailable",
            "domains": [],
        }


def make_client(fake_client=None):
    app = FastAPI()
    app.include_router(mcp.router, prefix="/api/mcp")
    app.dependency_overrides[mcp.get_mcp_client] = lambda: fake_client or FakeMCPClient()
    return TestClient(app)


def test_domains_route_returns_domain_list():
    client = make_client()

    response = client.get("/api/mcp/domains")

    assert response.status_code == 200
    assert response.json()["domains"][0]["key"] == "economy_business"


def test_search_route_passes_request_to_mcp_client():
    client = make_client()

    response = client.post(
        "/api/mcp/search",
        json={"domain": "economy_business", "keyword": "公司", "limit": 5},
    )

    assert response.status_code == 200
    assert response.json()["results"][0] == {
        "id": "dataset-1",
        "domain": "economy_business",
        "keyword": "公司",
    }


def test_query_route_passes_request_to_mcp_client():
    client = make_client()

    response = client.post(
        "/api/mcp/query",
        json={"dataset_id": "dataset-1", "query_text": "WEDO", "limit": 3},
    )

    assert response.status_code == 200
    assert response.json()["rows"][0] == {
        "dataset_id": "dataset-1",
        "query_text": "WEDO",
        "limit": 3,
    }


def test_exam_questions_route_passes_request_to_mcp_client():
    client = make_client()

    response = client.post(
        "/api/mcp/exam/questions",
        json={
            "query": "三相電路 有效功率",
            "subject_contains": "電力系統",
            "question_type": "申論題",
            "limit": 3,
        },
    )

    assert response.status_code == 200
    assert response.json()["n_corpus"] == 320663
    assert response.json()["hits"][0]["subject_name"] == "電力系統"


def test_tools_route_returns_tool_list():
    client = make_client()

    response = client.get("/api/mcp/tools")

    assert response.status_code == 200
    assert response.json()["tools"] == [{"name": "search-datasets"}]


def test_health_route_returns_mcp_status():
    client = make_client()

    response = client.get("/api/mcp/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_domains_route_returns_503_when_mcp_fails():
    client = make_client(FailingMCPClient())

    response = client.get("/api/mcp/domains")

    assert response.status_code == 503
    assert "service unavailable" in response.json()["detail"]


def test_search_route_validates_limit_bounds():
    client = make_client()

    response = client.post("/api/mcp/search", json={"limit": 101})

    assert response.status_code == 422

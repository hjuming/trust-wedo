import asyncio
import json as jsonlib
from datetime import datetime, timedelta

from app.core.mcp_integration import TwinkleMCPClient


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code

    def json(self):
        return self.payload

    @property
    def text(self):
        return jsonlib.dumps(self.payload)

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeAsyncClient:
    def __init__(self):
        self.posts = []
        self.gets = []
        self.closed = False

    async def post(self, path, json, headers=None):
        self.posts.append((path, json))
        if json.get("method") == "initialize":
            return FakeResponse({"result": {}})
        if json.get("method") == "tools/call":
            tool = json["params"]["name"]
            if tool == "opendata-search_exam_questions":
                exam_payload = {
                    "n_corpus": 320663,
                    "n_returned": 1,
                    "query": "三相電路",
                    "hits": [{"paper_id": "108_108070_703_08"}],
                }
                return FakeResponse(
                    {
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": jsonlib.dumps(
                                        exam_payload,
                                        ensure_ascii=False,
                                    ),
                                }
                            ]
                        }
                    }
                )

        tool = json["tool"]
        payloads = {
            "list-domains": {
                "result": [
                    {
                        "key": "economy_business",
                        "name_zh": "經濟與商業",
                    }
                ]
            },
            "list-tools": {
                "result": [
                    {
                        "name": "search-datasets",
                        "description": "搜尋資料集",
                    }
                ]
            },
            "search-datasets": {
                "result": [
                    {
                        "id": "dataset-1",
                        "title": "公司登記資料",
                    }
                ]
            },
            "query-rows": {
                "result": [
                    {
                        "company_name": "WEDO",
                    }
                ]
            },
        }
        return FakeResponse(payloads[tool])

    async def get(self, path, timeout):
        self.gets.append((path, timeout))
        return FakeResponse({}, status_code=200)

    async def aclose(self):
        self.closed = True


class ErrorPostClient(FakeAsyncClient):
    async def post(self, path, json):
        self.posts.append((path, json))
        return FakeResponse({"error": "upstream failed"}, status_code=500)


class ErrorGetClient(FakeAsyncClient):
    async def get(self, path, timeout):
        self.gets.append((path, timeout))
        raise RuntimeError("network down")


def make_client():
    client = TwinkleMCPClient(api_endpoint="https://example.test/mcp/")
    fake_http = FakeAsyncClient()
    client.client = fake_http
    return client, fake_http


def test_list_domains_returns_normalized_cached_response():
    client, fake_http = make_client()

    first = asyncio.run(client.list_domains())
    second = asyncio.run(client.list_domains())

    assert first["success"] is True
    assert first["domains"][0]["key"] == "economy_business"
    assert first["cached"] is False
    assert second["success"] is True
    assert second["domains"] == first["domains"]
    assert second["cached"] is True
    assert len(fake_http.posts) == 1


def test_list_tools_returns_normalized_cached_response():
    client, fake_http = make_client()

    first = asyncio.run(client.list_tools())
    second = asyncio.run(client.list_tools())

    assert first["success"] is True
    assert first["tools"][0]["name"] == "search-datasets"
    assert first["cached"] is False
    assert second["success"] is True
    assert second["tools"] == first["tools"]
    assert second["cached"] is True
    assert len(fake_http.posts) == 1


def test_search_datasets_sends_expected_payload():
    client, fake_http = make_client()

    result = asyncio.run(
        client.search_datasets(domain="economy_business", keyword="公司", limit=5)
    )

    assert result["success"] is True
    assert result["count"] == 1
    assert fake_http.posts[0] == (
        "invoke",
        {
            "tool": "search-datasets",
            "input": {
                "domain": "economy_business",
                "query": "公司",
                "limit": 5,
            },
        },
    )


def test_query_rows_sends_expected_payload():
    client, fake_http = make_client()

    result = asyncio.run(
        client.query_rows(dataset_id="dataset-1", query_text="WEDO", limit=3)
    )

    assert result["success"] is True
    assert result["rows"] == [{"company_name": "WEDO"}]
    assert fake_http.posts[0] == (
        "invoke",
        {
            "tool": "query-rows",
            "input": {
                "dataset_id": "dataset-1",
                "limit": 3,
                "query": "WEDO",
            },
        },
    )


def test_search_exam_questions_calls_json_rpc_tool():
    client, fake_http = make_client()
    client.api_key = "test-token"

    result = asyncio.run(
        client.search_exam_questions(
            query="三相電路",
            subject_contains="電力系統",
            limit=3,
        )
    )

    assert result["success"] is True
    assert result["n_corpus"] == 320663
    assert result["hits"][0]["paper_id"] == "108_108070_703_08"
    assert fake_http.posts[0][1]["method"] == "initialize"
    assert fake_http.posts[1][1]["params"]["name"] == "opendata-search_exam_questions"
    assert fake_http.posts[1][1]["params"]["arguments"]["subject_contains"] == "電力系統"


def test_health_check_reports_healthy_endpoint():
    client, fake_http = make_client()

    result = asyncio.run(client.health_check())

    assert result == {
        "success": True,
        "status": "healthy",
        "endpoint": "https://example.test/mcp/",
    }
    assert fake_http.gets == [("health", 5.0)]


def test_list_domains_returns_error_response_when_upstream_fails():
    client = TwinkleMCPClient(api_endpoint="https://example.test/mcp/")
    client.client = ErrorPostClient()

    result = asyncio.run(client.list_domains())

    assert result["success"] is False
    assert result["domains"] == []
    assert "HTTP 500" in result["error"]


def test_search_datasets_returns_error_response_when_upstream_fails():
    client = TwinkleMCPClient(api_endpoint="https://example.test/mcp/")
    client.client = ErrorPostClient()

    result = asyncio.run(client.search_datasets(keyword="公司"))

    assert result["success"] is False
    assert result["results"] == []
    assert result["count"] == 0
    assert "HTTP 500" in result["error"]


def test_query_rows_returns_error_response_when_upstream_fails():
    client = TwinkleMCPClient(api_endpoint="https://example.test/mcp/")
    client.client = ErrorPostClient()

    result = asyncio.run(client.query_rows(dataset_id="dataset-1"))

    assert result["success"] is False
    assert result["rows"] == []
    assert result["count"] == 0
    assert "HTTP 500" in result["error"]


def test_list_tools_returns_error_response_when_upstream_fails():
    client = TwinkleMCPClient(api_endpoint="https://example.test/mcp/")
    client.client = ErrorPostClient()

    result = asyncio.run(client.list_tools())

    assert result["success"] is False
    assert result["tools"] == []
    assert "HTTP 500" in result["error"]


def test_health_check_reports_unreachable_endpoint():
    client = TwinkleMCPClient(api_endpoint="https://example.test/mcp/")
    client.client = ErrorGetClient()

    result = asyncio.run(client.health_check())

    assert result["success"] is False
    assert result["status"] == "unreachable"
    assert result["endpoint"] == "https://example.test/mcp/"
    assert result["error"] == "network down"


def test_expired_cache_entry_is_removed():
    client, _ = make_client()
    client._cache["domains"] = (
        {"success": True},
        datetime.now() - timedelta(seconds=1),
    )

    result = asyncio.run(client._get_cached("domains"))

    assert result is None
    assert "domains" not in client._cache


def test_close_closes_underlying_http_client():
    client, fake_http = make_client()

    asyncio.run(client.close())

    assert fake_http.closed is True

"""
MCP Integration Layer - Twinkle Hub Client
Connects to Twinkle Hub MCP endpoint for data queries
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class TwinkleMCPClient:
    """
    Client for Twinkle Hub MCP API
    Handles connections and queries to external MCP endpoint
    """

    def __init__(self, api_endpoint: str = "https://api.twinkleai.tw/mcp/"):
        self.api_endpoint = (
            os.getenv("TWINKLE_HUB_API_ENDPOINT", api_endpoint).rstrip("/") + "/"
        )
        self.api_key = os.getenv("TWINKLE_HUB_API_KEY") or os.getenv(
            "TWINKLE_HUB_TOKEN", ""
        )
        self.client = httpx.AsyncClient(
            base_url=self.api_endpoint,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
        self._cache: dict[str, tuple[Any, datetime]] = {}
        self._cache_ttl = {
            "domains": 3600,  # 1 hour
            "tools": 86400,  # 24 hours
        }
        self._request_id = 0

    async def _get_cached(self, key: str) -> Any | None:
        """Check if cached data is still valid"""
        if key in self._cache:
            data, expiry = self._cache[key]
            if datetime.now() < expiry:
                logger.info(f"Cache hit for key: {key}")
                return data
            else:
                del self._cache[key]
        return None

    async def _set_cache(self, key: str, data: Any, ttl: int) -> None:
        """Store data in cache"""
        expiry = datetime.now() + timedelta(seconds=ttl)
        self._cache[key] = (data, expiry)

    def _next_request_id(self) -> int:
        self._request_id += 1
        return self._request_id

    @staticmethod
    def _parse_mcp_response_text(body: str) -> dict[str, Any]:
        """Parse plain JSON or SSE-style MCP JSON-RPC response."""
        data_lines = [
            line.strip()[5:].strip()
            for line in body.splitlines()
            if line.strip().startswith("data:")
        ]
        payload = data_lines[-1] if data_lines else body
        return json.loads(payload)

    async def _send_json_rpc(
        self, method: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("TWINKLE_HUB_API_KEY is not configured")

        body: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": self._next_request_id(),
            "method": method,
        }
        if params is not None:
            body["params"] = params

        response = await self.client.post(
            "",
            headers={"Accept": "application/json, text/event-stream"},
            json=body,
        )
        response.raise_for_status()
        payload = self._parse_mcp_response_text(response.text)
        if payload.get("error"):
            raise RuntimeError(payload["error"].get("message", "MCP request failed"))
        return payload.get("result", {})

    async def _initialize_json_rpc(self) -> None:
        await self._send_json_rpc(
            "initialize",
            {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {
                    "name": "trust-wedo-backend",
                    "version": "1.0.0",
                },
            },
        )

    async def call_tool(self, name: str, args: dict[str, Any]) -> Any:
        """Call a Twinkle Hub MCP tool through Streamable HTTP JSON-RPC."""
        await self._initialize_json_rpc()
        result = await self._send_json_rpc(
            "tools/call",
            {
                "name": name,
                "arguments": args,
            },
        )
        content = result.get("content", [])
        text = "\n".join(
            item.get("text", "")
            for item in content
            if item.get("type") == "text" and item.get("text")
        )
        return json.loads(text) if text else {}

    async def search_exam_questions(
        self,
        query: str,
        stem_contains: str | None = None,
        exam_name_contains: str | None = None,
        subject_contains: str | None = None,
        question_type: str | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        limit: int = 12,
    ) -> dict[str, Any]:
        """Search Taiwan national exam questions from Twinkle Hub."""
        args: dict[str, Any] = {"query": query, "limit": limit}
        if stem_contains:
            args["stem_contains"] = stem_contains
        if exam_name_contains:
            args["exam_name_contains"] = exam_name_contains
        if subject_contains:
            args["subject_contains"] = subject_contains
        if question_type:
            args["question_type"] = question_type
        if year_from is not None:
            args["year_from"] = year_from
        if year_to is not None:
            args["year_to"] = year_to

        payload = await self.call_tool("opendata-search_exam_questions", args)
        hits = payload.get("hits", []) if isinstance(payload, dict) else []
        return {
            "success": True,
            **(payload if isinstance(payload, dict) else {"data": payload}),
            "count": len(hits),
        }

    async def list_domains(self) -> dict[str, Any]:
        """
        List all available data domains from Twinkle Hub

        Returns:
            Dict with 'success' and 'domains' list
        """
        try:
            # Check cache first
            cached = await self._get_cached("domains")
            if cached:
                return {**cached, "cached": True}

            response = await self.client.post(
                "invoke",
                json={
                    "tool": "list-domains",
                    "input": {},
                },
            )
            response.raise_for_status()
            data = response.json()

            result = {
                "success": True,
                "domains": data.get("result", []),
                "cached": False,
            }

            # Cache result
            await self._set_cache(
                "domains", result, self._cache_ttl.get("domains", 3600)
            )

            return result
        except Exception as e:
            logger.error(f"Error listing domains: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "domains": [],
            }

    async def search_datasets(
        self, domain: str | None = None, keyword: str | None = None, limit: int = 10
    ) -> dict[str, Any]:
        """
        Search datasets from Twinkle Hub

        Args:
            domain: Data domain (e.g., 'economy_business')
            keyword: Search keyword
            limit: Number of results

        Returns:
            Dict with 'success' and 'results' list
        """
        try:
            input_data = {}
            if domain:
                input_data["domain"] = domain
            if keyword:
                input_data["query"] = keyword
            input_data["limit"] = limit

            response = await self.client.post(
                "invoke",
                json={
                    "tool": "search-datasets",
                    "input": input_data,
                },
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "results": data.get("result", []),
                "count": len(data.get("result", [])),
            }
        except Exception as e:
            logger.error(f"Error searching datasets: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "count": 0,
            }

    async def query_rows(
        self,
        dataset_id: str,
        query_text: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """
        Query rows from a specific dataset

        Args:
            dataset_id: Dataset ID
            query_text: Filter/search text
            limit: Number of rows

        Returns:
            Dict with 'success' and 'rows' list
        """
        try:
            input_data = {
                "dataset_id": dataset_id,
                "limit": limit,
            }
            if query_text:
                input_data["query"] = query_text

            response = await self.client.post(
                "invoke",
                json={
                    "tool": "query-rows",
                    "input": input_data,
                },
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "rows": data.get("result", []),
                "count": len(data.get("result", [])),
            }
        except Exception as e:
            logger.error(f"Error querying rows: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "rows": [],
                "count": 0,
            }

    async def list_tools(self) -> dict[str, Any]:
        """
        List all available MCP tools

        Returns:
            Dict with 'success' and 'tools' list
        """
        try:
            # Check cache first
            cached = await self._get_cached("tools")
            if cached:
                return {**cached, "cached": True}

            response = await self.client.post(
                "invoke",
                json={
                    "tool": "list-tools",
                    "input": {},
                },
            )
            response.raise_for_status()
            data = response.json()

            result = {
                "success": True,
                "tools": data.get("result", []),
                "cached": False,
            }

            # Cache result
            await self._set_cache("tools", result, self._cache_ttl.get("tools", 86400))

            return result
        except Exception as e:
            logger.error(f"Error listing tools: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "tools": [],
            }

    async def health_check(self) -> dict[str, Any]:
        """
        Check MCP endpoint health

        Returns:
            Dict with health status
        """
        try:
            response = await self.client.get("health", timeout=5.0)
            return {
                "success": response.status_code == 200,
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "endpoint": self.api_endpoint,
            }
        except Exception as e:
            logger.warning(f"MCP health check failed: {str(e)}")
            return {
                "success": False,
                "status": "unreachable",
                "endpoint": self.api_endpoint,
                "error": str(e),
            }

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global MCP client instance
_mcp_client: TwinkleMCPClient | None = None


async def get_mcp_client() -> TwinkleMCPClient:
    """Get or create MCP client instance"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = TwinkleMCPClient()
    return _mcp_client

from app.api import research
from fastapi import FastAPI
from fastapi.testclient import TestClient


def make_client():
    app = FastAPI()
    app.include_router(research.router, prefix="/api/research")
    return TestClient(app)


def test_modules_route_returns_all_seed_modules():
    client = make_client()

    response = client.get("/api/research/modules")

    assert response.status_code == 200
    modules = response.json()
    assert len(modules) == 12
    assert modules[0]["id"] == "ai-productivity"


def test_get_module_route_returns_matching_module():
    client = make_client()

    response = client.get("/api/research/modules/ethical-ai")

    assert response.status_code == 200
    assert response.json()["title"] == "倫理 AI 採用指南"


def test_get_module_route_returns_404_for_unknown_module():
    client = make_client()

    response = client.get("/api/research/modules/unknown-module")

    assert response.status_code == 404
    assert response.json()["detail"] == "Module not found: unknown-module"


def test_create_study_path_preserves_requested_module_order():
    client = make_client()

    response = client.post(
        "/api/research/path",
        json={
            "module_ids": ["ethical-ai", "ai-productivity"],
            "title": "AI 治理與生產力路徑",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["title"] == "AI 治理與生產力路徑"
    assert [module["id"] for module in body["modules"]] == [
        "ethical-ai",
        "ai-productivity",
    ]
    assert len(body["aio_insights"]) == 2


def test_create_study_path_rejects_empty_selection():
    client = make_client()

    response = client.post("/api/research/path", json={"module_ids": []})

    assert response.status_code == 400
    assert response.json()["detail"] == "At least one module must be selected"


def test_create_study_path_rejects_unknown_module():
    client = make_client()

    response = client.post(
        "/api/research/path",
        json={"module_ids": ["ai-productivity", "unknown-module"]},
    )

    assert response.status_code == 400
    assert "unknown-module" in response.json()["detail"]

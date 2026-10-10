"""
Tests de app/api/flask_app.py (Fase 7).

Usa el test client de Flask (no levanta un servidor real).
"""

import pytest

from app.api.flask_app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_index_returns_summary(client):
    r = client.get("/")
    assert r.status_code == 200
    data = r.get_json()
    assert data["total_commands"] == 236
    assert data["total_categories"] == 16


def test_list_categories_returns_16(client):
    r = client.get("/categories")
    assert r.status_code == 200
    assert len(r.get_json()) == 16


def test_get_category_known(client):
    r = client.get("/categories/docker")
    assert r.status_code == 200
    data = r.get_json()
    assert data["id"] == "docker"
    assert len(data["commands"]) == 23


def test_get_category_unknown_returns_404(client):
    r = client.get("/categories/categoria_fantasma")
    assert r.status_code == 404
    assert r.get_json()["error"] == "category_not_found"


def test_list_commands_returns_all_by_default(client):
    r = client.get("/commands")
    assert r.status_code == 200
    assert len(r.get_json()) == 236


def test_list_commands_filters_by_category(client):
    r = client.get("/commands?category=docker")
    data = r.get_json()
    assert len(data) == 23
    assert all(c["category"] == "docker" for c in data)


def test_list_commands_filters_by_tag(client):
    r = client.get("/commands?tag=maintenance")
    data = r.get_json()
    assert len(data) > 0
    assert all("maintenance" in c["tags"] for c in data)


def test_list_commands_combined_filters(client):
    r = client.get("/commands?category=docker&tag=maintenance")
    data = r.get_json()
    ids = sorted(c["id"] for c in data)
    assert ids == ["compose-down", "docker-rm", "docker-rmi", "docker-system-prune"]


def test_get_command_known(client):
    r = client.get("/commands/rm")
    assert r.status_code == 200
    data = r.get_json()
    assert data["id"] == "rm"
    assert data["risk"] == "Peligroso"
    assert data["precautions"] != ""


def test_get_command_unknown_returns_404(client):
    r = client.get("/commands/comando_fantasma")
    assert r.status_code == 404
    assert r.get_json()["error"] == "command_not_found"


def test_get_command_with_lang_en_translates(client):
    r = client.get("/commands/cd?lang=en")
    data = r.get_json()
    assert data["description"] == "Changes the current working directory."


def test_get_command_with_lang_en_falls_back_for_untranslated(client):
    r_es = client.get("/commands/ping")
    r_en = client.get("/commands/ping?lang=en")
    assert r_es.get_json()["description"] == r_en.get_json()["description"]


def test_search_requires_query(client):
    r = client.get("/search")
    assert r.status_code == 400
    assert r.get_json()["error"] == "missing_query"


def test_search_returns_ranked_results(client):
    r = client.get("/search?q=grep")
    assert r.status_code == 200
    data = r.get_json()
    assert data[0]["id"] == "grep"
    assert data[0]["score"] == 100


def test_get_tag_known(client):
    r = client.get("/tags/docker")
    assert r.status_code == 200
    data = r.get_json()
    assert len(data["commands"]) == 23


def test_get_tag_unknown_returns_404(client):
    r = client.get("/tags/tag_fantasma")
    assert r.status_code == 404
    assert r.get_json()["error"] == "tag_not_found"


def test_404_handler_returns_json_not_html(client):
    r = client.get("/ruta/que/no/existe")
    assert r.status_code == 404
    assert r.content_type == "application/json"

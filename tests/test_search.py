"""
Tests de app/core/search.py (Fase 7).
"""

from app.core.search import (
    autocomplete,
    get_command,
    list_by_category,
    related_commands,
    search,
    search_by_tag,
)


def test_search_exact_id_scores_highest():
    results = search("grep")
    assert results[0].command.id == "grep"
    assert results[0].score == 100


def test_search_is_case_insensitive():
    lower = search("docker")
    upper = search("DOCKER")
    assert [r.command.id for r in lower] == [r.command.id for r in upper]


def test_search_empty_query_returns_empty():
    assert search("") == []
    assert search("   ") == []


def test_search_nonexistent_term_returns_empty():
    assert search("zzz_no_deberia_existir_zzz") == []


def test_search_respects_limit():
    results = search("d", limit=3)
    assert len(results) <= 3


def test_search_finds_by_description_content():
    # "permisos" no es el nombre de ningún comando, pero aparece en varias
    # descripciones (chmod, umask, etc.)
    results = search("permisos")
    assert len(results) > 0


def test_search_by_tag_returns_only_matching_commands():
    results = search_by_tag("docker")
    assert len(results) > 0
    assert all("docker" in c.tags for c in results)


def test_search_by_tag_unknown_tag_returns_empty():
    assert search_by_tag("tag_que_no_existe") == []


def test_get_command_returns_none_for_unknown_id():
    assert get_command("comando_que_no_existe") is None


def test_get_command_returns_command_for_known_id():
    cmd = get_command("rm")
    assert cmd is not None
    assert cmd.id == "rm"


def test_get_command_is_case_insensitive():
    assert get_command("RM") is not None
    assert get_command("RM").id == "rm"


def test_list_by_category_filters_correctly():
    commands = list_by_category("docker")
    assert len(commands) > 0
    assert all(c.category == "docker" for c in commands)


def test_list_by_category_with_subcategory_filters_further():
    all_docker = list_by_category("docker")
    containers_only = list_by_category("docker", "containers")
    assert len(containers_only) < len(all_docker)
    assert all(c.subcategory == "containers" for c in containers_only)


def test_list_by_category_unknown_category_returns_empty():
    assert list_by_category("categoria_que_no_existe") == []


def test_autocomplete_returns_matching_prefixes():
    results = autocomplete("doc")
    assert len(results) > 0
    assert all(r.startswith("doc") for r in results)


def test_autocomplete_empty_prefix_returns_empty():
    assert autocomplete("") == []


def test_related_commands_resolves_to_full_objects():
    related = related_commands("rm")
    assert len(related) > 0
    # 'rm' está relacionado con 'rmdir' y 'mv' (ver app/data/commands/files.py)
    ids = [r.id for r in related]
    assert "rmdir" in ids


def test_related_commands_unknown_id_returns_empty():
    assert related_commands("comando_que_no_existe") == []

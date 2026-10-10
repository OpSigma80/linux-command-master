"""
Tests de app/core/navigation.py (Fase 7).
"""

from app.core.navigation import (
    get_all_categories,
    get_category,
    get_commands,
    get_subcategories,
)


def test_get_all_categories_returns_16():
    assert len(get_all_categories()) == 16


def test_get_category_known_id():
    cat = get_category("docker")
    assert cat is not None
    assert cat.id == "docker"


def test_get_category_unknown_id_returns_none():
    assert get_category("categoria_fantasma") is None


def test_get_subcategories_have_correct_counts():
    subs = get_subcategories("docker")
    assert len(subs) > 0
    for info in subs:
        expected = len(get_commands("docker", info.subcategory.id))
        assert info.command_count == expected


def test_get_subcategories_unknown_category_returns_empty():
    assert get_subcategories("categoria_fantasma") == []


def test_get_commands_without_subcategory_returns_all_in_category():
    all_cmds = get_commands("docker")
    assert len(all_cmds) == 23  # ver conteo confirmado en Fase 2


def test_maintenance_category_has_zero_direct_commands():
    """'maintenance' es intencionalmente una vista transversal (Fase 1),
    no debe tener comandos propios."""
    assert get_commands("maintenance") == []

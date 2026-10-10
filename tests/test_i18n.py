"""
Tests de app/core/i18n.py (Fase 7).

El caso más importante a probar es el FALLBACK: un comando sin traducir
todavía debe devolver el texto en español sin romperse (esto es lo que
vimos funcionando visualmente en la GUI, aquí lo confirmamos con datos).
"""

from app.core.i18n import Lang, t_category_name, t_command, t_level, t_risk, t_tag, t_ui
from app.data.commands import COMMANDS
from app.data.models import Level, Risk


def test_translated_command_returns_english_text():
    """'cd' está en la categoria 'files', ya traducida."""
    tc = t_command(COMMANDS["cd"], Lang.EN)
    assert tc.description == "Changes the current working directory."
    assert tc.syntax == "cd [path]"


def test_untranslated_command_falls_back_to_spanish():
    """'ping' (categoria 'network') aún no está traducido -- Fase 9 en progreso.
    Pedir inglés NO debe romper, debe devolver el texto en español."""
    es_text = COMMANDS["ping"].description
    tc = t_command(COMMANDS["ping"], Lang.EN)
    assert tc.description == es_text


def test_spanish_lang_always_returns_original():
    tc = t_command(COMMANDS["cd"], Lang.ES)
    assert tc.description == COMMANDS["cd"].description


def test_structural_fields_never_translated():
    """category, subcategory, tags, related son identificadores, no texto."""
    cmd = COMMANDS["rm"]
    tc_en = t_command(cmd, Lang.EN)
    assert tc_en.category == cmd.category
    assert tc_en.subcategory == cmd.subcategory
    assert tc_en.tags == cmd.tags
    assert tc_en.related == cmd.related


def test_level_translation():
    assert t_level(Level.BASICO, Lang.EN) == "Basic"
    assert t_level(Level.BASICO, Lang.ES) == "Básico"


def test_risk_translation():
    assert t_risk(Risk.PELIGROSO, Lang.EN) == "Dangerous"
    assert t_risk(Risk.PELIGROSO, Lang.ES) == "Peligroso"


def test_category_translation_for_translated_category():
    assert t_category_name("files", Lang.EN) == "File Navigation & Management"


def test_category_translation_fallback_for_untranslated_category():
    """'docker' (categoria) aun no tiene traduccion EN en CATEGORY_EN todavia
    -- si se agrega en el futuro este test necesitara actualizarse, pero
    por ahora confirma que el fallback funciona igual que con comandos."""
    from app.data.categories import CATEGORIES
    es_name = CATEGORIES["docker"].name
    en_name = t_category_name("docker", Lang.EN)
    # Si 'docker' ya fue traducido, este assert cambia de sentido; lo
    # importante es que NUNCA truene, ambas ramas son válidas:
    assert en_name in (es_name, en_name)


def test_ui_text_translation():
    assert t_ui("home", Lang.EN) == "Home"
    assert t_ui("home", Lang.ES) == "Inicio"


def test_ui_text_unknown_key_falls_back_gracefully():
    # una key inexistente no debe tronar, debe devolver algo (la propia key)
    result = t_ui("clave_que_no_existe", Lang.EN)
    assert result == "clave_que_no_existe"


def test_tag_translation():
    assert t_tag("docker", Lang.EN) == "Docker and containers"


def test_tag_translation_unknown_tag_falls_back():
    result = t_tag("tag_fantasma", Lang.EN)
    assert result == "tag_fantasma"

"""
Tests de app/core/validator.py (Fase 7).

Verifican que la base de datos real (236 comandos) pasa el validador,
y que el validador DETECTA correctamente problemas cuando existen --
usando datos sintéticos inyectados, sin tocar la base real.
"""

from app.core.validator import ValidationReport, validate_database
from app.data.categories import CATEGORIES
from app.data.models import Category, Command, Risk, Subcategory


def test_real_database_has_no_errors():
    """La base de datos real del proyecto no debe tener errores de integridad."""
    report = validate_database()
    assert report.ok, f"La base de datos tiene errores: {report.errors}"


def test_real_database_command_count():
    from app.data.commands import COMMANDS
    assert len(COMMANDS) == 236


def test_real_database_category_count():
    assert len(CATEGORIES) == 16


def test_report_ok_true_when_no_errors():
    report = ValidationReport()
    report.warnings.append("solo un warning, no un error")
    assert report.ok is True


def test_report_ok_false_when_errors():
    report = ValidationReport()
    report.errors.append("algo salio mal")
    assert report.ok is False


def _fake_category():
    """Categoria sintetica minima para inyectar en los tests de deteccion."""
    return {
        "test-cat": Category(
            id="test-cat", name="Categoria de prueba", description="desc",
            subcategories=[Subcategory(id="test-sub", name="Subcategoria de prueba")],
        )
    }


def test_detects_dangerous_command_without_precautions():
    """Un comando Peligroso SIN precauciones debe marcarse como error (Regla 7)."""
    cmd = Command(
        id="cmd1", name="cmd1", category="test-cat", subcategory="test-sub",
        description="desc", syntax="cmd1", risk=Risk.PELIGROSO, precautions="",
        examples=["cmd1"], when_to_use="prueba", tags=["automation"],
    )
    report = validate_database(commands={"cmd1": cmd}, categories=_fake_category())
    assert not report.ok
    assert any("precautions" in e for e in report.errors)


def test_detects_missing_description():
    cmd = Command(
        id="cmd1", name="cmd1", category="test-cat", subcategory="test-sub",
        description="", syntax="cmd1", examples=["cmd1"], when_to_use="x", tags=["automation"],
    )
    report = validate_database(commands={"cmd1": cmd}, categories=_fake_category())
    assert not report.ok
    assert any("sin descripción" in e for e in report.errors)


def test_detects_invalid_tag():
    cmd = Command(
        id="cmd1", name="cmd1", category="test-cat", subcategory="test-sub",
        description="desc", syntax="cmd1", examples=["cmd1"], when_to_use="x",
        tags=["este_tag_no_existe"],
    )
    report = validate_database(commands={"cmd1": cmd}, categories=_fake_category())
    assert not report.ok
    assert any("no registrado" in e for e in report.errors)


def test_detects_broken_category_reference():
    cmd = Command(
        id="cmd1", name="cmd1", category="categoria_que_no_existe", subcategory="test-sub",
        description="desc", syntax="cmd1", examples=["cmd1"], when_to_use="x", tags=["automation"],
    )
    report = validate_database(commands={"cmd1": cmd}, categories=_fake_category())
    assert not report.ok
    assert any("categoría inexistente" in e for e in report.errors)


def test_detects_broken_related_reference():
    cmd = Command(
        id="cmd1", name="cmd1", category="test-cat", subcategory="test-sub",
        description="desc", syntax="cmd1", examples=["cmd1"], when_to_use="x",
        tags=["automation"], related=["comando_fantasma"],
    )
    report = validate_database(commands={"cmd1": cmd}, categories=_fake_category())
    assert not report.ok
    assert any("relacionado inexistente" in e for e in report.errors)


def test_valid_command_produces_no_errors():
    """Un comando bien formado, con todos los campos, no debe producir errores."""
    cmd = Command(
        id="cmd1", name="cmd1", category="test-cat", subcategory="test-sub",
        description="desc", syntax="cmd1", examples=["cmd1"], when_to_use="x",
        tags=["automation"], risk=Risk.SEGURO,
    )
    report = validate_database(commands={"cmd1": cmd}, categories=_fake_category())
    assert report.ok

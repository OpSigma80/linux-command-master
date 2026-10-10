"""
Validador de la base de datos (sección 31 del brief).

validate_database() recorre COMMANDS y CATEGORIES y produce un reporte
con errores (bloqueantes: la app no debería arrancar con estos) y
warnings (no bloqueantes: calidad de datos mejorable).

Este módulo NO modifica datos, solo los audita. Se ejecuta:
  - manualmente: python -m app.core.validator
  - o al arrancar cualquier interfaz (CLI/Tkinter/Flask), que puede
    decidir advertir o abortar según el resultado.
"""

from dataclasses import dataclass, field

from app.data.categories import CATEGORIES
from app.data.commands import COMMANDS
from app.data.tags import is_valid_tag


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def summary(self) -> str:
        lines = [
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "  REPORTE DE VALIDACIÓN — Linux Command Master",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"Comandos analizados : {len(COMMANDS)}",
            f"Categorías analizadas: {len(CATEGORIES)}",
            f"Errores  : {len(self.errors)}",
            f"Warnings : {len(self.warnings)}",
            "",
        ]
        if self.errors:
            lines.append("🔴 ERRORES (bloqueantes):")
            lines += [f"  - {e}" for e in self.errors]
            lines.append("")
        if self.warnings:
            lines.append("🟡 WARNINGS (mejorables):")
            lines += [f"  - {w}" for w in self.warnings]
            lines.append("")
        if not self.errors and not self.warnings:
            lines.append("✅ Base de datos limpia, sin errores ni warnings.")
        return "\n".join(lines)


def validate_database(commands=None, categories=None) -> ValidationReport:
    """
    Valida la base de datos. Por defecto usa COMMANDS/CATEGORIES reales
    (así lo llaman CLI/GUI/API). Acepta datos inyectados para poder
    probar la lógica de detección con casos sintéticos en los tests,
    sin tocar ni depender de la base de datos real.
    """
    commands = COMMANDS if commands is None else commands
    categories = CATEGORIES if categories is None else categories
    report = ValidationReport()

    # 1) IDs de comando duplicados (ya se agregan en un dict, así que aquí
    #    detectamos colisiones silenciosas: si dos fichas comparten id,
    #    una sobreescribió a la otra al construir COMMANDS).
    seen_names: dict[str, list[str]] = {}
    for cmd_id, cmd in commands.items():
        seen_names.setdefault(cmd.name.lower(), []).append(cmd_id)
    for name, ids in seen_names.items():
        if len(ids) > 1:
            report.warnings.append(
                f"Nombre de comando repetido '{name}' en ids distintos: {ids} "
                f"(revisar si deberían fusionarse)"
            )

    # 2) Categorías duplicadas (mismo id o mismo nombre)
    cat_names: dict[str, list[str]] = {}
    for cat_id, cat in categories.items():
        cat_names.setdefault(cat.name.lower(), []).append(cat_id)
    for name, ids in cat_names.items():
        if len(ids) > 1:
            report.errors.append(f"Categoría duplicada '{name}': ids {ids}")

    # 3) Campos obligatorios por comando
    for cmd_id, cmd in commands.items():
        if not cmd.description or not cmd.description.strip():
            report.errors.append(f"[{cmd_id}] sin descripción")
        if not cmd.syntax or not cmd.syntax.strip():
            report.errors.append(f"[{cmd_id}] sin sintaxis")
        if not cmd.examples:
            report.warnings.append(f"[{cmd_id}] sin ejemplos")
        if not cmd.when_to_use or not cmd.when_to_use.strip():
            report.warnings.append(f"[{cmd_id}] sin 'cuándo usarlo'")
        if not cmd.tags:
            report.warnings.append(f"[{cmd_id}] sin tags (no será encontrado por búsqueda por tag)")

        # 4) Riesgo != Seguro debe traer precauciones (Regla 7/29)
        if cmd.risk.name != "SEGURO" and not cmd.precautions.strip():
            report.errors.append(
                f"[{cmd_id}] marcado como {cmd.risk.value} pero sin campo 'precautions'"
            )

        # 5) Tags inexistentes en el registro canónico
        for tag in cmd.tags:
            if not is_valid_tag(tag):
                report.errors.append(f"[{cmd_id}] usa tag no registrado: '{tag}'")

        # 6) category/subcategory deben existir en categories
        cat = categories.get(cmd.category)
        if cat is None:
            report.errors.append(f"[{cmd_id}] apunta a categoría inexistente: '{cmd.category}'")
        else:
            sub_ids = {s.id for s in cat.subcategories}
            if cmd.subcategory not in sub_ids:
                report.errors.append(
                    f"[{cmd_id}] apunta a subcategoría inexistente "
                    f"'{cmd.subcategory}' dentro de '{cmd.category}'"
                )

        # 7) Referencias 'related' deben apuntar a ids existentes
        for rel_id in cmd.related:
            if rel_id not in commands:
                report.errors.append(
                    f"[{cmd_id}] referencia comando relacionado inexistente: '{rel_id}'"
                )

        # 8) replaces/replaced_by deben apuntar a ids existentes si están definidos
        if cmd.replaces and cmd.replaces not in commands:
            report.warnings.append(
                f"[{cmd_id}] 'replaces' apunta a id inexistente '{cmd.replaces}' "
                f"(puede ser un comando aún no catalogado, ej: ifconfig/netstat)"
            )
        if cmd.replaced_by and cmd.replaced_by not in commands:
            report.errors.append(
                f"[{cmd_id}] 'replaced_by' apunta a id inexistente '{cmd.replaced_by}'"
            )

    # 9) Categorías o subcategorías vacías (sin ningún comando apuntando a ellas)
    used_categories = {c.category for c in commands.values()}
    used_subcats = {(c.category, c.subcategory) for c in commands.values()}

    for cat_id, cat in categories.items():
        if cat_id not in used_categories and cat_id != "maintenance":
            # 'maintenance' es intencionalmente una vista transversal (Fase 1)
            report.warnings.append(f"Categoría '{cat_id}' no tiene ningún comando asignado")
        for sub in cat.subcategories:
            if (cat_id, sub.id) not in used_subcats and cat_id != "maintenance":
                report.warnings.append(
                    f"Subcategoría '{sub.id}' de '{cat_id}' está vacía"
                )

    return report


if __name__ == "__main__":
    print(validate_database().summary())

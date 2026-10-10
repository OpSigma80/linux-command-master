"""
API Flask (Fase 6, sección 33 del brief).

Reusa EXCLUSIVAMENTE app/core (search.py, navigation.py, i18n.py) para
datos y lógica -- cero reglas de negocio propias aquí, igual que CLI y
GUI (Regla 34: DATA -> SERVICES -> INTERFACES).

Endpoints:
    GET /categories
    GET /categories/<category>
    GET /commands
    GET /commands/<command>
    GET /search?q=<query>
    GET /tags/<tag>

Todos aceptan ?lang=es|en (por defecto es). Si un comando no tiene
traducción todavía, cae automáticamente a español (ver app/core/i18n.py).
"""

from flask import Flask, jsonify, request

from app.core import navigation, search
from app.core.i18n import Lang, t_category_description, t_category_name, t_command, t_subcategory_name, t_tag
from app.data.categories import CATEGORIES
from app.data.commands import COMMANDS
from app.data.tags import TAGS


def _get_lang() -> Lang:
    """Lee ?lang=en|es de la query string; por defecto español."""
    raw = request.args.get("lang", "es").strip().lower()
    return Lang.EN if raw == "en" else Lang.ES


def _serialize_command(cmd, lang: Lang) -> dict:
    tc = t_command(cmd, lang)
    return {
        "id": tc.id,
        "name": tc.name,
        "category": tc.category,
        "subcategory": tc.subcategory,
        "description": tc.description,
        "syntax": tc.syntax,
        "examples": tc.examples,
        "when_to_use": tc.when_to_use,
        "options": tc.options,
        "precautions": tc.precautions,
        "related": tc.related,
        "tags": tc.tags,
        "level": tc.level_label,
        "risk": tc.risk_label,
        "replaces": tc.replaces,
        "replaced_by": tc.replaced_by,
    }


def _serialize_category(cat_id: str, lang: Lang) -> dict:
    cat = CATEGORIES[cat_id]
    subs = navigation.get_subcategories(cat_id)
    return {
        "id": cat.id,
        "name": t_category_name(cat_id, lang),
        "description": t_category_description(cat_id, lang),
        "subcategories": [
            {
                "id": s.subcategory.id,
                "name": t_subcategory_name(cat_id, s.subcategory.id, lang),
                "command_count": s.command_count,
            }
            for s in subs
        ],
    }


def create_app() -> Flask:
    app = Flask(__name__)

    @app.errorhandler(404)
    def not_found(_e):
        return jsonify({"error": "not_found"}), 404

    @app.get("/")
    def index():
        return jsonify({
            "name": "Linux Command Master API",
            "endpoints": [
                "/categories", "/categories/<category>",
                "/commands", "/commands/<command>",
                "/search?q=<query>", "/tags/<tag>",
            ],
            "total_commands": len(COMMANDS),
            "total_categories": len(CATEGORIES),
        })

    @app.get("/categories")
    def list_categories():
        lang = _get_lang()
        return jsonify([_serialize_category(cid, lang) for cid in CATEGORIES])

    @app.get("/categories/<category_id>")
    def get_category(category_id: str):
        if category_id not in CATEGORIES:
            return jsonify({"error": "category_not_found", "category": category_id}), 404
        lang = _get_lang()
        data = _serialize_category(category_id, lang)
        data["commands"] = [
            _serialize_command(c, lang) for c in navigation.get_commands(category_id)
        ]
        return jsonify(data)

    @app.get("/commands")
    def list_commands():
        lang = _get_lang()
        category = request.args.get("category")
        subcategory = request.args.get("subcategory")
        tag = request.args.get("tag")

        commands = list(COMMANDS.values())
        if category:
            commands = [c for c in commands if c.category == category]
        if subcategory:
            commands = [c for c in commands if c.subcategory == subcategory]
        if tag:
            commands = [c for c in commands if tag in c.tags]

        commands.sort(key=lambda c: c.id)
        return jsonify([_serialize_command(c, lang) for c in commands])

    @app.get("/commands/<command_id>")
    def get_command(command_id: str):
        cmd = COMMANDS.get(command_id)
        if not cmd:
            return jsonify({"error": "command_not_found", "command": command_id}), 404
        return jsonify(_serialize_command(cmd, _get_lang()))

    @app.get("/search")
    def search_commands():
        query = request.args.get("q", "").strip()
        if not query:
            return jsonify({"error": "missing_query", "hint": "use ?q=<texto>"}), 400
        lang = _get_lang()
        results = search.search(query, limit=30)
        return jsonify([
            {"score": r.score, "matched_on": r.matched_on, **_serialize_command(r.command, lang)}
            for r in results
        ])

    @app.get("/tags/<tag_id>")
    def get_tag(tag_id: str):
        if tag_id not in TAGS:
            return jsonify({"error": "tag_not_found", "tag": tag_id}), 404
        lang = _get_lang()
        commands = search.search_by_tag(tag_id)
        commands.sort(key=lambda c: c.id)
        return jsonify({
            "id": tag_id,
            "description": t_tag(tag_id, lang),
            "commands": [_serialize_command(c, lang) for c in commands],
        })

    return app


def main() -> None:
    app = create_app()
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()

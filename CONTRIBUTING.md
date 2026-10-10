# Contributing

## Core rule: one master entry per command

Every command lives in exactly ONE file, in ONE category (its "owner"
category). If it's relevant to other categories, it gets referenced
through `tags`, never duplicated. Before adding a command, search if it
already exists:

    grep -rn "id=\"your_command\"" app/data/commands/

## Adding a new command

1. Pick the category file it belongs to (`app/data/commands/<category>.py`).
2. Add a `Command(...)` entry following the existing pattern in that file
   -- every field matters:
   - `description`, `syntax`: required, non-empty.
   - `examples`: at least one is strongly recommended (the validator
     warns, but doesn't block, if missing).
   - `risk`: if not `Risk.SEGURO`, `precautions` becomes REQUIRED (the
     validator blocks this).
   - `tags`: must exist in `app/data/tags.py` (`TAGS` dict). Don't
     invent new tags casually -- check if an existing one fits first.
   - `related`: must point to real command ids that already exist.
3. Run the validator:

       python run.py --validate

   Zero errors required before committing. Warnings are fine to leave
   for now, but read them.
4. Run the tests:

       python -m pytest tests/ -v

## Adding a new category

1. Add it to `app/data/categories.py` (`CATEGORIES` dict), following the
   existing `Category`/`Subcategory` pattern.
2. Update `app/core/i18n.py`'s `CATEGORY_EN` dict if you're also adding
   the English translation (optional -- untranslated categories fall
   back to Spanish automatically, see "Translating a category" below).
3. A category with zero commands is only allowed if it's a genuine
   cross-cutting view (like `maintenance`) -- otherwise the validator
   will flag it as an error.

## Translating a category to English

The i18n system is per-category, not all-or-nothing (see
`app/data/i18n_commands/files_en.py` as the reference example):

1. Create `app/data/i18n_commands/<category>_en.py` with a `COMMAND_EN`
   dict, keyed by command id. Only include fields that need translating
   (`description`, `syntax`, `when_to_use`, `options`, `precautions`,
   `examples`, `name`) -- fields you omit fall back to Spanish
   automatically, so partial translations never break anything.
2. Register the new module in
   `app/data/i18n_commands/__init__.py`'s `_MODULES` tuple.
3. If the category name/subcategories aren't translated yet, add them to
   `CATEGORY_EN` in `app/core/i18n.py`.
4. Test it:

       python -c "
       from app.core.i18n import t_command, Lang
       from app.data.commands import COMMANDS
       tc = t_command(COMMANDS['your_command_id'], Lang.EN)
       print(tc.description)
       "

## Code style

- Source code comments and docstrings: Spanish (the project's primary
  development language).
- User-facing text (README, this file, commit messages): English.
- No new dependencies without a reason -- see the original design
  principle: "no introducir frameworks innecesarios." If you think one
  is needed, explain what problem it solves before adding it.

## Architecture reminder

    DATA (app/data)
       |
    CORE ENGINE (app/core: search.py, navigation.py, validator.py, i18n.py)
       |
       +-- CLI (app/cli)
       +-- GUI (app/gui)
       +-- Flask API (app/api)

CLI, GUI and the API must never duplicate business logic -- if you find
yourself writing the same filtering/searching/translating logic in more
than one interface, it belongs in `app/core` instead.

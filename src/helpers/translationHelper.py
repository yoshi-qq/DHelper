import json
import os
from enum import Enum
from os.path import dirname, join
from typing import Type, TypeVar

LANG_DIR = join(dirname(dirname(__file__)), "config", "languages")
SETTINGS_PATH = join(dirname(dirname(__file__)), "config", "settings.json")
_current_lang = "en"
_current_theme = "light"
_skip_missing = False
_print_missing = False
_translations: dict[str, dict[str, str]] = {}


def _load_settings() -> None:
    global _current_lang, _current_theme, _skip_missing, _print_missing
    if not os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "language": "en",
                    "theme": "light",
                    "skip_missing": False,
                    "print_missing": False,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        _current_lang = "en"
        _current_theme = "light"
        _skip_missing = False
        _print_missing = False
        return
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    _current_lang = data.get("language", "en")
    _current_theme = data.get("theme", "light")
    _skip_missing = data.get("skip_missing", False)
    _print_missing = data.get("print_missing", False)


def _save_settings() -> None:
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "language": _current_lang,
                "theme": _current_theme,
                "skip_missing": _skip_missing,
                "print_missing": _print_missing,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )


def load_language(lang: str) -> None:
    global _current_lang, _translations
    path = join(LANG_DIR, f"{lang}.json")
    with open(path, "r", encoding="utf-8") as f:
        _translations = json.load(f)
    _current_lang = lang
    _save_settings()


def get_language() -> str:
    return _current_lang


def set_language(lang: str) -> None:
    load_language(lang)


def get_theme() -> str:
    return _current_theme


def set_theme(theme: str) -> None:
    global _current_theme
    _current_theme = theme
    _save_settings()


def get_skip_missing() -> bool:
    return _skip_missing


def set_skip_missing(value: bool) -> None:
    global _skip_missing
    _skip_missing = value
    _save_settings()


def get_print_missing() -> bool:
    return _print_missing


def set_print_missing(value: bool) -> None:
    global _print_missing
    _print_missing = value
    _save_settings()


def translate(key: Enum) -> str:
    category = key.__class__.__name__
    return str(_translations.get(category, {}).get(key.name, key.value))


def shortName(key: Enum, translate_name: bool = False) -> str:
    """Return the first three letters of ``key`` in uppercase.

    Args:
        key: Enum value to shorten.
        translate_name: When ``True`` the translated name is used.

    Returns:
        Three letter abbreviation of ``key``.
    """
    name = translate(key) if translate_name else key.name
    return name[:3].upper()


E = TypeVar("E", bound=Enum)


def to_enum(enum: Type[E], value: str | Enum | None) -> E:
    if isinstance(value, enum):
        return value
    if value is None:
        raise ValueError("No value provided")
    for member in enum:
        if value in {member.name, member.value, translate(member)}:
            return member
    raise ValueError(f"Unknown value '{value}' for {enum.__name__}")


# initialize with language from settings
_load_settings()
load_language(_current_lang)

import json
import os
from enum import Enum
from os.path import dirname, join
from typing import Type, TypeVar

LANG_DIR = join(dirname(dirname(__file__)), "config", "languages")
SETTINGS_PATH = join(dirname(dirname(__file__)), "config", "settings.json")
_current_lang = "en"
_translations: dict[str, dict] = {}


def _load_settings() -> str:
    if not os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump({"language": "en"}, f)
        return "en"
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("language", "en")


def _save_settings(lang: str) -> None:
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump({"language": lang}, f, ensure_ascii=False, indent=2)


def load_language(lang: str) -> None:
    global _current_lang, _translations
    path = join(LANG_DIR, f"{lang}.json")
    with open(path, "r", encoding="utf-8") as f:
        _translations = json.load(f)
    _current_lang = lang
    _save_settings(lang)


def get_language() -> str:
    return _current_lang


def set_language(lang: str) -> None:
    load_language(lang)


def translate(key: Enum) -> str:
    category = key.__class__.__name__
    return _translations.get(category, {}).get(key.name, key.value)


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
load_language(_load_settings())

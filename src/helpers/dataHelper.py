import json
from json import load, dump
from classes.types import (
    Item,
    JsonItem,
    JsonItemCache,
    Spell,
    JsonSpell,
)
from config.constants import DATA, PATHS
import os
from helpers.conversionHelper import toItem, toSpell


def getItems() -> list[Item]:
    with open(DATA.ITEMS, "r", encoding="utf-8") as file:
        jsonItems: dict[str, JsonItem] = load(file)
    items: list[Item] = [toItem(_id=key, jsonItem=item) for key, item in jsonItems.items()]
    return items


def addItem(item: Item) -> None:
    with open(DATA.ITEMS, "r", encoding="utf-8") as file:
        data: dict[str, JsonItem] = load(file)
    data[item.id] = item.toJsonItem()
    with open(DATA.ITEMS, "w", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=4)


def loadItemCache() -> dict[str, JsonItemCache]:
    if not os.path.exists(PATHS.ITEM_CACHE):
        os.makedirs(PATHS.CACHE, exist_ok=True)
        with open(PATHS.ITEM_CACHE, "w", encoding="utf-8") as file:
            dump({}, file)
        return {}
    with open(PATHS.ITEM_CACHE, "r", encoding="utf-8") as file:
        return json.load(file)


def saveItemCache(cache: dict[str, JsonItemCache]) -> None:
    os.makedirs(PATHS.CACHE, exist_ok=True)
    with open(PATHS.ITEM_CACHE, "w", encoding="utf-8") as file:
        dump(cache, file, ensure_ascii=False, indent=4)


def updateItemCache(item_id: str, rotate: float, scale: float, flip: bool) -> None:
    cache = loadItemCache()
    cache[item_id] = {"rotate": rotate, "scale": scale, "flip": flip}
    saveItemCache(cache)


def getSpells() -> list[Spell]:
    with open(DATA.SPELLS, "r", encoding="utf-8") as file:
        jsonSpells: dict[str, JsonSpell] = load(file)
    return [toSpell(key, value) for key, value in jsonSpells.items()]


def addSpell(spell: Spell) -> None:
    with open(DATA.SPELLS, "r", encoding="utf-8") as file:
        data: dict[str, JsonSpell] = load(file)
    data[spell.id] = spell.toJsonSpell()
    with open(DATA.SPELLS, "w", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=4)


def loadSpellCache() -> dict[str, JsonItemCache]:
    if not os.path.exists(PATHS.SPELL_CACHE):
        os.makedirs(PATHS.CACHE, exist_ok=True)
        with open(PATHS.SPELL_CACHE, "w", encoding="utf-8") as file:
            dump({}, file)
        return {}
    with open(PATHS.SPELL_CACHE, "r", encoding="utf-8") as file:
        return json.load(file)


def saveSpellCache(cache: dict[str, JsonItemCache]) -> None:
    os.makedirs(PATHS.CACHE, exist_ok=True)
    with open(PATHS.SPELL_CACHE, "w", encoding="utf-8") as file:
        dump(cache, file, ensure_ascii=False, indent=4)


def updateSpellCache(spell_id: str, rotate: float, scale: float, flip: bool) -> None:
    cache = loadSpellCache()
    cache[spell_id] = {"rotate": rotate, "scale": scale, "flip": flip}
    saveSpellCache(cache)

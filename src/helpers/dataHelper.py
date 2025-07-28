import json
from json import load, dump
from classes.types import (
    Weapon,
    Armor,
    SimpleItem,
    JsonWeapon,
    JsonArmor,
    JsonSimpleItem,
    ItemCache,
    SpellCache,
    Spell,
    JsonSpell,
)
from config.constants import DATA, PATHS
import os
from helpers.conversionHelper import (
    toWeapon,
    toArmor,
    toSimpleItem,
    toSpell,
)


def getWeapons() -> list[Weapon]:
    with open(DATA.WEAPONS, "r", encoding="utf-8") as file:
        jsonItems: dict[str, JsonWeapon] = load(file)
    return [toWeapon(key, item) for key, item in jsonItems.items()]


def addWeapon(weapon: Weapon) -> None:
    with open(DATA.WEAPONS, "r", encoding="utf-8") as file:
        data: dict[str, JsonWeapon] = load(file)
    data[weapon.id] = weapon.toJsonWeapon()
    with open(DATA.WEAPONS, "w", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=4)


def getArmors() -> list[Armor]:
    with open(DATA.ARMOR, "r", encoding="utf-8") as file:
        jsonItems: dict[str, JsonArmor] = load(file)
    return [toArmor(key, item) for key, item in jsonItems.items()]


def addArmor(armor: Armor) -> None:
    with open(DATA.ARMOR, "r", encoding="utf-8") as file:
        data: dict[str, JsonArmor] = load(file)
    data[armor.id] = armor.toJsonArmor()
    with open(DATA.ARMOR, "w", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=4)


def getItems() -> list[SimpleItem]:
    with open(DATA.ITEMS, "r", encoding="utf-8") as file:
        jsonItems: dict[str, JsonSimpleItem] = load(file)
    return [toSimpleItem(key, item) for key, item in jsonItems.items()]


def addItem(item: SimpleItem) -> None:
    with open(DATA.ITEMS, "r", encoding="utf-8") as file:
        data: dict[str, JsonSimpleItem] = load(file)
    data[item.id] = item.toJsonSimpleItem()
    with open(DATA.ITEMS, "w", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=4)


def loadItemCache() -> ItemCache:
    if not os.path.exists(PATHS.ITEM_CACHE):
        os.makedirs(PATHS.CACHE, exist_ok=True)
        with open(PATHS.ITEM_CACHE, "w", encoding="utf-8") as file:
            dump({}, file)
        return {}
    with open(PATHS.ITEM_CACHE, "r", encoding="utf-8") as file:
        return json.load(file)


def saveItemCache(cache: ItemCache) -> None:
    os.makedirs(PATHS.CACHE, exist_ok=True)
    with open(PATHS.ITEM_CACHE, "w", encoding="utf-8") as file:
        dump(cache, file, ensure_ascii=False, indent=4)


def updateItemCache(
    item_id: str,
    rotate: float,
    scale: float,
    flip: bool,
    offset_x: float,
    offset_y: float,
) -> None:
    cache = loadItemCache()
    cache[item_id] = {
        "rotate": rotate,
        "scale": scale,
        "flip": flip,
        "offset_x": offset_x,
        "offset_y": offset_y,
    }
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


def loadSpellCache() -> SpellCache:
    if not os.path.exists(PATHS.SPELL_CACHE):
        os.makedirs(PATHS.CACHE, exist_ok=True)
        with open(PATHS.SPELL_CACHE, "w", encoding="utf-8") as file:
            dump({}, file)
        return {}
    with open(PATHS.SPELL_CACHE, "r", encoding="utf-8") as file:
        return json.load(file)


def saveSpellCache(cache: SpellCache) -> None:
    os.makedirs(PATHS.CACHE, exist_ok=True)
    with open(PATHS.SPELL_CACHE, "w", encoding="utf-8") as file:
        dump(cache, file, ensure_ascii=False, indent=4)


def updateSpellCache(
    spell_id: str,
    rotate: float,
    scale: float,
    flip: bool,
    offset_x: float,
    offset_y: float,
) -> None:
    cache = loadSpellCache()
    cache[spell_id] = {
        "rotate": rotate,
        "scale": scale,
        "flip": flip,
        "offset_x": offset_x,
        "offset_y": offset_y,
    }
    saveSpellCache(cache)

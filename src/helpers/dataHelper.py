import json
from json import load, dump
from classes.types import Item, JsonItem
from config.constants import ITEMS_LIST_PATH
from helpers.conversionHelper import toItem


def getItems() -> list[Item]:
    with open(ITEMS_LIST_PATH, "r", encoding="utf-8") as file:
        jsonItems: dict[str, JsonItem] = load(file)
    items: list[Item] = [toItem(_id=key, jsonItem=item) for key, item in jsonItems.items()]
    return items


def addItem(item: Item) -> None:
    with open(ITEMS_LIST_PATH, "r", encoding="utf-8") as file:
        data: dict[str, JsonItem] = load(file)
    data[item.id] = item.toJsonItem()
    with open(ITEMS_LIST_PATH, "w", encoding="utf-8") as file:
        dump(data, file, ensure_ascii=False, indent=4)

import json
from classes.types import Item, JsonItem
from config.constants import ITEMS_LIST_PATH
from json import load
from helpers.conversionHelper import toItem

def getItems() -> list[Item]:
    with open(ITEMS_LIST_PATH, "r", encoding="utf-8") as file:
        jsonItems: dict[str, JsonItem] = load(file)
    items: list[Item] = [
        toItem(_id=key,  jsonItem=item) for key, item in jsonItems.items()
    ]
    return items
from classes.types import JsonItem, Item
def toItem(_id: str, jsonItem: JsonItem) -> Item:
    return Item(
        _id = _id,
        name = jsonItem['name'],
        cost = jsonItem['cost'],
        weight = jsonItem['weight'],
        damageDiceAmount = jsonItem['damage']['diceAmount'],
        damageDiceType = jsonItem['damage']['diceType'],
        damageBonus = jsonItem['damage']['bonus'],
        damageType = jsonItem['damage']['damageType'],
        attributes = jsonItem['attributes']
    )

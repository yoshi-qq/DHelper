from classes.types import RGB, JsonItem, Item, HexColor, RGBA
def toItem(_id: str, jsonItem: JsonItem) -> Item:
    return Item(
        _id = _id,
        name = jsonItem['name'],
        price = jsonItem['price'],
        weight = jsonItem['weight'],
        attributes = jsonItem['attributes'],
        **(
            {
                "damageDiceAmount": jsonItem['damage']['diceAmount'],
                "damageDiceType": jsonItem['damage']['diceType'],
                "damageBonus": jsonItem['damage']['bonus'],
                "damageType": jsonItem['damage']['damageType']
            } if jsonItem['damage'] else {}
        )
    )

def toRGBA(hex: HexColor) -> RGBA:
    hex = hex.lstrip('#')
    if len(hex) == 3:
        hex = ''.join(2 * c for c in hex)
    rgb = list(int(hex[i:i+2], 16) for i in (0, 2, 4))
    return (rgb[0], rgb[1], rgb[2], 255)

def toHex(rgb: RGBA | RGB) -> str:
    return f'#{hex(rgb[0])}{hex(rgb[1])}{hex(rgb[2])}'

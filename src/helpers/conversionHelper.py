from classes.types import RGB, JsonItem, Item, HexColor, RGBA, Damage, DamageType, AttributeType
from helpers.translationHelper import to_enum
def toItem(_id: str, jsonItem: JsonItem) -> Item:
    ranges = {
        to_enum(AttributeType, k): (int(v[0]), int(v[1])) if isinstance(v, (list, tuple)) and len(v) >= 2 else (0, 0)
        for k, v in jsonItem.get("ranges", {}).items()
    }
    damage = jsonItem.get("damage")
    versatile = jsonItem.get("versatileDamage")
    primary_type_str = damage.get("damageType", "") if isinstance(damage, dict) else ""
    primary_type = to_enum(DamageType, primary_type_str) if primary_type_str else None
    return Item(
        _id=_id,
        name=jsonItem.get("name", ""),
        price=jsonItem.get("price", 0),
        weight=jsonItem.get("weight", 0),
        attributes=[to_enum(AttributeType, a) for a in jsonItem.get("attributes")] if isinstance(jsonItem.get("attributes"), list) else [],
        ranges=ranges if ranges else None,
        **(
            {
                "damageDiceAmount": damage.get("diceAmount", 0),
                "damageDiceType": damage.get("diceType", ""),
                "damageBonus": damage.get("bonus", 0),
                "damageType": to_enum(DamageType, damage.get("damageType")) if damage.get("damageType") else None,
            }
            if damage
            else {}
        ),
        versatileDamage=(
            (lambda vt: Damage(
                versatile.get("diceAmount", 0),
                versatile.get("diceType", 1),
                versatile.get("bonus", 0),
                vt,
            ) if vt else None)(
                to_enum(DamageType, versatile.get("damageType", primary_type_str))
                if versatile and (versatile.get("damageType") or primary_type_str)
                else None
            )
            if versatile
            else None
        ),
    )

def toRGBA(hex: HexColor) -> RGBA:
    hex = hex.lstrip('#')
    if len(hex) == 3:
        hex = ''.join(2 * c for c in hex)
    rgb = list(int(hex[i:i+2], 16) for i in (0, 2, 4))
    return (rgb[0], rgb[1], rgb[2], 255)

def toHex(rgb: RGBA | RGB) -> str:
    return f'#{hex(rgb[0])}{hex(rgb[1])}{hex(rgb[2])}'

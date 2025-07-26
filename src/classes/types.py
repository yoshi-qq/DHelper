from enum import Enum
from typing import Literal, Optional, Type, TypedDict, Annotated, Tuple
import re

HexColor = Annotated[
    str,
    re.compile(r'^#(?:[0-9A-Fa-f]{3}){1,2}$')
]
RGB = Annotated[
    Tuple[int, int, int],
    lambda value: all(0 <= v <= 255 for v in value)
]
RGBA = Annotated[
    Tuple[int, int, int, int],
    lambda value: all(0 <= v <= 255 for v in value)
]


DamageType = Literal["Blitz", "Energie", "Feuer", "Gift", "Gleißend", "Hieb", "Kälte", "Nekrotisch", "Psychisch", "Säure", "Schall", "Stich", "Wucht"]
AttributeType = Literal["Finesse", "Geschosse", "Laden", "Leicht", "Reichweite", "Schwer", "Speziell", "Vielseitig", "Weitreichend", "Wurfwaffe", "Zweihändig"]


# ========
# = JSON
# ========
class JsonDamage(TypedDict):
    diceAmount: int
    diceType: int
    bonus: int
    damageType: DamageType

class JsonItem(TypedDict):
    name: str
    price: int
    weight: float
    damage: JsonDamage | None
    attributes: list[AttributeType]


# ==========
# = Python
# ==========

class Currency(Enum):
    GOLD = 1
    SILVER = 0.1
    COPPER = 0.01

class Damage:
    def __init__(self, diceAmount: int, diceType: int, bonus: int, damageType: DamageType) -> None:
        self.diceAmount: int = diceAmount
        self.diceType: int = diceType
        self.bonus: int = bonus
        self.damageType: DamageType = damageType
    def toJsonDamage(self) -> JsonDamage:
        return {
            "diceAmount": self.diceAmount,
            "diceType": self.diceType,
            "bonus": self.bonus,
            "damageType": self.damageType
        }

class Item:
    def __init__(self, _id: str, name: str, price: int, weight: float, damageDiceAmount: int = 0, damageDiceType: int = 1, damageBonus: int = 0, damageType: Optional[DamageType] = None, attributes: Optional[list[AttributeType]] = None) -> None:
        self.id: str = _id
        self.name: str = name
        self.price: int = price
        self.weight: float = weight
        self.damage = Damage(damageDiceAmount, damageDiceType, damageBonus, damageType) if damageType is not None else None
        self.attributes: list[AttributeType] = attributes if attributes else []
    def toJsonItem(self) -> JsonItem:
        return {
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "damage": self.damage.toJsonDamage() if self.damage else None,
            "attributes": self.attributes
        }


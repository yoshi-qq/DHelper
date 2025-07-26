from enum import Enum
from typing import Optional, Type, TypedDict, Annotated, Tuple
from helpers.translationHelper import translate, to_enum
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


class DamageType(Enum):
    LIGHTNING = "Lightning"
    FORCE = "Force"
    FIRE = "Fire"
    POISON = "Poison"
    RADIANT = "Radiant"
    SLASHING = "Slashing"
    COLD = "Cold"
    NECROTIC = "Necrotic"
    PSYCHIC = "Psychic"
    ACID = "Acid"
    THUNDER = "Thunder"
    PIERCING = "Piercing"
    BLUDGEONING = "Bludgeoning"

    def __str__(self) -> str:  # pragma: no cover - simple delegation
        return translate(self)

class AttributeType(Enum):
    FINESSE = "Finesse"
    AMMUNITION = "Ammunition"
    LOADING = "Loading"
    LIGHT = "Light"
    REACH = "Reach"
    HEAVY = "Heavy"
    SPECIAL = "Special"
    VERSATILE = "Versatile"
    RANGED = "Ranged"
    THROWN = "Thrown"
    TWO_HANDED = "Two-Handed"

    def __str__(self) -> str:  # pragma: no cover - simple delegation
        return translate(self)


# ========
# = JSON
# ========
class JsonDamage(TypedDict):
    diceAmount: int
    diceType: int
    bonus: int
    damageType: DamageType

class JsonItem(TypedDict, total=False):
    name: str
    price: float
    weight: float
    damage: JsonDamage | None
    versatileDamage: JsonDamage | None
    attributes: list[AttributeType]
    ranges: dict[str, list[int]]

class JsonItemCache(TypedDict):
    rotate: float
    scale: float
    flip: bool


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
            "damageType": self.damageType.value,
        }

class Item:
    def __init__(
        self,
        _id: str,
        name: str,
        price: float,
        weight: float,
        damageDiceAmount: int = 0,
        damageDiceType: int = 1,
        damageBonus: int = 0,
        damageType: Optional[DamageType] = None,
        attributes: Optional[list[AttributeType]] = None,
        ranges: Optional[dict[AttributeType, tuple[int, int]]] = None,
        versatileDamage: Optional[Damage] = None,
    ) -> None:
        self.id: str = _id
        self.name: str = name
        self.price: float = price
        self.weight: float = weight
        self.damage = Damage(damageDiceAmount, damageDiceType, damageBonus, damageType) if damageType is not None else None
        self.versatileDamage: Optional[Damage] = versatileDamage
        self.attributes: list[AttributeType] = attributes if attributes else []
        self.ranges: dict[AttributeType, tuple[int, int]] = ranges if ranges else {}
    def toJsonItem(self) -> JsonItem:
        return {
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "damage": self.damage.toJsonDamage() if self.damage else None,
            "versatileDamage": self.versatileDamage.toJsonDamage() if self.versatileDamage else None,
            "attributes": [a.value for a in self.attributes],
            **({"ranges": {k.value: [v[0], v[1]] for k, v in self.ranges.items()}} if self.ranges else {})
        }  # type: ignore


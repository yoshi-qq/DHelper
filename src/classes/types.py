from datetime import timedelta
from enum import Enum
from typing import Literal, Optional, Type, TypedDict, Annotated, Tuple
import re
from src.classes.types import JsonDamage

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

# TODO: Enums to be translated later
DamageType = Literal["Blitz", "Energie", "Feuer", "Gift", "Gleißend", "Hieb", "Kälte", "Nekrotisch", "Psychisch", "Säure", "Schall", "Stich", "Wucht"]
AttributeType = Literal["Finesse", "Geschosse", "Laden", "Leicht", "Reichweite", "Schwer", "Speziell", "Vielseitig", "Weitreichend", "Wurfwaffe", "Zweihändig"]

SpellType = Literal["Bannmagie", "Beschwörungsmagie", "Verwandlungsmagie", "Hervorrufungsmagie", "Illusionsmagie", "Nekromantie", "Verzauberungsmagie", "Erkenntnismagie"]

CasterClassType = Literal["Barde", "Kleriker", "Druide", "Hexenmeister", "Magier", "Paladin", "Waldläufer", "Zauberer", "Kunsthandwerker"]

CastingTimeType = Literal["Aktion", "Bonusaktion", "Reaktion", "1 Minute", "10 Minuten", "1 Stunde", "8 Stunden", "24 Stunden"]

TargetType = Literal["Selbst", "Kreatur", "Objekt", "Punkt", "Bereich", "Kegel", "Linie", "Kugel", "Zylinder", "Würfel"]

SavingThrowType = Literal["Stärke", "Geschicklichkeit", "Konstitution", "Intelligenz", "Weisheit", "Charisma"]

AreaOfEffectType = Literal["Kegel", "Würfel", "Zylinder", "Linie", "Kugel", "Rechteck"]


# ========
# = JSON
# ========

class JsonMaterial(TypedDict, total=False):
    name: str
    cost: Optional[float]

class JsonComponents(TypedDict):
    verbal: bool
    gestural: bool
    material: Optional[JsonMaterial]

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

class JsonSpell(TypedDict):
    id: str
    name: str
    level: int
    type: SpellType
    casterClass: CasterClassType
    duration: float # in seconds
    cooldown: float # in seconds
    range: float
    subRange: Optional[float]
    damage: JsonDamage | None
    components: JsonComponents
    levelBonus: str
    castingTime: CastingTimeType
    ritual: bool
    concentration: bool
    target: TargetType
    savingThrow: Optional[SavingThrowType]
    areaOfEffect: Optional[AreaOfEffectType]

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


class Material:
    def __init__(self, name: str, cost: Optional[float]) -> None:
        self.name: str = name
        self.cost: Optional[float] = cost
    
    def toJsonMaterial(self) -> JsonMaterial:
        return {
            "name": self.name,
            "cost": self.cost
        }

class Components:
    def __init__(self, verbal: bool, gestural: bool, material: Optional[Material]) -> None:
        self.verbal: bool = verbal
        self.gestural: bool = gestural
        self.material: Optional[Material] = material
    
    def toJsonComponents(self) -> JsonComponents:
        return {
            "verbal": self.verbal,
            "gestural": self.gestural,
            "material": self.material.toJsonMaterial() if self.material else None
        }

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
        ranges: Optional[dict[str, tuple[int, int]]] = None,
        versatileDamage: Optional[Damage] = None,
    ) -> None:
        self.id: str = _id
        self.name: str = name
        self.price: float = price
        self.weight: float = weight
        self.damage = Damage(damageDiceAmount, damageDiceType, damageBonus, damageType) if damageType is not None else None
        self.versatileDamage: Optional[Damage] = versatileDamage
        self.attributes: list[AttributeType] = attributes if attributes else []
        self.ranges: dict[str, tuple[int, int]] = ranges if ranges else {}
    def toJsonItem(self) -> JsonItem:
        return {
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "damage": self.damage.toJsonDamage() if self.damage else None,
            "versatileDamage": self.versatileDamage.toJsonDamage() if self.versatileDamage else None,
            "attributes": self.attributes,
            **({"ranges": {k: [v[0], v[1]] for k, v in self.ranges.items()}} if self.ranges else {})
        }  # type: ignore

class Spell:
    def __init__(self, id: str, name: str, level: int, type: SpellType, casterClass: CasterClassType, duration: timedelta, cooldown: timedelta, range: float, castingTime: CastingTimeType, ritual: bool, concentration: bool, target: TargetType, subRange: Optional[float] = None, damage: Optional[Damage] = None, components: Components = Components(False, False, None), levelBonus: str = "", savingThrow: Optional[SavingThrowType] = None, areaOfEffect: Optional[AreaOfEffectType] = None) -> None:
        self.id: str = id
        self.name: str = name
        self.level: int = level
        self.type: SpellType = type
        self.casterClass: CasterClassType = casterClass
        self.duration: timedelta = duration
        self.cooldown: timedelta = cooldown
        self.range: float = range
        self.subRange: Optional[float] = subRange
        self.damage: Optional[Damage] = damage
        self.components: Components = components
        self.levelBonus: str = levelBonus
        self.castingTime: CastingTimeType = castingTime
        self.ritual: bool = ritual
        self.concentration: bool = concentration
        self.target: TargetType = target
        self.savingThrow: Optional[SavingThrowType] = savingThrow
        self.areaOfEffect: Optional[AreaOfEffectType] = areaOfEffect

    def toJsonSpell(self) -> JsonSpell:
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "type": self.type,
            "casterClass": self.casterClass,
            "duration": self.duration.total_seconds(),
            "cooldown": self.cooldown.total_seconds(),
            "range": self.range,
            "subRange": self.subRange,
            "damage": self.damage.toJsonDamage() if self.damage else None,
            "components": self.components.toJsonComponents(),
            "levelBonus": self.levelBonus,
            "castingTime": self.castingTime,
            "ritual": self.ritual,
            "concentration": self.concentration,
            "target": self.target,
            "savingThrow": self.savingThrow,
            "areaOfEffect": self.areaOfEffect
        }
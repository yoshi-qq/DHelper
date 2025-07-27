from datetime import timedelta
from enum import Enum
from typing import Optional, Type, TypedDict, Annotated, Tuple, Literal
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

# alias for weapon properties to keep backwards compatibility
WeaponProperty = AttributeType


class ArmorCategory(Enum):
    LIGHT = "LIGHT"
    MEDIUM = "MEDIUM"
    HEAVY = "HEAVY"
    SHIELD = "SHIELD"

    def __str__(self) -> str:  # pragma: no cover - simple delegation
        return translate(self)

class SpellType(Enum):
    ABJURATION = "ABJURATION"
    CONJURATION = "CONJURATION"
    TRANSMUTATION = "TRANSMUTATION"
    EVOCATION = "EVOCATION"
    ILLUSION = "ILLUSION"
    NECROMANCY = "NECROMANCY"
    ENCHANTMENT = "ENCHANTMENT"
    DIVINATION = "DIVINATION"

    def __str__(self) -> str:  # pragma: no cover - simple delegation
        return translate(self)

class CasterClassType(Enum):
    BARD = "BARD"
    CLERIC = "CLERIC"
    DRUID = "DRUID"
    WARLOCK = "WARLOCK"
    WIZARD = "WIZARD"
    PALADIN = "PALADIN"
    RANGER = "RANGER"
    SORCERER = "SORCERER"
    ARTIFICER = "ARTIFICER"

    def __str__(self) -> str:  # pragma: no cover - simple delegation
        return translate(self)

class CastingTimeType(Enum):
    ACTION = "ACTION"
    BONUS_ACTION = "BONUS_ACTION"
    REACTION = "REACTION"
    ONE_MINUTE = "ONE_MINUTE"
    TEN_MINUTES = "TEN_MINUTES"
    ONE_HOUR = "ONE_HOUR"
    EIGHT_HOURS = "EIGHT_HOURS"
    TWENTY_FOUR_HOURS = "TWENTY_FOUR_HOURS"

    def __str__(self) -> str:  # pragma: no cover - simple delegation
        return translate(self)

class TargetType(Enum):
    SELF = "SELF"
    CREATURE = "CREATURE"
    OBJECT = "OBJECT"
    POINT = "POINT"
    CONE = "CONE"
    LINE = "LINE"
    SPHERE = "SPHERE"
    CYLINDER = "CYLINDER"
    CUBE = "CUBE"
    RECTANGLE = "RECTANGLE"

    def __str__(self) -> str:
        return translate(self)

class SavingThrowType(Enum):
    STRENGTH = "STRENGTH"
    DEXTERITY = "DEXTERITY"
    CONSTITUTION = "CONSTITUTION"
    INTELLIGENCE = "INTELLIGENCE"
    WISDOM = "WISDOM"
    CHARISMA = "CHARISMA"

    def __str__(self) -> str:
        return translate(self)


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
    damageType: str

class JsonItem(TypedDict, total=False):
    name: str
    price: float
    weight: float
    damage: JsonDamage | None
    versatileDamage: JsonDamage | None
    attributes: list[str]
    ranges: dict[str, list[int]]

# separated json structures for new item classes
class JsonWeapon(JsonItem):
    properties: list[str]


class JsonArmor(TypedDict):
    name: str
    price: float
    weight: float
    armorClass: int
    dexBonus: bool
    dexBonusMax: Optional[int]
    strengthRequirement: Optional[int]
    stealthDisadvantage: bool
    category: str


class JsonSimpleItem(TypedDict, total=False):
    name: str
    price: float
    weight: float
    description: Optional[str]

class JsonSpell(TypedDict):
    id: str
    name: str
    level: int
    type: str
    casterClasses: list[str]
    duration: float # in seconds
    cooldown: float # in seconds
    range: float
    subRange: Optional[float]
    damage: JsonDamage | None
    components: JsonComponents
    levelBonus: str
    castingTime: str
    ritual: bool
    concentration: bool
    target: str
    savingThrow: Optional[str]
    areaOfEffect: Optional[str]

class JsonItemCache(TypedDict):
    rotate: float
    scale: float
    flip: bool
    offset_x: float
    offset_y: float


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


class Weapon(Item):
    """Subclass representing weapons."""

    def toJsonWeapon(self) -> JsonWeapon:
        data: JsonItem = super().toJsonItem()
        return data  # type: ignore


class Armor:
    def __init__(
        self,
        _id: str,
        name: str,
        price: float,
        weight: float,
        armorClass: int,
        dexBonus: bool,
        dexBonusMax: Optional[int] = None,
        strengthRequirement: Optional[int] = None,
        stealthDisadvantage: bool = False,
        category: ArmorCategory = ArmorCategory.LIGHT,
    ) -> None:
        self.id = _id
        self.name = name
        self.price = price
        self.weight = weight
        self.armorClass = armorClass
        self.dexBonus = dexBonus
        self.dexBonusMax = dexBonusMax
        self.strengthRequirement = strengthRequirement
        self.stealthDisadvantage = stealthDisadvantage
        self.category = category

    def toJsonArmor(self) -> JsonArmor:
        return {
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "armorClass": self.armorClass,
            "dexBonus": self.dexBonus,
            "dexBonusMax": self.dexBonusMax,
            "strengthRequirement": self.strengthRequirement,
            "stealthDisadvantage": self.stealthDisadvantage,
            "category": self.category.value,
        }


class SimpleItem:
    def __init__(
        self,
        _id: str,
        name: str,
        price: float,
        weight: float,
        description: str = "",
    ) -> None:
        self.id = _id
        self.name = name
        self.price = price
        self.weight = weight
        self.description = description

    def toJsonSimpleItem(self) -> JsonSimpleItem:
        return {
            "name": self.name,
            "price": self.price,
            "weight": self.weight,
            "description": self.description,
        }

class Spell:
    def __init__(
        self,
        id: str,
        name: str,
        level: int,
        type: SpellType,
        casterClasses: list[CasterClassType],
        duration: timedelta,
        cooldown: timedelta,
        range: float,
        castingTime: CastingTimeType,
        ritual: bool,
        concentration: bool,
        target: TargetType,
        subRange: Optional[float] = None,
        damage: Optional[Damage] = None,
        components: Components = Components(False, False, None),
        levelBonus: str = "",
        savingThrow: Optional[SavingThrowType] = None,
        areaOfEffect: Optional[TargetType] = None,
    ) -> None:
        self.id: str = id
        self.name: str = name
        self.level: int = level
        self.type: SpellType = type
        self.casterClasses: list[CasterClassType] = casterClasses
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
        self.areaOfEffect: Optional[TargetType] = areaOfEffect

    def toJsonSpell(self) -> JsonSpell:
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "type": self.type.value,
            "casterClasses": [c.value for c in self.casterClasses],
            "duration": self.duration.total_seconds(),
            "cooldown": self.cooldown.total_seconds(),
            "range": self.range,
            "subRange": self.subRange,
            "damage": self.damage.toJsonDamage() if self.damage else None,
            "components": self.components.toJsonComponents(),
            "levelBonus": self.levelBonus,
            "castingTime": self.castingTime.value,
            "ritual": self.ritual,
            "concentration": self.concentration,
            "target": self.target.value,
            "savingThrow": self.savingThrow.value if self.savingThrow else None,
            "areaOfEffect": self.areaOfEffect.value if self.areaOfEffect else None
        }
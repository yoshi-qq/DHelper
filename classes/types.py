from typing import Literal, Type, TypedDict

DamageType = Literal["Blitz", "Energie", "Feuer", "Gift", "Gleißend", "Hieb", "Kälte", "Nekrotisch", "Psychisch", "Säure", "Schall", "Stich", "Wucht"]
AttributeType = Literal["Finesse", "Geschosse", "Laden", "Leicht", "Reichweite", "Schwer", "Speziell", "Vielseitig", "Weitreichend", "Wurfwaffe", "Zweihändig"]

class JsonDamage(TypedDict):
    diceAmount: int
    diceType: int
    bonus: int
    damageType: DamageType

class JsonItem(TypedDict):
    name: str
    cost: int
    weight: float
    damage: JsonDamage
    attributes: list[AttributeType]

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
    def __init__(self, _id: str, name: str, cost: int, weight: float, damageDiceAmount: int, damageDiceType: int, damageBonus: int, damageType: DamageType, attributes: list[AttributeType]) -> None:
        self.id: str = _id
        self.name: str = name
        self.cost: int = cost
        self.weight: float = weight
        self.damage = Damage(damageDiceAmount, damageDiceType, damageBonus, damageType)
        self.attributes: list[AttributeType] = attributes
    def toJsonItem(self) -> JsonItem:
        return {
            "name": self.name,
            "cost": self.cost,
            "weight": self.weight,
            "damage": self.damage.toJsonDamage(),
            "attributes": self.attributes
        }


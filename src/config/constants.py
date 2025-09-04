from os.path import join, dirname
from helpers.tupleHelper import twoDTruncate
from helpers.conversionHelper import toRGBA


# =============
# = CONSTANT
# =============
SRC = dirname(dirname(__file__))
ROOT = dirname(SRC)


# = Game =
class _GameConstants:
    """Game-related constants."""

    def __init__(self) -> None:
        self.DICE_SIZES: list[int] = [4, 6, 8, 10, 12, 20]


GAME = _GameConstants()


# = Card =
class _CardConstants:
    def __init__(self) -> None:
        self.RESOLUTION: tuple[int, int] = (1780, 2485)  # (x, y)


CARD = _CardConstants()


# = Font Paths =
class _FontPaths:
    def __init__(self) -> None:
        folder = join(SRC, "fonts")
        self.REGULAR: str = join(folder, "timesbd.ttf")
        self.BOLD: str = join(folder, "timesbd.ttf")
        self.ITALIC: str = join(folder, "timesi.ttf")
        self.BOLD_ITALIC: str = join(folder, "timesbi.ttf")


class _FontConstants:
    def __init__(self) -> None:
        self.PATHS: _FontPaths = _FontPaths()
        self.TITLE_PATH: str = self.PATHS.BOLD_ITALIC
        self.PRICE_PATH: str = self.PATHS.BOLD
        self.STATS_PATH: str = self.PATHS.BOLD


FONT = _FontConstants()


# = Image Paths =
class _ImagePaths:
    def __init__(self) -> None:
        assets = join(SRC, "assets")
        self.ASSETS: str = assets
        self.ITEMS: str = join(assets, "items")
        self.WEAPONS: str = join(assets, "weapons")
        self.ARMOR: str = join(assets, "armor")
        self.SPELLS: str = join(assets, "spells")
        self.BACKGROUND: str = join(assets, "background")
        self.APP_ICON: str = join(self.ASSETS, "logo.png")


class _BackgroundImages:
    def __init__(self) -> None:
        bg_path = join(SRC, "assets", "background")
        self.GOLD_ITEM: str = join(bg_path, "item_gold_template.png")
        self.SILVER_ITEM: str = join(bg_path, "item_silver_template.png")
        self.COPPER_ITEM: str = join(bg_path, "item_copper_template.png")
        self.SPELL: str = join(bg_path, "spell_background.png")


class _TargetIconPaths:
    def __init__(self) -> None:
        targets_path = join(SRC, "assets", "icons", "targets")
        self.CONE: str = join(targets_path, "cone.png")
        self.CREATURE: str = join(targets_path, "creature.png")
        self.CUBE: str = join(targets_path, "cube.png")
        self.CYLINDER: str = join(targets_path, "cylinder.png")
        self.LINE: str = join(targets_path, "line.png")
        self.OBJECT: str = join(targets_path, "object.png")
        self.POINT: str = join(targets_path, "point.png")
        self.RECTANGLE: str = join(targets_path, "rectangle.png")
        self.SELF: str = join(targets_path, "self.png")
        self.SPHERE: str = join(targets_path, "sphere.png")


class _LevelIconPaths:
    def __init__(self) -> None:
        levels_path = join(SRC, "assets", "icons", "levels")
        self.LEVEL_1: str = join(levels_path, "1seal.png")
        self.LEVEL_2: str = join(levels_path, "2nature_seal.png")
        self.LEVEL_3: str = join(levels_path, "3blue_seal.png")
        self.LEVEL_4: str = join(levels_path, "4bronze_seal.png")
        self.LEVEL_5: str = join(levels_path, "5silver_seal.png")
        self.LEVEL_6: str = join(levels_path, "6gold_seal.png")
        self.LEVEL_7: str = join(levels_path, "7dark_seal.png")
        self.LEVEL_8: str = join(levels_path, "8enchanted_seal.png")
        self.LEVEL_9: str = join(levels_path, "9molten_seal.png")


class _IconPaths:
    def __init__(self) -> None:
        icons_path = join(SRC, "assets", "icons")
        # Spell component and status icons
        self.CONCENTRATION: str = join(icons_path, "concentration.png")
        self.COOLDOWN: str = join(icons_path, "cooldown.png")
        self.DAMAGE: str = join(icons_path, "damage.png")
        self.DURATION: str = join(icons_path, "duration.png")
        self.GESTURAL: str = join(icons_path, "gestural.png")
        self.MATERIAL: str = join(icons_path, "material.png")
        self.RANGE: str = join(icons_path, "range.png")
        self.RITUAL: str = join(icons_path, "ritual.png")
        self.SIGHT: str = join(icons_path, "sight.png")
        self.SPOKEN: str = join(icons_path, "spoken.png")
        self.STRIKE: str = join(icons_path, "strike.png")
        # Target icons
        self.TARGETS: _TargetIconPaths = _TargetIconPaths()
        # Level icons
        self.LEVELS: _LevelIconPaths = _LevelIconPaths()


class _ImageConstants:
    def __init__(self) -> None:
        self.FORMAT: str = "png"
        self.PATHS: _ImagePaths = _ImagePaths()
        self.BACKGROUNDS: _BackgroundImages = _BackgroundImages()
        self.ICONS: _IconPaths = _IconPaths()


IMAGE = _ImageConstants()


# = Data Paths =
class _DataPaths:
    def __init__(self) -> None:
        data = join(ROOT, "data")
        self.DIRECTORY: str = data
        # new separated item files
        self.WEAPONS: str = join(data, "weapons.json")
        self.ARMOR: str = join(data, "armor.json")
        self.ITEMS: str = join(data, "items.json")
        self.SPELLS: str = join(data, "spells.json")


DATA = _DataPaths()


# = Output & Cache Paths =
class _PathConstants:
    def __init__(self) -> None:
        output = join(ROOT, "output")
        self.OUTPUT: str = output
        self.ITEM_OUTPUT: str = join(output, "items")
        self.WEAPON_OUTPUT: str = join(output, "weapons")
        self.ARMOR_OUTPUT: str = join(output, "armor")
        self.SPELL_OUTPUT: str = join(output, "spells")
        self.MISSING: str = join(output, "missing")
        self.MISSING_ITEMS: str = join(self.MISSING, "items.json")
        self.MISSING_SPELLS: str = join(self.MISSING, "spells.json")
        self.CACHE: str = join(ROOT, "cache")
        self.ITEM_CACHE: str = join(self.CACHE, "itemCache.json")
        self.SPELL_CACHE: str = join(self.CACHE, "spellCache.json")


PATHS = _PathConstants()


# =============
# = CHANGEABLE
# =============


# = Font Styling =
class _FontColors:
    def __init__(self, primary: bool = True) -> None:
        self.BLUE_INK: tuple[int, int, int, int] = toRGBA("#00053b" if primary else "#ffffff")
        self.TITLE: tuple[int, int, int, int] = self.BLUE_INK
        self.PRICE: tuple[int, int, int, int] = self.BLUE_INK
        self.STATS: tuple[int, int, int, int] = self.BLUE_INK


class _FontSizes:
    def __init__(self) -> None:
        self.TITLE: int = 50 * 4
        self.PRICE: int = 50 * 4
        self.STATS: int = 18 * 4


class _FontStyling:
    def __init__(self, primary: bool = True) -> None:
        self.COLORS: _FontColors = _FontColors(primary)
        self.SIZES: _FontSizes = _FontSizes()


FONT_STYLE = _FontStyling()
SECONDARY_FONT_STYLE = _FontStyling(primary=False)


# = Items =
class _Position:
    def __init__(
        self, relative: tuple[float, float], absolute: tuple[int, int]
    ) -> None:
        self.RELATIVE: tuple[float, float] = relative
        self.ABSOLUTE: tuple[int, int] = absolute


class _Size:
    def __init__(
        self, relative: tuple[float, float], absolute: tuple[int, int]
    ) -> None:
        self.RELATIVE: tuple[float, float] = relative
        self.ABSOLUTE: tuple[int, int] = absolute


class LayoutElement:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        rel_pos = (x / CARD.RESOLUTION[0], y / CARD.RESOLUTION[1])
        rel_size = (width / CARD.RESOLUTION[0], height / CARD.RESOLUTION[1])
        abs_pos = twoDTruncate(rel_pos, CARD.RESOLUTION)
        abs_size = twoDTruncate(rel_size, CARD.RESOLUTION)

        self.POSITION: _Position = _Position(rel_pos, abs_pos)
        self.SIZE: _Size = _Size(rel_size, abs_size)


class _ItemConstants:
    def __init__(self) -> None:
        self.TITLE: LayoutElement = LayoutElement(885, 275, 1000, 275)
        self.PRICE: LayoutElement = LayoutElement(1460, 580, 350, 250)
        self.STATS: LayoutElement = LayoutElement(300, 1930, 1350, 350)
        self.IMAGE: LayoutElement = LayoutElement(900, 1145, 1565, 1330)


class _MaterialConstants:
    def __init__(self) -> None:
        sY = _SpellConstants.SMALLS_Y_OFFSET
        lY = _SpellConstants.LOWER_Y_OFFSET
        self.SPOKEN: LayoutElement = LayoutElement(750, 1900 + lY + sY, 125, 125)
        self.MATERIAL: LayoutElement = LayoutElement(950, 1830 + lY + sY, 250, 250)
        self.GESTURAL: LayoutElement = LayoutElement(1100, 1900 + lY + sY, 125, 125)
        self.NAME: LayoutElement = LayoutElement(925, 2050 + lY + sY, 1000, 175)
        self.COST: LayoutElement = LayoutElement(930, 1850 + lY + sY, 250, 100)


class _SpellConstants:
    SMALLS_Y_OFFSET: int = 325
    LOWER_Y_OFFSET: int = -175
    MID_Y_OFFSET: int = -75
    MID_X_OFFSET: int = 125
    def __init__(self) -> None:
        sY = _SpellConstants.SMALLS_Y_OFFSET
        mY = _SpellConstants.MID_Y_OFFSET
        # mX = _SpellConstants.MID_X_OFFSET
        lY = _SpellConstants.LOWER_Y_OFFSET
        self.TITLE: LayoutElement = LayoutElement(1000, 275, 675, 275)
        self.LEVEL: LayoutElement = LayoutElement(545, 305, 280, 280)
        self.CATEGORY: LayoutElement = LayoutElement(900, 520, 765, 130)
        self.IMAGE: LayoutElement = LayoutElement(885, 1000, 1550, 750)
        self.DURATION: LayoutElement = LayoutElement(300, 2150 + lY, 180, 180)
        self.DURATION_TEXT: LayoutElement = LayoutElement(300, 2300 + lY, 300, 130)
        # self.COOLDOWN: LayoutElement = LayoutElement(525, 1975 + lY + mY, 180, 180)
        # self.COOLDOWN_TEXT: LayoutElement = LayoutElement(525, 2125 + lY + mY, 180, 130)
        self.DAMAGE: LayoutElement = LayoutElement(1275, 1975 + lY + mY, 180, 180)
        self.DAMAGE_TEXT: LayoutElement = LayoutElement(1275, 2125 + lY + mY, 300, 130)
        self.RANGE: LayoutElement = LayoutElement(1500, 2150 + lY, 180, 180)
        self.RANGE_TEXT: LayoutElement = LayoutElement(1500, 2300 + lY, 300, 130)
        self.MATERIAL: _MaterialConstants = _MaterialConstants()
        self.CONCENTRATION: LayoutElement = LayoutElement(750, 1775 + lY + sY, 125, 125)
        self.CAST_TIME: LayoutElement = LayoutElement(525, 1975 + lY + mY, 180, 180)
        self.CAST_TIME_TEXT: LayoutElement = LayoutElement(525, 2125 + lY + mY, 300, 130)
        self.RITUAL: LayoutElement = LayoutElement(1100, 1775 + lY + sY, 125, 125)
        self.SAVING_THROW: LayoutElement = LayoutElement(1275, 1750 + lY, 200, 90)
        self.SUB_RANGE: LayoutElement = LayoutElement(925, 1925 + lY, 250, 100)
        self.TARGET: LayoutElement = LayoutElement(925, 1800 + lY, 200, 200)
        self.OVERLEVEL: LayoutElement = LayoutElement(
            1600, 1375 + lY, 150, 950
        )  # for later use


ITEM = _ItemConstants()
SPELL = _SpellConstants()

# = Text Constants =
from classes.textKeys import PrefixText


class _TextConstants:
    def __init__(self) -> None:
        self.WEIGHT_PREFIX = PrefixText.WEIGHT_PREFIX
        self.WEIGHT_SUFFIX = PrefixText.WEIGHT_SUFFIX
        self.DAMAGE_PREFIX = PrefixText.DAMAGE_PREFIX
        self.DEX_MAX_PREFIX = PrefixText.DEX_MAX_PREFIX
        self.STRENGTH_REQ_PREFIX = PrefixText.STRENGTH_REQ_PREFIX
        self.STEALTH_DISADVANTAGE = PrefixText.STEALTH_DISADVANTAGE
        self.DAMAGE_SPLIT: str = "D"
        self.DAMAGE_SUFFIX: str = ""


TEXT = _TextConstants()

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
        self.RESOLUTION: tuple[int, int] = (356, 497)  # (x, y)

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
        # Semantic aliases for specific uses
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
        self.SPELLS: str = join(assets, "spells")
        self.BACKGROUND: str = join(assets, "background")
        # icon used for application windows
        self.APP_ICON: str = join(self.SPELLS, "feuerball.png")

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
        self.SPELL_OUTPUT: str = join(output, "spells")
        self.CACHE: str = join(ROOT, "cache")
        self.ITEM_CACHE: str = join(self.CACHE, "itemCache.json")
        self.SPELL_CACHE: str = join(self.CACHE, "spellCache.json")

PATHS = _PathConstants()



# =============
# = CHANGEABLE
# =============

# = Font Styling =
class _FontColors:
    def __init__(self) -> None:
        self.BLUE_INK: tuple[int, int, int, int] = toRGBA("#00053b")
        self.TITLE: tuple[int, int, int, int] = self.BLUE_INK
        self.PRICE: tuple[int, int, int, int] = self.BLUE_INK
        self.STATS: tuple[int, int, int, int] = self.BLUE_INK

class _FontSizes:
    def __init__(self) -> None:
        self.TITLE: int = 50
        self.PRICE: int = 50
        self.STATS: int = 18

class _FontStyling:
    def __init__(self) -> None:
        self.COLORS: _FontColors = _FontColors()
        self.SIZES: _FontSizes = _FontSizes()

FONT_STYLE = _FontStyling()

# = Items =
class _Position:
    def __init__(self, relative: tuple[float, float], absolute: tuple[int, int]) -> None:
        self.RELATIVE: tuple[float, float] = relative
        self.ABSOLUTE: tuple[int, int] = absolute

class _Size:
    def __init__(self, relative: tuple[float, float], absolute: tuple[int, int]) -> None:
        self.RELATIVE: tuple[float, float] = relative
        self.ABSOLUTE: tuple[int, int] = absolute

class _LayoutElement:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        rel_pos = (x / 356, y / 497)
        rel_size = (width / 356, height / 497)
        abs_pos = twoDTruncate(rel_pos, CARD.RESOLUTION)
        abs_size = twoDTruncate(rel_size, CARD.RESOLUTION)

        self.POSITION: _Position = _Position(rel_pos, abs_pos)
        self.SIZE: _Size = _Size(rel_size, abs_size)

class _ItemConstants:
    def __init__(self) -> None:
        self.TITLE: _LayoutElement = _LayoutElement(177, 55, 200, 55)
        self.PRICE: _LayoutElement = _LayoutElement(292, 116, 70, 50)
        self.STATS: _LayoutElement = _LayoutElement(60, 386, 270, 70)
        self.IMAGE: _LayoutElement = _LayoutElement(180, 229, 313, 266)


class _MaterialConstants:
    def __init__(self) -> None:
        sY = _SpellConstants.SMALLS_Y_OFFSET
        self.SPOKEN: _LayoutElement = _LayoutElement(150, 380+sY, 25, 25)
        self.MATERIAL: _LayoutElement = _LayoutElement(185, 380+sY, 25, 25)
        self.GESTURAL: _LayoutElement = _LayoutElement(220, 380+sY, 25, 25)
        self.NAME: _LayoutElement = _LayoutElement(185, 400+sY, 100, 18)
        self.COST: _LayoutElement = _LayoutElement(185, 420+sY, 75, 20)

class _SpellConstants:
    SMALLS_Y_OFFSET: int = 60
    MID_Y_OFFSET: int = -15
    def __init__(self) -> None:
        sY = _SpellConstants.SMALLS_Y_OFFSET
        mY = _SpellConstants.MID_Y_OFFSET
        self.TITLE: _LayoutElement = _LayoutElement(200, 55, 135, 55)
        self.LEVEL: _LayoutElement = _LayoutElement(109, 61, 56, 56)
        self.CATEGORY: _LayoutElement = _LayoutElement(180, 104, 153, 26)
        self.IMAGE: _LayoutElement = _LayoutElement(177, 240, 310, 190)
        self.DURATION: _LayoutElement = _LayoutElement(60, 430, 36, 36)
        self.DURATION_TEXT: _LayoutElement = _LayoutElement(60, 460, 36, 26)
        self.COOLDOWN: _LayoutElement = _LayoutElement(105, 395+mY, 36, 36)
        self.COOLDOWN_TEXT: _LayoutElement = _LayoutElement(105, 425+mY, 36, 26)
        self.DAMAGE: _LayoutElement = _LayoutElement(255, 395+mY, 36, 36)
        self.DAMAGE_TEXT: _LayoutElement = _LayoutElement(255, 425+mY, 36, 26)
        self.RANGE: _LayoutElement = _LayoutElement(300, 430, 36, 36)
        self.RANGE_TEXT: _LayoutElement = _LayoutElement(300, 460, 36, 26)
        self.MATERIAL: _MaterialConstants = _MaterialConstants()
        self.CONCENTRATION: _LayoutElement = _LayoutElement(150, 355+sY, 25, 25)
        self.CAST_TIME: _LayoutElement = _LayoutElement(185, 355+sY, 25, 25)
        self.RITUAL: _LayoutElement = _LayoutElement(220, 355+sY, 25, 25)
        self.SAVING_THROW: _LayoutElement = _LayoutElement(260, 365, 40, 18)
        self.SUB_RANGE: _LayoutElement = _LayoutElement(185, 385, 50, 20)
        self.TARGET: _LayoutElement = _LayoutElement(185, 360, 40, 40)
        self.OVERLEVEL: _LayoutElement = _LayoutElement(320, 275, 30, 190) # for later use

ITEM = _ItemConstants()
SPELL = _SpellConstants()

# = Text Constants =
from classes.textKeys import PrefixText

class _TextConstants:
    def __init__(self) -> None:
        self.WEIGHT_PREFIX = PrefixText.WEIGHT_PREFIX
        self.WEIGHT_SUFFIX = PrefixText.WEIGHT_SUFFIX
        self.DAMAGE_PREFIX = PrefixText.DAMAGE_PREFIX
        self.DAMAGE_SPLIT: str = "D"
        self.DAMAGE_SUFFIX: str = ""

TEXT = _TextConstants()
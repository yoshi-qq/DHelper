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

class _BackgroundImages:
    def __init__(self) -> None:
        bg_path = join(SRC, "assets", "background")
        self.GOLD_ITEM: str = join(bg_path, "item_gold_template.png")
        self.SILVER_ITEM: str = join(bg_path, "item_silver_template.png")
        self.COPPER_ITEM: str = join(bg_path, "item_copper_template.png")

class _ImageConstants:
    def __init__(self) -> None:
        self.FORMAT: str = "png"
        self.PATHS: _ImagePaths = _ImagePaths()
        self.BACKGROUNDS: _BackgroundImages = _BackgroundImages()

IMAGE = _ImageConstants()

# = Data Paths =
class _DataPaths:
    def __init__(self) -> None:
        data = join(ROOT, "data")
        self.DIRECTORY: str = data
        self.ITEMS: str = join(data, "items.json")
        self.SPELLS: str = join(data, "spells.json")

DATA = _DataPaths()

# = Output & Cache Paths =
class _PathConstants:
    def __init__(self) -> None:
        self.OUTPUT: str = join(ROOT, "output")
        self.CACHE: str = join(ROOT, "cache")
        self.ITEM_CACHE: str = join(ROOT, "cache", "itemCache.json")

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
        self.TITLE: _LayoutElement = _LayoutElement(177, 55, 200, 55)     # Title text area
        self.PRICE: _LayoutElement = _LayoutElement(292, 116, 70, 50)     # Price text area  
        self.STATS: _LayoutElement = _LayoutElement(60, 386, 270, 70)     # Stats/description text area
        self.IMAGE: _LayoutElement = _LayoutElement(180, 229, 313, 266)   # Item image area

ITEM = _ItemConstants()

# Backward compatibility constants (keeping old names for existing code)
ITEM_RELATIVE_TITLE_POSITION: tuple[float, float] = ITEM.TITLE.POSITION.RELATIVE
ITEM_RELATIVE_TITLE_SIZE: tuple[float, float] = ITEM.TITLE.SIZE.RELATIVE
ITEM_ABSOLUTE_TITLE_POSITION: tuple[int, int] = ITEM.TITLE.POSITION.ABSOLUTE
ITEM_ABSOLUTE_TITLE_SIZE: tuple[int, int] = ITEM.TITLE.SIZE.ABSOLUTE

ITEM_RELATIVE_PRICE_POSITION: tuple[float, float] = ITEM.PRICE.POSITION.RELATIVE
ITEM_RELATIVE_PRICE_SIZE: tuple[float, float] = ITEM.PRICE.SIZE.RELATIVE
ITEM_ABSOLUTE_PRICE_POSITION: tuple[int, int] = ITEM.PRICE.POSITION.ABSOLUTE
ITEM_ABSOLUTE_PRICE_SIZE: tuple[int, int] = ITEM.PRICE.SIZE.ABSOLUTE

ITEM_RELATIVE_STATS_POSITION: tuple[float, float] = ITEM.STATS.POSITION.RELATIVE
ITEM_RELATIVE_STATS_SIZE: tuple[float, float] = ITEM.STATS.SIZE.RELATIVE
ITEM_ABSOLUTE_STATS_POSITION: tuple[int, int] = ITEM.STATS.POSITION.ABSOLUTE
ITEM_ABSOLUTE_STATS_SIZE: tuple[int, int] = ITEM.STATS.SIZE.ABSOLUTE

ITEM_RELATIVE_IMAGE_POSITION: tuple[float, float] = ITEM.IMAGE.POSITION.RELATIVE
ITEM_RELATIVE_IMAGE_MAX_SIZE: tuple[float, float] = ITEM.IMAGE.SIZE.RELATIVE
ITEM_ABSOLUTE_IMAGE_POSITION: tuple[int, int] = ITEM.IMAGE.POSITION.ABSOLUTE
ITEM_ABSOLUTE_IMAGE_MAX_SIZE: tuple[int, int] = ITEM.IMAGE.SIZE.ABSOLUTE

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
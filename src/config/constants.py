from os.path import join, dirname
from helpers.tupleHelper import twoDTruncate
from helpers.conversionHelper import toRGBA


# =============
# = CONSTANT
# =============
SRC = dirname(dirname(__file__))
ROOT = dirname(SRC)

# = Card =
# (x, y)
CARD_RESOLUTION: tuple[int, int] = (356, 497)

# = Font Paths =
FONTS_FOLDER_PATH = join(SRC, "fonts")
REGULAR_FONT_PATH = join(FONTS_FOLDER_PATH, "timesbd.ttf")
BOLD_FONT_PATH = join(FONTS_FOLDER_PATH, "timesbd.ttf")
ITALIC_FONT_PATH = join(FONTS_FOLDER_PATH, "timesi.ttf")
BOLD_ITALIC_FONT_PATH = join(FONTS_FOLDER_PATH, "timesbi.ttf")
FONT_PATHS = {
    "regular": REGULAR_FONT_PATH,
    "bold": BOLD_FONT_PATH,
    "italic": ITALIC_FONT_PATH,
    "boldItalic": BOLD_ITALIC_FONT_PATH
}

TITLE_FONT_PATH = FONT_PATHS["boldItalic"]
PRICE_FONT_PATH = FONT_PATHS["bold"]
STATS_FONT_PATH = FONT_PATHS["bold"]

# = Image Paths =
IMAGE_FORMAT = "png"
ASSETS_PATH = join(SRC, "assets")
ITEM_IMAGES_PATH = join(ASSETS_PATH, "items")
SPELLS_IMAGES_PATH = join(ASSETS_PATH, "spells")

BACKGROUND_PATH = join(ASSETS_PATH, "background")
GOLD_ITEM_BACKGROUND = join(BACKGROUND_PATH, "item_gold_template.png")
SILVER_ITEM_BACKGROUND = join(BACKGROUND_PATH, "item_silver_template.png")
COPPER_ITEM_BACKGROUND = join(BACKGROUND_PATH, "item_copper_template.png")

# = Data Paths =
DATA_PATH = join(ROOT, "data")

ITEMS_LIST_PATH = join(DATA_PATH, "items.json")
SPELLS_LIST_PATH = join(DATA_PATH, "spells.json")

# = Paths =
OUTPUT_PATH = join(ROOT, "output")



# =============
# = CHANGEABLE
# =============

# = Font =
BLUE_INK_COLOR = toRGBA("#00053b")
TITLE_FONT_COLOR = BLUE_INK_COLOR
PRICE_FONT_COLOR = BLUE_INK_COLOR
STATS_FONT_COLOR = BLUE_INK_COLOR
TITLE_FONT_SIZE = 50
PRICE_FONT_SIZE = 50
STATS_FONT_SIZE = 18

# = Items =
# - Text Positions
ITEM_RELATIVE_TITLE_POSITION: tuple[float, float] = (177/356, 55/497)
ITEM_RELATIVE_TITLE_SIZE: tuple[float, float] = (200/356, 55/497)
ITEM_ABSOLUTE_TITLE_POSITION: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_TITLE_POSITION, CARD_RESOLUTION)
ITEM_ABSOLUTE_TITLE_SIZE: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_TITLE_SIZE, CARD_RESOLUTION)

ITEM_RELATIVE_PRICE_POSITION: tuple[float, float] = (292/356, 116/497)
ITEM_RELATIVE_PRICE_SIZE: tuple[float, float] = (70/356, 50/497)
ITEM_ABSOLUTE_PRICE_POSITION: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_PRICE_POSITION, CARD_RESOLUTION)
ITEM_ABSOLUTE_PRICE_SIZE: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_PRICE_SIZE, CARD_RESOLUTION)

ITEM_RELATIVE_STATS_POSITION: tuple[float, float] = (60/356, 386/497)
ITEM_RELATIVE_STATS_SIZE: tuple[float, float] = (270/356, 70/497)
ITEM_ABSOLUTE_STATS_POSITION: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_STATS_POSITION, CARD_RESOLUTION)
ITEM_ABSOLUTE_STATS_SIZE: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_STATS_SIZE, CARD_RESOLUTION)

ITEM_RELATIVE_IMAGE_POSITION: tuple[float, float] = (180/356, 229/497)
ITEM_RELATIVE_IMAGE_MAX_SIZE: tuple[float, float] = (313/356, 266/497)
ITEM_ABSOLUTE_IMAGE_POSITION: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_IMAGE_POSITION, CARD_RESOLUTION)
ITEM_ABSOLUTE_IMAGE_MAX_SIZE: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_IMAGE_MAX_SIZE, CARD_RESOLUTION)

# = Text =
WEIGHT_PREFIX =  "Gewicht: "
WEIGHT_SUFFIX = " kg"
DAMAGE_PREFIX = "Schaden: "
DAMAGE_SPLIT = "D"
DAMAGE_SUFFIX = ""

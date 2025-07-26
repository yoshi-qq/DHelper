from os.path import join
from helpers.tupleHelper import twoDTruncate
# =============
# = CONSTANT
# =============

# = Image Paths =
IMAGE_FORMAT = "png"
ASSETS_PATH = "assets"
ITEM_IMAGES_PATH = join(ASSETS_PATH, "items")
SPELLS_IMAGES_PATH = join(ASSETS_PATH, "spells")

BACKGROUND_PATH = join(ASSETS_PATH, "background")
GOLD_ITEM_BACKGROUND = join(BACKGROUND_PATH, "item_gold_template.png")
SILVER_ITEM_BACKGROUND = join(BACKGROUND_PATH, "item_silver_template.png")
COPPER_ITEM_BACKGROUND = join(BACKGROUND_PATH, "item_copper_template.png")

# = Data Paths =
DATA_PATH = "data"

ITEMS_LIST_PATH = join(DATA_PATH, "items.json")
SPELLS_LIST_PATH = join(DATA_PATH, "spells.json")

# = Paths =
OUTPUT_PATH = "output"

# =============
# = CHANGEABLE
# =============

# (x, y)
CARD_RESOLUTION: tuple[int, int] = (356, 497)

# = Items =
# - Text Positions
ITEM_RELATIVE_TITLE_POSITION: tuple[float, float] = (177/356, 60/497)
ITEM_RELATIVE_TITLE_SIZE: tuple[float, float] = (200/356, 55/497)
ITEM_ABSOLUTE_TITLE_POSITION: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_TITLE_POSITION, CARD_RESOLUTION)
ITEM_ABSOLUTE_TITLE_SIZE: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_TITLE_SIZE, CARD_RESOLUTION)

ITEM_RELATIVE_COST_POSITION: tuple[float, float] = (292/356, 130/497)
ITEM_RELATIVE_COST_SIZE: tuple[float, float] = (70/356, 50/497)
ITEM_ABSOLUTE_COST_POSITION: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_COST_POSITION, CARD_RESOLUTION)
ITEM_ABSOLUTE_COST_SIZE: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_COST_SIZE, CARD_RESOLUTION)

ITEM_RELATIVE_STATS_POSITION: tuple[float, float] = (60/356, 425/497)
ITEM_RELATIVE_STATS_SIZE: tuple[float, float] = (270/356, 70/497)
ITEM_ABSOLUTE_STATS_POSITION: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_STATS_POSITION, CARD_RESOLUTION)
ITEM_ABSOLUTE_STATS_SIZE: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_STATS_SIZE, CARD_RESOLUTION)

ITEM_RELATIVE_IMAGE_POSITION: tuple[float, float] = (180/356, 229/497)
ITEM_RELATIVE_IMAGE_MAX_SIZE: tuple[float, float] = (313/356, 266/497)
ITEM_ABSOLUTE_IMAGE_POSITION: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_IMAGE_POSITION, CARD_RESOLUTION)
ITEM_ABSOLUTE_IMAGE_MAX_SIZE: tuple[int, int] = twoDTruncate(ITEM_RELATIVE_IMAGE_MAX_SIZE, CARD_RESOLUTION)
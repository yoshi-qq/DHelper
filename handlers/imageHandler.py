from config.constants import GOLD_ITEM_BACKGROUND, IMAGE_FORMAT, ITEM_ABSOLUTE_IMAGE_MAX_SIZE, ITEM_ABSOLUTE_IMAGE_POSITION, OUTPUT_PATH, SILVER_ITEM_BACKGROUND, COPPER_ITEM_BACKGROUND, ITEM_IMAGES_PATH
from classes.types import Item
from helpers.dataHelper import getItems
from os.path import join
from PIL import Image
from PIL.Image import Resampling

from helpers.tupleHelper import twoDSub, twoDTruncate

class ImageHandler:
    def __init__(self) -> None:
        pass
    def createImage(self, item: Item) -> None:
        backgroundPath = GOLD_ITEM_BACKGROUND if item.cost % 1 == 0 else SILVER_ITEM_BACKGROUND if item.cost % 10 == 0 else COPPER_ITEM_BACKGROUND
        bg = Image.open(backgroundPath).convert("RGBA")
        overlayPath = join(ITEM_IMAGES_PATH, item.id)
        overlay = Image.open(f"{overlayPath}.{IMAGE_FORMAT}").convert("RGBA")
        overlaySize = overlay.size

        maxWidth, maxHeight = ITEM_ABSOLUTE_IMAGE_MAX_SIZE
        origWidth, origHeight = overlay.size
        ratio = min(maxWidth / origWidth, maxHeight / origHeight)
        width = int(origWidth * ratio)
        height = int(origHeight * ratio)
        x, y = twoDSub(ITEM_ABSOLUTE_IMAGE_POSITION, twoDTruncate((width, height), (1/2, 1/2)))

        overlay_resized = overlay.resize((width, height), resample=Resampling.LANCZOS)

        bg.paste(overlay_resized, (x, y), mask=overlay_resized)

        bg.save(join(OUTPUT_PATH, f"{item.id}.png"))

    def createImages(self) -> None:
        items: list[Item] = getItems()
        for item in items:
            self.createImage(item)
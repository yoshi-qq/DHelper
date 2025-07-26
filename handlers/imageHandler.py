from config.constants import BLUE_INK_COLOR, GOLD_ITEM_BACKGROUND, IMAGE_FORMAT, ITEM_ABSOLUTE_IMAGE_MAX_SIZE, ITEM_ABSOLUTE_IMAGE_POSITION, ITEM_ABSOLUTE_PRICE_POSITION, OUTPUT_PATH, PRICE_FONT_SIZE, SILVER_ITEM_BACKGROUND, COPPER_ITEM_BACKGROUND, ITEM_IMAGES_PATH, HEADING_FONT_PATH, PRICE_FONT_PATH
from classes.types import Currency, Item
from helpers.dataHelper import getItems
from os.path import join
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Resampling

from helpers.tupleHelper import twoDSub, twoDTruncate

class ImageHandler:
    def __init__(self) -> None:
        pass
    def createItemImage(self, item: Item) -> None:
        # Currency Matching
        if item.price % 1 == 0:
            currency = Currency.GOLD
        elif item.price % 10 == 1:
            currency = Currency.SILVER
        else:
            currency = Currency.COPPER

        # Background
        match currency:
            case Currency.GOLD:
                backgroundPath = GOLD_ITEM_BACKGROUND
            case Currency.SILVER:
                backgroundPath = SILVER_ITEM_BACKGROUND
            case Currency.COPPER:
                backgroundPath = SILVER_ITEM_BACKGROUND
        bg = Image.open(backgroundPath).convert("RGBA")

        # Image
        imagePath = join(ITEM_IMAGES_PATH, item.id)
        image = Image.open(f"{imagePath}.{IMAGE_FORMAT}").convert("RGBA")
        imageSize = image.size
        maxWidth, maxHeight = ITEM_ABSOLUTE_IMAGE_MAX_SIZE
        originWidth, originHeight = image.size
        ratio = min(maxWidth / originWidth, maxHeight / originHeight)
        width = int(originWidth * ratio)
        height = int(originHeight * ratio)
        imageX, imageY = twoDSub(ITEM_ABSOLUTE_IMAGE_POSITION, twoDTruncate((width, height), (1/2, 1/2)))
        resizedImage = image.resize((width, height), resample=Resampling.LANCZOS)

        # Price
        draw = ImageDraw.Draw(bg)
        priceText = str(int(item.price/currency.value))
        priceX, priceY = ITEM_ABSOLUTE_PRICE_POSITION
        priceFont = ImageFont.truetype(PRICE_FONT_PATH, PRICE_FONT_SIZE)
        # Text Size
        bbox = draw.textbbox((0, 0), priceText, font=priceFont)
        priceWidth = bbox[2] - bbox[0]
        priceHeight = bbox[3] - bbox[1]
        draw.text((priceX-priceWidth/2, priceY-priceHeight/2), priceText, font=priceFont, fill=BLUE_INK_COLOR)


        # Combination
        bg.paste(resizedImage, (imageX, imageY), mask=resizedImage)
        # Export
        bg.save(join(OUTPUT_PATH, f"{item.id}.png"))

    def createItemImages(self) -> None:
        items: list[Item] = getItems()
        for item in items:
            self.createItemImage(item)
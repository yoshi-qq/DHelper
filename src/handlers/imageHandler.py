from config.constants import BLUE_INK_COLOR, GOLD_ITEM_BACKGROUND, IMAGE_FORMAT, ITEM_ABSOLUTE_IMAGE_MAX_SIZE, ITEM_ABSOLUTE_IMAGE_POSITION, ITEM_ABSOLUTE_PRICE_POSITION, ITEM_ABSOLUTE_TITLE_POSITION, ITEM_ABSOLUTE_TITLE_SIZE, OUTPUT_PATH, PRICE_FONT_SIZE, SILVER_ITEM_BACKGROUND, COPPER_ITEM_BACKGROUND, ITEM_IMAGES_PATH, TITLE_FONT_PATH, PRICE_FONT_PATH, TITLE_FONT_SIZE
from classes.types import Currency, Item
from helpers.dataHelper import getItems
from os.path import join
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Resampling

from helpers.tupleHelper import twoDSub, twoDTruncate

class ImageHandler:
    def __init__(self) -> None:
        pass
    def createItemCard(self, item: Item) -> None:
        def getCurrency(price: float) -> Currency:
            if price % 1 == 0:
                return Currency.GOLD
            elif price % 10 == 1:
                return Currency.SILVER
            else:
                return Currency.COPPER

        def createBackground(currency: Currency) -> Image.Image:
            match currency:
                case Currency.GOLD:
                    backgroundPath = GOLD_ITEM_BACKGROUND
                case Currency.SILVER:
                    backgroundPath = SILVER_ITEM_BACKGROUND
                case Currency.COPPER:
                    backgroundPath = SILVER_ITEM_BACKGROUND
            return Image.open(backgroundPath).convert("RGBA")

        def addImage(background: Image.Image, id: str) -> None:
            imagePath = join(ITEM_IMAGES_PATH, id) # ! TODO: Error Handling
            image = Image.open(f"{imagePath}.{IMAGE_FORMAT}").convert("RGBA")
            imageSize = image.size
            maxWidth, maxHeight = ITEM_ABSOLUTE_IMAGE_MAX_SIZE
            originWidth, originHeight = image.size
            ratio = min(maxWidth / originWidth, maxHeight / originHeight)
            width = int(originWidth * ratio)
            height = int(originHeight * ratio)
            imageX, imageY = twoDSub(ITEM_ABSOLUTE_IMAGE_POSITION, twoDTruncate((width, height), (1/2, 1/2)))
            resizedImage = image.resize((width, height), resample=Resampling.LANCZOS)
            background.paste(resizedImage, (imageX, imageY), mask=resizedImage)

        def addPrice(background: Image.Image, price: float, currency: Currency) -> None:
            draw = ImageDraw.Draw(background)
            priceText = str(int(price/currency.value))
            priceX, priceY = ITEM_ABSOLUTE_PRICE_POSITION
            priceFont = ImageFont.truetype(PRICE_FONT_PATH, PRICE_FONT_SIZE)
            # Text Size
            bbox = draw.textbbox((0, 0), priceText, font=priceFont)
            priceWidth = bbox[2] - bbox[0]
            priceHeight = bbox[3] - bbox[1]
            draw.text((priceX-priceWidth/2, priceY-priceHeight/2), priceText, font=priceFont, fill=BLUE_INK_COLOR)

        def addTitle(background: Image.Image, title: str) -> None:
            def getMaxFontSize(text: str, fontPath: str, maxSize: int, maxWidth: float, maxHeight: float = float("inf")) -> int:
                size = maxSize
                for size in range(maxSize, 1, -1):
                    testFont = ImageFont.truetype(fontPath, size)
                    bbox = draw.textbbox((0, 0), text, font=testFont)
                    testWidth = bbox[2] - bbox[0]
                    testHeight = bbox[3] - bbox[1]
                    if testWidth < maxWidth and testHeight < maxHeight:
                        break
                return size

            draw = ImageDraw.Draw(background)
            titleX, titleY = ITEM_ABSOLUTE_TITLE_POSITION
            titleFont = ImageFont.truetype(TITLE_FONT_PATH, getMaxFontSize(title, TITLE_FONT_PATH, TITLE_FONT_SIZE, ITEM_ABSOLUTE_TITLE_SIZE[0]))
            # Text Size
            bbox = draw.textbbox((0, 0), title, font=titleFont)
            titleWidth = bbox[2] - bbox[0]
            titleHeight = bbox[3] - bbox[1]
            draw.text((titleX-titleWidth/2, titleY-titleHeight/2), title, font=titleFont, fill=BLUE_INK_COLOR)

        currency = getCurrency(item.price)
        cardImage = createBackground(currency)
        addImage(cardImage, item.id)
        addPrice(cardImage, item.price, currency)
        addTitle(cardImage, item.name)

        # Export
        cardImage.save(join(OUTPUT_PATH, f"{item.id}.png"))

    def createItemCards(self) -> None:
        items: list[Item] = getItems()
        for item in items:
            self.createItemCard(item)
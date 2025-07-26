from typing import Optional
from config.constants import BLUE_INK_COLOR, DAMAGE_PREFIX, DAMAGE_SPLIT, GOLD_ITEM_BACKGROUND, IMAGE_FORMAT, ITEM_ABSOLUTE_IMAGE_MAX_SIZE, ITEM_ABSOLUTE_IMAGE_POSITION, ITEM_ABSOLUTE_PRICE_POSITION, ITEM_ABSOLUTE_STATS_POSITION, ITEM_ABSOLUTE_STATS_SIZE, ITEM_ABSOLUTE_TITLE_POSITION, ITEM_ABSOLUTE_TITLE_SIZE, OUTPUT_PATH, PRICE_FONT_SIZE, SILVER_ITEM_BACKGROUND, COPPER_ITEM_BACKGROUND, ITEM_IMAGES_PATH, STATS_FONT_PATH, STATS_FONT_SIZE, TITLE_FONT_PATH, PRICE_FONT_PATH, TITLE_FONT_SIZE, WEIGHT_PREFIX, WEIGHT_SUFFIX
from classes.types import AttributeType, Currency, Damage, Item
from helpers.dataHelper import getItems
from helpers.formattingHelper import getMaxFontSize
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
            draw = ImageDraw.Draw(background)
            titleX, titleY = ITEM_ABSOLUTE_TITLE_POSITION
            titleFont = ImageFont.truetype(TITLE_FONT_PATH, getMaxFontSize(title, TITLE_FONT_PATH, TITLE_FONT_SIZE, ITEM_ABSOLUTE_TITLE_SIZE[0]))
            # Text Size
            bbox = draw.textbbox((0, 0), title, font=titleFont)
            titleWidth = bbox[2] - bbox[0]
            titleHeight = bbox[3] - bbox[1]
            draw.text((titleX-titleWidth/2, titleY-titleHeight/2), title, font=titleFont, fill=BLUE_INK_COLOR)

        def addStats(background: Image.Image, weight: float, damage: Optional[Damage], attributes: list[AttributeType]) -> None:
            rows: list[str] = []
            rows.append(f"{WEIGHT_PREFIX}{weight}{WEIGHT_SUFFIX}")
            if damage:
                diceString = f"{damage.diceAmount}{DAMAGE_SPLIT}{damage.diceType}" if damage.diceAmount > 0 else ""
                bonusString = "" if damage.bonus == 0 else str(damage.bonus) if not diceString else f" {'+' if damage.bonus > 0 else ""}{damage.bonus}"
                rows.append(f"{DAMAGE_PREFIX}{diceString}{bonusString} {damage.damageType}")
            attributesString = attributes[0] if attributes else ""
            for attribute in attributes[1:]:
                attributesString += f", {attribute}"
            rows.append(attributesString)
            statsString = "\n".join(rows)

            draw = ImageDraw.Draw(background)
            statsX, statsY = ITEM_ABSOLUTE_STATS_POSITION
            statsFont = ImageFont.truetype(STATS_FONT_PATH, getMaxFontSize(statsString, STATS_FONT_PATH, STATS_FONT_SIZE, ITEM_ABSOLUTE_STATS_SIZE[0]))
            # Text Size
            bbox = draw.textbbox((0, 0), statsString, font=statsFont)
            statsWidth = bbox[2] - bbox[0]
            statsHeight = bbox[3] - bbox[1]
            draw.text((statsX, statsY), statsString, font=statsFont, fill=BLUE_INK_COLOR)


        currency = getCurrency(item.price)
        cardImage = createBackground(currency)
        addImage(cardImage, item.id)
        addPrice(cardImage, item.price, currency)
        addTitle(cardImage, item.name)
        addStats(cardImage, item.weight, item.damage, item.attributes)

        # Export
        cardImage.save(join(OUTPUT_PATH, f"{item.id}.png"))

    def createItemCards(self) -> None:
        items: list[Item] = getItems()
        for item in items:
            self.createItemCard(item)
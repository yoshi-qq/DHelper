from typing import Optional
import os
from config.constants import (
    BLUE_INK_COLOR,
    DAMAGE_PREFIX,
    DAMAGE_SPLIT,
    GOLD_ITEM_BACKGROUND,
    IMAGE_FORMAT,
    ITEM_ABSOLUTE_IMAGE_MAX_SIZE,
    ITEM_ABSOLUTE_IMAGE_POSITION,
    ITEM_ABSOLUTE_PRICE_POSITION,
    ITEM_ABSOLUTE_STATS_POSITION,
    ITEM_ABSOLUTE_STATS_SIZE,
    ITEM_ABSOLUTE_TITLE_POSITION,
    ITEM_ABSOLUTE_TITLE_SIZE,
    OUTPUT_PATH,
    PRICE_FONT_SIZE,
    SILVER_ITEM_BACKGROUND,
    COPPER_ITEM_BACKGROUND,
    ITEM_IMAGES_PATH,
    STATS_FONT_PATH,
    STATS_FONT_SIZE,
    TITLE_FONT_PATH,
    PRICE_FONT_PATH,
    TITLE_FONT_SIZE,
    WEIGHT_PREFIX,
    WEIGHT_SUFFIX,
)
from classes.types import AttributeType, Currency, Damage, Item
from helpers.dataHelper import getItems
from helpers.formattingHelper import getMaxFontSize, findOptimalAttributeLayout
from os.path import join
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Resampling, Transpose

from helpers.tupleHelper import twoDSub, twoDTruncate

class ImageHandler:
    def __init__(self) -> None:
        pass

    def createItemCard(
        self,
        item: Item,
        rotate: float = 0,
        flip: bool = False,
        scale: float = 1.0,
    ) -> None:
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

        def addImage(background: Image.Image, id: str, rotate: float, flip: bool, scale: float) -> None:
            imagePath = join(ITEM_IMAGES_PATH, id)
            if not os.path.exists(f"{imagePath}.{IMAGE_FORMAT}"):
                raise FileNotFoundError(imagePath)
            image = Image.open(f"{imagePath}.{IMAGE_FORMAT}").convert("RGBA")
            if flip:
                image = image.transpose(Transpose.FLIP_LEFT_RIGHT)
            if rotate:
                image = image.rotate(rotate, expand=True, resample=Resampling.BICUBIC)

            maxWidth, maxHeight = ITEM_ABSOLUTE_IMAGE_MAX_SIZE
            originWidth, originHeight = image.size
            ratio = min(maxWidth / originWidth, maxHeight / originHeight) * scale
            width = int(originWidth * ratio)
            height = int(originHeight * ratio)
            imageX, imageY = twoDSub(
                ITEM_ABSOLUTE_IMAGE_POSITION, twoDTruncate((width, height), (1 / 2, 1 / 2))
            )
            resized = image.resize((width, height), resample=Resampling.LANCZOS)
            background.paste(resized, (imageX, imageY), mask=resized)

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

        def format_damage(d: Damage, with_type: bool = False) -> str:
            dice_str = f"{d.diceAmount}{DAMAGE_SPLIT}{d.diceType}" if d.diceAmount > 0 else ""
            bonus_str = "" if d.bonus == 0 else str(d.bonus) if not dice_str else f" {'+' if d.bonus > 0 else ''}{d.bonus}"
            result = f"{dice_str}{bonus_str}"
            if with_type:
                result = f"{result} {d.damageType}".strip()
            return result

        def addStats(
            background: Image.Image,
            weight: float,
            damage: Optional[Damage],
            versatile: Optional[Damage],
            attributes: list[AttributeType],
            ranges: dict[str, tuple[int, int]],
        ) -> None:
            fixedRows: list[str] = []
            fixedRows.append(f"{WEIGHT_PREFIX}{weight}{WEIGHT_SUFFIX}")
            if damage:
                fixedRows.append(f"{DAMAGE_PREFIX}{format_damage(damage, True)}")

            attr_strings: list[str] = []
            for attr in attributes:
                if attr == "Vielseitig" and versatile:
                    attr_strings.append(f"{attr} ({format_damage(versatile)})")
                elif attr in ranges:
                    low, high = ranges[attr]
                    attr_strings.append(f"{attr} ({low}/{high})")
                else:
                    attr_strings.append(str(attr))

            optimalRows, optimalFontSize = findOptimalAttributeLayout(
                attr_strings,
                fixedRows,
                STATS_FONT_PATH,
                STATS_FONT_SIZE,
                ITEM_ABSOLUTE_STATS_SIZE[0],
                ITEM_ABSOLUTE_STATS_SIZE[1],
            )
            statsString = "\n".join(optimalRows)

            draw = ImageDraw.Draw(background)
            statsX, statsY = ITEM_ABSOLUTE_STATS_POSITION
            statsFont = ImageFont.truetype(STATS_FONT_PATH, optimalFontSize)
            bbox = draw.textbbox((0, 0), statsString, font=statsFont)
            statsWidth = bbox[2] - bbox[0]
            statsHeight = bbox[3] - bbox[1]
            draw.text((statsX, statsY), statsString, font=statsFont, fill=BLUE_INK_COLOR)


        currency = getCurrency(item.price)
        cardImage = createBackground(currency)
        addImage(cardImage, item.id, rotate, flip, scale)
        addPrice(cardImage, item.price, currency)
        addTitle(cardImage, item.name)
        addStats(cardImage, item.weight, item.damage, item.versatileDamage, item.attributes, item.ranges)

        # Export
        cardImage.save(join(OUTPUT_PATH, f"{item.id}.png"))

    def createItemCards(self) -> None:
        items: list[Item] = getItems()
        for item in items:
            self.createItemCard(item)

from typing import Optional
import os
from config.constants import (
    # New hierarchical constants
    FONT_STYLE, IMAGE, ITEM, PATHS, TEXT, FONT
)
from classes.types import AttributeType, Currency, Damage, Item
from helpers.translationHelper import translate
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
                    backgroundPath = IMAGE.BACKGROUNDS.GOLD_ITEM
                case Currency.SILVER:
                    backgroundPath = IMAGE.BACKGROUNDS.SILVER_ITEM
                case Currency.COPPER:
                    backgroundPath = IMAGE.BACKGROUNDS.SILVER_ITEM
            return Image.open(backgroundPath).convert("RGBA")

        def addImage(background: Image.Image, id: str, rotate: float, flip: bool, scale: float) -> None:
            imagePath = join(IMAGE.PATHS.ITEMS, id)
            if not os.path.exists(f"{imagePath}.{IMAGE.FORMAT}"):
                raise FileNotFoundError(imagePath)
            image = Image.open(f"{imagePath}.{IMAGE.FORMAT}").convert("RGBA")
            if flip:
                image = image.transpose(Transpose.FLIP_LEFT_RIGHT)
            if rotate:
                image = image.rotate(rotate, expand=True, resample=Resampling.BICUBIC)

            maxWidth, maxHeight = ITEM.IMAGE.SIZE.ABSOLUTE
            originWidth, originHeight = image.size
            ratio = min(maxWidth / originWidth, maxHeight / originHeight) * scale
            width = int(originWidth * ratio)
            height = int(originHeight * ratio)
            imageX, imageY = twoDSub(
                ITEM.IMAGE.POSITION.ABSOLUTE, twoDTruncate((width, height), (1 / 2, 1 / 2))
            )
            resized = image.resize((width, height), resample=Resampling.LANCZOS)
            background.paste(resized, (imageX, imageY), mask=resized)

        def addPrice(background: Image.Image, price: float, currency: Currency) -> None:
            draw = ImageDraw.Draw(background)
            priceText = str(int(price/currency.value))
            priceX, priceY = ITEM.PRICE.POSITION.ABSOLUTE
            priceFont = ImageFont.truetype(FONT.PRICE_PATH, FONT_STYLE.SIZES.PRICE)
            # Text Size
            bbox = draw.textbbox((0, 0), priceText, font=priceFont)
            priceWidth = bbox[2] - bbox[0]
            priceHeight = bbox[3] - bbox[1]
            draw.text((priceX-priceWidth/2, priceY-priceHeight/2), priceText, font=priceFont, fill=FONT_STYLE.COLORS.PRICE)

        def addTitle(background: Image.Image, title: str) -> None:
            draw = ImageDraw.Draw(background)
            titleX, titleY = ITEM.TITLE.POSITION.ABSOLUTE
            titleFont = ImageFont.truetype(FONT.TITLE_PATH, getMaxFontSize(title, FONT.TITLE_PATH, FONT_STYLE.SIZES.TITLE, ITEM.TITLE.SIZE.ABSOLUTE[0]))
            # Text Size
            bbox = draw.textbbox((0, 0), title, font=titleFont)
            titleWidth = bbox[2] - bbox[0]
            titleHeight = bbox[3] - bbox[1]
            draw.text((titleX-titleWidth/2, titleY-titleHeight/2), title, font=titleFont, fill=FONT_STYLE.COLORS.TITLE)

        def format_damage(d: Damage, with_type: bool = False) -> str:
            dice_str = f"{d.diceAmount}{TEXT.DAMAGE_SPLIT}{d.diceType}" if d.diceAmount > 0 else ""
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
            ranges: dict[AttributeType, tuple[int, int]],
        ) -> None:
            fixedRows: list[str] = []
            fixedRows.append(f"{translate(TEXT.WEIGHT_PREFIX)}{weight}{translate(TEXT.WEIGHT_SUFFIX)}")
            if damage:
                fixedRows.append(f"{translate(TEXT.DAMAGE_PREFIX)}{format_damage(damage, True)}")

            attr_strings: list[str] = []
            for attr in attributes:
                name = str(attr)
                if attr == AttributeType.VERSATILE and versatile:
                    attr_strings.append(f"{name} ({format_damage(versatile)})")
                elif attr in ranges:
                    low, high = ranges[attr]
                    attr_strings.append(f"{name} ({low}/{high})")
                else:
                    attr_strings.append(name)

            optimalRows, optimalFontSize = findOptimalAttributeLayout(
                attr_strings,
                fixedRows,
                FONT.STATS_PATH,
                FONT_STYLE.SIZES.STATS,
                ITEM.STATS.SIZE.ABSOLUTE[0],
                ITEM.STATS.SIZE.ABSOLUTE[1],
            )
            statsString = "\n".join(optimalRows)

            draw = ImageDraw.Draw(background)
            statsX, statsY = ITEM.STATS.POSITION.ABSOLUTE
            statsFont = ImageFont.truetype(FONT.STATS_PATH, optimalFontSize)
            bbox = draw.textbbox((0, 0), statsString, font=statsFont)
            statsWidth = bbox[2] - bbox[0]
            statsHeight = bbox[3] - bbox[1]
            draw.text((statsX, statsY), statsString, font=statsFont, fill=FONT_STYLE.COLORS.STATS)


        currency = getCurrency(item.price)
        cardImage = createBackground(currency)
        addImage(cardImage, item.id, rotate, flip, scale)
        addPrice(cardImage, item.price, currency)
        addTitle(cardImage, item.name)
        addStats(cardImage, item.weight, item.damage, item.versatileDamage, item.attributes, item.ranges)

        # Export
        cardImage.save(join(PATHS.OUTPUT, f"{item.id}.png"))

    def createItemCards(self) -> None:
        items: list[Item] = getItems()
        for item in items:
            self.createItemCard(item)

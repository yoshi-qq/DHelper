from typing import Optional
import os
from config.constants import (
    # New hierarchical constants
    FONT_STYLE, IMAGE, ITEM, PATHS, SPELL, TEXT, FONT
)
from classes.types import AttributeType, Currency, Damage, Item, Spell, TargetType
from helpers.translationHelper import translate
from helpers.dataHelper import getItems, getSpells
from helpers.formattingHelper import (
    getMaxFontSize,
    findOptimalAttributeLayout,
    formatDamage,
    formatTimedelta,
)
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
        offset_x: float = 0.0,
        offset_y: float = 0.0,
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

        def addImage(
            background: Image.Image,
            id: str,
            rotate: float,
            flip: bool,
            scale: float,
            offset_x: float,
            offset_y: float,
        ) -> None:
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
            imageX += int(offset_x)
            imageY += int(offset_y)
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
                fixedRows.append(
                    f"{translate(TEXT.DAMAGE_PREFIX)}{formatDamage(damage, True)}"
                )

            attr_strings: list[str] = []
            for attr in attributes:
                name = str(attr)
                if attr == AttributeType.VERSATILE and versatile:
                    attr_strings.append(f"{name} ({formatDamage(versatile)})")
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
        addImage(cardImage, item.id, rotate, flip, scale, offset_x, offset_y)
        addPrice(cardImage, item.price, currency)
        addTitle(cardImage, item.name)
        addStats(cardImage, item.weight, item.damage, item.versatileDamage, item.attributes, item.ranges)

        # Export
        os.makedirs(PATHS.ITEM_OUTPUT, exist_ok=True)
        cardImage.save(join(PATHS.ITEM_OUTPUT, f"{item.id}.png"))

    def createItemCards(self) -> None:
        items: list[Item] = getItems()
        for item in items:
            self.createItemCard(item)

    def createSpellCard(
        self,
        spell: Spell,
        rotate: float = 0.0,
        flip: bool = False,
        scale: float = 1.0,
        offset_x: float = 0.0,
        offset_y: float = 0.0,
    ) -> None:
        def addIcon(background: Image.Image, path: str, layout, center: bool = True) -> None:
            icon = Image.open(path).convert("RGBA")
            icon = icon.resize(layout.SIZE.ABSOLUTE, Resampling.LANCZOS)
            pos = layout.POSITION.ABSOLUTE
            if center:
                pos = (
                    pos[0] - layout.SIZE.ABSOLUTE[0] // 2,
                    pos[1] - layout.SIZE.ABSOLUTE[1] // 2,
                )
            background.paste(icon, pos, mask=icon)

        def addText(background: Image.Image, text: str, layout, fontPath: str, maxSize: int) -> None:
            draw = ImageDraw.Draw(background)
            fontSize = getMaxFontSize(text, fontPath, maxSize, layout.SIZE.ABSOLUTE[0])
            font = ImageFont.truetype(fontPath, fontSize)
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            draw.text(
                (layout.POSITION.ABSOLUTE[0] - w / 2, layout.POSITION.ABSOLUTE[1] - h / 2),
                text,
                font=font,
                fill=FONT_STYLE.COLORS.STATS,
            )


        card = Image.open(IMAGE.BACKGROUNDS.SPELL).convert("RGBA")

        def addImage(
            background: Image.Image,
            id: str,
            rotate: float,
            flip: bool,
            scale: float,
            offset_x: float,
            offset_y: float,
        ) -> None:
            imagePath = join(IMAGE.PATHS.SPELLS, id)
            if not os.path.exists(f"{imagePath}.{IMAGE.FORMAT}"):
                raise FileNotFoundError(imagePath)
            image = Image.open(f"{imagePath}.{IMAGE.FORMAT}").convert("RGBA")
            if flip:
                image = image.transpose(Transpose.FLIP_LEFT_RIGHT)
            if rotate:
                image = image.rotate(rotate, expand=True, resample=Resampling.BICUBIC)
            maxWidth, maxHeight = SPELL.IMAGE.SIZE.ABSOLUTE
            oW, oH = image.size
            ratio = min(maxWidth / oW, maxHeight / oH) * scale
            width = int(oW * ratio)
            height = int(oH * ratio)
            imageX, imageY = twoDSub(
                SPELL.IMAGE.POSITION.ABSOLUTE, twoDTruncate((width, height), (1 / 2, 1 / 2))
            )
            imageX += int(offset_x)
            imageY += int(offset_y)
            resized = image.resize((width, height), resample=Resampling.LANCZOS)
            background.paste(resized, (imageX, imageY), mask=resized)

        levelIcons = {
            1: IMAGE.ICONS.LEVELS.LEVEL_1,
            2: IMAGE.ICONS.LEVELS.LEVEL_2,
            3: IMAGE.ICONS.LEVELS.LEVEL_3,
            4: IMAGE.ICONS.LEVELS.LEVEL_4,
            5: IMAGE.ICONS.LEVELS.LEVEL_5,
            6: IMAGE.ICONS.LEVELS.LEVEL_6,
            7: IMAGE.ICONS.LEVELS.LEVEL_7,
            8: IMAGE.ICONS.LEVELS.LEVEL_8,
            9: IMAGE.ICONS.LEVELS.LEVEL_9,
        }
        levelIcon = levelIcons.get(spell.level, IMAGE.ICONS.LEVELS.LEVEL_1)
        addIcon(card, levelIcon, SPELL.LEVEL, center=True)

        addText(card, spell.name, SPELL.TITLE, FONT.TITLE_PATH, FONT_STYLE.SIZES.TITLE)
        addText(card, str(spell.type), SPELL.CATEGORY, FONT.TITLE_PATH, FONT_STYLE.SIZES.TITLE)
        addImage(card, spell.id, rotate, flip, scale, offset_x, offset_y)

        addIcon(card, IMAGE.ICONS.DURATION, SPELL.DURATION)
        addText(
            card,
            formatTimedelta(spell.duration),
            SPELL.DURATION_TEXT,
            FONT.STATS_PATH,
            FONT_STYLE.SIZES.STATS,
        )
        addIcon(card, IMAGE.ICONS.COOLDOWN, SPELL.COOLDOWN)
        addText(
            card,
            formatTimedelta(spell.cooldown),
            SPELL.COOLDOWN_TEXT,
            FONT.STATS_PATH,
            FONT_STYLE.SIZES.STATS,
        )
        addIcon(card, IMAGE.ICONS.DAMAGE, SPELL.DAMAGE)
        if spell.damage:
            dmg_text = f"{formatDamage(spell.damage)}\n{spell.damage.damageType}"
            addText(card, dmg_text, SPELL.DAMAGE_TEXT, FONT.STATS_PATH, FONT_STYLE.SIZES.STATS)
        addIcon(card, IMAGE.ICONS.RANGE, SPELL.RANGE)
        addText(card, f"{int(spell.range)}m", SPELL.RANGE_TEXT, FONT.STATS_PATH, FONT_STYLE.SIZES.STATS)

        # Components
        addIcon(card, IMAGE.ICONS.SPOKEN, SPELL.MATERIAL.SPOKEN)
        if not spell.components.verbal:
            addIcon(card, IMAGE.ICONS.STRIKE, SPELL.MATERIAL.SPOKEN)
        addIcon(card, IMAGE.ICONS.MATERIAL, SPELL.MATERIAL.MATERIAL)
        if not spell.components.material:
            addIcon(card, IMAGE.ICONS.STRIKE, SPELL.MATERIAL.MATERIAL)
        addIcon(card, IMAGE.ICONS.GESTURAL, SPELL.MATERIAL.GESTURAL)
        if not spell.components.gestural:
            addIcon(card, IMAGE.ICONS.STRIKE, SPELL.MATERIAL.GESTURAL)
        if spell.components.material:
            if spell.components.material.name:
                addText(card, spell.components.material.name, SPELL.MATERIAL.NAME, FONT.STATS_PATH, FONT_STYLE.SIZES.STATS)
            if spell.components.material.cost is not None:
                addText(card, str(spell.components.material.cost), SPELL.MATERIAL.COST, FONT.STATS_PATH, FONT_STYLE.SIZES.STATS)

        addIcon(card, IMAGE.ICONS.CONCENTRATION, SPELL.CONCENTRATION)
        if not spell.concentration:
            addIcon(card, IMAGE.ICONS.STRIKE, SPELL.CONCENTRATION)
        addIcon(card, IMAGE.ICONS.RITUAL, SPELL.RITUAL)
        if not spell.ritual:
            addIcon(card, IMAGE.ICONS.STRIKE, SPELL.RITUAL)

        addText(card, str(spell.castingTime), SPELL.CAST_TIME, FONT.STATS_PATH, FONT_STYLE.SIZES.STATS)

        if spell.savingThrow:
            addText(card, str(spell.savingThrow)[:3].upper(), SPELL.SAVING_THROW, FONT.STATS_PATH, FONT_STYLE.SIZES.STATS)

        if spell.subRange is not None:
            addText(card, f"{int(spell.subRange)}m", SPELL.SUB_RANGE, FONT.STATS_PATH, FONT_STYLE.SIZES.STATS)
        targetIcons = {
            TargetType.CONE: IMAGE.ICONS.TARGETS.CONE,
            TargetType.CREATURE: IMAGE.ICONS.TARGETS.CREATURE,
            TargetType.CUBE: IMAGE.ICONS.TARGETS.CUBE,
            TargetType.CYLINDER: IMAGE.ICONS.TARGETS.CYLINDER,
            TargetType.LINE: IMAGE.ICONS.TARGETS.LINE,
            TargetType.OBJECT: IMAGE.ICONS.TARGETS.OBJECT,
            TargetType.POINT: IMAGE.ICONS.TARGETS.POINT,
            TargetType.RECTANGLE: IMAGE.ICONS.TARGETS.RECTANGLE,
            TargetType.SELF: IMAGE.ICONS.TARGETS.SELF,
            TargetType.SPHERE: IMAGE.ICONS.TARGETS.SPHERE,
        }
        addIcon(card, targetIcons.get(spell.target, IMAGE.ICONS.TARGETS.SELF), SPELL.TARGET)

        level_dir = join(PATHS.SPELL_OUTPUT, f"level{spell.level}")
        os.makedirs(level_dir, exist_ok=True)
        card.save(join(level_dir, f"{spell.id}.png"))

    def createSpellCards(self) -> None:
        spells: list[Spell] = getSpells()
        for spell in spells:
            self.createSpellCard(spell)

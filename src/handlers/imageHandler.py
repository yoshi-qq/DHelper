from typing import Optional, Callable, List, Any
import os
from config.constants import (
    # New hierarchical constants
    FONT_STYLE, IMAGE, ITEM, PATHS, SPELL, TEXT, FONT, LayoutElement
)
from classes.types import (
    AttributeType,
    Currency,
    Damage,
    Armor,
    SimpleItem,
    Item,
    Weapon,
    Spell,
    TargetType,
)
from helpers.translationHelper import translate
from helpers.dataHelper import getWeapons, getArmors, getItems, getSpells
from helpers.formattingHelper import (
    getMaxFontSize,
    findOptimalAttributeLayout,
    formatDamage,
    formatTimedelta,
    formatFloatAsInt,
    formatPriceWithSuffix,
)
from os.path import join
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Resampling, Transpose

from helpers.tupleHelper import twoDSub, twoDTruncate

class ImageHandler:
    def __init__(self) -> None:
        pass

    def getItemOutputPath(self, item: Item | SimpleItem | Armor) -> str:
        """Get the output path for an item based on its type."""
        if isinstance(item, Armor):
            return join(PATHS.ARMOR_OUTPUT, f"{item.id}.png")
        elif isinstance(item, Weapon):
            return join(PATHS.WEAPON_OUTPUT, f"{item.id}.png")
        elif isinstance(item, SimpleItem):
            return join(PATHS.ITEM_OUTPUT, f"{item.id}.png")
        else:  # isinstance(item, Item) - covers general items and weapons
            return join(PATHS.WEAPON_OUTPUT, f"{item.id}.png")

    def getItemAssetPath(self, item: Item | SimpleItem | Armor) -> str:
        """Get the asset path for an item based on its type."""
        if isinstance(item, Armor):
            return join(IMAGE.PATHS.ARMOR, f"{item.id}.{IMAGE.FORMAT}")
        elif isinstance(item, Weapon):
            return join(IMAGE.PATHS.WEAPONS, f"{item.id}.{IMAGE.FORMAT}")
        elif isinstance(item, SimpleItem):
            return join(IMAGE.PATHS.ITEMS, f"{item.id}.{IMAGE.FORMAT}")
        else:  # isinstance(item, Item) - covers general items and weapons
            return join(IMAGE.PATHS.WEAPONS, f"{item.id}.{IMAGE.FORMAT}")

    def _iconOp(self, path: str, layout: LayoutElement, center: bool = True) -> Callable[[Image.Image], None]:
        def op(background: Image.Image) -> None:
            icon = Image.open(path).convert("RGBA")
            icon = icon.resize(tuple(map(int, layout.SIZE.ABSOLUTE)), Resampling.LANCZOS) # type: ignore
            pos = layout.POSITION.ABSOLUTE
            if center:
                pos = (
                    pos[0] - layout.SIZE.ABSOLUTE[0] // 2,
                    pos[1] - layout.SIZE.ABSOLUTE[1] // 2,
                )
            background.paste(icon, pos, mask=icon)

        return op

    def _textOp(
        self,
        text: str,
        layout: LayoutElement,
        fontPath: str,
        maxSize: int,
    ) -> Callable[[Image.Image], None]:
        def op(background: Image.Image) -> None:
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

        return op

    def _imageOp(
        self,
        path: str,
        layout: Any,
        rotate: float = 0.0,
        flip: bool = False,
        scale: float = 1.0,
        offset_x: float = 0.0,
        offset_y: float = 0.0,
    ) -> Callable[[Image.Image], None]:
        def op(background: Image.Image) -> None:
            if not os.path.exists(path):
                raise FileNotFoundError(path)
            image = Image.open(path).convert("RGBA")
            if flip:
                image = image.transpose(Transpose.FLIP_LEFT_RIGHT)
            if rotate:
                image = image.rotate(rotate, expand=True, resample=Resampling.BICUBIC)
            maxWidth, maxHeight = layout.SIZE.ABSOLUTE
            originWidth, originHeight = image.size
            ratio = min(maxWidth / originWidth, maxHeight / originHeight) * scale
            width = int(originWidth * ratio)
            height = int(originHeight * ratio)
            imageX, imageY = twoDSub(
                layout.POSITION.ABSOLUTE, twoDTruncate((width, height), (1 / 2, 1 / 2))
            )
            imageX += int(offset_x)
            imageY += int(offset_y)
            resized = image.resize((width, height), resample=Resampling.LANCZOS) # type: ignore
            background.paste(resized, (imageX, imageY), mask=resized)

        return op

    def _statsOp(
        self,
        weight: float,
        damage: Optional[Damage],
        versatile: Optional[Damage],
        attributes: list[AttributeType],
        ranges: dict[AttributeType, tuple[int, int]],
    ) -> Callable[[Image.Image], None]:
        def op(background: Image.Image) -> None:
            fixedRows: list[str] = []
            fixedRows.append(f"{translate(TEXT.WEIGHT_PREFIX)}{formatFloatAsInt(weight)}{translate(TEXT.WEIGHT_SUFFIX)}")
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
                    low_str = formatFloatAsInt(float(low))
                    high_str = formatFloatAsInt(float(high))
                    attr_strings.append(f"{name} ({low_str}/{high_str})")
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
            draw.text((statsX, statsY), statsString, font=statsFont, fill=FONT_STYLE.COLORS.STATS)

        return op

    def _simpleStatsOp(self, weight: float, description: str) -> Callable[[Image.Image], None]:
        def op(background: Image.Image) -> None:
            text = f"{translate(TEXT.WEIGHT_PREFIX)}{formatFloatAsInt(weight)}{translate(TEXT.WEIGHT_SUFFIX)}\n{description}".strip()
            draw = ImageDraw.Draw(background)
            size = getMaxFontSize(
                text,
                FONT.STATS_PATH,
                FONT_STYLE.SIZES.STATS,
                ITEM.STATS.SIZE.ABSOLUTE[0],
                ITEM.STATS.SIZE.ABSOLUTE[1],
            )
            font = ImageFont.truetype(FONT.STATS_PATH, size)
            draw.multiline_text(
                ITEM.STATS.POSITION.ABSOLUTE,
                text,
                font=font,
                fill=FONT_STYLE.COLORS.STATS,
            )

        return op

    def _armorStatsOp(self, armor: Armor) -> Callable[[Image.Image], None]:
        def op(background: Image.Image) -> None:
            text_lines: list[str] = []
            text_lines.append(f"{translate(TEXT.WEIGHT_PREFIX)}{formatFloatAsInt(armor.weight)}{translate(TEXT.WEIGHT_SUFFIX)}")
            text_lines.append(f"AC {armor.armorClass}")

            if armor.dexBonusMax is not None:
                text_lines.append(f"{translate(TEXT.DEX_MAX_PREFIX)}{armor.dexBonusMax}")

            if armor.strengthRequirement is not None:
                text_lines.append(f"{translate(TEXT.STRENGTH_REQ_PREFIX)}{armor.strengthRequirement}")

            if armor.stealthDisadvantage:
                text_lines.append(translate(TEXT.STEALTH_DISADVANTAGE))

            text = "\n".join(text_lines)

            draw = ImageDraw.Draw(background)
            size = getMaxFontSize(
                text,
                FONT.STATS_PATH,
                FONT_STYLE.SIZES.STATS,
                ITEM.STATS.SIZE.ABSOLUTE[0],
                ITEM.STATS.SIZE.ABSOLUTE[1],
            )
            font = ImageFont.truetype(FONT.STATS_PATH, size)
            draw.multiline_text(
                ITEM.STATS.POSITION.ABSOLUTE,
                text,
                font=font,
                fill=FONT_STYLE.COLORS.STATS,
            )

        return op

    def _createCard(
        self, background: Image.Image, instructions: List[Callable[[Image.Image], None]], outputPath: str
    ) -> None:
        for inst in instructions:
            inst(background)
        os.makedirs(os.path.dirname(outputPath), exist_ok=True)
        background.save(outputPath)

    def createItemCard(
        self,
        item: Item | SimpleItem | Armor,
        rotate: float = 0,
        flip: bool = False,
        scale: float = 1.0,
        offset_x: float = 0.0,
        offset_y: float = 0.0,
    ) -> None:
        def getCurrency(price: float) -> Currency:
            if price % 1 == 0:
                return Currency.GOLD
            elif price % 0.1 == 0:
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
                    backgroundPath = IMAGE.BACKGROUNDS.COPPER_ITEM
            return Image.open(backgroundPath).convert("RGBA")

        currency = getCurrency(item.price)
        cardImage = createBackground(currency)

        instructions: List[Callable[[Image.Image], None]] = [
            self._imageOp(
                self.getItemAssetPath(item),
                ITEM.IMAGE,
                rotate,
                flip,
                scale,
                offset_x,
                offset_y,
            ),
            self._textOp(
                formatPriceWithSuffix(item.price / currency.value),
                ITEM.PRICE,
                FONT.PRICE_PATH,
                FONT_STYLE.SIZES.PRICE,
            ),
            self._textOp(
                item.name,
                ITEM.TITLE,
                FONT.TITLE_PATH,
                FONT_STYLE.SIZES.TITLE,
            ),
            (
                self._simpleStatsOp(item.weight, item.description)
                if isinstance(item, SimpleItem)
                else self._armorStatsOp(item)
                if isinstance(item, Armor)
                else self._statsOp(
                    item.weight,
                    getattr(item, "damage", None),
                    getattr(item, "versatileDamage", None),
                    getattr(item, "attributes", []),
                    getattr(item, "ranges", {}),
                )
            ),
        ]

        self._createCard(cardImage, instructions, self.getItemOutputPath(item))

    def createItemCards(self) -> None:
        """Create cards for all items: weapons, armor, and simple items."""
        self.createWeaponCards()
        self.createArmorCards()
        self.createSimpleItemCards()

    def createWeaponCards(self) -> None:
        """Create cards for all weapons."""
        weapons = getWeapons()
        for weapon in weapons:
            self.createItemCard(weapon)

    def createArmorCards(self) -> None:
        """Create cards for all armor."""
        armors = getArmors()
        for armor in armors:
            self.createItemCard(armor)

    def createSimpleItemCards(self) -> None:
        """Create cards for all simple items."""
        items = getItems()
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
        card = Image.open(IMAGE.BACKGROUNDS.SPELL).convert("RGBA")

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

        instructions: List[Callable[[Image.Image], None]] = [
            self._iconOp(levelIcon, SPELL.LEVEL, center=True),
            self._textOp(spell.name, SPELL.TITLE, FONT.TITLE_PATH, FONT_STYLE.SIZES.TITLE),
            self._textOp(str(spell.type), SPELL.CATEGORY, FONT.TITLE_PATH, FONT_STYLE.SIZES.TITLE),
            self._imageOp(
                join(IMAGE.PATHS.SPELLS, f"{spell.id}.{IMAGE.FORMAT}"),
                SPELL.IMAGE,
                rotate,
                flip,
                scale,
                offset_x,
                offset_y,
            ),
            self._iconOp(IMAGE.ICONS.DURATION, SPELL.DURATION),
            self._textOp(
                formatTimedelta(spell.duration),
                SPELL.DURATION_TEXT,
                FONT.STATS_PATH,
                FONT_STYLE.SIZES.STATS,
            ),
            self._iconOp(IMAGE.ICONS.COOLDOWN, SPELL.COOLDOWN),
            self._textOp(
                formatTimedelta(spell.cooldown),
                SPELL.COOLDOWN_TEXT,
                FONT.STATS_PATH,
                FONT_STYLE.SIZES.STATS,
            ),
            self._iconOp(IMAGE.ICONS.DAMAGE, SPELL.DAMAGE),
            self._iconOp(IMAGE.ICONS.RANGE, SPELL.RANGE),
            self._textOp(
                f"{formatFloatAsInt(spell.range)}m",
                SPELL.RANGE_TEXT,
                FONT.STATS_PATH,
                FONT_STYLE.SIZES.STATS,
            ),
            self._iconOp(IMAGE.ICONS.SPOKEN, SPELL.MATERIAL.SPOKEN),
            self._iconOp(IMAGE.ICONS.MATERIAL, SPELL.MATERIAL.MATERIAL),
            self._iconOp(IMAGE.ICONS.GESTURAL, SPELL.MATERIAL.GESTURAL),
            self._iconOp(IMAGE.ICONS.CONCENTRATION, SPELL.CONCENTRATION),
            self._iconOp(IMAGE.ICONS.RITUAL, SPELL.RITUAL),
            self._textOp(
                str(spell.castingTime), SPELL.CAST_TIME, FONT.STATS_PATH, FONT_STYLE.SIZES.STATS
            ),
        ]

        if spell.damage:
            dmg_text = f"{formatDamage(spell.damage)}\n{spell.damage.damageType}"
            instructions.append(
                self._textOp(dmg_text, SPELL.DAMAGE_TEXT, FONT.STATS_PATH, FONT_STYLE.SIZES.STATS)
            )
        if not spell.components.verbal:
            instructions.append(self._iconOp(IMAGE.ICONS.STRIKE, SPELL.MATERIAL.SPOKEN))
        if not spell.components.material:
            instructions.append(self._iconOp(IMAGE.ICONS.STRIKE, SPELL.MATERIAL.MATERIAL))
        if not spell.components.gestural:
            instructions.append(self._iconOp(IMAGE.ICONS.STRIKE, SPELL.MATERIAL.GESTURAL))
        if spell.components.material:
            if spell.components.material.name:
                instructions.append(
                    self._textOp(
                        spell.components.material.name,
                        SPELL.MATERIAL.NAME,
                        FONT.STATS_PATH,
                        FONT_STYLE.SIZES.STATS,
                    )
                )
            if spell.components.material.cost is not None:
                instructions.append(
                    self._textOp(
                        formatFloatAsInt(spell.components.material.cost),
                        SPELL.MATERIAL.COST,
                        FONT.STATS_PATH,
                        FONT_STYLE.SIZES.STATS,
                    )
                )
        if not spell.concentration:
            instructions.append(self._iconOp(IMAGE.ICONS.STRIKE, SPELL.CONCENTRATION))
        if not spell.ritual:
            instructions.append(self._iconOp(IMAGE.ICONS.STRIKE, SPELL.RITUAL))
        if spell.savingThrow:
            instructions.append(
                self._textOp(
                    str(spell.savingThrow)[:3].upper(),
                    SPELL.SAVING_THROW,
                    FONT.STATS_PATH,
                    FONT_STYLE.SIZES.STATS,
                )
            )
        if spell.subRange is not None:
            instructions.append(
                self._textOp(
                    f"{formatFloatAsInt(spell.subRange)}m",
                    SPELL.SUB_RANGE,
                    FONT.STATS_PATH,
                    FONT_STYLE.SIZES.STATS,
                )
            )
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
        instructions.append(self._iconOp(targetIcons.get(spell.target, IMAGE.ICONS.TARGETS.SELF), SPELL.TARGET))

        level_dir = join(PATHS.SPELL_OUTPUT, f"level{spell.level}")
        outputPath = join(level_dir, f"{spell.id}.png")
        self._createCard(card, instructions, outputPath)


    def createSpellCards(self) -> None:
        spells: list[Spell] = getSpells()
        for spell in spells:
            self.createSpellCard(spell)

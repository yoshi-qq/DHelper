from datetime import timedelta
from PIL import ImageFont, ImageDraw, Image
from classes.types import Damage


def formatFloatAsInt(value: float) -> str:
    if value == int(value):
        return str(int(value))
    else:
        return str(value)


def formatPriceWithSuffix(value: float) -> str:
    """Format a price with K/M suffixes for large numbers."""
    if value >= 1000000:
        # Format as millions
        millions = value / 1000000
        if millions == int(millions):
            return f"{int(millions)}M"
        else:
            return f"{millions:.1f}M"
    elif value >= 1000:
        # Format as thousands
        thousands = value / 1000
        if thousands == int(thousands):
            return f"{int(thousands)}K"
        else:
            return f"{thousands:.1f}K"
    else:
        # Format as regular number
        return formatFloatAsInt(value)


def getMaxFontSize(text: str, fontPath: str, maxSize: int, maxWidth: float, maxHeight: float = float("inf")) -> int:
    size = maxSize
    dummyImage = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummyImage)
    for size in range(maxSize, 1, -1):
        testFont = ImageFont.truetype(fontPath, size)
        bbox = draw.textbbox((0, 0), text, font=testFont)
        testWidth = bbox[2] - bbox[0]
        testHeight = bbox[3] - bbox[1]
        if testWidth < maxWidth and testHeight < maxHeight:
            break
    return size


def findOptimalAttributeLayout(attributes: list[str], fixedRows: list[str], fontPath: str, maxFontSize: int, maxWidth: float, maxHeight: float) -> tuple[list[str], int]:
    if not attributes:
        return fixedRows, getMaxFontSize("\n".join(fixedRows), fontPath, maxFontSize, maxWidth, maxHeight)

    bestLayout = fixedRows + [", ".join(attributes)]
    bestFontSize = getMaxFontSize("\n".join(bestLayout), fontPath, maxFontSize, maxWidth, maxHeight)

    if len(attributes) > 1:
        for splitPoint in range(1, len(attributes)):
            line1 = ", ".join(attributes[:splitPoint])
            line2 = ", ".join(attributes[splitPoint:])
            testRows = fixedRows + [line1, line2]
            testString = "\n".join(testRows)

            fontSize = getMaxFontSize(testString, fontPath, maxFontSize, maxWidth, maxHeight)

            if fontSize > bestFontSize:
                bestFontSize = fontSize
                bestLayout = testRows

    if len(attributes) > 3:
        third = len(attributes) // 3
        split1 = third
        split2 = third * 2

        line1 = ", ".join(attributes[:split1])
        line2 = ", ".join(attributes[split1:split2])
        line3 = ", ".join(attributes[split2:])
        testRows = fixedRows + [line1, line2, line3]
        testString = "\n".join(testRows)

        fontSize = getMaxFontSize(testString, fontPath, maxFontSize, maxWidth, maxHeight)

        if fontSize > bestFontSize:
            bestFontSize = fontSize
            bestLayout = testRows

        for split1 in range(1, len(attributes) - 1):
            for split2 in range(split1 + 1, len(attributes)):
                line1 = ", ".join(attributes[:split1])
                line2 = ", ".join(attributes[split1:split2])
                line3 = ", ".join(attributes[split2:])
                testRows = fixedRows + [line1, line2, line3]
                testString = "\n".join(testRows)

                fontSize = getMaxFontSize(testString, fontPath, maxFontSize, maxWidth, maxHeight)

                if fontSize > bestFontSize:
                    bestFontSize = fontSize
                    bestLayout = testRows

    return bestLayout, bestFontSize


def formatDamage(d: Damage, withType: bool = False) -> str:
    """Return a formatted damage string."""
    diceStr = f"{d.diceAmount}D{d.diceType}" if d.diceAmount > 0 else ""
    bonusStr = "" if d.bonus == 0 else str(d.bonus) if not diceStr else f" {'+' if d.bonus > 0 else ''}{d.bonus}"
    result = f"{diceStr}{bonusStr}"
    if withType:
        result = f"{result} {d.damageType}".strip()
    return result


def formatTimedelta(delta: timedelta) -> str:
    """Return a human readable representation of a timedelta."""
    total = int(delta.total_seconds())
    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    if minutes:
        return f"{minutes}:{seconds:02d}"
    return f"{seconds}s"

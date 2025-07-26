from PIL import ImageFont, ImageDraw, Image

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
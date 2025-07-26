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
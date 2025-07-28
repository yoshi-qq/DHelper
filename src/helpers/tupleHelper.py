def twoDMultiply(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return (a[0] * b[0], a[1] * b[1])

def twoDTruncate(a: tuple[float, float], b: tuple[float, float]) -> tuple[int, int]:
    return (int(a[0] * b[0]), int(a[1] * b[1]))

def twoDAdd(a: tuple[float, float], b: tuple[float, float]) -> tuple[int, int]:
    return (int(a[0] + b[0]), int(a[1] + b[1]))

def twoDSub(a: tuple[float, float], b: tuple[float, float]) -> tuple[int, int]:
    return (int(a[0] - b[0]), int(a[1] - b[1]))
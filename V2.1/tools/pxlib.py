"""Biblioteca de Pixel Art da V2: paletas, ruído periódico, sombreamento por volume e utilitários."""
import json
import math

from PIL import Image


def hexc(value, alpha=255):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def ramp(*colors):
    return [hexc(color) for color in colors]


# Rampas escuras -> claras; a luz vem do canto superior esquerdo.
GRASS = ramp("#08170f", "#0d241a", "#143222", "#1d4529", "#285a30", "#377235", "#4c8c40")
MOSS = ramp("#0f2a19", "#194022", "#27582a", "#3a7430", "#54903a", "#7bb04c", "#a3cf65")
STONE = ramp("#0a1011", "#141c1c", "#222c2a", "#333f3a", "#475347", "#5f6b58", "#7d8670")
RUIN = ramp("#12120e", "#1f1e17", "#322f23", "#4a4533", "#686046", "#8c815b")
WATER = ramp("#041821", "#082833", "#0d3a45", "#14505a", "#1f6c75", "#3a929a", "#79c2bf", "#c6efe3")
WOOD = ramp("#0f0b09", "#1b120e", "#2d1e15", "#443022", "#5e442c", "#7a5a3a")
BARK = ramp("#0b0807", "#191210", "#2a1e17", "#3e2c21", "#56402e", "#725740")
BIRCH = ramp("#1b1a17", "#38362f", "#625f55", "#8f8c7e", "#bbb8a8", "#dedbca")
LEAF_MAIN = ramp("#06130d", "#0b2016", "#112e1e", "#193f27", "#245631", "#33703a", "#4b8c42", "#72ab4c", "#9ccb66")
LEAF_TEAL = ramp("#061617", "#0c2626", "#133831", "#1b4d3d", "#276a4d", "#3a875e", "#5aa575", "#86c593", "#b3e0b0")
LEAF_YEL = ramp("#141b0b", "#212c0d", "#363f11", "#4f5a17", "#6d7822", "#8e9533", "#b0b04d", "#cfca72", "#e8e29b")
LEAF_AUT = ramp("#1f0c05", "#3a1608", "#5c260d", "#823b12", "#ab571a", "#d17a26", "#eba649", "#ffd078")
PINE = ramp("#050f0c", "#0a1b15", "#102a21", "#183b2f", "#234f40", "#33684f", "#4d856a", "#78a98c")
CRYSTAL = ramp("#05202a", "#093640", "#0f5560", "#177781", "#27a0a6", "#4ec9c2", "#97ecdb", "#e2fff3")
SKIN = ramp("#4a2a20", "#774736", "#a56a4e", "#cc9170", "#ebb994")
HAIR = ramp("#140d0a", "#25170f", "#3a2418", "#563622")
CLOAK = ramp("#081a19", "#102a28", "#193f3a", "#245450", "#32706a", "#4a8c82")
SCARF = ramp("#3a1613", "#62241d", "#8a362a", "#b4553d")
TROUSER = ramp("#15130f", "#26221a", "#3b3426", "#54493a")
METAL = ramp("#0c0d0f", "#202226", "#3b3e44", "#62666d", "#92969d")
FLAME = ramp("#7a2f10", "#c85c17", "#ff9e2d", "#ffd36b", "#fff4c2")
FLOWER_BLUE = ramp("#142a66", "#2b55c4", "#5a8cf2", "#a8c8ff")
FLOWER_PINK = ramp("#4a1556", "#8a2f9a", "#c566d4", "#f0b0f5")
FLOWER_GOLD = ramp("#5a3a08", "#a8741a", "#e4b13a", "#fff0a0")
SHADOW = (3, 8, 8)

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def bay(x, y):
    return (BAYER[int(y) & 3][int(x) & 3] + 0.5) / 16.0


def clamp(value, low, high):
    return low if value < low else high if value > high else value


DITHER_BAND = 1.0  # 1 = dithering completo; valores menores endurecem as transições (pixel art mais limpa)


def pick(palette, level, x=0, y=0, dither=True):
    """Escolhe um tom da rampa com dithering ordenado entre dois níveis."""
    level = clamp(level, 0.0, len(palette) - 1.0)
    base = math.floor(level)
    frac = level - base
    index = base + (1 if dither and frac > 0.5 + (bay(x, y) - 0.5) * DITHER_BAND else 0)
    return palette[min(index, len(palette) - 1)]


def hsh(ix, iy, seed):
    n = (int(ix) * 374761393 + int(iy) * 668265263 + int(seed) * 2246822519) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def vnoise(x, y, seed, px=0, py=0):
    x0, y0 = math.floor(x), math.floor(y)
    fx, fy = x - x0, y - y0

    def corner(ix, iy):
        if px:
            ix %= px
        if py:
            iy %= py
        return hsh(ix, iy, seed)

    sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = corner(x0, y0), corner(x0 + 1, y0)
    c, d = corner(x0, y0 + 1), corner(x0 + 1, y0 + 1)
    return (a + (b - a) * sx) * (1 - sy) + (c + (d - c) * sx) * sy


def tn(x, y, seed, cell, size=32):
    """Ruído suave que repete a cada `size` pixels (tiles sem emendas)."""
    n = max(1, size // cell)
    return vnoise(x / cell, y / cell, seed, n, n)


def nn(x, y, seed, cell):
    return vnoise(x / cell, y / cell, seed)


def tfbm(x, y, seed, size=32, cells=(16, 8, 4), weights=(0.5, 0.3, 0.2)):
    return sum(w * tn(x, y, seed + i * 7, c, size) for i, (c, w) in enumerate(zip(cells, weights)))


def voronoi(x, y, cell, seed, size=None):
    """Retorna (d1, d2, hash_da_célula). Periódico se `size` for informado."""
    gx, gy = x / cell, y / cell
    ix, iy = math.floor(gx), math.floor(gy)
    n = (size // cell) if size else 0
    d1 = d2 = 9.0
    cid = 0.0
    for oy in (-1, 0, 1):
        for ox in (-1, 0, 1):
            cx, cy = ix + ox, iy + oy
            wx, wy = (cx % n, cy % n) if n else (cx, cy)
            px = cx + hsh(wx, wy, seed) * 0.8 + 0.1
            py = cy + hsh(wx, wy, seed + 91) * 0.8 + 0.1
            d = math.hypot(gx - px, gy - py)
            if d < d1:
                d2, d1 = d1, d
                cid = hsh(wx, wy, seed + 5)
            elif d < d2:
                d2 = d
    return d1, d2, cid


def new_image(width, height):
    return Image.new("RGBA", (width, height), (0, 0, 0, 0))


def put(image, x, y, color):
    x, y = int(x), int(y)
    if 0 <= x < image.width and 0 <= y < image.height:
        image.putpixel((x, y), color)


def get(image, x, y):
    if 0 <= x < image.width and 0 <= y < image.height:
        return image.getpixel((int(x), int(y)))
    return (0, 0, 0, 0)


def rect(image, x0, y0, x1, y1, color):
    for y in range(int(y0), int(y1) + 1):
        for x in range(int(x0), int(x1) + 1):
            put(image, x, y, color)


def line(image, x0, y0, x1, y1, color, width=1):
    steps = int(max(abs(x1 - x0), abs(y1 - y0))) * 2 + 1
    for i in range(steps + 1):
        t = i / steps
        cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        if width <= 1:
            put(image, round(cx), round(cy), color)
        else:
            for ox in range(width):
                put(image, round(cx) + ox - width // 2, round(cy), color)


def outline(image, color, min_alpha=200):
    """Contorno escuro de 1 px ao redor de pixels opacos."""
    source = image.copy()
    for y in range(image.height):
        for x in range(image.width):
            if source.getpixel((x, y))[3] >= 40:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < image.width and 0 <= ny < image.height and source.getpixel((nx, ny))[3] >= min_alpha:
                    image.putpixel((x, y), color)
                    break


def ground_shadow(image, cx, cy, rx, ry, strength=0.55):
    """Sombra elíptica pontilhada ao pé do sprite (preenche só pixels vazios)."""
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            if d < 1.0 and get(image, x, y)[3] == 0:
                if (1.0 - d) * strength * 2.2 > bay(x, y):
                    put(image, x, y, SHADOW + (150,))


LIGHT = (-0.5, -0.68, 0.54)
_LN = math.sqrt(sum(v * v for v in LIGHT))
LIGHT = tuple(v / _LN for v in LIGHT)


def render_blobs(img, blobs, ramps, seed, cell=3.6, facet=0.55, edge_dark=0.2, contrast=1.0,
                 accent_odds=(0.0, 0.0), moss=None, bias=0.0, rim=0.22, outline_color=None, cell_amp=0.28):
    """Renderiza uma união de esferas (cx, cy, r, z[, rampa]) com folhas/facetas e luz direcional.

    ramps = (principal, acento1, acento2). accent_odds define a chance de uma folha usar cada acento.
    """
    W, H = img.size
    owner = {}
    for y in range(H):
        for x in range(W):
            best, best_h = None, -1e9
            for i, b in enumerate(blobs):
                dx, dy = x + 0.5 - b[0], y + 0.5 - b[1]
                d2 = dx * dx + dy * dy
                if d2 >= b[2] * b[2]:
                    continue
                nz = math.sqrt(b[2] * b[2] - d2)
                h = b[3] + nz
                if h > best_h:
                    best_h, best = h, (i, dx / b[2], dy / b[2], nz / b[2])
            if best:
                owner[(x, y)] = best + (best_h,)
    for (x, y), (i, nx, ny, nz, h) in owner.items():
        blob = blobs[i]
        d1, d2, cid = voronoi(x, y, cell, seed)
        jx = (hsh(int(cid * 9973), 1, seed) - 0.5) * facet
        jy = (hsh(int(cid * 9973), 2, seed) - 0.5) * facet
        nx2, ny2 = nx + jx, ny + jy
        nz2 = math.sqrt(max(0.05, 1 - min(0.95, nx2 * nx2 + ny2 * ny2)))
        diffuse = nx2 * LIGHT[0] + ny2 * LIGHT[1] + nz2 * LIGHT[2]
        level = 0.5 + 0.5 * diffuse * contrast
        level += (cid - 0.5) * cell_amp + bias
        if d2 - d1 < 0.16:
            level -= edge_dark
        if (x - 1, y - 1) not in owner:
            level += rim
        if (x + 1, y + 1) not in owner:
            level -= rim * 0.8
        ramp_set = blob[4] if len(blob) > 4 else ramps
        palette = ramp_set[0]
        if cid < accent_odds[0] and len(ramp_set) > 1:
            palette = ramp_set[1]
        elif cid < accent_odds[0] + accent_odds[1] and len(ramp_set) > 2:
            palette = ramp_set[2]
        if moss and ny2 < -0.05 and (-ny2 + nn(x, y, seed + 3, 4) * 0.9) > moss:
            palette = MOSS
            level = level * (len(MOSS) - 1) / 1.0 * 0.95
            put(img, x, y, pick(MOSS, clamp(level, 0, len(MOSS) - 1), x, y))
            continue
        put(img, x, y, pick(palette, clamp(level, 0, 1) * (len(palette) - 1), x, y))
    if outline_color:
        outline(img, outline_color)


def draw_vine(img, x, y, length, seed, ramp_leaf=LEAF_MAIN, direction=1, wiggle=1.6, leaf_every=3, flowers=False):
    """Trepadeira: caule ondulado com folhas alternadas em pequenos clusters."""
    stem = ramp_leaf[1]
    cx = float(x)
    for i in range(length):
        cx = x + math.sin(i * 0.5 + seed) * wiggle
        cy = y + i * direction
        put(img, round(cx), cy, stem)
        if i % leaf_every == int(hsh(i, seed, 3) * leaf_every):
            side = -1 if hsh(i, seed, 8) < 0.5 else 1
            lvl = 3 + int(hsh(i, seed, 11) * 3)
            lx, ly = round(cx) + side, cy
            put(img, lx, ly, ramp_leaf[min(lvl, len(ramp_leaf) - 1)])
            put(img, lx + side, ly, ramp_leaf[min(lvl + 1, len(ramp_leaf) - 1)])
            put(img, lx, ly + 1, ramp_leaf[max(lvl - 1, 0)])
            if hsh(i, seed, 13) < 0.5:
                put(img, lx + side, ly - 1, ramp_leaf[min(lvl + 2, len(ramp_leaf) - 1)])
        if flowers and i % 11 == 5:
            put(img, round(cx) + 1, cy, FLOWER_PINK[3])
            put(img, round(cx) + 1, cy + 1, FLOWER_PINK[2])


def pack_atlas(frames, width=1024, padding=2):
    """Empacota frames em prateleiras e devolve (imagem, json no formato hash do Phaser)."""
    items = sorted(frames.items(), key=lambda item: (-item[1].height, item[0]))
    x = y = row_height = 0
    placed = {}
    for name, image in items:
        if x + image.width + padding > width:
            x, y, row_height = 0, y + row_height + padding, 0
        placed[name] = (x, y)
        x += image.width + padding
        row_height = max(row_height, image.height)
    height = 1
    while height < y + row_height + padding:
        height *= 2
    atlas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    data = {}
    for name, (px, py) in placed.items():
        image = frames[name]
        atlas.paste(image, (px, py))
        data[name] = {
            "frame": {"x": px, "y": py, "w": image.width, "h": image.height},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": image.width, "h": image.height},
            "sourceSize": {"w": image.width, "h": image.height},
        }
    meta = {"image": "decor.png", "format": "RGBA8888", "size": {"w": width, "h": height}, "scale": "1"}
    return atlas, json.dumps({"frames": data, "meta": meta}, indent=1)

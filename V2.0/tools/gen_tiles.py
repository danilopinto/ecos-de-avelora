"""Gera o atlas de tiles 32x32 (8 colunas x 4 linhas) da V2.

Mapa de GIDs (id Tiled = gid):
 1-3 chão, 4-7 pedra do caminho, 8-9 água, 10-11 ponte, 12-14 muro de ruína,
 14-16 detalhes (tufo, samambaia, cogumelos), 17-18 borda do caminho (esq/dir),
 19-24 detalhes (flores, folhas, seixos), 25-28 variações de chão.
Todos os tiles opacos repetem sem emendas (ruído e voronoi periódicos).
"""
import random

from pxlib import *

T = 32


def wput(img, x, y, color):
    put(img, int(x) % T, int(y) % T, color)


def blades(img, rng, count, palettes=(GRASS, MOSS), lo=3, hi=6, hmin=2, hmax=5):
    """Folhas de grama finas com ponta clara e base escura."""
    for _ in range(count):
        x, y = rng.randrange(T), rng.randrange(T)
        height = rng.randint(hmin, hmax)
        lean = rng.choice((-1, 0, 0, 1))
        palette = rng.choice(palettes)
        top = min(hi, len(palette) - 1)
        for i in range(height):
            level = lo + (top - lo) * i // max(1, height - 1)
            wput(img, x + (lean if i > height // 2 else 0), y - i, palette[level])


def ground_tile(seed, kind=0):
    rng = random.Random(seed)
    img = new_image(T, T)
    for y in range(T):
        for x in range(T):
            big = tfbm(x, y, seed)
            fine = tn(x, y, seed + 31, 2, T)
            level = 1.1 + big * 2.7 + fine * 0.9 - 0.35
            if kind == 1:  # sombra densa de sub-bosque
                level -= 0.7
            if kind == 2:  # clareira mais viva
                level += 0.55
            patch = tn(x, y, seed + 71, 8, T)
            palette = MOSS if patch > 0.72 and kind != 1 else GRASS
            if palette is MOSS:
                level = 0.7 + (level * 0.55)
            wput(img, x, y, pick(palette, level, x, y))
    blades(img, rng, 26 + 8 * (kind == 2))
    if kind == 1:  # folhas secas e raízes finas
        for _ in range(7):
            x, y = rng.randrange(T), rng.randrange(T)
            c = rng.choice((WOOD[2], WOOD[3], LEAF_AUT[1], LEAF_AUT[2]))
            wput(img, x, y, c)
            wput(img, x + 1, y, WOOD[1])
    for _ in range(5):  # miolos escuros para quebrar o padrão
        x, y = rng.randrange(T), rng.randrange(T)
        wput(img, x, y, GRASS[1])
        wput(img, x + 1, y + 1, GRASS[0])
    for _ in range(2 + kind):  # trevos/grãos claros
        x, y = rng.randrange(T), rng.randrange(T)
        wput(img, x, y, MOSS[5])
    return img


def cobble_rows(rng, heights=(10, 11, 11), wmin=9, wmax=15):
    rows = []
    for h in heights:
        widths, total = [], 0
        while total < T:
            w = rng.randint(wmin, wmax)
            if T - total - w < wmin:
                w = T - total
            widths.append(w)
            total += w
        rows.append((h, widths, rng.randrange(T)))
    return rows


def paint_stone(img, x0, y0, w, h, rng, seed, palette=STONE, moss=0.55, warm=0.25):
    """Uma pedra chanfrada com grão, poços, rachadura e musgo nas juntas."""
    pal = RUIN if rng.random() < warm else palette
    base = rng.uniform(2.6, 4.1)
    crack = None
    if rng.random() < 0.33:
        cx = rng.randint(2, max(2, w - 3))
        crack = (cx, rng.randint(1, h // 2))
    for v in range(h):
        for u in range(w):
            dl, dr, dt, db = u, w - 1 - u, v, h - 1 - v
            px, py = (x0 + u) % T, (y0 + v) % T
            corner = (dl + dt == 0) or (dr + dt == 0) or (dl + db == 0) or (dr + db == 0)
            moss_n = nn(x0 + u, y0 + v, seed + 5, 3)
            if dr == 0 or db == 0 or corner:
                joint = pal[0] if moss_n < moss else MOSS[1]
                if moss_n > moss + 0.12:
                    joint = MOSS[2]
                put(img, px, py, joint)
                continue
            level = base + (tn(x0 + u, y0 + v, seed + 9, 4, T) - 0.5) * 1.5
            level += (tn(x0 + u, y0 + v, seed + 13, 2, T) - 0.5) * 0.8
            if dt == 0 or dl == 0:
                level += 1.0
            elif dt == 1 or dl == 1:
                level += 0.45
            if dr == 1 or db == 1:
                level -= 0.8
            if crack and abs((u - crack[0]) - (v - crack[1]) * 0.6) < 0.55 and v >= crack[1]:
                level -= 1.8
            color = pick(pal, level, px, py)
            near_edge = min(dl, dr, dt, db)
            if near_edge <= 2 and moss_n > moss and (db <= 2 or dr <= 2 or moss_n > moss + 0.18):
                color = pick(MOSS, 1.2 + moss_n * 3.2 + (2 - near_edge) * 0.3, px, py)
            put(img, px, py, color)
    for _ in range(rng.randint(0, 2)):  # poços
        u, v = rng.randint(2, max(2, w - 4)), rng.randint(2, max(2, h - 4))
        put(img, (x0 + u) % T, (y0 + v) % T, pal[1])


def cobble_tile(seed, moss=0.55, warm=0.25, palette=STONE, heights=(10, 11, 11), wmin=9, wmax=15):
    rng = random.Random(seed)
    img = new_image(T, T)
    # terra escura sob as juntas
    for y in range(T):
        for x in range(T):
            put(img, x, y, pick(WOOD, 0.4 + tn(x, y, seed + 2, 4, T) * 1.4, x, y))
    y = rng.randrange(T)
    for h, widths, off in cobble_rows(rng, heights, wmin, wmax):
        pos = off
        for w in widths:
            paint_stone(img, pos, y, w, h, rng, seed + pos + y, palette, moss, warm)
            pos += w
        y += h
    # pontos de luz de musgo e folhinhas
    for _ in range(9):
        x, yy = rng.randrange(T), rng.randrange(T)
        put(img, x, yy, MOSS[rng.randint(3, 5)])
    return img


def path_edge(seed, side):
    """Borda do caminho: curb de pedra com terra e grama invadindo o lado de fora."""
    base = cobble_tile(seed, moss=0.4)
    rng = random.Random(seed + 40)
    out = new_image(T, T)
    for y in range(T):
        wave = 3 + int(tn(0, y, seed, 4, T) * 4) + (1 if rng.random() < 0.15 else 0)
        for x in range(T):
            d = x if side == 0 else T - 1 - x
            if d < wave:
                continue
            color = base.getpixel((x, y))
            if d < wave + 3:  # faixa de terra com raízes
                color = pick(WOOD, 1.6 + tn(x, y, seed + 6, 2, T) * 2.2 - (d - wave) * 0.3, x, y)
                if tn(x, y, seed + 8, 3, T) > 0.62:
                    color = pick(MOSS, 1.4 + tn(x, y, seed + 9, 2, T) * 3, x, y)
            out.putpixel((x, y), color)
    for _ in range(14):  # grama avançando sobre a borda
        y = rng.randrange(T)
        wave = 3 + int(tn(0, y, seed, 4, T) * 4)
        x = wave + rng.randint(-1, 2)
        x = x if side == 0 else T - 1 - x
        for i in range(rng.randint(2, 4)):
            put(out, x + (i // 2 if side == 0 else -(i // 2)), (y - i) % T, GRASS[3 + i % 3])
    return out


def water_tile(seed, variant):
    img = new_image(T, T)
    rng = random.Random(seed)
    for y in range(T):
        for x in range(T):
            warp = tn(x, y, seed, 8, T) * 5
            swell = math.sin((y + warp) / T * math.pi * 4 + x / T * math.pi * 2)
            level = 2.4 + swell * 0.8 + tn(x, y, seed + 3, 4, T) * 1.3
            put(img, x, y, pick(WATER, level, x, y))
    for _ in range(9):  # cristas de luz alongadas
        x, y = rng.randrange(T), rng.randrange(T)
        for i in range(rng.randint(2, 5)):
            wput(img, x + i, y, WATER[6])
        wput(img, x + 1, y + 1, WATER[3])
    for _ in range(variant * 3 + 2):  # brilhos pontuais
        wput(img, rng.randrange(T), rng.randrange(T), WATER[7])
    return img


def bridge_tile(seed):
    img = new_image(T, T)
    rng = random.Random(seed)
    y = 0
    for h in (8, 8, 8, 8):
        tone = rng.uniform(2.0, 3.6)
        end_x = rng.randrange(8, 24)
        for v in range(h):
            for x in range(T):
                if v == h - 1:
                    put(img, x, y + v, WOOD[0])
                    continue
                grain = math.sin((x * 0.55 + tn(x, y + v, seed + y, 4, T) * 5) + v * 0.9)
                level = tone + grain * 0.35 + (0.7 if v == 0 else 0) - (0.4 if v >= h - 3 else 0)
                level += (tn(x, y + v, seed + 14, 2, T) - 0.5) * 0.6
                color = pick(WOOD, level, x, y + v)
                if x == end_x:
                    color = WOOD[1]
                put(img, x, y + v, color)
        for nx in (1, T - 3):  # pregos
            put(img, nx, y + 3, METAL[3])
            put(img, nx, y + 4, METAL[1])
        y += h
    for _ in range(5):
        put(img, rng.randrange(T), rng.randrange(T), MOSS[rng.randint(2, 4)])
    return img


def ruin_wall_tile(seed):
    img = cobble_tile(seed, moss=0.32, warm=0.55, palette=RUIN, heights=(15, 17), wmin=14, wmax=18)
    rng = random.Random(seed + 200)
    for x in range(T):  # cortina de musgo no topo
        depth = int(tn(x, 0, seed + 4, 4, T) * 6)
        for y in range(depth):
            put(img, x, y, pick(MOSS, 2.2 + tn(x, y, seed + 6, 2, T) * 3.5 - y * 0.2, x, y))
    for _ in range(3):  # trepadeira
        draw_vine(img, rng.randrange(T), 0, rng.randint(10, 22), rng.random() * 9, LEAF_MAIN)
    return img


def tuft_tile(seed):
    img = new_image(T, T)
    rng = random.Random(seed)
    for _ in range(18):
        x = rng.randint(4, T - 5)
        y = rng.randint(14, T - 3)
        palette = rng.choice((GRASS, MOSS, LEAF_TEAL))
        hh = rng.randint(5, 11)
        lean = rng.choice((-2, -1, 0, 1, 2))
        for i in range(hh):
            level = 2 + int(5 * i / hh)
            put(img, x + lean * i // hh, y - i, palette[min(level, len(palette) - 1)])
    return img


def fern_tile(seed):
    img = new_image(T, T)
    rng = random.Random(seed)
    cx, cy = 16, 26
    for frond in range(9):
        ang = -math.pi / 2 + (frond - 4) * 0.34 + rng.uniform(-0.08, 0.08)
        length = rng.uniform(9, 15)
        for i in range(int(length)):
            t = i / length
            x = cx + math.cos(ang) * i * (1 + 0.15 * t) + (frond - 4) * 0.4 * t * 3
            y = cy + math.sin(ang) * i + t * t * 5
            put(img, round(x), round(y), LEAF_MAIN[2])
            if i > 2 and i % 2 == 0:
                shade = LEAF_MAIN[min(8, 3 + int((1 - t) * 4))]
                for side in (-1, 1):
                    put(img, round(x) + side, round(y) + (1 if t > 0.5 else 0), shade)
                    if i % 4 == 0:
                        put(img, round(x) + 2 * side, round(y) + 1, LEAF_MAIN[5])
    return img


def mushroom_tile(seed):
    img = new_image(T, T)
    rng = random.Random(seed)
    for k in range(3):
        x, y = rng.randint(7, 24), rng.randint(16, 27)
        size = rng.randint(2, 4)
        for i in range(3):
            put(img, x, y + i, BIRCH[4 - i])
        for dx in range(-size, size + 1):
            for dy in range(-(size // 2 + 1), 1):
                if dx * dx / (size * size) + dy * dy / ((size // 2 + 1) ** 2) <= 1:
                    put(img, x + dx, y + dy, pick(FLOWER_PINK[:2] + [hexc("#9a3a3a")] * 1 + [hexc("#c8584a")], 1.4 + dy * 0.2 - dx * 0.1, x + dx, y + dy))
        put(img, x - size // 2, y - 1, BIRCH[5])
    return img


def flowers_tile(seed, petal):
    img = new_image(T, T)
    rng = random.Random(seed)
    for _ in range(6):
        x, y = rng.randint(4, T - 5), rng.randint(10, T - 4)
        put(img, x, y + 1, LEAF_MAIN[3])
        put(img, x, y + 2, LEAF_MAIN[2])
        put(img, x - 1, y + 2, LEAF_MAIN[4])
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            put(img, x + dx, y + dy, petal[2])
        put(img, x, y, FLOWER_GOLD[3] if petal is not FLOWER_GOLD else hexc("#ffffff"))
        put(img, x - 1, y - 1, petal[3])
    for _ in range(6):
        x, y = rng.randint(2, T - 3), rng.randint(14, T - 2)
        put(img, x, y, LEAF_MAIN[rng.randint(3, 6)])
        put(img, x + 1, y - 1, LEAF_MAIN[rng.randint(4, 7)])
    return img


def litter_tile(seed):
    img = new_image(T, T)
    rng = random.Random(seed)
    for _ in range(18):
        x, y = rng.randrange(T), rng.randrange(T)
        c = rng.choice((LEAF_AUT[2], LEAF_AUT[3], WOOD[3], LEAF_YEL[3], LEAF_AUT[4]))
        put(img, x, y, c)
        put(img, x + 1, y, c if rng.random() < 0.6 else WOOD[2])
        put(img, x, y + 1, WOOD[1])
    return img


def pebbles_tile(seed):
    img = new_image(T, T)
    rng = random.Random(seed)
    for _ in range(7):
        x, y = rng.randint(3, T - 6), rng.randint(5, T - 5)
        w, h = rng.randint(3, 5), rng.randint(2, 3)
        for v in range(h):
            for u in range(w):
                if (u in (0, w - 1)) and (v in (0, h - 1)):
                    continue
                put(img, x + u, y + v, STONE[min(6, 3 + (2 if v == 0 else 0) - (1 if v == h - 1 else 0) + (u == 0))])
        put(img, x + 1, y + h, STONE[0])
        if rng.random() < 0.5:
            put(img, x + 1, y, MOSS[3])
    return img


def moss_patch_tile(seed):
    img = new_image(T, T)
    for y in range(T):
        for x in range(T):
            n = tfbm(x, y, seed, T, (16, 8, 4), (0.45, 0.35, 0.2))
            if n > 0.5:
                put(img, x, y, pick(MOSS, 1.0 + (n - 0.5) * 11, x, y))
    return img


def build():
    tiles = [None] * 32
    tiles[0] = ground_tile(11, 0)
    tiles[1] = ground_tile(23, 2)
    tiles[2] = ground_tile(37, 1)
    for i in range(4):
        tiles[3 + i] = cobble_tile(100 + i * 17, moss=0.5 + 0.04 * i)
    tiles[7] = water_tile(301, 0)
    tiles[8] = water_tile(333, 1)
    tiles[9] = bridge_tile(401)
    tiles[10] = bridge_tile(433)
    tiles[11] = ruin_wall_tile(501)
    tiles[12] = ruin_wall_tile(533)
    tiles[13] = tuft_tile(601)
    tiles[14] = fern_tile(633)
    tiles[15] = mushroom_tile(667)
    tiles[16] = path_edge(701, 0)
    tiles[17] = path_edge(733, 1)
    tiles[18] = flowers_tile(801, FLOWER_PINK)
    tiles[19] = flowers_tile(833, FLOWER_GOLD)
    tiles[20] = flowers_tile(867, FLOWER_BLUE)
    tiles[21] = litter_tile(901)
    tiles[22] = pebbles_tile(933)
    tiles[23] = moss_patch_tile(967)
    tiles[24] = ground_tile(1011, 0)
    tiles[25] = ground_tile(1033, 1)
    tiles[26] = ground_tile(1061, 2)
    tiles[27] = ground_tile(1087, 0)
    tiles[28] = tuft_tile(1103)
    tiles[29] = fern_tile(1129)
    tiles[30] = flowers_tile(1151, FLOWER_GOLD)
    tiles[31] = litter_tile(1181)
    atlas = new_image(256, 128)
    for index, tile in enumerate(tiles):
        atlas.paste(tile, ((index % 8) * T, (index // 8) * T))
    return atlas


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "public/assets/tiles/avelora-tiles.png"
    build().save(out)
    print("tiles ->", out)

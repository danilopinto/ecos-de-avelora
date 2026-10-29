"""Gera o atlas de decoração (árvores, rochas, ruínas, cristais, runas...) em decor.png + decor.json.

Uso: python3 gen_decor.py [saida_dir]   (padrão: public/assets/sprites)
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

from pxlib import *  # noqa: F401,F403
from pxlib import (BARK, BIRCH, CRYSTAL, FLAME, FLOWER_BLUE, FLOWER_GOLD, FLOWER_PINK, LEAF_AUT, LEAF_MAIN, LEAF_TEAL,
                   LEAF_YEL, METAL, MOSS, PINE, RUIN, STONE, WOOD, bay, clamp, draw_vine, get, ground_shadow, hsh,
                   new_image, nn, outline, pack_atlas, pick, put, render_blobs, voronoi, rect, line)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "public", "assets", "sprites")
DARK = (4, 9, 8, 255)
frames = {}


def mossify(img, seed, amount=0.5, top_bias=0.6, ramp=MOSS):
    """Cobre superfícies opacas com musgo, favorecendo o topo e as bordas voltadas para cima."""
    src = img.copy()
    for y in range(img.height):
        for x in range(img.width):
            if src.getpixel((x, y))[3] < 200:
                continue
            above = src.getpixel((x, y - 1))[3] < 40 if y > 0 else True
            n = nn(x, y, seed, 5) * 0.6 + nn(x, y, seed + 9, 2) * 0.4
            score = n + (top_bias if above else 0) - (1 - amount) - (y / img.height) * 0.25
            if score > 0.18:
                lvl = clamp(2.2 + score * 5 + (2 if above else 0), 0, len(ramp) - 1)
                put(img, x, y, pick(ramp, lvl, x, y))


def shade_stone(img, box, seed, ramp=STONE, cell=6, light=0.0, bevel=True):
    """Preenche um retângulo com pedra facetada (voronoi) e bisel de luz a esquerda/cima."""
    x0, y0, x1, y1 = box
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d1, d2, cid = voronoi(x, y, cell, seed)
            lvl = 2.6 + (cid - 0.5) * 2.2 + light
            if d2 - d1 < 0.14:
                lvl -= 1.4
            lvl += (nn(x, y, seed + 4, 3) - 0.5) * 1.2
            if bevel:
                if x - x0 < 2:
                    lvl += 1.3 if x - x0 == 0 else 0.6
                if x1 - x < 2:
                    lvl -= 1.4
                if y - y0 < 1:
                    lvl += 1.5
                if y1 - y < 2:
                    lvl -= 1.4
            put(img, x, y, pick(ramp, clamp(lvl, 0, len(ramp) - 1), x, y))


def brick_wall(img, box, seed, ramp=STONE, brick_w=14, brick_h=8):
    x0, y0, x1, y1 = box
    for y in range(y0, y1 + 1):
        row = (y - y0) // brick_h
        off = (row % 2) * (brick_w // 2)
        for x in range(x0, x1 + 1):
            col = (x - x0 + off) // brick_w
            bx = (x - x0 + off) % brick_w
            by = (y - y0) % brick_h
            cid = hsh(col, row, seed)
            lvl = 2.8 + (cid - 0.5) * 2.4 + (nn(x, y, seed, 3) - 0.5) * 1.3
            if bx == 0 or by == brick_h - 1:
                lvl = 0.6
            elif bx == 1 or by == 0:
                lvl += 1.0
            elif bx == brick_w - 1:
                lvl -= 0.8
            put(img, x, y, pick(ramp, clamp(lvl, 0, len(ramp) - 1), x, y))


def add_cracks(img, seed, count, color):
    r = random.Random(seed)
    for _ in range(count):
        x, y = r.randrange(img.width), r.randrange(img.height)
        if get(img, x, y)[3] < 200:
            continue
        for _ in range(r.randrange(4, 10)):
            put(img, x, y, color)
            x += r.choice((-1, 0, 1))
            y += 1


# ---------------------------------------------------------------- árvores

def tree(name, seed, leaf_sets, trunk_ramp=BARK, w=96, h=120, accents=(0.18, 0.1), crown=1.0, mossy=True, vines=True):
    r = random.Random(seed)
    img = new_image(w, h)
    cx = w // 2 + r.randint(-2, 2)
    base = h - 6
    top_trunk = int(h * 0.46)
    # copa antes do tronco: o tronco entra por baixo e é sobreposto pelas folhas
    ground_shadow(img, cx, base + 1, 24, 5, 0.9)
    # tronco
    for y in range(top_trunk, base + 1):
        t = (y - top_trunk) / (base - top_trunk)
        half = 4.5 + t * 2.0 + max(0, (t - 0.82) * 28)
        lean = math.sin(y * 0.09 + seed) * 1.3
        for x in range(int(cx - half + lean) - 1, int(cx + half + lean) + 2):
            u = (x - (cx + lean)) / max(half, 1)
            if abs(u) > 1.0:
                continue
            groove = nn(x, y, seed, 3) * 0.8 + math.sin((x + seed) * 1.7) * 0.25
            lvl = 3.1 - u * 1.9 + (groove - 0.5) * 2.1
            if abs(u) > 0.84:
                lvl -= 1.4
            if u < -0.55:
                lvl += 0.5
            put(img, x, y, pick(trunk_ramp, clamp(lvl, 0, len(trunk_ramp) - 1), x, y))
    # raízes
    for side in (-1, 1):
        for k in range(2):
            x = cx + side * (6 + k * 3)
            for i in range(9 + k * 2):
                put(img, x + side * (i // 2), base - 1 + (i // 4) - 1, trunk_ramp[2 if side > 0 else 3])
                put(img, x + side * (i // 2), base - 2 + (i // 4) - 1, trunk_ramp[3 if side < 0 else 2])
    # galhos escuros entrando na copa
    for side in (-1, 1):
        bx, by = cx, top_trunk + 12
        for i in range(14):
            bx += side * 1.0
            by -= 0.55 + hsh(i, seed, side) * 0.3
            put(img, bx, by, trunk_ramp[2])
            put(img, bx, by + 1, trunk_ramp[1])
    if mossy:
        mossify(img, seed + 2, 0.5, 0.5)
    # copa
    blobs = []
    cy0 = h * 0.30
    n = r.randint(9, 12)
    for i in range(n):
        ang = r.random() * math.tau
        dist = r.random() ** 0.7 * 23 * crown
        rad = r.randint(12, 19) * (1.1 - dist / 70)
        bxx = cx + math.cos(ang) * dist * 1.15
        byy = cy0 + math.sin(ang) * dist * 0.72
        blobs.append((bxx, byy, rad, (-byy * 0.12) + r.random() * 4))
    blobs.append((cx, cy0 + 4, 20 * crown, 4))
    crown_img = new_image(w, h)
    render_blobs(crown_img, blobs, leaf_sets, seed, cell=3.4, facet=0.7, edge_dark=0.28, contrast=1.15,
                 accent_odds=accents, bias=-0.04, rim=0.2, outline_color=(3, 9, 6, 255), cell_amp=0.34)
    img.alpha_composite(crown_img)
    # buracos de luz / sombra interna sob a copa sobre o tronco
    for y in range(top_trunk - 2, top_trunk + 12):
        for x in range(cx - 9, cx + 10):
            px = get(img, x, y)
            if px[3] > 200 and get(crown_img, x, y)[3] < 40 and (y - top_trunk) < 8 and bay(x, y) < 0.45:
                put(img, x, y, tuple(int(c * 0.55) for c in px[:3]) + (255,))
    if vines:
        for k in range(3):
            vx = cx - 8 + k * 8 + r.randint(-2, 2)
            draw_vine(img, vx, int(h * 0.52) + r.randint(0, 4), r.randint(14, 30), seed + k * 5, LEAF_MAIN, 1, 1.2, 3)
    outline(img, (3, 8, 6, 255))
    frames[name] = img


def pine(name, seed, w=64, h=112):
    r = random.Random(seed)
    img = new_image(w, h)
    cx = w // 2
    base = h - 5
    ground_shadow(img, cx, base + 1, 17, 4, 0.9)
    for y in range(int(h * 0.55), base + 1):
        for x in range(cx - 3, cx + 4):
            u = (x - cx) / 3.0
            put(img, x, y, pick(BARK, clamp(2.8 - u * 1.8 + (nn(x, y, seed, 3) - 0.5) * 1.7, 0, 5), x, y))
    tiers = 6
    for t in range(tiers):
        ty = 8 + t * (h * 0.6 / tiers)
        half = 7 + t * 4.2
        blobs = [(cx + dx, ty + 8 + abs(dx) * 0.22, 7.5 + t * 0.9 - abs(dx) * 0.04, 2 + t * 0.4)
                 for dx in range(-int(half), int(half) + 1, 5)]
        blobs.append((cx, ty + 3, 8 + t * 1.2, 4))
        layer = new_image(w, h)
        render_blobs(layer, blobs, (PINE, LEAF_TEAL, LEAF_MAIN), seed + t, cell=3.0, facet=0.7, edge_dark=0.3,
                     contrast=1.1, accent_odds=(0.12, 0.06), bias=-0.15 + t * 0.02, rim=0.25,
                     outline_color=(2, 8, 6, 255))
        img.alpha_composite(layer)
    outline(img, (2, 8, 6, 255))
    frames[name] = img


# ---------------------------------------------------------------- vegetação baixa

def bush(name, seed, ramps, w=44, h=30, flowers=None):
    r = random.Random(seed)
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, w * 0.42, 4, 0.9)
    blobs = []
    for i in range(r.randint(4, 6)):
        bxx = w / 2 + (i - 2.2) * 6 + r.randint(-2, 2)
        byy = h - 12 + r.randint(-4, 2)
        blobs.append((bxx, byy, r.randint(7, 11), r.random() * 3))
    render_blobs(img, blobs, ramps, seed, cell=3.0, facet=0.7, edge_dark=0.3, contrast=1.1, accent_odds=(0.2, 0.1),
                 bias=-0.1, rim=0.22, outline_color=(3, 9, 6, 255), cell_amp=0.34)
    if flowers:
        for i in range(12):
            x, y = r.randrange(6, w - 6), r.randrange(4, h - 8)
            if get(img, x, y)[3] > 200:
                put(img, x, y, flowers[3])
                put(img, x + 1, y, flowers[2])
                put(img, x, y + 1, flowers[1])
    frames[name] = img


def fern(name, seed, w=34, h=24, ramp=LEAF_MAIN):
    img = new_image(w, h)
    cx, base = w // 2, h - 2
    ground_shadow(img, cx, base, 11, 2.5, 0.8)
    n = 9
    for i in range(n):
        ang = -math.pi / 2 + (i - (n - 1) / 2) * 0.33 + (hsh(i, seed, 1) - 0.5) * 0.2
        ln = 10 + hsh(i, seed, 2) * 8 - abs(i - n // 2) * 0.5
        for s in range(int(ln * 2)):
            t = s / 2.0
            x = cx + math.cos(ang) * t
            y = base + math.sin(ang) * t + (t * t) * 0.018
            lvl = 2 + int(t / ln * 4)
            put(img, x, y, ramp[min(lvl, len(ramp) - 1)])
            if s % 2 == 0 and 2 < t < ln:
                put(img, x + 1, y + 1, ramp[min(lvl + 1, len(ramp) - 1)])
                put(img, x - 1, y + 1, ramp[max(lvl - 1, 1)])
    outline(img, (3, 9, 6, 255))
    frames[name] = img


def tall_grass(name, seed, w=26, h=22):
    img = new_image(w, h)
    cx = w // 2
    for i in range(16):
        x0 = cx + int((hsh(i, seed, 3) - 0.5) * 16)
        ln = 8 + int(hsh(i, seed, 4) * 12)
        lean = (hsh(i, seed, 5) - 0.5) * 7
        for s in range(ln):
            t = s / ln
            put(img, x0 + lean * t * t, h - 1 - s, LEAF_MAIN[min(8, 3 + int(t * 6) + (i % 2))])
    outline(img, (3, 9, 6, 255))
    frames[name] = img


def lily(name, seed, w=34, h=22, flower=True):
    img = new_image(w, h)
    r = random.Random(seed)
    for i in range(3):
        cx, cy = 8 + i * 8 + r.randint(-2, 2), 8 + r.randint(0, 6)
        rx, ry = 6 + r.randint(0, 2), 3
        notch = r.random() * math.tau
        for y in range(cy - ry - 1, cy + ry + 2):
            for x in range(cx - rx - 1, cx + rx + 2):
                dx, dy = (x - cx) / rx, (y - cy) / ry
                if dx * dx + dy * dy < 1:
                    if abs(math.atan2(dy, dx) - notch) < 0.28:
                        continue
                    lvl = 4.5 - dy * 1.5 + (nn(x, y, seed, 2) - 0.5) * 1.5 - dx * 0.5
                    put(img, x, y, pick(LEAF_MAIN, clamp(lvl, 0, 8), x, y))
        if flower and i == 1:
            for p in range(5):
                a = p * math.tau / 5
                put(img, cx + math.cos(a) * 2, cy - 2 + math.sin(a), FLOWER_PINK[3])
            put(img, cx, cy - 2, FLOWER_GOLD[3])
    outline(img, (4, 20, 22, 200))
    frames[name] = img


# ---------------------------------------------------------------- rochas e ruínas

def boulder(name, seed, w, h, mossy=0.28):
    img = new_image(w, h)
    r = random.Random(seed)
    ground_shadow(img, w / 2, h - 3, w * 0.46, 4, 0.9)
    blobs = [(w * 0.5, h * 0.55, min(w, h) * 0.45, 4)]
    for _ in range(3):
        blobs.append((w * (0.25 + r.random() * 0.5), h * (0.5 + r.random() * 0.2), min(w, h) * (0.22 + r.random() * 0.15), r.random() * 3))
    render_blobs(img, blobs, (STONE,), seed, cell=5.0, facet=0.8, edge_dark=0.5, contrast=1.2,
                 bias=-0.05, rim=0.3, outline_color=(3, 8, 7, 255), cell_amp=0.3, moss=mossy)
    add_cracks(img, seed, 3, STONE[1])
    frames[name] = img


def pillar(name, seed, w=26, h=60, broken=True):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, w * 0.5, 4, 0.9)
    top = 10 if broken else 4
    shade_stone(img, (3, top, w - 4, h - 7), seed, STONE, 6)
    # base e capitel
    shade_stone(img, (1, h - 11, w - 2, h - 5), seed + 1, STONE, 5)
    if not broken:
        shade_stone(img, (1, 2, w - 2, 9), seed + 2, STONE, 5)
    else:
        for x in range(3, w - 3):
            cut = int(3 + nn(x, 0, seed, 2) * 6)
            for y in range(top, top + cut):
                put(img, x, y, (0, 0, 0, 0))
    add_cracks(img, seed + 7, 4, STONE[0])
    mossify(img, seed + 3, 0.55, 0.7)
    draw_vine(img, w // 2 + 3, top + 8, 22, seed, LEAF_MAIN, 1, 1.0, 3)
    outline(img, (3, 8, 7, 255))
    frames[name] = img


def wall_piece(name, seed, w=64, h=40):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, w * 0.5, 4, 0.9)
    brick_wall(img, (0, 8, w - 1, h - 6), seed, RUIN, 14, 8)
    for x in range(w):
        cut = int(2 + nn(x, 0, seed, 3) * 7)
        for y in range(8, 8 + cut):
            put(img, x, y, (0, 0, 0, 0))
    mossify(img, seed + 4, 0.6, 0.8)
    draw_vine(img, 10, 14, 18, seed, LEAF_MAIN, 1, 1.0, 3)
    draw_vine(img, 44, 12, 14, seed + 3, LEAF_TEAL, 1, 1.0, 3)
    outline(img, (3, 8, 7, 255))
    frames[name] = img


def arch(name, seed, w=104, h=100):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, w * 0.5, 5, 0.9)
    shade_stone(img, (4, 20, 24, h - 6), seed, RUIN, 7)
    shade_stone(img, (w - 25, 20, w - 5, h - 6), seed + 3, RUIN, 7)
    for cx0 in (14, w - 15):
        shade_stone(img, (cx0 - 12, h - 14, cx0 + 11, h - 6), seed + 5, RUIN, 5)
    # lintel arqueado
    for y in range(4, 44):
        for x in range(4, w - 4):
            dx = (x - w / 2) / (w / 2 - 4)
            top_edge = 14 + dx * dx * 14
            if top_edge - 8 < y < top_edge + 10 and abs(dx) < 1:
                d1, d2, cid = voronoi(x, y, 7, seed + 8)
                lvl = 3.0 + (cid - 0.5) * 2 - (1.4 if d2 - d1 < 0.14 else 0) + (1.0 if y < top_edge - 5 else 0)
                put(img, x, y, pick(RUIN, clamp(lvl, 0, 5), x, y))
    mossify(img, seed + 6, 0.65, 0.9)
    for vx in (8, 16, 24, 38, 52, 66, 80, 90, 98):
        draw_vine(img, vx, 16 + int(((vx - w / 2) / (w / 2)) ** 2 * 12), 14 + int(hsh(vx, seed, 2) * 30), seed + vx,
                  LEAF_MAIN, 1, 1.3, 3, flowers=(vx % 3 == 0))
    outline(img, (3, 8, 7, 255))
    frames[name] = img


def slab(name, seed, w=36, h=48, glow=False):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, 14, 3.5, 0.9)
    for y in range(4, h - 5):
        half = 12 - int(max(0, 6 - y) * 1.5)
        for x in range(w // 2 - half, w // 2 + half + 1):
            u = (x - w / 2) / max(half, 1)
            lvl = 3.0 - u * 1.6 + (nn(x, y, seed, 3) - 0.5) * 1.5
            if abs(u) > 0.88:
                lvl -= 1.2
            put(img, x, y, pick(STONE, clamp(lvl, 0, 6), x, y))
    # inscrições
    for row in range(6):
        y = 14 + row * 4
        for x in range(10, w - 10, 3):
            if hsh(x, row, seed) > 0.3:
                put(img, x, y, STONE[0])
                put(img, x + 1, y, STONE[0])
                put(img, x, y + 1, (CRYSTAL[5] if glow else STONE[5]))
    mossify(img, seed + 1, 0.6, 0.8)
    draw_vine(img, 11, 8, 12, seed, LEAF_MAIN, 1, 0.8, 3)
    outline(img, (3, 8, 7, 255))
    frames[name] = img


def stump(name, seed, w=34, h=26):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, 14, 4, 0.9)
    for y in range(8, h - 4):
        for x in range(5, w - 5):
            u = (x - w / 2) / (w / 2 - 5)
            if abs(u) > 1:
                continue
            lvl = 3.0 - u * 1.8 + (nn(x, y, seed, 3) - 0.5) * 1.8
            if abs(u) > 0.85:
                lvl -= 1.2
            put(img, x, y, pick(BARK, clamp(lvl, 0, 5), x, y))
    for y in range(2, 11):
        for x in range(5, w - 5):
            dx, dy = (x - w / 2) / (w / 2 - 5), (y - 6.5) / 4.6
            if dx * dx + dy * dy < 1:
                ring = int(math.hypot(dx, dy * 1.4) * 5) % 2
                put(img, x, y, WOOD[4 - ring] if dx * dx + dy * dy < 0.8 else BARK[3])
    mossify(img, seed + 1, 0.55, 0.5)
    outline(img, (3, 8, 7, 255))
    frames[name] = img


def log(name, seed, w=54, h=22):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, w * 0.45, 3.5, 0.9)
    for y in range(4, h - 4):
        for x in range(2, w - 2):
            u = (y - 12) / 7.0
            if abs(u) > 1:
                continue
            lvl = 3.0 - u * 1.6 + (nn(x, y, seed, 5) - 0.5) * 1.1 + math.sin(x * 0.9 + seed) * 0.25
            if abs(u) > 0.85:
                lvl -= 1.2
            put(img, x, y, pick(BARK, clamp(lvl, 0, 5), x, y))
    for y in range(4, h - 4):
        for x in range(2, 8):
            dx, dy = (x - 5) / 3.0, (y - 12) / 7.0
            if dx * dx + dy * dy < 1:
                put(img, x, y, WOOD[4 - int(math.hypot(dx, dy) * 3) % 2])
    mossify(img, seed + 1, 0.6, 0.7)
    outline(img, (3, 8, 7, 255))
    frames[name] = img


def stake(name, seed, w=14, h=34):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 2, 5, 2, 0.9)
    for y in range(2, h - 3):
        half = 3 if y > 7 else 3 - (8 - y) // 3
        for x in range(w // 2 - half, w // 2 + half):
            u = (x - w / 2 + 0.5) / 3.0
            put(img, x, y, pick(WOOD, clamp(3.1 - u * 1.6 + (nn(x, y, seed, 3) - 0.5) * 1.5, 0, 5), x, y))
    for x in range(w // 2 - 3, w // 2 + 3):
        put(img, x, 18, WOOD[0])
    mossify(img, seed, 0.5, 0.3)
    outline(img, (3, 8, 7, 255))
    frames[name] = img


def barrel(name, seed, w=28, h=32):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, 11, 3.5, 0.9)
    for y in range(3, h - 4):
        t = (y - 3) / (h - 7)
        half = 8 + math.sin(t * math.pi) * 2.5
        for x in range(int(w / 2 - half), int(w / 2 + half) + 1):
            u = (x - w / 2) / half
            plank = int((x + 0.5) // 3)
            lvl = 3.0 - u * 1.8 + (hsh(plank, seed, 1) - 0.5) * 1.4 + (nn(x, y, seed, 3) - 0.5) * 0.8
            if (x % 3) == 0:
                lvl -= 1.0
            put(img, x, y, pick(WOOD, clamp(lvl, 0, 5), x, y))
    for y in (7, h - 9):
        for x in range(w // 2 - 11, w // 2 + 11):
            if get(img, x, y)[3] > 200:
                put(img, x, y, METAL[2] if x > w // 2 - 4 else METAL[3])
                put(img, x, y + 1, METAL[1])
    for x in range(w // 2 - 6, w // 2 + 7):
        put(img, x, 3, WOOD[5])
    mossify(img, seed + 1, 0.4, 0.4)
    outline(img, (3, 8, 7, 255))
    frames[name] = img


# ---------------------------------------------------------------- cristais, tochas e runas

def facet_poly(draw, pts, color):
    draw.polygon(pts, fill=color)


def crystal(name, seed, w=36, h=48, spikes=3):
    img = new_image(w, h)
    r = random.Random(seed)
    ground_shadow(img, w / 2, h - 3, w * 0.38, 3.5, 0.8)
    draw = ImageDraw.Draw(img)
    order = sorted(range(spikes), key=lambda i: -abs(i - spikes // 2))
    for i in order:
        bx = w * (0.28 + 0.44 * i / max(1, spikes - 1)) if spikes > 1 else w / 2
        bw = r.randint(5, 8)
        hh = r.randint(int(h * 0.42), int(h * 0.82)) if i != spikes // 2 else int(h * 0.88)
        lean = r.randint(-3, 3)
        base_y = h - 6 + r.randint(-1, 1)
        tip = (bx + lean, base_y - hh)
        l, rr = (bx - bw, base_y), (bx + bw, base_y)
        mid = (bx + lean * 0.5, base_y - hh * 0.62)
        draw.polygon([l, tip, mid], fill=CRYSTAL[3])
        draw.polygon([mid, tip, rr], fill=CRYSTAL[5])
        draw.polygon([l, mid, rr, (bx, base_y + 1)], fill=CRYSTAL[2])
        draw.line([tip, mid], fill=CRYSTAL[7])
        draw.line([l, tip], fill=CRYSTAL[1])
        draw.line([tip, rr], fill=CRYSTAL[4])
    # brilho em dithering
    for y in range(h):
        for x in range(w):
            px = get(img, x, y)
            if px[3] > 200 and y < h * 0.45 and hsh(x, y, seed) > 0.93:
                put(img, x, y, CRYSTAL[7] + (255,) if len(CRYSTAL[7]) == 3 else CRYSTAL[7])
    outline(img, (2, 22, 28, 255))
    frames[name] = img


def torch(name, seed, w=28, h=60):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, 10, 3, 0.9)
    shade_stone(img, (8, 28, w - 9, h - 8), seed, STONE, 5)
    shade_stone(img, (5, h - 12, w - 6, h - 6), seed + 1, STONE, 4)
    shade_stone(img, (6, 22, w - 7, 29), seed + 2, STONE, 4)
    # tigela
    for y in range(14, 23):
        t = (y - 14) / 8
        for x in range(int(w / 2 - 5 + t * 2 * -1 + 1), int(w / 2 + 5 - 1 + t * 1)):
            put(img, x, y, METAL[3 - (1 if x > w / 2 else 0) + (1 if y == 14 else 0)])
    for x in range(w // 2 - 5, w // 2 + 5):
        put(img, x, 14, METAL[4])
    # chama
    for y in range(1, 14):
        t = (13 - y) / 13
        half = 4.2 * math.sin(math.pi * (1 - t) * 0.9 + 0.2) * (1 - t * 0.2)
        for x in range(int(w / 2 - half - 1), int(w / 2 + half + 2)):
            u = abs(x - w / 2 + 0.5) / max(half, 0.5)
            if u <= 1:
                lvl = (1 - u) * 3.2 + (1 - y / 14) * 1.2 + (hsh(x, y, seed) - 0.5) * 0.8
                put(img, x, y, pick(FLAME, clamp(lvl, 0, 4), x, y))
    mossify(img, seed, 0.5, 0.5)
    outline(img, (3, 8, 7, 255))
    frames[name] = img


def glyph(img, kind, cx, cy, color, glow=None):
    if kind == "sun":
        for y in range(-3, 4):
            for x in range(-3, 4):
                if x * x + y * y <= 5:
                    put(img, cx + x, cy + y, color)
        for a in range(8):
            ang = a * math.pi / 4
            put(img, cx + math.cos(ang) * 5.2, cy + math.sin(ang) * 5.2, color)
            put(img, cx + math.cos(ang) * 6.2, cy + math.sin(ang) * 6.2, color)
    elif kind == "moon":
        for y in range(-6, 7):
            for x in range(-6, 7):
                if x * x + y * y <= 30 and (x - 3) ** 2 + (y + 1) ** 2 > 24:
                    put(img, cx + x, cy + y, color)
    else:
        for x in range(-7, 8):
            put(img, cx + x, cy + round(math.sin(x * 0.9) * 1.6) - 3, color)
            put(img, cx + x, cy + round(math.sin(x * 0.9 + 1.5) * 1.6) + 1, color)
            put(img, cx + x, cy + round(math.sin(x * 0.9 + 3) * 1.6) + 5, color)


def rune(name, seed, kind, lit, w=40, h=64):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, 15, 4, 0.9)
    shade_stone(img, (6, 12, w - 7, h - 8), seed, RUIN, 6)
    shade_stone(img, (3, h - 14, w - 4, h - 6), seed + 1, RUIN, 5)
    shade_stone(img, (4, 6, w - 5, 14), seed + 2, RUIN, 5)
    for y in range(18, 40):
        for x in range(10, w - 10):
            put(img, x, y, pick(STONE, 1.2 + nn(x, y, seed, 3) * 1.2, x, y))
    if lit:
        for y in range(14, 46):
            for x in range(6, w - 6):
                d = math.hypot(x - w / 2, y - 29) / 16
                if d < 1 and (1 - d) * 1.4 > bay(x, y) + 0.2 and get(img, x, y)[3] > 200:
                    put(img, x, y, pick(CRYSTAL, 2.5 + (1 - d) * 2, x, y))
        glyph(img, kind, w // 2, 29, CRYSTAL[7])
    else:
        glyph(img, kind, w // 2, 29, STONE[3])
        glyph(img, kind, w // 2 + 1, 30, STONE[0])
        glyph(img, kind, w // 2, 29, STONE[4])
    mossify(img, seed + 5, 0.45, 0.6)
    outline(img, (3, 8, 7, 255))
    frames[name] = img


def artifact(name, seed, w=34, h=52):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 3, 13, 3.5, 0.9)
    shade_stone(img, (8, 30, w - 9, h - 8), seed, RUIN, 5)
    shade_stone(img, (5, h - 13, w - 6, h - 6), seed + 1, RUIN, 4)
    shade_stone(img, (6, 25, w - 7, 31), seed + 2, RUIN, 4)
    draw = ImageDraw.Draw(img)
    cx, cy = w // 2, 14
    draw.polygon([(cx, cy - 11), (cx + 7, cy), (cx, cy + 11), (cx - 7, cy)], fill=CRYSTAL[4])
    draw.polygon([(cx, cy - 11), (cx + 7, cy), (cx, cy)], fill=CRYSTAL[6])
    draw.polygon([(cx, cy - 11), (cx - 7, cy), (cx, cy)], fill=CRYSTAL[5])
    draw.line([(cx, cy - 11), (cx, cy + 11)], fill=CRYSTAL[7])
    outline(img, (2, 22, 28, 255))
    mossify(img, seed + 4, 0.4, 0.5)
    frames[name] = img


def echo(name, seed, w=36, h=48):
    img = new_image(w, h)
    cx = w // 2
    for y in range(2, h - 2):
        t = y / h
        half = math.sin(min(1, t * 1.15) * math.pi * 0.95) * 8.5 * (1 - t * 0.35) + 1
        for x in range(int(cx - half - 4), int(cx + half + 5)):
            u = abs(x - cx + 0.5) / max(half, 1)
            if u <= 1.0:
                lvl = 7.0 - u * 3.2 - t * 2.0 + (nn(x, y, seed, 3) - 0.5)
                put(img, x, y, pick(CRYSTAL, clamp(lvl, 0, 7), x, y))
            elif u < 1.7 and (1.7 - u) * 0.9 > bay(x, y) + 0.35:
                put(img, x, y, CRYSTAL[3] + (140,) if len(CRYSTAL[3]) == 3 else CRYSTAL[3])
    for (ex, ey) in ((cx - 3, 18), (cx + 3, 18)):
        put(img, ex, ey, CRYSTAL[1])
        put(img, ex, ey + 1, CRYSTAL[1])
    frames[name] = img


def core(name, seed, w=56, h=72):
    img = new_image(w, h)
    ground_shadow(img, w / 2, h - 4, 20, 4, 0.9)
    shade_stone(img, (10, 44, w - 11, h - 9), seed, RUIN, 6)
    shade_stone(img, (6, h - 14, w - 7, h - 7), seed + 1, RUIN, 5)
    shade_stone(img, (8, 38, w - 9, 45), seed + 2, RUIN, 5)
    draw = ImageDraw.Draw(img)
    cx = w // 2
    draw.polygon([(cx, 3), (cx + 14, 22), (cx + 8, 37), (cx - 8, 37), (cx - 14, 22)], fill=CRYSTAL[3])
    draw.polygon([(cx, 3), (cx + 14, 22), (cx + 8, 37), (cx, 37)], fill=CRYSTAL[5])
    draw.polygon([(cx, 3), (cx, 22), (cx + 14, 22)], fill=CRYSTAL[6])
    draw.polygon([(cx, 3), (cx - 14, 22), (cx, 22)], fill=CRYSTAL[4])
    draw.line([(cx, 3), (cx, 37)], fill=CRYSTAL[7])
    draw.line([(cx - 14, 22), (cx + 14, 22)], fill=CRYSTAL[7])
    outline(img, (2, 22, 28, 255))
    frames[name] = img


def seal(name, seed, w=60, h=40):
    img = new_image(w, h)
    for y in range(h):
        for x in range(w):
            wave = math.sin(x * 0.45 + y * 0.3) * 0.5 + 0.5
            if x < 2 or x >= w - 2 or y < 2 or y >= h - 2:
                put(img, x, y, pick(CRYSTAL, 3.5 + wave * 2, x, y))
            elif (x + y) % 6 == 0 and hsh(x, y, seed) > 0.25:
                put(img, x, y, pick(CRYSTAL, 3 + wave * 2.5, x, y))
            elif bay(x, y) < 0.22:
                put(img, x, y, CRYSTAL[1] + (170,) if len(CRYSTAL[1]) == 3 else CRYSTAL[1])
    frames[name] = img


def shrine(seed=88):
    """Santuário 256x272 (coordenadas 672,112 do mundo): fundo com pisos/paredes e peças frontais."""
    w, h = 256, 272
    img = new_image(w, h)
    # piso interno
    for y in range(48, 232):
        for x in range(48, 208):
            d1, d2, cid = voronoi(x, y, 16, seed)
            lvl = 1.4 + cid * 1.5 + (nn(x, y, seed, 4) - 0.5) * 1.0 - (1.2 if d2 - d1 < 0.1 else 0)
            put(img, x, y, pick(RUIN, clamp(lvl, 0, 5), x, y))
    # círculo rúnico no piso
    for y in range(48, 232):
        for x in range(48, 208):
            d = math.hypot(x - 128, (y - 158) * 1.15)
            if 44 < d < 47 or 60 < d < 62:
                put(img, x, y, CRYSTAL[2] if bay(x, y) < 0.6 else CRYSTAL[3])
    for k in range(12):
        a = k * math.tau / 12
        for s in range(5):
            put(img, 128 + math.cos(a) * (50 + s * 2), 158 + math.sin(a) * (50 + s * 2) / 1.15, CRYSTAL[3])
    mossify_region = new_image(w, h)
    # parede do fundo (face frontal visível)
    brick_wall(img, (48, 0, 207, 47), seed + 1, RUIN, 16, 9)
    for x in range(48, 208):
        for y in range(40, 48):
            put(img, x, y, pick(RUIN, 0.3 + (y - 40) * 0.05, x, y))
    # paredes laterais (colunas altas)
    for x0 in (0, 208):
        shade_stone(img, (x0, 0, x0 + 47, h - 1), seed + 2 + x0, RUIN, 12)
        brick_wall(img, (x0 + 4, 14, x0 + 43, h - 8), seed + 3 + x0, RUIN, 13, 8)
        shade_stone(img, (x0, 0, x0 + 47, 12), seed + 4, RUIN, 9)
        shade_stone(img, (x0, h - 8, x0 + 47, h - 1), seed + 5, RUIN, 9)
    # reentrâncias de sombra nas paredes laterais
    for y in range(0, h):
        for x in range(48, 56):
            lvl = (x - 48) / 8
            px = get(img, x, y)
            if px[3] > 0 and bay(x, y) > lvl * 0.9:
                put(img, x, y, tuple(int(c * 0.55) for c in px[:3]) + (255,))
        for x in range(200, 208):
            px = get(img, x, y)
            if px[3] > 0 and bay(x, y) > (208 - x) / 8 * 0.9:
                put(img, x, y, tuple(int(c * 0.6) for c in px[:3]) + (255,))
    mossify(img, seed + 6, 0.38, 0.5)
    for vx in range(6, 250, 11):
        draw_vine(img, vx, 12 + int(hsh(vx, seed, 1) * 6), 12 + int(hsh(vx, seed, 2) * 40), seed + vx, LEAF_MAIN, 1, 1.4, 3,
                  flowers=(vx % 4 == 0))
    # arco da porta no fundo
    outline(img, (3, 8, 7, 255))
    frames["shrine_back"] = img

    front = new_image(w, 40)
    for x0, x1 in ((48, 98), (158, 208)):
        brick_wall(front, (x0, 0, x1 - 1, 39), seed + x0, RUIN, 14, 8)
        for x in range(x0, x1):
            put(front, x, 0, RUIN[5])
    mossify(front, seed + 12, 0.75, 0.9)
    for vx in (56, 72, 88, 166, 184, 198):
        draw_vine(front, vx, 3, 10 + int(hsh(vx, seed, 4) * 14), seed + vx, LEAF_MAIN, 1, 1.0, 3)
    outline(front, (3, 8, 7, 255))
    frames["shrine_front"] = front


def build():
    palettes = [
        (LEAF_MAIN, LEAF_TEAL, LEAF_YEL),
        (LEAF_TEAL, LEAF_MAIN, LEAF_YEL),
        (LEAF_MAIN, LEAF_YEL, LEAF_AUT),
        (LEAF_YEL, LEAF_MAIN, LEAF_AUT),
        (LEAF_MAIN, LEAF_TEAL, LEAF_AUT),
    ]
    trunks = [BARK, BARK, BIRCH, BARK, WOOD]
    for i, (leaves, trunk) in enumerate(zip(palettes, trunks)):
        tree(f"tree_{i}", 100 + i * 13, leaves, trunk, accents=(0.2, 0.12), crown=1.0 + (i % 2) * 0.08, vines=(i != 2))
    tree("tree_big", 777, (LEAF_MAIN, LEAF_TEAL, LEAF_YEL), BARK, w=128, h=150, crown=1.35, accents=(0.22, 0.12))
    pine("pine_0", 211)
    pine("pine_1", 233)
    bush("bush_0", 31, (LEAF_MAIN, LEAF_TEAL, LEAF_YEL))
    bush("bush_1", 37, (LEAF_TEAL, LEAF_MAIN, LEAF_YEL))
    bush("bush_flower", 41, (LEAF_MAIN, LEAF_TEAL, LEAF_YEL), flowers=FLOWER_PINK)
    bush("bush_flower_b", 43, (LEAF_MAIN, LEAF_YEL, LEAF_TEAL), flowers=FLOWER_GOLD)
    fern("fern_0", 5)
    fern("fern_1", 9, ramp=LEAF_TEAL)
    tall_grass("grass_0", 3)
    tall_grass("grass_1", 8)
    lily("lily_0", 4)
    lily("lily_1", 12, flower=False)
    boulder("rock_0", 51, 44, 34)
    boulder("rock_1", 53, 32, 26, 0.35)
    boulder("rock_2", 57, 22, 18, 0.4)
    pillar("pillar_broken", 61)
    pillar("pillar_full", 63, broken=False, h=72)
    wall_piece("wall_ruin", 65)
    arch("arch", 67)
    slab("slab", 69)
    slab("slab_lit", 69, glow=True)
    stump("stump", 71)
    log("log", 73)
    stake("stake_0", 75)
    stake("stake_1", 77)
    barrel("barrel", 79)
    crystal("crystal_0", 81, 36, 52, 3)
    crystal("crystal_1", 83, 28, 40, 2)
    crystal("crystal_2", 85, 44, 60, 4)
    torch("torch", 87)
    for kind in ("sun", "moon", "wave"):
        rune(f"rune_{kind}", 91, kind, False)
        rune(f"rune_{kind}_on", 91, kind, True)
    artifact("artifact", 93)
    echo("echo", 95)
    core("core", 97)
    seal("seal", 99)
    shrine()


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build()
    atlas, data = pack_atlas(frames, 1024)
    atlas.save(os.path.join(OUT, "decor.png"))
    with open(os.path.join(OUT, "decor.json"), "w") as fh:
        fh.write(data)
    print("decor ->", os.path.join(OUT, "decor.png"), len(frames), "frames", atlas.size)

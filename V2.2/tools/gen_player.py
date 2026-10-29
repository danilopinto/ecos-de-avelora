"""Gera player.png: 4 direções x 4 frames de 32x48. Linhas: 0 baixo, 1 direita, 2 esquerda (espelho), 3 cima.

Ciclo de caminhada: frames 0 e 2 = contato (passada aberta), 1 e 3 = passagem. Idle = frame 1.
Uso: python3 gen_player.py [saida.png]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageOps

from pxlib import (CLOAK, FLAME, HAIR, METAL, SCARF, SKIN, TROUSER, WOOD, bay, clamp, new_image, outline, pick, put,
                   ground_shadow, BARK)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "public", "assets", "sprites", "player.png")
W, H = 32, 48
EDGE = (6, 10, 9, 255)


def shape(img, draw_fn, ramp, base, grad=1.0, top=0.5, edge=0.9):
    mask = Image.new("L", (W, H), 0)
    draw_fn(ImageDraw.Draw(mask))
    px = mask.load()
    pts = [(x, y) for y in range(H) for x in range(W) if px[x, y]]
    if not pts:
        return
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    hw = max(1.0, (x1 - x0 + 1) / 2)
    hh = max(1.0, (y1 - y0 + 1) / 2)
    cx, cy = (x0 + x1 + 1) / 2, (y0 + y1 + 1) / 2

    def inside(x, y):
        return 0 <= x < W and 0 <= y < H and px[x, y]

    for x, y in pts:
        lvl = base + ((cx - x - 0.5) / hw) * grad + ((cy - y - 0.5) / hh) * top * 0.6
        if not inside(x + 1, y) or not inside(x, y + 1):
            lvl -= edge
        if not inside(x - 1, y) or not inside(x, y - 1):
            lvl += 0.5
        put(img, x, y, pick(ramp, clamp(lvl, 0, len(ramp) - 1), x, y))


def rc(x0, y0, x1, y1):
    return lambda d: d.rectangle([x0, y0, x1, y1], fill=255)


def el(x0, y0, x1, y1):
    return lambda d: d.ellipse([x0, y0, x1, y1], fill=255)


def poly(pts):
    return lambda d: d.polygon(pts, fill=255)


def lantern(img, x, y, swing=0):
    """Lanterna pendurada: topo no ponto (x, y)."""
    put(img, x, y, METAL[3])
    put(img, x, y + 1, METAL[2])
    for yy in range(y + 2, y + 7):
        for xx in range(x - 2, x + 3):
            edge = xx in (x - 2, x + 2) or yy in (y + 2, y + 6)
            put(img, xx, yy, METAL[2] if edge else FLAME[3 if abs(xx - x) < 1 else 2])
    put(img, x, y + 4, FLAME[4])
    put(img, x, y + 5, FLAME[3])
    put(img, x - 1, y + 3, FLAME[3])


# ---------------------------------------------------------------- frente / costas

def leg_offsets(phase):
    return {0: (1, -1), 1: (0, 0), 2: (-1, 1), 3: (0, 0)}[phase]  # (esq, dir): +1 = pé à frente (mais baixo)


def front_or_back(back, phase):
    img = new_image(W, H)
    ground_shadow(img, 16, 44, 9, 2.5, 0.9)
    l, r = leg_offsets(phase)
    for side, off in ((-1, l), (1, r)):
        x0 = 11 if side < 0 else 17
        top, bot = 33, 43 + (1 if off > 0 else 0) - (2 if off < 0 else 0)
        shape(img, rc(x0, top, x0 + 3, bot - 3), TROUSER, 3.0, 1.0)
        shape(img, rc(x0 - (0), bot - 3, x0 + 3, bot), HAIR, 2.6, 0.8, 0.3)
        put(img, x0 + 1, bot - 3, (90, 66, 44, 255))
        for xx in range(x0, x0 + 4):
            put(img, xx, bot, (8, 8, 6, 255))
    # braços atrás do corpo
    swing = {0: 1, 1: 0, 2: -1, 3: 0}[phase]
    arm_l = (7, 21 + max(0, -swing), 9, 31 + max(0, -swing))
    arm_r = (22, 21 + max(0, swing), 24, 31 + max(0, swing))
    # corpo (manto)
    body = [(10, 19), (21, 19), (23, 28), (24, 36), (22, 37), (20, 35), (17, 37), (14, 35), (11, 37), (8, 36), (9, 28)]
    shape(img, poly(body), CLOAK, 3.0, 1.1, 0.4)
    # barra do manto e dobras
    for x in range(9, 24):
        put(img, x, 36, CLOAK[1])
    for y in range(24, 35):
        put(img, 15 if not back else 16, y, CLOAK[1] if y % 2 else CLOAK[2])
    # cinto
    for x in range(10, 23):
        put(img, x, 29, METAL[1])
        put(img, x, 28, WOOD[3])
    put(img, 16, 28, METAL[4])
    put(img, 17, 28, METAL[4])
    # braços
    for (ax0, ay0, ax1, ay1), hand_side in ((arm_l, -1), (arm_r, 1)):
        shape(img, rc(ax0, ay0, ax1, ay1), CLOAK, 3.2 if hand_side < 0 else 2.6, 1.0)
        shape(img, rc(ax0, ay1, ax1, ay1 + 2), SKIN, 3.0, 0.5, 0.3)
    # lanterna na mão direita (do personagem = esquerda do espectador para o jogador de frente)
    lx = 8 if not back else 23
    lantern(img, lx, 33 + (0 if not back else 0))
    # cachecol
    for x in range(10, 22):
        for y in range(18, 22):
            put(img, x, y, pick(SCARF, 2.4 - (x - 10) * 0.12 + (0.5 if y == 18 else 0), x, y))
    if not back:
        for y in range(21, 28):
            put(img, 13, y, SCARF[1])
            put(img, 14, y, SCARF[2] if y < 26 else SCARF[1])
    # cabeça
    shape(img, el(10, 5, 21, 19), SKIN, 3.2, 0.9, 0.3, 0.7)
    if back:
        shape(img, el(9, 4, 22, 18), HAIR, 2.6, 1.0, 0.5, 0.6)
        for y in range(8, 15):
            put(img, 16, y, HAIR[1])
        shape(img, poly([(12, 16), (20, 16), (18, 20), (14, 20)]), HAIR, 2.0, 0.6)
    else:
        # cabelo: topo + franja com mechas
        shape(img, poly([(9, 12), (9, 7), (12, 4), (19, 4), (22, 7), (22, 12), (20, 9), (17, 11), (14, 9), (11, 12)]), HAIR, 2.8, 1.0, 0.5, 0.7)
        put(img, 16, 3, HAIR[3])
        put(img, 17, 4, HAIR[3])
        # olhos (2 px de altura, simétricos) + brilho
        for ex in (12, 18):
            put(img, ex, 13, (14, 8, 8, 255))
            put(img, ex, 14, (14, 8, 8, 255))
            put(img, ex + 1, 13, (30, 20, 20, 255))
            put(img, ex + 1, 14, (14, 8, 8, 255))
            put(img, ex, 12, SKIN[1])
        put(img, 15, 15, SKIN[2])
        put(img, 16, 15, SKIN[2])
        put(img, 15, 17, SKIN[1])
        put(img, 16, 17, SKIN[1])
        for ex in (11, 21):
            put(img, ex, 15, SKIN[4])
    outline(img, EDGE)
    return img


# ---------------------------------------------------------------- lado direito (3/4)

def side(phase):
    img = new_image(W, H)
    ground_shadow(img, 16, 44, 10, 2.5, 0.9)
    stride = {0: 4, 1: 0, 2: -4, 3: 0}[phase]
    lift = {0: 0, 1: 1, 2: 0, 3: 1}[phase]

    def leg(dx, shade, back):
        x = 14 + dx
        top = 33
        bot = 43 - (lift if not back else 0) - (1 if back and phase in (1, 3) else 0)
        # perna levemente inclinada para a direção da passada
        pts = [(x, top), (x + 4, top), (x + 4 + dx // 2, bot - 3), (x + dx // 2, bot - 3)]
        shape(img, poly(pts), TROUSER, shade, 0.8)
        fx = x + dx // 2
        shape(img, poly([(fx - 1, bot - 3), (fx + 4, bot - 3), (fx + 7, bot - 1), (fx + 7, bot), (fx - 1, bot)]), HAIR, 2.6 if not back else 1.8, 0.7, 0.3)
        for xx in range(fx - 1, fx + 8):
            put(img, xx, bot, (8, 8, 6, 255))

    # perna de trás (mais escura) primeiro
    leg(-stride // 2 if stride else 0, 1.8, True)
    # mochila (atrás)
    shape(img, poly([(7, 22), (12, 21), (12, 33), (8, 33), (6, 29)]), WOOD, 3.2, 1.0, 0.4)
    for y in range(24, 31):
        put(img, 9, y, WOOD[1])
    put(img, 8, 22, WOOD[5])
    shape(img, rc(6, 30, 12, 32), WOOD, 2.2, 0.8)
    # braço de trás (longe), com a lanterna
    far_swing = -stride // 2
    shape(img, rc(15 + far_swing, 21, 17 + far_swing, 30), CLOAK, 1.6, 0.8)
    # corpo
    body = [(11, 19), (19, 19), (21, 28), (21, 36), (18, 37), (15, 35), (12, 37), (10, 36), (10, 28)]
    shape(img, poly(body), CLOAK, 3.0, 1.0, 0.4)
    for y in range(24, 35):
        put(img, 13 + (y % 3 == 0), y, CLOAK[2])
    for x in range(10, 21):
        put(img, x, 36, CLOAK[1])
        put(img, x, 28, WOOD[3])
        put(img, x, 29, METAL[1])
    put(img, 17, 28, METAL[4])
    # cachecol envolvendo o pescoço
    for x in range(11, 21):
        for y in range(18, 21):
            put(img, x, y, pick(SCARF, 2.3 - (x - 11) * 0.12 + (0.4 if y == 18 else 0), x, y))
    for y in range(20, 27):
        put(img, 11, y, SCARF[1])
        put(img, 10, y, SCARF[2] if y < 25 else SCARF[1])
    # perna da frente
    leg(stride // 2 if stride else 0, 3.1, False)
    # braço da frente com lanterna balançando
    near_swing = stride // 2
    ax = 14 - near_swing
    shape(img, poly([(ax, 21), (ax + 3, 21), (ax + 3 + near_swing // 2, 30), (ax + near_swing // 2, 30)]), CLOAK, 3.6, 1.0)
    shape(img, rc(ax + near_swing // 2, 30, ax + 3 + near_swing // 2, 32), SKIN, 3.0, 0.5, 0.3)
    lantern(img, ax + 2 + near_swing // 2 + 1, 32)
    # cabeça em 3/4: rosto à direita
    shape(img, el(10, 5, 22, 19), SKIN, 3.2, 0.9, 0.3, 0.7)
    put(img, 22, 13, SKIN[3])
    put(img, 23, 14, SKIN[3])
    put(img, 23, 15, SKIN[2])
    # cabelo: nuca/fundo + topo + franja
    shape(img, poly([(9, 14), (9, 8), (12, 4), (19, 4), (22, 6), (22, 10), (19, 8), (16, 10), (14, 9), (13, 14), (14, 18), (10, 18)]), HAIR, 2.7, 1.0, 0.5, 0.7)
    shape(img, poly([(8, 11), (11, 11), (11, 17), (9, 19), (7, 17)]), HAIR, 1.8, 0.8, 0.3)
    put(img, 17, 3, HAIR[3])
    put(img, 18, 4, HAIR[3])
    # dois olhos visíveis: o próximo (maior) e o distante (mais estreito, junto à borda do rosto)
    near, far = 17, 21
    for ex, wide in ((near, 2), (far, 1)):
        for k in range(wide):
            put(img, ex + k, 13, (14, 8, 8, 255))
            put(img, ex + k, 14, (14, 8, 8, 255))
        put(img, ex, 12, SKIN[1])
    put(img, near + 1, 13, (60, 44, 40, 255))
    put(img, 23, 15, SKIN[3])
    put(img, 21, 16, SKIN[1])
    put(img, 20, 17, SKIN[1])
    put(img, 18, 15, SKIN[4])
    outline(img, EDGE)
    return img


def build():
    sheet = Image.new("RGBA", (W * 4, H * 4), (0, 0, 0, 0))
    for phase in range(4):
        down = front_or_back(False, phase)
        up = front_or_back(True, phase)
        right = side(phase)
        left = ImageOps.mirror(right)
        for row, frame in enumerate((down, right, left, up)):
            sheet.paste(frame, (phase * W, row * H))
    return sheet


if __name__ == "__main__":
    sheet = build()
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    sheet.save(OUT)
    print("player ->", OUT, sheet.size)
